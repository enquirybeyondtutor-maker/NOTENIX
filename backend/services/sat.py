"""Notenix SAT: Digital-SAT-style practice tests.

A form (backend/sat_content/<slug>.json, written by the scripts in that folder) is either
  • a mock: Reading & Writing module 1 → module 2 (easier "rw2e" or harder "rw2h", chosen by
    how module 1 went) → Math module 1 → module 2 ("m2e" / "m2h"), like the real adaptive test;
  • the diagnostic: one short R&W module and one short Math module, sat without an account.

Questions: {id, section rw|math, domain, skill, difficulty 1-3, type mcq|spr, passage?,
question, options? (mcq), answer ("A".."D" for mcq; list of accepted strings for spr),
explanation}. Students never receive `answer` or `explanation` before submitting.

Scores are Notenix estimates on the 200–800 per section / 400–1600 scale: real SAT scores use
item response theory, which a practice test can only approximate.
"""
import json
import re
from functools import lru_cache
from pathlib import Path

CONTENT = Path(__file__).resolve().parent.parent / "sat_content"

# Order of a mock; a tuple is the adaptive choice for module 2 (easier, harder).
MOCK_STAGES = ["rw1", ("rw2e", "rw2h"), "m1", ("m2e", "m2h")]
DIAG_STAGES = ["rw", "m"]
HARD_ROUTE_AT = 0.6   # share of module 1 right needed for the harder module 2

SECTION_NAMES = {"rw": "Reading and Writing", "math": "Math"}
DOMAINS = {
    "rw": ["Information and Ideas", "Craft and Structure", "Expression of Ideas", "Standard English Conventions"],
    "math": ["Algebra", "Advanced Math", "Problem-Solving and Data Analysis", "Geometry and Trigonometry"],
}


@lru_cache(maxsize=None)
def forms() -> dict[str, dict]:
    out = {}
    if CONTENT.exists():
        for f in sorted(CONTENT.glob("*.json")):
            data = json.loads(f.read_text(encoding="utf-8"))
            out[data["slug"]] = data
    return out


def form(slug: str) -> dict | None:
    return forms().get(slug)


def mocks() -> list[dict]:
    return [f for f in forms().values() if f.get("kind") == "mock"]


def stage_key(f: dict, stage: int, route: dict) -> str | None:
    """Module key for this stage of the form, given the adaptive routes taken so far."""
    stages = MOCK_STAGES if f.get("kind") == "mock" else DIAG_STAGES
    if stage >= len(stages):
        return None
    s = stages[stage]
    if isinstance(s, tuple):
        section = "rw" if s[0].startswith("rw") else "m"
        return s[1] if route.get(section) == "h" else s[0]
    return s


def n_stages(f: dict) -> int:
    return len(MOCK_STAGES if f.get("kind") == "mock" else DIAG_STAGES)


def public_question(q: dict) -> dict:
    return {k: v for k, v in q.items() if k not in ("answer", "explanation")}


def public_module(f: dict, key: str) -> dict:
    m = f["modules"][key]
    return {"key": key, "title": m["title"], "section": m["section"], "minutes": m["minutes"],
            "questions": [public_question(q) for q in m["questions"]]}


# ── Marking ───────────────────────────────────────────────────────────────────

def _num(s: str) -> float | None:
    s = (s or "").strip().replace(" ", "").replace(",", "")
    try:
        if re.fullmatch(r"-?\d+/\d+", s):
            a, b = s.split("/")
            return int(a) / int(b) if int(b) else None
        return float(s)
    except ValueError:
        return None


def is_correct(q: dict, given) -> bool:
    if given is None or str(given).strip() == "":
        return False
    if q["type"] == "mcq":
        return str(given).strip().upper() == str(q["answer"]).strip().upper()
    g = str(given).strip()
    for ok in q["answer"]:
        if g.replace(" ", "") == str(ok).replace(" ", ""):
            return True
        a, b = _num(g), _num(str(ok))
        if a is not None and b is not None and abs(a - b) < 1e-6:
            return True
        # SAT grid-ins accept a decimal cut to the space available: 2/3 as .6666 or .6667
        if a is not None and b is not None and len(g.lstrip("-")) >= 5 and abs(a - b) < 1e-3:
            return True
    return False


def module_score(f: dict, key: str, answers: dict) -> tuple[int, int]:
    qs = f["modules"][key]["questions"]
    return sum(is_correct(q, answers.get(q["id"])) for q in qs), len(qs)


def route_for(correct: int, total: int) -> str:
    return "h" if total and correct / total >= HARD_ROUTE_AT else "e"


def _round10(x: float) -> int:
    return int(round(x / 10.0) * 10)


def section_score(c1: int, n1: int, c2: int, n2: int, route: str) -> int:
    """Estimated 200–800 section score. The harder module 2 opens the top of the scale;
    after the easier one, the section score tops out around 650, as on the real test."""
    frac = (c1 + c2) / (n1 + n2) if (n1 + n2) else 0
    if route == "h":
        s = 380 + 420 * frac
    else:
        s = 200 + 450 * frac
    return max(200, min(800, _round10(s)))


def diagnostic_band(correct: int, total: int) -> tuple[int, int]:
    """A short mixed-difficulty module only supports a band, ±40 around the estimate."""
    mid = 200 + 600 * (correct / total if total else 0)
    return max(200, _round10(mid - 40)), min(800, _round10(mid + 40))


def breakdown(questions_and_answers: list[tuple[dict, object]]) -> list[dict]:
    """Per domain and skill: right / total, weakest first within each section."""
    by: dict[tuple, list[int]] = {}
    for q, given in questions_and_answers:
        k = (q["section"], q["domain"], q["skill"])
        r = by.setdefault(k, [0, 0])
        r[0] += int(is_correct(q, given))
        r[1] += 1
    rows = [{"section": s, "domain": d, "skill": sk, "right": r, "total": t} for (s, d, sk), (r, t) in by.items()]
    order = {d: i for sec in DOMAINS.values() for i, d in enumerate(sec)}
    rows.sort(key=lambda x: (x["section"] != "rw", order.get(x["domain"], 99), x["right"] / x["total"]))
    return rows


def weakest(rows: list[dict], n: int = 3) -> list[dict]:
    """Skills losing the most points (at least one wrong), most points lost first."""
    lost = [r for r in rows if r["right"] < r["total"]]
    lost.sort(key=lambda r: (-(r["total"] - r["right"]), r["right"] / r["total"]))
    return lost[:n]


def review(f: dict, key: str, answers: dict) -> list[dict]:
    """Every question with the student's answer, the right answer and the explanation."""
    out = []
    for q in f["modules"][key]["questions"]:
        given = answers.get(q["id"])
        out.append({**q, "given": given, "correct": is_correct(q, given)})
    return out


def score_diagnostic(answers: dict) -> dict:
    f = form("diagnostic")
    if not f:
        raise ValueError("The diagnostic isn't available yet.")
    rw_c, rw_n = module_score(f, "rw", answers)
    m_c, m_n = module_score(f, "m", answers)
    rw_band, m_band = diagnostic_band(rw_c, rw_n), diagnostic_band(m_c, m_n)
    pairs = [(q, answers.get(q["id"])) for k in ("rw", "m") for q in f["modules"][k]["questions"]]
    rows = breakdown(pairs)
    return {
        "rw": {"right": rw_c, "total": rw_n, "band": rw_band},
        "math": {"right": m_c, "total": m_n, "band": m_band},
        "total_band": [rw_band[0] + m_band[0], rw_band[1] + m_band[1]],
        "skills": rows, "weakest": weakest(rows),
        "review": review(f, "rw", answers) + review(f, "m", answers),
    }
