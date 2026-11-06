"""Builds docs/ks3-content-review.html (+ PDF if Chrome is found): every KS3 question with
its answer and explanation, and every note, so the content can be checked before it goes live."""
import html, json, shutil, subprocess
from pathlib import Path

HERE = Path(__file__).parent
DOCS = HERE.parent.parent / "docs"
DOCS.mkdir(exist_ok=True)
esc = lambda s: html.escape(s).replace("\n", "<br>")

parts = []
for f in sorted((HERE / "tests").glob("*.json")):
    t = json.loads(f.read_text(encoding="utf-8"))
    parts.append(f"<h2>{esc(t['title'])} <small>{len(t['questions'])} questions · {t.get('duration')} min · slot {t['slot']}</small></h2>")
    for i, q in enumerate(t["questions"], 1):
        opts = "".join(f"<li class='{'ok' if o == q['answer'] else ''}'>{esc(o)}</li>" for o in q["options"])
        parts.append(f"<div class='q'><div class='meta'>Q{i} · {esc(q['topic'])}</div><div>{esc(q['question'])}</div>"
                     f"<ol type='A'>{opts}</ol><div class='exp'><b>Why:</b> {esc(q.get('explanation', ''))}</div></div>")
parts.append("<h2 class='break'>Notes</h2>")
for f in sorted((HERE / "notes").glob("*.json")):
    n = json.loads(f.read_text(encoding="utf-8"))
    parts.append(f"<div class='note'><h3>{esc(n['title'])}</h3><div>{esc(n['body'])}</div></div>")

page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Notenix KS3 content review</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
 onload="renderMathInElement(document.body,{{delimiters:[{{left:'$',right:'$',display:false}}]}})"></script>
<style>body{{font:14px/1.55 Segoe UI,system-ui,sans-serif;color:#0f172a;max-width:820px;margin:24px auto;padding:0 16px}}
h1{{color:#4F46E5;margin-bottom:4px}}h2{{margin-top:32px;border-bottom:2px solid #4F46E5;padding-bottom:4px}}h2 small{{font-size:12px;color:#64748b;font-weight:500}}
.q{{border:1px solid #e2e8f0;border-radius:10px;padding:12px 14px;margin:10px 0;break-inside:avoid}}.meta{{font-size:12px;color:#64748b;margin-bottom:4px}}
li.ok{{color:#047857;font-weight:700}}li.ok::after{{content:"  ✓ answer"}}.exp{{font-size:13px;color:#475569;background:#f8fafc;border-radius:6px;padding:6px 8px}}
.note{{border:1px solid #e2e8f0;border-radius:10px;padding:12px 16px;margin:12px 0;break-inside:avoid}}.note h3{{margin:0 0 8px;color:#4F46E5}}
.break{{break-before:page}}</style></head><body>
<h1>Notenix KS3 · content review</h1><p>Years 7–9 baseline tests (handed out when a free week starts), Year 7 half-term tests (paying families, one set per half-term) and the notes for each year. Correct answers are marked in green.</p>
{''.join(parts)}</body></html>"""
out = DOCS / "ks3-content-review.html"
out.write_text(page, encoding="utf-8")
print("wrote", out)

for chrome in (r"C:\Program Files\Google\Chrome\Application\chrome.exe", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", shutil.which("chrome") or ""):
    if chrome and Path(chrome).exists():
        pdf = DOCS / "ks3-content-review.pdf"
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--virtual-time-budget=8000", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", out.as_uri()], capture_output=True, timeout=120)
        print("wrote", pdf, pdf.exists())
        break
