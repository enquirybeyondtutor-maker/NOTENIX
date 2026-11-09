"""Helpers for writing Notenix SAT forms (original questions in the Digital SAT style).

    from _sat import rw, mq, spr, module, save_form

rw(domain, skill, diff, passage, question, options, answer, explanation)   # Reading & Writing
mq(domain, skill, diff, question, options, answer, explanation, check=None)  # Math multiple choice
spr(domain, skill, diff, question, answers, explanation, check=None)          # Math student-produced response

`answer` is "A".."D". `check` is an optional zero-argument function that must return True:
use it to verify a Math answer by computation. save_form() validates everything and writes
<slug>.json next to this file, which services/sat.py loads.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

RW_SKILLS = {
    "Information and Ideas": ["Central Ideas and Details", "Command of Evidence: Textual",
                              "Command of Evidence: Quantitative", "Inferences"],
    "Craft and Structure": ["Words in Context", "Text Structure and Purpose", "Cross-Text Connections"],
    "Expression of Ideas": ["Rhetorical Synthesis", "Transitions"],
    "Standard English Conventions": ["Boundaries", "Form, Structure, and Sense"],
}
MATH_SKILLS = {
    "Algebra": ["Linear equations in one variable", "Linear functions", "Linear equations in two variables",
                "Systems of linear equations", "Linear inequalities"],
    "Advanced Math": ["Nonlinear functions", "Nonlinear equations and systems", "Equivalent expressions"],
    "Problem-Solving and Data Analysis": ["Ratios, rates and units", "Percentages", "One-variable data",
                                          "Two-variable data and models", "Probability",
                                          "Sample statistics and margin of error", "Studies and experiments"],
    "Geometry and Trigonometry": ["Area and volume", "Lines, angles and triangles", "Right triangles and trigonometry",
                                  "Circles"],
}
_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def rw(domain, skill, diff, passage, question, options, answer, explanation):
    assert skill in RW_SKILLS.get(domain, []), f"bad RW skill {domain} / {skill}"
    return {"section": "rw", "domain": domain, "skill": skill, "difficulty": diff, "type": "mcq",
            "passage": passage.strip(), "question": question.strip(), "options": list(options),
            "answer": answer, "explanation": explanation.strip()}


def mq(domain, skill, diff, question, options, answer, explanation, check=None):
    assert skill in MATH_SKILLS.get(domain, []), f"bad Math skill {domain} / {skill}"
    if check is not None:
        assert check() is True, f"check failed: {question[:60]}"
    return {"section": "math", "domain": domain, "skill": skill, "difficulty": diff, "type": "mcq",
            "question": question.strip(), "options": list(options), "answer": answer,
            "explanation": explanation.strip()}


def spr(domain, skill, diff, question, answers, explanation, check=None):
    assert skill in MATH_SKILLS.get(domain, []), f"bad Math skill {domain} / {skill}"
    if check is not None:
        assert check() is True, f"check failed: {question[:60]}"
    return {"section": "math", "domain": domain, "skill": skill, "difficulty": diff, "type": "spr",
            "question": question.strip(), "answer": [str(a) for a in answers], "explanation": explanation.strip()}


def module(key, title, section, minutes, questions):
    return key, {"title": title, "section": section, "minutes": minutes, "questions": questions}


def _walk_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _walk_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk_strings(v)


def _spread_rw(slug, key, questions):
    """Reading & Writing options have no natural order, so move each correct option to an
    evenly spread letter (a fixed, repeatable pattern per module). Explanations must therefore
    never refer to options by letter."""
    import hashlib
    seed = int(hashlib.md5(f"{slug}/{key}".encode()).hexdigest(), 16)
    order = []
    while len(order) < len(questions):
        block = ["A", "B", "C", "D"]
        # rotate each block of four by the seed so modules don't share a pattern
        r = (seed >> (len(order) // 4 * 2)) & 3
        order += block[r:] + block[:r]
    for q, target in zip(questions, order):
        if q["section"] != "rw" or q["type"] != "mcq":
            continue
        i, j = "ABCD".index(q["answer"]), "ABCD".index(target)
        q["options"][i], q["options"][j] = q["options"][j], q["options"][i]
        q["answer"] = target


def save_form(slug, title, kind, modules, summary=""):
    """modules: list of module(...) tuples. Assigns ids <slug>-<module>-<n>, validates, writes JSON."""
    out = {"slug": slug, "title": title, "kind": kind, "summary": summary, "modules": {}}
    problems = []
    for key, m in modules:
        if m["section"] == "rw":
            _spread_rw(slug, key, m["questions"])
        for q in m["questions"]:
            if re.search(r"\b[Cc]hoice [A-D]\b|\boption [A-D]\b|\b\(?[A-D]\) ", q["explanation"]):
                problems.append(f"{q['question'][:50]}: explanation refers to an option by letter")
        for i, q in enumerate(m["questions"], 1):
            q["id"] = f"{slug}-{key}-{i:02d}"
            where = q["id"]
            if q["section"] != m["section"]:
                problems.append(f"{where}: section {q['section']} in a {m['section']} module")
            if q["type"] == "mcq":
                if len(q["options"]) != 4 or len(set(q["options"])) != 4:
                    problems.append(f"{where}: needs 4 different options")
                if q["answer"] not in "ABCD" or len(q["answer"]) != 1:
                    problems.append(f"{where}: answer must be A-D")
            elif not q["answer"]:
                problems.append(f"{where}: no accepted answers")
            if q["difficulty"] not in (1, 2, 3):
                problems.append(f"{where}: difficulty must be 1-3")
            if len(q["explanation"]) < 20:
                problems.append(f"{where}: explanation too short")
        mcq = [q["answer"] for q in m["questions"] if q["type"] == "mcq"]
        if len(mcq) >= 8:
            worst = max(mcq.count(x) for x in "ABCD")
            if worst > len(mcq) * 0.4:
                problems.append(f"{key}: answers bunched ({ {x: mcq.count(x) for x in 'ABCD'} })")
        out["modules"][key] = m
    for s in _walk_strings(out):
        if _CTRL.search(s):
            problems.append(f"control character in: {s[:60]!r}")
    if problems:
        raise SystemExit("PROBLEMS:\n  " + "\n  ".join(problems))
    path = HERE / f"{slug}.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(len(m["questions"]) for _, m in modules)
    print(f"{slug}: {n} questions in {len(modules)} modules -> {path.name}")
