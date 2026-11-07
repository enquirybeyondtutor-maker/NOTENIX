"""Exports the KS3 notes (+ 4 sample practice questions each) for the public topic pages.

Writes frontend/lib/ks3-topics.json, which the website reads at build time (Vercel only
builds the frontend folder). Run after changing notes or tests:  python export_web.py

Sample questions come from the half-term tests where they exist (never the baselines, which
are the free-week diagnostic), else from the year's baseline (Years 8-9 have no half-terms yet).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "frontend" / "lib" / "ks3-topics.json"
STOP = {"and", "the", "with", "your", "year", "basics", "for", "of", "in", "a", "to", "how"}


def words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]+", s.lower()) if len(w) > 3 and w not in STOP}


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


tests = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((HERE / "tests").glob("*.json"))]
topics = []
for p in sorted((HERE / "notes").glob("*.json")):
    n = json.loads(p.read_text(encoding="utf-8"))
    year, subject = n["year"], n["subject"]
    short = n["title"].split(": ", 1)[-1]
    pool_ht = [q for t in tests if t["subject"] == subject and t["slot"].startswith(f"y{year}-ht") for q in t["questions"]]
    pool = pool_ht or [q for t in tests if t["subject"] == subject and t["slot"] == f"y{year}-baseline" for q in t["questions"]]
    key_words = words(short) | words(n["body"][:600])
    scored = []
    for q in pool:
        if q["question"].startswith("Read the passage"):
            continue  # passages are long; keep the pages focused
        score = len(words(q["topic"]) & key_words) * 3 + len(words(q["question"]) & key_words)
        if score:
            scored.append((score, q))
    scored.sort(key=lambda x: -x[0])
    picked, seen = [], set()
    for _, q in scored:
        if q["question"] in seen:
            continue
        picked.append({k: q[k] for k in ("question", "options", "answer", "explanation", "topic")})
        seen.add(q["question"])
        if len(picked) == 4:
            break
    topics.append({
        "key": n["key"], "year": year, "subject": subject, "title": short,
        "slug": slug(short), "body": n["body"], "questions": picked,
    })

OUT.write_text(json.dumps(topics, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"{len(topics)} topic pages -> {OUT}")
for t in topics:
    print(f"  /ks3/year-{t['year']}/{t['subject'].lower()}/{t['slug']}  ({len(t['questions'])} questions)")
