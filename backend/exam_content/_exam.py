r"""Helpers for writing exam-engine content (services/exams.py), e.g. TMUA.

    from _exam import q, module, save_form, save_drills

q(domain, skill, diff, question, options, answer, explanation, check=None, passage=None)
    A multiple-choice question with 2-8 options; answer is a letter "A".."H". `check` is an
    optional zero-argument function that must return True (verifies the answer by computation).
module(key, title, section, minutes, questions)
save_form(exam, slug, title, kind, modules, summary="")   # kind "mock" or "diagnostic"; stages = module order
save_drills(exam, {skill: (about, [questions])})            # one 'drills' form, one module per skill

Everything is validated (skills against the exam's list, options, answers, explanations,
answer letters not bunched) before <exam>/<slug>.json is written.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from services.exams import EXAMS, slugify  # noqa: E402

LETTERS = "ABCDEFGH"
_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_LETTER_REF = re.compile(r"\b[Cc]hoice [A-H]\b|\b[Oo]ption [A-H]\b|\([A-H]\) ")


def q(domain, skill, diff, question, options, answer, explanation, check=None, passage=None):
    if check is not None:
        assert check() is True, f"check failed: {question[:70]}"
    out = {"domain": domain, "skill": skill, "difficulty": diff, "type": "mcq", "question": question.strip(),
           "options": list(options), "answer": answer, "explanation": explanation.strip()}
    if passage:
        out["passage"] = passage.strip()
    return out


def module(key, title, section, minutes, questions):
    return key, {"title": title, "section": section, "minutes": minutes,
                 "questions": [{**x, "section": section} for x in questions]}


def _validate(exam, key, m, problems, where_prefix):
    cfg = EXAMS[exam]
    skills = {(d, s) for d, ss in cfg["domains"].items() for s in ss}
    if m["section"] not in cfg["sections"] and m["section"] != "drill":
        problems.append(f"{key}: unknown section {m['section']}")
    for i, x in enumerate(m["questions"], 1):
        x["id"] = f"{where_prefix}-{key}-{i:02d}"
        w = x["id"]
        if (x["domain"], x["skill"]) not in skills:
            problems.append(f"{w}: skill {x['domain']} / {x['skill']} is not in the {exam} skill list")
        n = len(x["options"])
        if not 2 <= n <= 8 or len(set(x["options"])) != n:
            problems.append(f"{w}: needs 2-8 different options")
        if len(x["answer"]) != 1 or x["answer"] not in LETTERS[:n]:
            problems.append(f"{w}: answer must be one of {LETTERS[:n]}")
        if x["difficulty"] not in (1, 2, 3):
            problems.append(f"{w}: difficulty must be 1-3")
        if len(x["explanation"]) < 25:
            problems.append(f"{w}: explanation too short")
        if _LETTER_REF.search(x["explanation"]):
            problems.append(f"{w}: explanation names an option by letter")
        if "underline" in x["question"].lower():
            problems.append(f"{w}: questions cannot rely on underlining")
    ans = [x["answer"] for x in m["questions"]]
    if len(ans) >= 8:
        worst = max(Counter(ans).values())
        if worst > len(ans) * 0.35:
            problems.append(f"{key}: answers bunched {dict(sorted(Counter(ans).items()))}")


def _write(exam, slug, out, problems):
    for s in _strings(out):
        if _CTRL.search(s):
            problems.append(f"control character in: {s[:60]!r}")
    if problems:
        raise SystemExit("PROBLEMS:\n  " + "\n  ".join(problems))
    folder = HERE / exam
    folder.mkdir(exist_ok=True)
    (folder / f"{slug}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    n = sum(len(m["questions"]) for m in out["modules"].values())
    print(f"{exam}/{slug}: {n} questions in {len(out['modules'])} modules")


def save_form(exam, slug, title, kind, modules, summary=""):
    assert kind in ("mock", "diagnostic")
    out = {"exam": exam, "slug": slug, "title": title, "kind": kind, "summary": summary,
           "stages": [k for k, _ in modules], "modules": {}}
    problems = []
    for key, m in modules:
        _validate(exam, key, m, problems, f"{exam}-{slug}")
        out["modules"][key] = m
    _write(exam, slug, out, problems)


def save_drills(exam, skills: dict):
    """skills: {skill name: (about, [q(...), ...])}. The domain comes from each question."""
    out = {"exam": exam, "slug": "drills", "title": f"{EXAMS[exam]['name']} skill drills", "kind": "drills",
           "stages": [], "modules": {}}
    problems = []
    known = [s for ss in EXAMS[exam]["domains"].values() for s in ss]
    for skill, (about, qs) in skills.items():
        if skill not in known:
            problems.append(f"drill for unknown skill {skill}")
            continue
        slug = slugify(skill)
        m = {"title": skill, "domain": qs[0]["domain"], "section": "drill", "minutes": 0, "about": about,
             "questions": [{**x, "section": "drill"} for x in qs]}
        if any(x["skill"] != skill for x in qs):
            problems.append(f"{slug}: a question is tagged with another skill")
        _validate(exam, slug, m, problems, f"{exam}-drill")
        out["modules"][slug] = m
    _write(exam, "drills", out, problems)


def _strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _strings(v)
