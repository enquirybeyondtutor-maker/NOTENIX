"""Claude-powered question generation and exam answer marking."""
import json
import re
import base64
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


def generate_mcqs_from_document(document_text: str, subject: str, level: str, n: int) -> list[dict]:
    """Read a source document (e.g. a past paper or worksheet PDF) and produce
    auto-gradable MCQs covering its content."""
    excerpt = document_text.strip()[:12000] or "(empty document)"
    prompt = f"""You are an expert {subject} examiner. Below is the text of a {level} document
(a past paper, worksheet or set of notes) uploaded by a teacher.

DOCUMENT:
\"\"\"
{excerpt}
\"\"\"

Create exactly {n} multiple choice questions that assess understanding of the material in this
document. Prefer questions grounded in the actual content above. Return ONLY a JSON array where
each object is:
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


def transcribe_mcqs_from_images(images: list[bytes], subject: str, n: int) -> list[dict]:
    """Read rendered PDF page images with vision and transcribe the multiple-choice
    questions EXACTLY as written (verbatim) — preserves original wording, numbers,
    equations and symbols. Only fills in options/answer when the source lacks them."""
    if not images:
        return []
    blocks: list[dict] = [{
        "type": "text",
        "text": (
            f"These images are pages of a {subject} exam paper or worksheet uploaded by a teacher.\n\n"
            f"Transcribe up to {n} multiple-choice questions from these pages EXACTLY as written — "
            "do NOT paraphrase, reword, simplify or fix anything. Preserve the original wording, "
            "numbers, units, equations and symbols verbatim. Include every answer option exactly as "
            "printed. If a question has no printed options, write four sensible options with the "
            "correct one included.\n\n"
            "The page images are numbered 0, 1, 2 … in the order given. If a question has "
            "an associated figure, diagram, graph, map or image, add a \"figure\" object: "
            '{"page": <0-based page index it appears on>, "box": [x0,y0,x1,y1]} where the '
            "box coordinates are fractions from 0 to 1 of that page's width/height "
            "(top-left origin) tightly bounding just the figure. Omit \"figure\" if there is none.\n\n"
            "Return ONLY a JSON array; each object:\n"
            '{"question": "verbatim question text", "options": ["A) ...","B) ...","C) ...","D) ..."], '
            '"answer": "the exact correct option (must match one of options)", '
            '"explanation": "one short sentence", "figure": {"page": 0, "box": [0.1,0.2,0.6,0.5]}}\n'
            "Return only the JSON array."
        ),
    }]
    for img in images[:8]:
        blocks.append({
            "type": "image",
            "source": {"type": "base64", "media_type": "image/png", "data": base64.b64encode(img).decode()},
        })

    for attempt in range(3):
        try:
            msg = client().messages.create(
                model=settings.claude_model,
                max_tokens=4500,
                messages=[{"role": "user", "content": blocks}],
            )
            data = _extract_json(msg.content[0].text)
            if isinstance(data, list) and data:
                return data[:n]
        except Exception:
            if attempt == 2:
                raise
    return []


def extract_written_from_images(images: list[bytes], subject: str, level: str, n: int) -> list[dict]:
    """Read rendered PDF page images with vision and transcribe the EXTENDED-RESPONSE
    (written-answer) questions EXACTLY as written — the ones a student answers in prose,
    not multiple choice. Preserves original wording, mark allocations and symbols, and
    drafts a concise mark scheme for each so answers can be marked later."""
    if not images:
        return []
    blocks: list[dict] = [{
        "type": "text",
        "text": (
            f"These images are pages of a {level} {subject} exam paper uploaded for practice.\n\n"
            f"Transcribe up to {n} EXTENDED-RESPONSE / written-answer questions from these pages — "
            "the questions a student answers in prose or working (e.g. 'Explain…', 'Describe…', "
            "'Calculate…', 'Evaluate…'), each worth a stated number of marks. IGNORE multiple-choice "
            "questions. Transcribe each question EXACTLY as written — do NOT paraphrase, reword or "
            "simplify. Preserve the original wording, numbers, units, equations and symbols verbatim. "
            "Use the printed mark allocation (e.g. '[6 marks]'); if none is printed, estimate a sensible "
            "one. For each question also draft a concise mark scheme (credit-worthy points, roughly one "
            "per mark).\n\n"
            "The page images are numbered 0, 1, 2 … in the order given. If a question has an associated "
            "figure, diagram, graph, map or image, add a \"figure\" object: "
            '{"page": <0-based page index it appears on>, "box": [x0,y0,x1,y1]} where the box '
            "coordinates are fractions from 0 to 1 of that page's width/height (top-left origin) tightly "
            "bounding just the figure. Omit \"figure\" if there is none.\n\n"
            "Return ONLY a JSON array; each object:\n"
            '{"question": "verbatim question text", "marks": <int>, '
            '"mark_scheme": "bullet points of credit-worthy points, one per line", '
            '"figure": {"page": 0, "box": [0.1,0.2,0.6,0.5]}}\n'
            "Return only the JSON array."
        ),
    }]
    for img in images[:8]:
        blocks.append({
            "type": "image",
            "source": {"type": "base64", "media_type": "image/png", "data": base64.b64encode(img).decode()},
        })

    for attempt in range(3):
        try:
            msg = client().messages.create(
                model=settings.claude_model,
                max_tokens=4500,
                messages=[{"role": "user", "content": blocks}],
            )
            data = _extract_json(msg.content[0].text)
            if isinstance(data, list) and data:
                out = []
                for q in data[:n]:
                    try:
                        marks = max(1, min(int(q.get("marks", 1)), 30))
                    except (TypeError, ValueError):
                        marks = 1
                    item = {
                        "question": (q.get("question") or "").strip(),
                        "marks": marks,
                        "mark_scheme": (q.get("mark_scheme") or "").strip(),
                    }
                    if isinstance(q.get("figure"), dict):
                        item["figure"] = q["figure"]  # cropped to an image later
                    out.append(item)
                out = [q for q in out if q["question"]]
                if out:
                    return out
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
