"""Tiny helpers for writing KS3 content as Python (less noise than raw JSON).

Q(topic, question, [options], index_of_correct, explanation)
save_test(slot, subject, title, minutes, questions)  -> tests/<slot>-<subject>.json
save_note(key, year, subject, title, body)          -> notes/<key>.json

Write anything with LaTeX as a raw string r"..." so \\times, \\frac etc. survive.
"""
import json
import random
from pathlib import Path

HERE = Path(__file__).parent
BAD = {"\t": "\\t", "\f": "\\f", "\b": "\\b", "\r": "\\r", "\v": "\\v", "\a": "\\a"}


def _clean(s: str, where: str) -> str:
    for ch, name in BAD.items():
        assert ch not in s, f"control character {name} in {where!r}: use a raw string r\"...\""
    return s


def Q(topic: str, question: str, options: list[str], correct: int, explanation: str) -> dict:
    assert len(options) == 4 and len(set(options)) == 4, f"need 4 different options: {question[:50]}"
    assert 0 <= correct < 4
    for s in [topic, question, explanation, *options]:
        _clean(s, question[:40])
    return {"topic": topic, "question": question, "options": list(options), "answer": options[correct], "explanation": explanation}


def _spread(slot: str, questions: list[dict]) -> None:
    """Move each correct answer to an evenly spread position (A-D), the same every build."""
    targets = [i % 4 for i in range(len(questions))]
    random.Random(slot).shuffle(targets)
    for q, t in zip(questions, targets):
        opts = q["options"]
        i = opts.index(q["answer"])
        opts[i], opts[t] = opts[t], opts[i]


def save_test(slot: str, subject: str, title: str, minutes: int, questions: list[dict]) -> None:
    assert len(questions) >= 10, f"{title}: only {len(questions)} questions"
    _spread(f"{slot}-{subject}", questions)
    for q in questions:
        assert q["answer"] in q["options"]
    out = HERE / "tests" / f"{slot}-{subject.lower()}.json"
    out.write_text(json.dumps({"slot": slot, "subject": subject, "title": title, "topic": slot.split("-", 1)[1],
                               "duration": minutes, "questions": questions}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  {out.name}: {len(questions)} Qs")


def save_note(key: str, year: int, subject: str, title: str, body: str) -> None:
    _clean(body, key)
    (HERE / "notes" / f"{key}.json").write_text(json.dumps(
        {"key": key, "year": year, "subject": subject, "title": f"Year {year} {subject}: {title}", "body": body.strip()},
        ensure_ascii=False, indent=2), encoding="utf-8")
