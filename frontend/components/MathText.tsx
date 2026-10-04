import katex from "katex";

// Renders text containing LaTeX: $$…$$ for display maths, $…$ for inline maths. Everything else is
// plain text, so existing questions are unaffected. Inline $ follows the pandoc rule (no space just
// inside the delimiters, closing $ not followed by a digit) so prices like "$5 and $10" stay as text.
const MATH = /\$\$([\s\S]+?)\$\$|\$(?![\s$])((?:\\.|[^$\\\n])+?)(?<!\s)\$(?!\d)/g;

type Part = { text: string } | { tex: string; display: boolean };

function split(src: string): Part[] {
  const parts: Part[] = [];
  let last = 0;
  for (const m of src.matchAll(MATH)) {
    if (m.index! > last) parts.push({ text: src.slice(last, m.index) });
    parts.push(m[1] != null ? { tex: m[1], display: true } : { tex: m[2], display: false });
    last = m.index! + m[0].length;
  }
  if (last < src.length) parts.push({ text: src.slice(last) });
  return parts;
}

export function MathText({ text }: { text?: string | null }) {
  if (!text) return null;
  if (!text.includes("$")) return <>{text}</>;
  return (
    <>
      {split(text).map((p, i) =>
        "text" in p ? (
          <span key={i}>{p.text}</span>
        ) : (
          <span
            key={i}
            className={p.display ? "block overflow-x-auto py-1" : undefined}
            // KaTeX escapes the source and trust is off, so this HTML is safe to inject.
            dangerouslySetInnerHTML={{ __html: katex.renderToString(p.tex, { displayMode: p.display, throwOnError: false }) }}
          />
        ),
      )}
    </>
  );
}
