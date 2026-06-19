import json
from openai import OpenAI

client = OpenAI()
MODEL = "gpt-4o"


def _strip_json(text: str) -> str:
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    return text.strip()


async def evaluate_answer(question: dict, student_answer: str, notes_text: str) -> dict:
    q_type = question.get("type", "mcq")
    q_id = question.get("id", "unknown")
    topic = question.get("topic", "")

    if q_type == "mcq":
        correct = question.get("correct_answer", "").upper()
        given = student_answer.strip().upper()
        is_correct = given == correct
        score = 100 if is_correct else 0
        explanation = question.get("explanation", "")
        feedback = (
            f"Correct! {explanation}" if is_correct
            else f"Incorrect. The right answer is **{correct}**. {explanation}"
        )
        return {
            "question_id": q_id,
            "is_correct": is_correct,
            "score": score,
            "feedback": feedback,
            "correct_answer": correct,
            "weak_topic": None if is_correct else topic,
        }

    elif q_type == "flashcard":
        return {
            "question_id": q_id,
            "is_correct": None,
            "score": None,
            "feedback": question.get("back", ""),
            "correct_answer": question.get("back", ""),
            "weak_topic": None,
        }

    else:  # short_answer
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert educational assessor. Evaluate student answers fairly "
                        "and constructively. Always respond with valid JSON only."
                    ),
                },
                {
                    "role": "user",
                    "content": f"""QUESTION: {question.get('question')}

MODEL ANSWER: {question.get('model_answer')}
KEY POINTS REQUIRED: {', '.join(question.get('key_points', []))}

STUDENT'S ANSWER: {student_answer}

Return JSON with:
- score (0-100)
- is_correct (true if score >= 70)
- feedback (2-3 sentences: what was good, what was missing)
- missing_points (array of key points the student missed)
- good_points (array of things the student got right)
- improvement_tip (one actionable suggestion)""",
                },
            ],
            max_tokens=1024,
            response_format={"type": "json_object"},
        )

        text = response.choices[0].message.content or "{}"
        result = json.loads(_strip_json(text))
        result["question_id"] = q_id
        result["weak_topic"] = topic if result.get("score", 0) < 60 else None
        return result
