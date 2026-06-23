import pdfplumber, sys

path = r"knowledge_base/A levels/BIOLOGY/AQA/1.6 ATP QP.pdf"
with pdfplumber.open(path) as pdf:
    print(f"TOTAL PAGES: {len(pdf.pages)}")
    for i, page in enumerate(pdf.pages[:3]):
        print(f"\n===== PAGE {i+1} =====")
        txt = page.extract_text() or "(no text)"
        print(txt[:1800])
