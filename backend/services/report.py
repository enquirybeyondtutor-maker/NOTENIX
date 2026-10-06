"""Student performance reports for admissions-test mocks (ESAT, TMUA, …).

Everything numeric is computed here in code; Claude is only used to (1) tag each
question with a syllabus topic + difficulty once per test (cached on the test), and
(2) write the plain-English commentary from the computed numbers.

Band estimates are *indicative*: our mocks are original papers, not calibrated past
papers, so we map raw % onto the official 1.0–9.0 scale with published/estimated
conversion anchors and always report a range.
"""
import json
import re
from collections import defaultdict
from datetime import datetime

from services import ai
from config import settings

# ── Exam knowledge ───────────────────────────────────────────────────────────

# Piecewise-linear anchors: (raw fraction of marks, scaled score).
# ESAT: per module, 27 questions. Typical candidate ≈ 4.5 ≈ 12–14/27; 6.0 ≈ 16–18;
# 7.0 ≈ 19–21; 8.0 ≈ 21–23 (public estimates, ±2 raw marks).
_ESAT_ANCHORS = [(0, 1.0), (5 / 27, 2.5), (9 / 27, 3.5), (13 / 27, 4.5), (17 / 27, 6.0),
                 (20 / 27, 7.0), (22.5 / 27, 8.0), (1.0, 9.0)]
# TMUA: total of 40 across two papers. 2023 published conversion (0→1.0, 9→2.8,
# 14→4.5, 20→6.2, 26→7.0, 38→9.0) blended with recent calibrated estimates.
_TMUA_ANCHORS = [(0, 1.0), (9 / 40, 2.8), (14 / 40, 4.5), (20 / 40, 6.0), (26 / 40, 7.0),
                 (32 / 40, 8.0), (38 / 40, 9.0), (1.0, 9.0)]

# (scaled score, approx. percentile of all candidates)
_ESAT_PCTL = [(1.0, 0), (3.0, 12), (4.5, 48), (5.0, 60), (6.0, 82), (7.0, 92), (8.0, 98), (9.0, 100)]
_TMUA_PCTL = [(1.0, 0), (3.8, 50), (4.5, 66), (5.0, 76), (6.0, 88), (6.5, 92), (7.0, 94), (8.0, 96.5), (9.0, 100)]

EXAMS = {
    "ESAT": {
        "name": "ESAT",
        "anchors": _ESAT_ANCHORS,
        "pctl": _ESAT_PCTL,
        "band_unit": "module",  # each module scored separately
        "benchmarks": [
            {"label": "Typical candidate", "score": 4.5},
            {"label": "Cambridge offer avg.", "score": 6.0},
            {"label": "Top 10%", "score": 7.0},
        ],
        "context": ("ESAT: each module is 27 MCQs in 40 minutes, scored 1.0–9.0, no negative marking. "
                    "Typical candidate ≈ 4.5. Cambridge offer-holder averages in 2025 were about 5.6–6.2 "
                    "(NatSci) and ~5.7 (Engineering, home); 7.0+ is roughly the top 10%. International "
                    "applicants should aim ~0.5–1.0 higher."),
        "taxonomy": {
            "Maths 1": ["Number & arithmetic", "Algebra & equations", "Ratio, proportion & rates",
                        "Geometry & mensuration", "Trigonometry", "Coordinate geometry", "Sequences",
                        "Functions & graphs", "Statistics", "Probability", "Basic calculus"],
            "Maths 2": ["Algebra & functions", "Sequences & series", "Coordinate geometry", "Trigonometry",
                        "Exponentials & logarithms", "Differentiation", "Integration", "Graph sketching",
                        "Probability & statistics"],
            "Physics": ["Kinematics & motion", "Forces & Newton's laws", "Energy, work & power",
                        "Momentum", "Electricity & circuits", "Magnetism & electromagnetism",
                        "Waves & optics", "Matter, density & pressure", "Thermal physics",
                        "Radioactivity & nuclear", "Units & estimation"],
            "Chemistry": ["Atomic structure", "Periodic table", "Bonding & structure", "Moles & stoichiometry",
                          "Energetics", "Rates & equilibrium", "Redox & electrolysis", "Acids & bases",
                          "Organic chemistry", "Analysis"],
            "Biology": ["Cells", "Movement across membranes", "Cell division", "Inheritance & genetics",
                        "DNA & protein synthesis", "Enzymes", "Animal physiology", "Ecosystems",
                        "Plant physiology", "Evolution"],
        },
    },
    "TMUA": {
        "name": "TMUA",
        "anchors": _TMUA_ANCHORS,
        "pctl": _TMUA_PCTL,
        "band_unit": "total",  # one score across Paper 1 + Paper 2
        "benchmarks": [
            {"label": "Median candidate", "score": 3.8},
            {"label": "Competitive", "score": 6.5},
            {"label": "Top 6%", "score": 7.0},
        ],
        "context": ("TMUA: two papers of 20 MCQs in 75 minutes each, one combined score 1.0–9.0, no negative "
                    "marking. Oct 2025: median ≈ 3.8, 6.0 ≈ 88th percentile, 7.0 ≈ 94th. Roughly 6.0–6.5+ "
                    "is broadly competitive for Cambridge, Imperial, LSE and Warwick maths/CS/econ."),
        "taxonomy": {
            "Paper 1": ["Algebra & equations", "Polynomials & factor theorem", "Inequalities",
                        "Functions & graph transformations", "Coordinate geometry & circles", "Trigonometry",
                        "Exponentials & logarithms", "Sequences & series", "Differentiation", "Integration",
                        "Binomial & counting"],
            "Paper 2": ["Necessary & sufficient conditions", "Logic & negation", "Proof & counterexample",
                        "Errors in proofs", "Number theory & reasoning", "Algebra & functions (reasoning)",
                        "Geometry & trigonometry (reasoning)", "Calculus (reasoning)", "Sequences (reasoning)"],
        },
    },
}

_PREFIX = re.compile(r"^\s*\[([^\]]+?)\s*[·—–\-]+\s*Q\d+\]\s*")


def exam_key(test) -> str:
    """Exam family for a test: ESAT / TMUA if recognised, else its subject."""
    blob = f"{test.subject} {test.title}".upper()
    for k in EXAMS:
        if k in blob:
            return k
    return (test.subject or "Other").strip()


def _section_of(test, q: dict, exam: str) -> str:
    m = _PREFIX.match(q.get("question") or "")
    label = m.group(1).strip() if m else ""
    if exam == "TMUA":
        src = f"{label} {test.title} {test.topic}".upper()
        return "Paper 2" if ("P2" in src or "PAPER 2" in src or "REASONING" in src) else "Paper 1"
    if exam == "ESAT":
        low = label.lower()
        if low in ("maths", "math", "mathematics"):
            return "Maths 1"
        for name in EXAMS["ESAT"]["taxonomy"]:
            if low == name.lower():
                return name
        return label.title() if label else "General"
    return label or (test.topic or "General")


def _strip_prefix(text: str) -> str:
    return _PREFIX.sub("", text or "", count=1)


def _interp(x: float, pts: list[tuple[float, float]]) -> float:
    if x <= pts[0][0]:
        return pts[0][1]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0) if x1 > x0 else y1
    return pts[-1][1]


def scaled(exam: str, frac: float) -> float | None:
    cfg = EXAMS.get(exam)
    return round(_interp(max(0.0, min(1.0, frac)), cfg["anchors"]), 1) if cfg else None


def percentile(exam: str, score: float) -> int | None:
    cfg = EXAMS.get(exam)
    return int(round(_interp(score, cfg["pctl"]))) if cfg else None


# ── Topic tagging (Claude, cached on the test) ───────────────────────────────

def _tag_prompt(exam: str, items: list[dict]) -> str:
    tax = EXAMS.get(exam, {}).get("taxonomy")
    tax_txt = (json.dumps(tax, ensure_ascii=False, indent=1) if tax
               else "(no fixed list — use short, standard syllabus topic names, max 4 words)")
    return f"""You are classifying {exam} admissions-test multiple-choice questions for a performance report.

For each question give:
- "topic": ONE topic name. For the question's section, choose from this list exactly when possible:
{tax_txt}
- "difficulty": 1 (routine/standard), 2 (multi-step), or 3 (hard/unfamiliar), judged against the real {exam}.

Questions (i = index, s = section):
{json.dumps(items, ensure_ascii=False)}

Return ONLY a JSON array of objects: [{{"i": 0, "topic": "...", "difficulty": 2}}, ...] covering every i."""


def tag_questions(test, exam: str) -> bool:
    """Ensure each question in `test.questions` has a `tag` {section, topic, difficulty}.
    Mutates `test.questions` (reassigned so SQLAlchemy sees the change). Returns True if changed."""
    qs = list(test.questions or [])
    missing = [i for i, q in enumerate(qs) if not isinstance(q.get("tag"), dict) or not q["tag"].get("topic")]
    if not missing:
        return False
    sections = {i: _section_of(test, qs[i], exam) for i in missing}
    tags: dict[int, dict] = {}
    if settings.anthropic_api_key:
        for start in range(0, len(missing), 30):  # keep each call small
            chunk = missing[start:start + 30]
            items = [{"i": i, "s": sections[i],
                      "q": _strip_prefix(qs[i].get("question") or "")[:500],
                      "answer": str(qs[i].get("answer") or "")[:80]} for i in chunk]
            try:
                msg = ai.client().messages.create(
                    model=settings.claude_model, max_tokens=3000,
                    messages=[{"role": "user", "content": _tag_prompt(exam, items)}],
                )
                for row in ai._extract_json(msg.content[0].text):
                    i = int(row.get("i"))
                    if i in sections:
                        d = int(row.get("difficulty") or 2)
                        tags[i] = {"topic": str(row.get("topic") or "General")[:60], "difficulty": max(1, min(3, d))}
            except Exception as e:  # tagging is best-effort; report still works by section
                print(f"[report] tagging failed for test {test.id}: {e}")
    for i in missing:
        t = tags.get(i)
        if not t:
            continue  # leave untagged so a later run retries
        q = dict(qs[i])
        q["tag"] = {"section": sections[i], **t}
        qs[i] = q
    if tags:
        test.questions = qs
        return True
    return False


# ── Per-question rows ────────────────────────────────────────────────────────

def _is_blank(v) -> bool:
    return v is None or (isinstance(v, str) and not v.strip())


def question_rows(test, attempt, exam: str, class_acc: list[float | None]) -> tuple[list[dict], bool]:
    """One row per question for this attempt. Returns (rows, skip_data_available)."""
    qs = test.questions or []
    results = attempt.results or []
    answers = attempt.answers
    times = attempt.question_times or []
    skip_known = True
    rows = []
    for i, q in enumerate(qs):
        r = results[i] if i < len(results) else {}
        correct = bool(r.get("is_correct"))
        if "skipped" in r:
            skipped = bool(r["skipped"])
        elif answers is not None:
            skipped = _is_blank(answers[i] if i < len(answers) else None)
        elif "your_answer" in r:
            skipped = _is_blank(r.get("your_answer"))
        else:
            skipped = False  # purged: can't tell a blank from a wrong answer
            skip_known = False
        tag = q.get("tag") or {}
        rows.append({
            "n": i + 1,
            "section": tag.get("section") or _section_of(test, q, exam),
            "topic": tag.get("topic") or "Untagged",
            "difficulty": tag.get("difficulty"),
            "status": "correct" if correct else ("skipped" if skipped else "wrong"),
            "seconds": int(times[i]) if i < len(times) and times[i] else 0,
            "options": len(q.get("options") or []) or 5,
            "class_acc": class_acc[i] if i < len(class_acc) else None,
        })
    return rows, skip_known


def class_accuracy(test, attempts: list) -> tuple[list[float | None], int]:
    """Per-question accuracy across every attempt at this test (None if < 3 attempts)."""
    n = len(attempts)
    qn = len(test.questions or [])
    if n < 3:
        return [None] * qn, n
    hits = [0] * qn
    for a in attempts:
        for i, r in enumerate((a.results or [])[:qn]):
            hits[i] += int(bool(r.get("is_correct")))
    return [round(h / n, 2) for h in hits], n


# ── Analysis ─────────────────────────────────────────────────────────────────

def _acc(c: int, n: int) -> float | None:
    return round(100 * c / n, 1) if n else None


def analyse_attempt(test, attempt, exam: str, rows: list[dict], skip_known: bool, cohort_n: int) -> dict:
    n = len(rows)
    dur = (test.duration_minutes or 0) * 60
    pace = dur / n if dur and n else None
    correct = sum(r["status"] == "correct" for r in rows)
    skipped = sum(r["status"] == "skipped" for r in rows)

    # sections
    sec = defaultdict(lambda: {"n": 0, "correct": 0, "skipped": 0, "seconds": 0})
    for r in rows:
        s = sec[r["section"]]
        s["n"] += 1
        s["correct"] += r["status"] == "correct"
        s["skipped"] += r["status"] == "skipped"
        s["seconds"] += r["seconds"]
    sections = []
    for name, s in sec.items():
        frac = s["correct"] / s["n"] if s["n"] else 0
        sections.append({
            "section": name, "n": s["n"], "correct": s["correct"], "skipped": s["skipped"],
            "accuracy": _acc(s["correct"], s["n"]), "seconds": s["seconds"],
            "band": scaled(exam, frac) if EXAMS.get(exam, {}).get("band_unit") == "module" else None,
        })

    # timing
    timed = [r for r in rows if r["seconds"] > 0]
    used = attempt.time_taken_seconds or sum(r["seconds"] for r in rows)
    quarters = []
    if n >= 8:
        size = n / 4
        for k in range(4):
            part = rows[int(k * size):int((k + 1) * size)]
            quarters.append({
                "label": f"Q{part[0]['n']}–{part[-1]['n']}",
                "accuracy": _acc(sum(r["status"] == "correct" for r in part), len(part)),
                "skipped": sum(r["status"] == "skipped" for r in part),
                "avg_seconds": round(sum(r["seconds"] for r in part) / len(part)) if part else 0,
            })
    sinks, rushed = [], []
    if pace:
        for r in timed:
            ratio = r["seconds"] / pace
            if r["status"] != "correct" and ratio >= 1.75:
                sinks.append(r)
            elif r["status"] == "wrong" and ratio <= 0.35:
                rushed.append(r)
        sinks.sort(key=lambda r: -r["seconds"])
    t_correct = [r["seconds"] for r in timed if r["status"] == "correct"]
    t_wrong = [r["seconds"] for r in timed if r["status"] == "wrong"]

    # skips
    skip_rows = [r for r in rows if r["status"] == "skipped"]
    easy_skips = [r for r in skip_rows if r["difficulty"] == 1 or (r["class_acc"] or 0) >= 0.7]
    guess_value = round(sum(1 / r["options"] for r in skip_rows), 1)
    careless = [r for r in rows if r["status"] == "wrong" and (r["difficulty"] == 1 or (r["class_acc"] or 0) >= 0.75)]

    by_diff = {}
    for d in (1, 2, 3):
        part = [r for r in rows if r["difficulty"] == d]
        if part:
            by_diff[str(d)] = {"n": len(part), "accuracy": _acc(sum(r["status"] == "correct" for r in part), len(part))}

    total_frac = correct / n if n else 0
    return {
        "attempt_id": attempt.id,
        "test_id": test.id,
        "title": test.title,
        "date": attempt.completed_at.isoformat() if attempt.completed_at else None,
        "n": n, "correct": correct, "wrong": n - correct - skipped, "skipped": skipped,
        "score": attempt.score, "accuracy_attempted": _acc(correct, n - skipped),
        "band": scaled(exam, total_frac) if EXAMS.get(exam, {}).get("band_unit") == "total" else None,
        "paper": rows[0]["section"] if exam == "TMUA" and rows else None,
        "sections": sections,
        "timing": {
            "allowed_seconds": dur or None, "used_seconds": used, "pace_seconds": round(pace) if pace else None,
            "auto_submitted": bool(getattr(attempt, "auto_submitted", False)),
            "avg_correct": round(sum(t_correct) / len(t_correct)) if t_correct else None,
            "avg_wrong": round(sum(t_wrong) / len(t_wrong)) if t_wrong else None,
            "time_on_unscored": sum(r["seconds"] for r in rows if r["status"] != "correct"),
            "quarters": quarters,
            "sinks": [{"n": r["n"], "topic": r["topic"], "seconds": r["seconds"], "status": r["status"]} for r in sinks[:6]],
            "rushed": [{"n": r["n"], "topic": r["topic"], "seconds": r["seconds"]} for r in rushed[:6]],
            "has_data": bool(timed),
        },
        "skips": {
            "known": skip_known, "count": skipped,
            "questions": [r["n"] for r in skip_rows],
            "easy": [{"n": r["n"], "topic": r["topic"]} for r in easy_skips],
            "guess_value": guess_value,
        },
        "careless": [{"n": r["n"], "topic": r["topic"]} for r in careless],
        "by_difficulty": by_diff,
        "cohort_n": cohort_n,
        "integrity": {
            "focus_lost": getattr(attempt, "focus_lost_count", 0) or 0,
            "time_away_seconds": getattr(attempt, "time_away_seconds", 0) or 0,
            "paste_attempts": getattr(attempt, "paste_attempts", 0) or 0,
            "fullscreen_exits": getattr(attempt, "fullscreen_exits", 0) or 0,
        },
        "questions": [{k: r[k] for k in ("n", "section", "topic", "status", "seconds", "difficulty")} for r in rows],
    }


def _weighted(values: list[float]) -> float | None:
    """Recency-weighted mean (newest counts most): weights 1,2,3,… oldest→newest."""
    if not values:
        return None
    w = range(1, len(values) + 1)
    return sum(v * k for v, k in zip(values, w)) / sum(w)


def build_report(exam: str, student, attempts: list[dict], all_rows: list[list[dict]]) -> dict:
    """Combine per-attempt analyses (oldest→newest) into the report payload."""
    cfg = EXAMS.get(exam)
    flat = [r for rows in all_rows for r in rows]

    # topics across every mock
    tp = defaultdict(lambda: {"n": 0, "correct": 0, "skipped": 0, "seconds": 0, "timed": 0, "section": ""})
    for r in flat:
        t = tp[(r["section"], r["topic"])]
        t["section"] = r["section"]
        t["n"] += 1
        t["correct"] += r["status"] == "correct"
        t["skipped"] += r["status"] == "skipped"
        if r["seconds"]:
            t["seconds"] += r["seconds"]
            t["timed"] += 1
    topics = []
    for (section, topic), t in tp.items():
        acc = _acc(t["correct"], t["n"])
        lost = t["n"] - t["correct"]
        rating = ("strong" if t["n"] >= 3 and acc >= 75 else
                  "weak" if t["n"] >= 3 and acc < 50 else
                  "developing" if t["n"] >= 3 else "limited data")
        topics.append({"section": section, "topic": topic, "n": t["n"], "correct": t["correct"],
                       "skipped": t["skipped"], "accuracy": acc, "marks_lost": lost, "rating": rating,
                       "avg_seconds": round(t["seconds"] / t["timed"]) if t["timed"] else None})
    topics.sort(key=lambda x: (x["section"], -(x["accuracy"] or 0)))
    priorities = sorted([t for t in topics if t["rating"] in ("weak", "developing")],
                        key=lambda x: (-x["marks_lost"], x["accuracy"] or 0))[:6]

    # section totals + trend
    sec_tot = defaultdict(lambda: {"n": 0, "correct": 0, "skipped": 0})
    for r in flat:
        s = sec_tot[r["section"]]
        s["n"] += 1
        s["correct"] += r["status"] == "correct"
        s["skipped"] += r["status"] == "skipped"
    sections = [{"section": k, **v, "accuracy": _acc(v["correct"], v["n"])} for k, v in sec_tot.items()]

    # band estimate
    band = None
    if cfg and cfg["band_unit"] == "module":
        per = {}
        for s in sections:
            hist = [sec["band"] for a in attempts for sec in a["sections"] if sec["section"] == s["section"] and sec["band"] is not None]
            est = _weighted(hist)
            if est is not None:
                est = round(est, 1)
                per[s["section"]] = {"estimate": est, "low": max(1.0, round(est - 0.5, 1)),
                                     "high": min(9.0, round(est + 0.5, 1)), "percentile": percentile(exam, est),
                                     "history": hist}
        band = {"unit": "module", "modules": per}
    elif cfg and cfg["band_unit"] == "total":
        # TMUA: combine the latest Paper 1 with the latest Paper 2 (40 marks); fall back to one paper.
        latest = {}
        for a in attempts:
            if a.get("paper"):
                latest[a["paper"]] = a
        if latest:
            marks = sum(a["correct"] for a in latest.values())
            out_of = sum(a["n"] for a in latest.values())
            est = scaled(exam, marks / out_of)
            hist = [a["band"] for a in attempts if a["band"] is not None]
            band = {"unit": "total", "estimate": est, "low": max(1.0, round(est - 0.5, 1)),
                    "high": min(9.0, round(est + 0.5, 1)), "percentile": percentile(exam, est),
                    "basis": {p: f"{a['correct']}/{a['n']} ({a['title']})" for p, a in sorted(latest.items())},
                    "combined_marks": f"{marks}/{out_of}", "history": hist}

    # overall timing / skipping across mocks
    timed_attempts = [a for a in attempts if a["timing"]["has_data"]]
    total_q = sum(a["n"] for a in attempts)
    return {
        "exam": exam,
        "student": {"id": student.id, "name": student.full_name},
        "generated_at": datetime.utcnow().isoformat(),
        "summary": {
            "mocks": len(attempts), "questions": total_q,
            "correct": sum(a["correct"] for a in attempts),
            "skipped": sum(a["skipped"] for a in attempts),
            "accuracy": _acc(sum(a["correct"] for a in attempts), total_q),
            "accuracy_attempted": _acc(sum(a["correct"] for a in attempts),
                                       total_q - sum(a["skipped"] for a in attempts)),
            "first_score": attempts[0]["score"] if attempts else None,
            "latest_score": attempts[-1]["score"] if attempts else None,
            "timed_mocks": len(timed_attempts),
            "skip_data": all(a["skips"]["known"] for a in attempts),
        },
        "band": band,
        "benchmarks": cfg["benchmarks"] if cfg else [],
        "sections": sections,
        "topics": topics,
        "priorities": priorities,
        "attempts": attempts,
    }


# ── Commentary (Claude) ──────────────────────────────────────────────────────

def _compact_for_ai(rep: dict) -> dict:
    """Numbers the model is allowed to talk about — nothing raw, nothing private."""
    return {
        "exam": rep["exam"], "first_name": (rep["student"]["name"] or "The student").split()[0],
        "summary": rep["summary"], "band": rep["band"], "benchmarks": rep["benchmarks"],
        "sections": rep["sections"],
        "topics": [{k: t[k] for k in ("section", "topic", "n", "accuracy", "skipped", "rating", "avg_seconds")} for t in rep["topics"]],
        "mocks": [{
            "mock": f"Mock {i + 1}", "title": a["title"], "date": (a["date"] or "")[:10], "score": a["score"], "n": a["n"],
            "correct": a["correct"], "wrong": a["wrong"], "skipped": a["skipped"],
            "accuracy_when_attempted": a["accuracy_attempted"], "band": a["band"],
            "sections": [{k: s[k] for k in ("section", "accuracy", "band", "skipped")} for s in a["sections"]],
            "timing": {k: a["timing"][k] for k in ("allowed_seconds", "used_seconds", "pace_seconds", "auto_submitted",
                                                     "avg_correct", "avg_wrong", "time_on_unscored", "quarters", "sinks", "rushed")},
            "skips": a["skips"], "careless": a["careless"], "by_difficulty": a["by_difficulty"],
        } for i, a in enumerate(rep["attempts"])],
    }


def write_commentary(rep: dict, target: str = "", pronouns: str = "") -> dict:
    """Ask Claude for the narrative. Falls back to a minimal template if unavailable."""
    exam = rep["exam"]
    cfg = EXAMS.get(exam, {})
    data = _compact_for_ai(rep)
    pro = {"he": "he/him/his", "she": "she/her", "they": "they/them/their"}.get((pronouns or "").lower())
    pronoun_rule = (f"Refer to the student by first name and the pronouns {pro}." if pro else
                    "Refer to the student by first name only; never use gendered pronouns (he/she/his/her).")
    prompt = f"""You are a senior {exam} tutor at Beyond Tutors writing a performance analysis that will be sent to a
student's parents. Write precisely and specifically from the DATA below. Every claim must be supported by a number in
the data; quote the numbers. Never invent scores, topics, dates or questions. Be honest but encouraging; no hype.
Write to the parents in the third person. {pronoun_rule} British English. No emoji. Do NOT write a
day-by-day study plan (that is produced separately).

Exam context: {cfg.get("context", "")}
Band estimates come from our mock papers (original, not past papers), so describe them as estimates/ranges. "percentile" is
the approximate percentile among ALL real test-takers nationally (not our group); "≈ top X%" = 100 − percentile.
{f"Target universities/courses: {target}" if target else "No target course was given; compare with the general benchmarks."}
Refer to sittings ONLY as "Mock 1", "Mock 2", … (the "mock" field), never by paper title, and to questions as
"Mock 2 Q14". Write for parents: never use field names or internal jargon (no "sinks", "guess value", "difficulty
level 1", "rating"); say e.g. "questions where time ran long without a mark", "a blind guess would have earned",
"routine questions". Round percentages to whole numbers. Give times as minutes and seconds (e.g. "78 min 12 s",
"about 3½ minutes per question"), never as raw seconds over 90. Keep it tight: no paragraph over 4 sentences.
Notes: "pace_seconds" = time per question if the paper is split evenly. "sinks" = questions not scored after
spending ≥1.75× pace. "rushed" = wrong answers in ≤0.35× pace. "guess_value" = expected marks a blind guess on
the skipped questions would have earned (no negative marking, so blanks are never better than a guess).
"careless" = wrong answers on questions rated easy or that most of the group got right.

DATA:
{json.dumps(data, ensure_ascii=False)}

Return ONLY JSON with these keys:
{{
 "headline": "one sentence, ≤ 22 words, the single most important takeaway",
 "overview": "3–4 sentences: where the student stands now and the direction of travel",
 "band_commentary": "2–3 sentences interpreting the estimated band vs the benchmarks/target",
 "strengths": ["3–4 bullets, each naming a section/topic with its numbers"],
 "focus_areas": [{{"area": "topic or skill", "evidence": "≤ 2 sentences with the numbers", "action": "≤ 2 sentences: what to change (concrete, not a schedule)"}}],  // 3–5 items, most marks-gainable first
 "timing": "2–3 sentences on time management with numbers (pace, sinks, end-of-paper effect)",
 "skipping": "2 sentences on skipping/answering strategy with numbers",
 "accuracy": "2 sentences on accuracy vs attempts, careless errors, difficulty profile",
 "closing": "1–2 sentences to parents: realistic expectation for the real exam if the focus areas are addressed"
}}"""
    if settings.anthropic_api_key:
        try:
            msg = ai.client().messages.create(
                model=settings.claude_model, max_tokens=3000,
                messages=[{"role": "user", "content": prompt}],
            )
            out = ai._extract_json(msg.content[0].text)
            if isinstance(out, dict) and out.get("headline"):
                return out
        except Exception as e:
            print(f"[report] commentary failed: {e}")
    s = rep["summary"]
    return {
        "headline": f"{s['correct']} of {s['questions']} questions correct across {s['mocks']} mock(s).",
        "overview": "", "band_commentary": "", "strengths": [], "focus_areas": [],
        "timing": "", "skipping": "", "accuracy": "", "closing": "",
        "unavailable": True,
    }
