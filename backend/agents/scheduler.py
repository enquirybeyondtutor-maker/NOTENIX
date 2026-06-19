import json
from datetime import datetime, timedelta
from openai import OpenAI

client = OpenAI()
MODEL = "gpt-4o"


def _strip_json(text: str) -> str:
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    return text.strip()


async def create_revision_plan(
    knowledge_map: dict,
    performance_data: dict,
    available_days: int = 7,
) -> dict:
    topics = knowledge_map.get("main_topics", [])
    weak_topics = performance_data.get("weak_topics", [])
    scores_by_topic = performance_data.get("scores_by_topic", {})
    overall_score = performance_data.get("overall_score", 0)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert in spaced repetition and educational psychology. "
                    "Apply Ebbinghaus forgetting curve principles: review weak topics at intervals "
                    "of 1, 3, and 7 days for maximum retention. Always respond with valid JSON only."
                ),
            },
            {
                "role": "user",
                "content": f"""Create a {available_days}-day spaced repetition revision plan.

SUBJECT: {knowledge_map.get('subject')}
ALL TOPICS: {json.dumps([t['name'] for t in topics])}
WEAK TOPICS (prioritize these): {json.dumps(weak_topics)}
SCORES BY TOPIC: {json.dumps(scores_by_topic)}
OVERALL SCORE: {overall_score}%

Return JSON:
{{
  "plan_summary": "string",
  "daily_schedule": [
    {{
      "day": 1,
      "date": "TBD",
      "focus_topics": ["topic1"],
      "activities": [
        {{
          "type": "flashcards"|"mcq"|"short_answer"|"review",
          "topic": "string",
          "duration_minutes": 15,
          "description": "string",
          "question_types": ["mcq"]
        }}
      ],
      "total_minutes": 45,
      "priority": "high"|"medium"|"low"
    }}
  ],
  "weak_area_focus": "string explaining the strategy for weak topics",
  "confidence_prediction": "string predicting score improvement"
}}""",
            },
        ],
        max_tokens=3000,
        response_format={"type": "json_object"},
    )

    text = response.choices[0].message.content or "{}"
    plan = json.loads(_strip_json(text))

    today = datetime.now()
    for i, day in enumerate(plan.get("daily_schedule", [])):
        day["date"] = (today + timedelta(days=i)).strftime("%Y-%m-%d")

    return plan
