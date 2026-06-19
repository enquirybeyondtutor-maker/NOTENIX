import json
import re
import anthropic
from config import get_settings
from services.rag_service import search_knowledge_base

settings = get_settings()
client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

SUBJECTS = {
    "maths": "Mathematics",
    "biology": "Biology",
    "chemistry": "Chemistry",
    "physics": "Physics",
    "computer_science": "Computer Science",
    "economics": "Economics",
    "english_literature": "English Literature",
    "geography": "Geography",
    "history": "History",
    "psychology": "Psychology",
    "business": "Business Studies",
}

GRADE_THRESHOLDS_GCSE = [
    (90, "Grade 9"), (80, "Grade 8"), (70, "Grade 7"), (60, "Grade 6"),
    (50, "Grade 5"), (40, "Grade 4"), (30, "Grade 3"), (20, "Grade 2"), (0, "Grade 1"),
]
GRADE_THRESHOLDS_A = [(90, "A*"), (80, "A"), (70, "B"), (60, "C"), (50, "D"), (0, "E")]


def sanitise_topic(topic: str) -> str:
    """Strip HTML tags and special chars, enforce max length."""
    topic = re.sub(r"<[^>]+>", "", topic)
    topic = re.sub(r"[<>\"'%;()&+\\|`$]", "", topic)
    return topic.strip()[:100]


def _extract_json(text: str) -> list:
    """Try to extract a JSON array from Claude's response."""
    text = text.strip()
    # Strip markdown fences
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("["):
                text = part
                break
    # Find first [ ... ] block
    start = text.find("[")
    end = text.rfind("]")
    if start != -1 and end != -1:
        text = text[start:end + 1]
    return json.loads(text)


async def generate_quiz(
    subject: str,
    topic: str,
    level: str,
    exam_board: str,
    num_questions: int,
    difficulty: str = "mixed",
) -> list[dict]:
    topic = sanitise_topic(topic)
    num_questions = max(1, min(40, num_questions))

    context_docs = await search_knowledge_base(topic, subject, level, n_results=5)
    context = "\n\n".join(context_docs) if context_docs else (
        f"{level.replace('_', '-').upper()} {SUBJECTS.get(subject, subject)} syllabus content for {exam_board}"
    )

    difficulty_instruction = {
        "easy": "Focus on straightforward recall and basic application questions (1-2 mark style).",
        "medium": "Include application and some analysis questions (3-4 mark style).",
        "hard": "Focus on complex analysis, evaluation and extended response questions (5-6 mark style).",
        "mixed": "Include a mix: 30% easy recall, 40% application, 30% analysis/evaluation.",
    }.get(difficulty, "mixed")

    prompt = f"""You are an expert {exam_board} {level.replace("_", "-").upper()} {SUBJECTS.get(subject, subject)} examiner.

Generate EXACTLY {num_questions} multiple-choice quiz questions on the topic: "{topic}"

Relevant syllabus context:
{context}

Requirements:
- All questions must align with {exam_board} {level.replace("_", "-").upper()} specification
- {difficulty_instruction}
- Each question has exactly 4 options labelled A, B, C, D
- Only ONE option is correct

Return ONLY a valid JSON array. No markdown, no explanation outside the array.
[
  {{
    "id": 1,
    "question": "Question text here?",
    "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
    "correct_answer": "A",
    "marks": 2,
    "difficulty": "easy",
    "subtopic": "specific subtopic name",
    "explanation": "Why the correct answer is right and why the others are wrong."
  }}
]"""

    last_error = None
    for attempt in range(3):
        try:
            message = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}],
            )
            questions = _extract_json(message.content[0].text)
            # Validate structure
            for q in questions:
                assert "question" in q and "options" in q and "correct_answer" in q
            return questions[:num_questions]
        except Exception as e:
            last_error = e
            if attempt < 2:
                # Retry with a stricter prompt nudge
                prompt += "\n\nIMPORTANT: Return ONLY the raw JSON array, starting with [ and ending with ]."
    raise ValueError(f"Quiz generation failed after 3 attempts: {last_error}")


async def analyze_quiz_results(
    questions: list[dict],
    answers: dict,
    subject: str,
    level: str,
) -> dict:
    correct = 0
    total_marks = 0
    earned_marks = 0
    breakdown = []
    subtopic_scores: dict[str, list] = {}

    for q in questions:
        qid = str(q["id"])
        user_answer = answers.get(qid, "")
        is_correct = user_answer == q["correct_answer"]
        marks = q.get("marks", 1)
        total_marks += marks
        if is_correct:
            correct += 1
            earned_marks += marks

        subtopic = q.get("subtopic", "General")
        subtopic_scores.setdefault(subtopic, []).append(1 if is_correct else 0)

        breakdown.append({
            "question_id": qid,
            "question": q["question"],
            "user_answer": user_answer,
            "correct_answer": q["correct_answer"],
            "is_correct": is_correct,
            "marks_earned": marks if is_correct else 0,
            "marks_available": marks,
            "explanation": q.get("explanation", ""),
            "subtopic": subtopic,
        })

    score_pct = (earned_marks / total_marks * 100) if total_marks > 0 else 0
    subtopic_avgs = {k: (sum(v) / len(v) * 100) for k, v in subtopic_scores.items()}
    strengths = [k for k, v in subtopic_avgs.items() if v >= 70]
    weaknesses = [k for k, v in subtopic_avgs.items() if v < 50]

    thresholds = GRADE_THRESHOLDS_A if level == "a_level" else GRADE_THRESHOLDS_GCSE
    grade = next((g for t, g in thresholds if score_pct >= t), thresholds[-1][1])

    feedback_prompt = f"""A UK student scored {score_pct:.1f}% ({earned_marks}/{total_marks} marks) on a {level.replace('_', '-')} {subject} quiz.
Strong areas: {strengths or 'None identified'}
Weak areas: {weaknesses or 'None identified'}

Write 3-4 sentences of encouraging personalised feedback and 3 specific improvement tips.
Return ONLY this JSON:
{{"feedback": "...", "tips": ["tip1", "tip2", "tip3"]}}"""

    try:
        fb_msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            messages=[{"role": "user", "content": feedback_prompt}],
        )
        fb_data = _extract_json_object(fb_msg.content[0].text)
    except Exception:
        fb_data = {"feedback": f"You scored {score_pct:.1f}%. Keep practising!", "tips": []}

    return {
        "overall_score": score_pct,
        "earned_marks": earned_marks,
        "total_marks": total_marks,
        "correct_count": correct,
        "total_questions": len(questions),
        "estimated_grade": grade,
        "strength_areas": strengths,
        "weak_areas": weaknesses,
        "subtopic_scores": subtopic_avgs,
        "question_breakdown": breakdown,
        "ai_feedback": fb_data.get("feedback", ""),
        "improvement_tips": fb_data.get("tips", []),
    }


def _extract_json_object(text: str) -> dict:
    text = text.strip()
    if "```" in text:
        parts = text.split("```")
        for part in parts:
            if part.startswith("json"):
                part = part[4:].strip()
            if part.startswith("{"):
                text = part
                break
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1:
        text = text[start:end + 1]
    return json.loads(text)


async def generate_study_plan(
    user_id: str,
    subject_progress: list[dict],
    level: str,
) -> dict:
    """Generate a personalised weekly study plan based on weak areas."""
    weak_subjects = [
        f"{p['subject']} (avg {p['average_score']:.0f}%)"
        for p in subject_progress
        if p.get("average_score", 100) < 65
    ]
    strong_subjects = [
        f"{p['subject']} (avg {p['average_score']:.0f}%)"
        for p in subject_progress
        if p.get("average_score", 0) >= 65
    ]

    prompt = f"""Create a personalised 7-day revision plan for a UK {level.replace("_", "-").upper()} student.

Weak areas needing focus: {weak_subjects or ['No data yet — general study plan']}
Strong areas for lighter revision: {strong_subjects or ['None']}

Create a practical day-by-day plan. Return ONLY this JSON:
{{
  "week_summary": "One sentence overview",
  "days": [
    {{
      "day": "Monday",
      "focus": "Subject/topic",
      "tasks": ["Task 1", "Task 2"],
      "duration_minutes": 60
    }}
  ],
  "tips": ["Study tip 1", "Study tip 2", "Study tip 3"]
}}"""

    try:
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return _extract_json_object(msg.content[0].text)
    except Exception:
        return {"week_summary": "Focus on your weakest subjects daily.", "days": [], "tips": []}
