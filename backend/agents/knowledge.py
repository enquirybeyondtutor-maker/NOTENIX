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


async def extract_knowledge(notes_text: str, subject_hint: str = "") -> dict:
    system = (
        "You are an expert educational content analyzer. Analyze study notes and extract "
        "structured knowledge including topics, concepts, formulas, and difficulty levels. "
        "Always respond with valid JSON only — no markdown, no commentary."
    )

    subject_line = f"Subject/Context: {subject_hint}\n\n" if subject_hint else ""
    prompt = f"""{subject_line}Analyze these study notes and extract a comprehensive knowledge map.

NOTES:
{notes_text}

Return a JSON object with exactly these keys:
- subject (string)
- difficulty_level ("beginner" | "intermediate" | "advanced")
- main_topics (array of objects: name, subtopics[], key_concepts[], importance 1-10)
- formulas (array: name, expression, variables[], topic)
- definitions (array: term, definition, topic)
- estimated_questions (object: mcq, flashcards, short_answer)
- summary (2-3 sentence overview)"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        max_tokens=4096,
        response_format={"type": "json_object"},
    )

    text = response.choices[0].message.content or "{}"
    return json.loads(_strip_json(text))
