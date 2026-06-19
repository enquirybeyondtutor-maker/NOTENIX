from typing import AsyncIterator
from openai import OpenAI

client = OpenAI()
MODEL = "gpt-4o"


async def tutor_response(
    notes_text: str,
    conversation_history: list[dict],
    user_question: str,
    knowledge_map: dict,
) -> AsyncIterator[str]:
    subject = knowledge_map.get("subject", "the subject")
    topics = [t["name"] for t in knowledge_map.get("main_topics", [])]

    system = f"""You are a personalized AI tutor for {subject}.

Your job:
- Answer questions by referencing the student's own notes whenever possible
- Quote or paraphrase directly from the notes to ground your explanations
- Use Socratic questioning to deepen understanding ("What do you think happens when…?")
- If a concept isn't covered in the notes, say so and offer a concise explanation anyway
- Keep answers focused — prefer clarity over length
- Topics in scope: {', '.join(topics)}

STUDENT'S NOTES (reference these when answering):
{notes_text}"""

    # Build messages: system + last 6 history turns + new question
    messages = [{"role": "system", "content": system}]
    messages.extend(conversation_history[-6:])
    messages.append({"role": "user", "content": user_question})

    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=2048,
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
