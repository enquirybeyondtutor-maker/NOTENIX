r"""Review copy of every Notenix SAT question (answers + explanations) for a human check.
Run: python make_review.py  ->  notenix-v2/docs/sat-content-review.pdf (needs Chrome)."""
import html
import json
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
DOCS = HERE.parent.parent / "docs"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ORDER = ["diagnostic", "mock-1", "mock-2", "drills"]
MODULE_NAMES = {"rw": "Reading and Writing", "m": "Math", "rw1": "Reading and Writing · Module 1",
                "rw2e": "Reading and Writing · Module 2 (easier)", "rw2h": "Reading and Writing · Module 2 (harder)",
                "m1": "Math · Module 1", "m2e": "Math · Module 2 (easier)", "m2h": "Math · Module 2 (harder)"}


def text(s: str) -> str:
    """Escape, keep $maths$ for KaTeX, turn pipe tables and bullets into HTML."""
    out, table = [], []
    for line in s.split("\n"):
        if line.strip().startswith("|"):
            if not re.match(r"^\|\s*-", line.strip()):
                table.append([c.strip() for c in line.strip().strip("|").split("|")])
            continue
        if table:
            out.append("<table>" + "".join("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r) + "</tr>" for r in table) + "</table>")
            table = []
        out.append(html.escape(line) if line.strip() else "<br>")
    if table:
        out.append("<table>" + "".join("<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in r) + "</tr>" for r in table) + "</table>")
    return "<br>".join(x for x in out)


def main():
    parts = []
    total = 0
    for slug in ORDER:
        f = json.loads((HERE / f"{slug}.json").read_text(encoding="utf-8"))
        parts.append(f'<h1>{html.escape(f["title"])}</h1>')
        for key, m in f["modules"].items():
            mins = f" · {m['minutes']} min" if m["minutes"] else ""
            parts.append(f'<h2>{MODULE_NAMES.get(key, m["title"])} · {len(m["questions"])} questions{mins}</h2>')
            for i, q in enumerate(m["questions"], 1):
                total += 1
                meta = f'{q["domain"]} · {q["skill"]} · difficulty {q["difficulty"]}'
                body = ""
                if q.get("passage"):
                    body += f'<div class="passage">{text(q["passage"])}</div>'
                body += f'<div class="q">{text(q["question"])}</div>'
                if q["type"] == "mcq":
                    body += "<ol type=A>" + "".join(
                        f'<li class="{"right" if "ABCD"[k] == q["answer"] else ""}">{html.escape(o)}</li>' for k, o in enumerate(q["options"])) + "</ol>"
                else:
                    body += f'<p class="right">Type-in answer: {html.escape(" or ".join(q["answer"]))}</p>'
                body += f'<div class="ex"><b>Answer {q["answer"] if q["type"] == "mcq" else q["answer"][0]}.</b> {text(q["explanation"])}</div>'
                parts.append(f'<div class="item"><div class="meta">{html.escape(q["id"])} · {html.escape(meta)}</div>{body}</div>')
    page = f"""<!doctype html><html><head><meta charset="utf-8"><title>Notenix SAT content review</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
 onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}],throwOnError:false}})"></script>
<style>
 @page {{ size: A4; margin: 14mm 13mm; }}
 body {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 10.5pt; color: #1d1b33; }}
 h1 {{ color: #5444DC; font-size: 20pt; margin: 0 0 4px; page-break-before: always; }}
 h1:first-of-type {{ page-break-before: avoid; }}
 h2 {{ font-size: 12.5pt; border-bottom: 2px solid #5444DC; padding-bottom: 3px; margin-top: 18px; }}
 .item {{ border: 1px solid #ddd; border-radius: 8px; padding: 8px 11px; margin: 9px 0; page-break-inside: avoid; }}
 .meta {{ font-size: 8pt; color: #777; margin-bottom: 4px; }}
 .passage {{ background: #f6f6fa; border-radius: 6px; padding: 6px 9px; margin-bottom: 6px; }}
 .q {{ font-weight: 600; }}
 ol {{ margin: 5px 0; padding-left: 22px; }}
 li.right, p.right {{ color: #0a7d3b; font-weight: 700; }}
 .ex {{ background: #f2f1ff; border-radius: 6px; padding: 5px 9px; font-size: 9.5pt; margin-top: 5px; }}
 table {{ border-collapse: collapse; margin: 4px 0; }} td {{ border: 1px solid #bbb; padding: 2px 7px; }}
 .cover {{ text-align: center; margin-top: 30mm; }}
</style></head><body>
<div class="cover"><h1 style="page-break-before:avoid;font-size:28pt">Notenix SAT</h1>
<p style="font-size:13pt">Content review: {total} original questions</p>
<p>Diagnostic (26) · Practice Test 1 (147) · Practice Test 2 (147) · Skill drills (180)<br>Correct options in green, explanation below each question.</p></div>
{''.join(parts)}
<script>window.addEventListener('load', () => setTimeout(() => document.title += ' ready', 2500));</script>
</body></html>"""
    DOCS.mkdir(exist_ok=True)
    src = DOCS / "sat-content-review.html"
    src.write_text(page, encoding="utf-8")
    pdf = DOCS / "sat-content-review.pdf"
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=15000",
                    f"--print-to-pdf={pdf}", src.as_uri()], check=True, capture_output=True)
    print(f"{total} questions -> {pdf}")


if __name__ == "__main__":
    main()
