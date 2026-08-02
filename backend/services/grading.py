"""MCQ auto-grading + estimated-grade mapping for assigned tests."""


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
            "your_answer": given,
            "correct_answer": right,
            "is_correct": is_correct,
            "explanation": q.get("explanation"),
        })
    score = round(100 * correct / len(questions), 1) if questions else 0.0
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
