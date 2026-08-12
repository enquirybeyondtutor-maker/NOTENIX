"""MCQ auto-grading + estimated-grade mapping for assigned tests."""
import asyncio
from fastapi.concurrency import run_in_threadpool

from services import ai


def grade_mcq(questions: list[dict], answers: list) -> tuple[float, list[dict]]:
    """Compare answers against the stored question snapshot.
    Returns (score_percent, per-question results with correctness + explanation)."""
    results: list[dict] = []
    correct = 0
    for i, q in enumerate(questions):
        given = answers[i] if i < len(answers) else None
        right = q.get("answer")
        is_correct = str(given).strip() == str(right).strip() if given is not None else False
        correct += int(is_correct)
        results.append({
            "question": q.get("question"),
            "options": q.get("options"),
            "image": q.get("image"),
            "your_answer": given,
            "correct_answer": right,
            "is_correct": is_correct,
            "explanation": q.get("explanation"),
        })
    score = round(100 * correct / len(questions), 1) if questions else 0.0
    return score, results


def _pending_written_results(questions: list[dict], answers: list) -> list[dict]:
    """Result rows for a submitted written test that has not been marked yet."""
    results = []
    for i, q in enumerate(questions):
        results.append({
            "question": q.get("question"),
            "marks": q.get("marks"),
            "image": q.get("image"),
            "your_answer": answers[i] if i < len(answers) else "",
            "marks_awarded": None,
            "feedback": None,
            "model_answer": None,
        })
    return results


async def grade_written(questions: list[dict], answers: list, subject: str) -> tuple[float, list[dict]]:
    """AI-mark each written answer against its mark scheme (Pro path). The Anthropic
    client is sync, so each `mark_answer` runs in a thread and they mark concurrently.
    Returns (score_percent, per-question results)."""
    async def mark_one(i: int, q: dict) -> dict:
        ans = str(answers[i]) if i < len(answers) and answers[i] is not None else ""
        marks = int(q.get("marks") or 0)
        if not ans.strip():
            return {
                "question": q.get("question"), "marks": marks, "image": q.get("image"), "your_answer": ans,
                "marks_awarded": 0, "feedback": "No answer was given.", "model_answer": "",
            }
        m = await run_in_threadpool(
            ai.mark_answer, q.get("question", ""), marks, q.get("mark_scheme", ""), ans, subject,
        )
        return {
            "question": q.get("question"), "marks": marks, "image": q.get("image"), "your_answer": ans,
            "marks_awarded": m.get("marks_awarded", 0),
            "feedback": m.get("feedback", ""),
            "model_answer": m.get("model_answer", ""),
        }

    results = await asyncio.gather(*(mark_one(i, q) for i, q in enumerate(questions)))
    results = list(results)
    total = sum(int(q.get("marks") or 0) for q in questions)
    awarded = sum(int(r.get("marks_awarded") or 0) for r in results)
    score = round(100 * awarded / total, 1) if total else 0.0
    return score, results


def finalize_written_marks(questions: list[dict], per_q: list[dict], answers: list) -> tuple[float, list[dict]]:
    """Build final result rows from MANUALLY entered marks (teacher/admin path).
    `per_q[i]` = {marks_awarded, feedback?, model_answer?}. Returns (score, results)."""
    results = []
    total = awarded = 0
    for i, q in enumerate(questions):
        marks = int(q.get("marks") or 0)
        entry = per_q[i] if i < len(per_q) else {}
        got = max(0, min(int(entry.get("marks_awarded") or 0), marks))
        total += marks
        awarded += got
        results.append({
            "question": q.get("question"),
            "marks": marks,
            "image": q.get("image"),
            "your_answer": answers[i] if i < len(answers) else "",
            "marks_awarded": got,
            "feedback": (entry.get("feedback") or "").strip(),
            "model_answer": (entry.get("model_answer") or "").strip(),
        })
    score = round(100 * awarded / total, 1) if total else 0.0
    return score, results


def estimate_grade(score: float, level: str) -> str:
    """Map a percentage to an indicative GCSE (1–9) or A-Level (A*–E) grade."""
    if (level or "").upper().startswith("A"):  # A-Level
        bands = [(90, "A*"), (80, "A"), (70, "B"), (60, "C"), (50, "D"), (40, "E")]
        for cutoff, g in bands:
            if score >= cutoff:
                return g
        return "U"
    # GCSE 9–1
    bands = [(95, "9"), (85, "8"), (75, "7"), (65, "6"), (55, "5"), (45, "4"), (35, "3"), (25, "2"), (10, "1")]
    for cutoff, g in bands:
        if score >= cutoff:
            return g
    return "U"
