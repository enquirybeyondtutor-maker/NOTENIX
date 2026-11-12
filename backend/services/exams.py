"""Notenix exam engine: timed practice tests, score estimates, skill map, study plan and weekly
email for the admissions exams (TMUA now; ESAT, TARA and course diagnostics next).

Each exam is a settings block in EXAMS. Its content lives in backend/exam_content/<exam>/*.json,
written by the scripts in that folder (see exam_content/_exam.py):
  • "diagnostic": a short test anyone can take without an account (a score band);
  • kind "mock": a full practice test, modules sat in order (form["stages"]);
  • "drills": one module per skill, six questions each, checked one at a time.

Questions: {id, section, domain, skill, difficulty 1-3, type "mcq", passage?, question,
options (2-8), answer "A".."H", explanation}. Students never see answer/explanation before
submitting. SAT keeps its own adaptive engine (services/sat.py).

Scores are Notenix estimates from the share of questions right, mapped onto the exam's
scale. Real scores use the test owner's own scaling, which a practice test can only approximate.
"""
import json
from functools import lru_cache
from pathlib import Path

from services.sat import is_correct  # same marking rules (mcq letter, or accepted answers)

CONTENT = Path(__file__).resolve().parent.parent / "exam_content"

EXAMS: dict[str, dict] = {
    "tmua": {
        "name": "TMUA",
        "full_name": "Test of Mathematics for University Admission",
        "course": "tmua",
        "sections": {"p1": "Paper 1: Applications of Mathematical Knowledge", "p2": "Paper 2: Mathematical Reasoning"},
        # Skill map: domain -> skills (the same list for both papers).
        "domains": {
            "Algebra and functions": ["Algebraic manipulation", "Equations and inequalities", "Polynomials",
                                      "Exponentials and logarithms", "Sequences and series"],
            "Geometry and graphs": ["Coordinate geometry", "Trigonometry", "Graphs and transformations"],
            "Calculus": ["Differentiation", "Integration"],
            "Logic": ["Logical statements", "Necessary and sufficient conditions"],
            "Proof": ["Proof and counterexamples", "Errors in proofs"],
        },
        # Share right -> score. Roughly the shape of past TMUA conversions; an estimate only.
        "scale": {"min": 1.0, "max": 9.0, "decimals": 1,
                  "points": [(0.0, 1.0), (0.2, 2.5), (0.4, 4.0), (0.55, 5.0), (0.7, 6.0), (0.85, 7.2), (1.0, 9.0)]},
        "band": 0.7,                 # ± around a diagnostic estimate
        "target_range": (1.0, 9.0),
        "calculator": False,
        "mock_detail": "2 papers · 40 questions · 2 h 30 min",
        "about_score": "TMUA scores run from 1.0 to 9.0. Ours are Notenix estimates from the share of questions you get right; the real test uses its own scaling.",
    },
    "ap-calc-ab": {
        "name": "AP Calculus AB",
        "full_name": "AP Calculus AB (College Board)",
        "course": "ap-calc-ab",
        "sections": {"mcq-a": "Section I Part A: Multiple choice, no calculator",
                     "mcq-b": "Section I Part B: Multiple choice, graphing calculator"},
        "no_calculator": ["mcq-a"],
        # The eight College Board units, grouped.
        "domains": {
            "Limits and continuity": ["Limits and continuity"],
            "Differentiation": ["Derivative rules", "Chain, implicit and inverse",
                                "Contextual applications", "Analytical applications"],
            "Integration": ["Integration and accumulation", "Differential equations",
                            "Applications of integration"],
        },
        # Share right -> AP score 1-5 (roughly the usual AB cut-offs; an estimate only).
        "scale": {"min": 1.0, "max": 5.0, "decimals": 1,
                  "points": [(0.0, 1.0), (0.25, 1.5), (0.4, 2.5), (0.5, 3.0), (0.62, 4.0), (0.72, 4.6), (1.0, 5.0)]},
        "band": 0.5,
        "target_range": (1.0, 5.0),
        "calculator": True,
        "mock_detail": "Section I · 45 multiple-choice questions · 1 h 45 min (Part A no calculator, Part B calculator)",
        "about_score": "AP scores run from 1 to 5; most universities look for a 4 or 5. Ours are Notenix estimates from the multiple-choice share you get right. The real score also counts the six written free-response questions.",
    },
    "gcse-maths": {
        "name": "GCSE Maths",
        "full_name": "GCSE Mathematics (AQA, Edexcel, OCR)",
        "course": "gcse-maths",
        "access": ("GCSE", "maths"),   # opened by the gcse-maths course (see routers/exam._allowed)
        "sections": {"non-calc": "Non-calculator", "calc": "Calculator"},
        "no_calculator": ["non-calc"],   # sections sat without the on-screen calculator
        "domains": {
            "Number": ["Fractions, decimals and percentages", "Indices, standard form and surds", "Factors, multiples and estimation"],
            "Algebra": ["Expressions and formulae", "Equations and inequalities", "Sequences", "Graphs and functions"],
            "Ratio and proportion": ["Ratio and proportion", "Percentage change and growth"],
            "Geometry and measures": ["Angles and shapes", "Area, volume and Pythagoras", "Trigonometry", "Vectors and transformations"],
            "Probability and statistics": ["Probability", "Statistics"],
        },
        # Share right -> grade 1-9. An estimate only: real boundaries move each year.
        "scale": {"min": 1.0, "max": 9.0, "decimals": 0,
                  "points": [(0.0, 1.0), (0.15, 2.0), (0.3, 3.0), (0.42, 4.0), (0.54, 5.0), (0.65, 6.0),
                             (0.76, 7.0), (0.86, 8.0), (0.94, 9.0), (1.0, 9.0)]},
        "band": 1.0,
        "target_range": (1.0, 9.0),
        "calculator": True,
        "mock_detail": "Multiple-choice practice papers · non-calculator and calculator sections",
        "about_score": "GCSE grades run from 1 to 9. Ours are Notenix estimates from the share of questions you get right; real grade boundaries change every year and depend on your tier and exam board.",
    },
    "gcse-biology": {
        "name": "GCSE Biology",
        "full_name": "GCSE Biology (AQA, Edexcel, OCR)",
        "course": "gcse-biology",
        "access": ("GCSE", "biology"),   # opened by the gcse-biology course (see routers/exam._allowed)
        "sections": {"p1": "Paper 1 topics", "p2": "Paper 2 topics"},
        "domains": {
            "Cells and organisation": ["Cell structure and transport", "Cell division", "Organisation and digestion", "Heart, blood and circulation"],
            "Infection and bioenergetics": ["Infection and response", "Photosynthesis", "Respiration"],
            "Control and inheritance": ["Homeostasis and hormones", "Nervous system", "Inheritance and genetics", "Variation and evolution"],
            "Ecology": ["Ecology"],
        },
        # Share right -> grade 1-9. An estimate only: real boundaries move each year.
        "scale": {"min": 1.0, "max": 9.0, "decimals": 0,
                  "points": [(0.0, 1.0), (0.15, 2.0), (0.3, 3.0), (0.42, 4.0), (0.54, 5.0), (0.65, 6.0),
                             (0.76, 7.0), (0.86, 8.0), (0.94, 9.0), (1.0, 9.0)]},
        "band": 1.0,
        "target_range": (1.0, 9.0),
        "calculator": True,
        "mock_detail": "Multiple-choice practice papers · Paper 1 and Paper 2 topics",
        "about_score": "GCSE grades run from 1 to 9. Ours are Notenix estimates from the share of questions you get right; real grade boundaries change every year and depend on your tier and exam board.",
    },
    "gcse-chemistry": {
        "name": "GCSE Chemistry",
        "full_name": "GCSE Chemistry (AQA, Edexcel, OCR)",
        "course": "gcse-chemistry",
        "access": ("GCSE", "chemistry"),   # opened by the gcse-chemistry course (see routers/exam._allowed)
        "sections": {"p1": "Paper 1 topics", "p2": "Paper 2 topics"},
        "domains": {
            "Atoms and bonding": ["Atomic structure", "Periodic table", "Bonding and structure"],
            "Quantities and reactions": ["Quantitative chemistry", "Chemical changes", "Electrolysis", "Energy changes"],
            "Rates and organic": ["Rates and equilibrium", "Organic chemistry"],
            "Analysis and the Earth": ["Chemical analysis", "Atmosphere", "Using resources"],
        },
        # Share right -> grade 1-9. An estimate only: real boundaries move each year.
        "scale": {"min": 1.0, "max": 9.0, "decimals": 0,
                  "points": [(0.0, 1.0), (0.15, 2.0), (0.3, 3.0), (0.42, 4.0), (0.54, 5.0), (0.65, 6.0),
                             (0.76, 7.0), (0.86, 8.0), (0.94, 9.0), (1.0, 9.0)]},
        "band": 1.0,
        "target_range": (1.0, 9.0),
        "calculator": True,
        "mock_detail": "Multiple-choice practice papers · Paper 1 and Paper 2 topics",
        "about_score": "GCSE grades run from 1 to 9. Ours are Notenix estimates from the share of questions you get right; real grade boundaries change every year and depend on your tier and exam board.",
    },
    "gcse-physics": {
        "name": "GCSE Physics",
        "full_name": "GCSE Physics (AQA, Edexcel, OCR)",
        "course": "gcse-physics",
        "access": ("GCSE", "physics"),   # opened by the gcse-physics course (see routers/exam._allowed)
        "sections": {"p1": "Paper 1 topics", "p2": "Paper 2 topics"},
        "domains": {
            "Energy and electricity": ["Energy stores and transfers", "Electricity", "Particle model", "Atomic structure and radiation"],
            "Forces and motion": ["Forces and their effects", "Motion and Newton's laws", "Momentum"],
            "Waves and magnetism": ["Waves", "Electromagnetic spectrum", "Magnetism and electromagnetism"],
            "Space": ["Space physics"],
        },
        # Share right -> grade 1-9. An estimate only: real boundaries move each year.
        "scale": {"min": 1.0, "max": 9.0, "decimals": 0,
                  "points": [(0.0, 1.0), (0.15, 2.0), (0.3, 3.0), (0.42, 4.0), (0.54, 5.0), (0.65, 6.0),
                             (0.76, 7.0), (0.86, 8.0), (0.94, 9.0), (1.0, 9.0)]},
        "band": 1.0,
        "target_range": (1.0, 9.0),
        "calculator": True,
        "mock_detail": "Multiple-choice practice papers · Paper 1 and Paper 2 topics",
        "about_score": "GCSE grades run from 1 to 9. Ours are Notenix estimates from the share of questions you get right; real grade boundaries change every year and depend on your tier and exam board.",
    },
}


def config(exam: str) -> dict | None:
    return EXAMS.get(exam)


def skill_list(exam: str) -> list[tuple[str, str]]:
    """[(domain, skill), ...] in display order."""
    return [(d, s) for d, skills in EXAMS[exam]["domains"].items() for s in skills]


def slugify(skill: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in skill.lower()).strip("-").replace("--", "-")


# ── Content ───────────────────────────────────────────────────────────────────

@lru_cache(maxsize=None)
def forms(exam: str) -> dict[str, dict]:
    out = {}
    folder = CONTENT / exam
    if folder.exists():
        for f in sorted(folder.glob("*.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            out[data["slug"]] = data
    return out


def form(exam: str, slug: str) -> dict | None:
    return forms(exam).get(slug)


def mocks(exam: str) -> list[dict]:
    return [f for f in forms(exam).values() if f.get("kind") == "mock"]


def drills(exam: str) -> dict:
    f = form(exam, "drills")
    return f["modules"] if f else {}


def public_question(q: dict) -> dict:
    return {k: v for k, v in q.items() if k not in ("answer", "explanation")}


def calculator_for(exam: str, section: str) -> bool:
    """Is the on-screen calculator offered in this section of this exam?"""
    cfg = EXAMS[exam]
    return bool(cfg["calculator"]) and section not in cfg.get("no_calculator", ())


def public_module(f: dict, key: str) -> dict:
    m = f["modules"][key]
    return {"key": key, "title": m["title"], "section": m["section"], "minutes": m["minutes"],
            "questions": [public_question(q) for q in m["questions"]]}


# ── Scoring ───────────────────────────────────────────────────────────────────

def scaled(exam: str, frac: float) -> float:
    """Map a share right (0-1) onto the exam's scale by straight lines between the points."""
    sc = EXAMS[exam]["scale"]
    pts = sc["points"]
    frac = max(0.0, min(1.0, frac))
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if frac <= x1:
            y = y0 + (y1 - y0) * (frac - x0) / (x1 - x0)
            return round(max(sc["min"], min(sc["max"], y)), sc["decimals"])
    return sc["max"]


def module_score(f: dict, key: str, answers: dict) -> tuple[int, int]:
    qs = f["modules"][key]["questions"]
    return sum(is_correct(q, answers.get(q["id"])) for q in qs), len(qs)


def score(exam: str, f: dict, answers: dict[str, dict]) -> dict:
    """{"sections": {sec: {"right", "total", "score"}}, "right", "total", "score"} for a finished sitting."""
    secs: dict[str, list[int]] = {}
    for key in f["stages"]:
        c, n = module_score(f, key, answers.get(key, {}))
        r = secs.setdefault(f["modules"][key]["section"], [0, 0])
        r[0] += c
        r[1] += n
    right, total = sum(r[0] for r in secs.values()), sum(r[1] for r in secs.values())
    return {"sections": {s: {"right": r[0], "total": r[1], "score": scaled(exam, r[0] / r[1] if r[1] else 0)}
                         for s, r in secs.items()},
            "right": right, "total": total, "score": scaled(exam, right / total if total else 0)}


def band(exam: str, value: float) -> list[float]:
    sc, b = EXAMS[exam]["scale"], EXAMS[exam]["band"]
    return [round(max(sc["min"], value - b), sc["decimals"]), round(min(sc["max"], value + b), sc["decimals"])]


def breakdown(exam: str, pairs: list[tuple[dict, object]]) -> list[dict]:
    """Per domain and skill: right / total, in the exam's skill order."""
    by: dict[tuple, list[int]] = {}
    for q, given in pairs:
        r = by.setdefault((q["domain"], q["skill"]), [0, 0])
        r[0] += int(is_correct(q, given))
        r[1] += 1
    order = {k: i for i, k in enumerate(skill_list(exam))}
    rows = [{"domain": d, "skill": s, "right": r, "total": t} for (d, s), (r, t) in by.items()]
    rows.sort(key=lambda x: order.get((x["domain"], x["skill"]), 999))
    return rows


def weakest(rows: list[dict], n: int = 3) -> list[dict]:
    lost = [r for r in rows if r["right"] < r["total"]]
    lost.sort(key=lambda r: (-(r["total"] - r["right"]), r["right"] / r["total"]))
    return lost[:n]


def review(f: dict, key: str, answers: dict) -> list[dict]:
    return [{**q, "given": answers.get(q["id"]), "correct": is_correct(q, answers.get(q["id"]))}
            for q in f["modules"][key]["questions"]]


def report(exam: str, f: dict, answers: dict[str, dict]) -> dict:
    """Everything a score report needs: scores, skills, weakest skills and the review."""
    s = score(exam, f, answers)
    pairs = [(q, answers.get(k, {}).get(q["id"])) for k in f["stages"] for q in f["modules"][k]["questions"]]
    rows = breakdown(exam, pairs)
    out = {**s, "skills": rows, "weakest": weakest(rows),
           "modules": [{"key": k, "title": f["modules"][k]["title"], "section": f["modules"][k]["section"],
                        "questions": review(f, k, answers.get(k, {}))} for k in f["stages"]]}
    if f.get("kind") == "diagnostic":
        out["band"] = band(exam, s["score"])
        for sec in out["sections"].values():
            sec["band"] = band(exam, sec["score"])
    return out


def split_answers(f: dict, flat: dict) -> dict[str, dict]:
    """{question_id: answer} (as the public diagnostic sends them) -> {module: {qid: answer}}."""
    return {k: {q["id"]: flat.get(q["id"]) for q in f["modules"][k]["questions"] if flat.get(q["id"])}
            for k in f["stages"]}
