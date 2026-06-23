"""Claude-powered question generation and exam answer marking."""
import json
import re
from anthropic import Anthropic
from config import settings

_client = None


def client() -> Anthropic:
    global _client
    if _client is None:
        _client = Anthropic(api_key=settings.anthropic_api_key)
    return _client


def _extract_json(text: str):
    """Robustly pull a JSON array/object out of a model response."""
    text = text.strip()
    # strip code fences
    text = re.sub(r"^```(?:json)?", "", text).strip().rstrip("`").strip()
    start = min((i for i in (text.find("["), text.find("{")) if i != -1), default=-1)
    if start == -1:
        raise ValueError("No JSON found")
    end = max(text.rfind("]"), text.rfind("}"))
    return json.loads(text[start:end + 1])


def generate_mcqs(subject: str, topic: str, difficulty: str, n: int, context: list[str]) -> list[dict]:
    """Generate n MCQs grounded in real past-paper questions (context)."""
    context_block = "\n\n".join(f"- {c[:600]}" for c in context[:10]) or "(no source questions available)"
    prompt = f"""You are an expert {subject} examiner creating GCSE/A-Level multiple choice questions.

Below are REAL past-paper questions on the topic "{topic}". Use them to ground your questions in
authentic exam content and style, but write NEW multiple choice questions (do not copy verbatim).

SOURCE QUESTIONS:
{context_block}

Create exactly {n} multiple choice questions at {difficulty} difficulty about "{topic}" in {subject}.
Return ONLY a JSON array. Each object must have:
{{
  "question": "the question text",
  "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "answer": "B) ...",   // must exactly match one option
  "explanation": "1-2 sentence explanation of why the answer is correct"
}}
Return only the JSON array, nothing else."""

    for attempt in range(3):
        try:
            msg = client().messages.create(
                model=settings.claude_model,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}],
            )
            data = _extract_json(msg.content[0].text)
            if isinstance(data, list) and data:
                return data[:n]
        except Exception:
            if attempt == 2:
                raise
    return []


def generate_mark_scheme(question: str, marks: int, subject: str) -> str:
    """Generate a concise mark scheme for an extracted exam question."""
    prompt = f"""You are a {subject} examiner. Write a concise mark scheme for this {marks}-mark question.
List the credit-worthy points as bullet points (roughly one per mark).

QUESTION:
{question}

Return only the mark scheme bullet points."""
    msg = client().messages.create(
        model=settings.claude_model,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def mark_answer(question: str, marks: int, mark_scheme: str, student_answer: str, subject: str) -> dict:
    """Mark a student's written answer against the mark scheme."""
    prompt = f"""You are a {subject} examiner marking a {marks}-mark question.

QUESTION:
{question}

MARK SCHEME:
{mark_scheme}

STUDENT ANSWER:
{student_answer}

Award marks fairly using the mark scheme. Return ONLY JSON:
{{
  "marks_awarded": <int 0..{marks}>,
  "feedback": "specific feedback: what earned marks, what was missing",
  "model_answer": "a concise model answer that would score full marks"
}}"""
    for attempt in range(3):
        try:
            msg = client().messages.create(
                model=settings.claude_model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}],
            )
            data = _extract_json(msg.content[0].text)
            data["marks_awarded"] = max(0, min(int(data.get("marks_awarded", 0)), marks))
            return data
        except Exception:
            if attempt == 2:
                return {"marks_awarded": 0, "feedback": "Could not mark answer automatically.", "model_answer": ""}
    return {"marks_awarded": 0, "feedback": "", "model_answer": ""}
