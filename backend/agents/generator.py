import json
from typing import AsyncIterator
from openai import OpenAI

client = OpenAI()
MODEL = "gpt-4o"


async def generate_questions(
    notes_text: str,
    knowledge_map: dict,
    question_types: list[str] | None = None,
) -> AsyncIterator[str]:
    if question_types is None:
        question_types = ["mcq", "flashcard", "short_answer"]

    subject = knowledge_map.get("subject", "the subject")
    topics = [t["name"] for t in knowledge_map.get("main_topics", [])]

    system = (
        f"You are an expert question creator for {subject}. "
        "Create high-quality, curriculum-aligned practice questions. "
        "Always output valid JSON only — no markdown wrappers."
    )

    prompt = f"""Generate comprehensive practice questions from these study notes.

NOTES:
{notes_text}

TOPICS COVERED: {', '.join(topics)}
QUESTION TYPES NEEDED: {', '.join(question_types)}

Return a single JSON object with a "questions" array. Each item must have:
- id (string, e.g. "q1")
- type ("mcq" | "flashcard" | "short_answer")
- topic (topic name it belongs to)
- question (the question text)

For MCQ also include:
- options (object: A, B, C, D)
- correct_answer ("A"|"B"|"C"|"D")
- explanation (why the answer is correct)

For flashcard also include:
- front (the prompt)
- back (the answer)

For short_answer also include:
- model_answer (ideal answer)
- key_points (array of must-include points)

Minimums: 15 MCQs, 20 flashcards, 8 short_answer questions."""

    stream = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        max_tokens=8192,
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


async def collect_questions(
    notes_text: str,
    knowledge_map: dict,
    question_types: list[str] | None = None,
) -> list[dict]:
    chunks: list[str] = []
    async for chunk in generate_questions(notes_text, knowledge_map, question_types):
        chunks.append(chunk)

    raw = "".join(chunks)
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0]
    elif "```" in raw:
        raw = raw.split("```")[1].split("```")[0]

    data = json.loads(raw.strip())
    return data.get("questions", [])
