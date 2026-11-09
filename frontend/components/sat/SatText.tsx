"use client";
import { MathText } from "@/components/MathText";

/** SAT passage / question text: paragraphs, "Text 1"/"Text 2" headings, bullet notes (•),
 *  pipe tables ("| a | b |") and $maths$. Content is ours (backend/sat_content), not user input. */
export default function SatText({ text, className = "" }: { text: string; className?: string }) {
  const lines = (text || "").split("\n");
  const blocks: React.ReactNode[] = [];
  let para: string[] = [];
  let table: string[] = [];
  let bullets: string[] = [];

  const flushPara = () => {
    if (para.length) {
      const t = para.join(" ");
      const heading = /^Text \d$/.test(t.trim());
      blocks.push(heading
        ? <p key={blocks.length} className="font-semibold text-ink">{t}</p>
        : <p key={blocks.length}><MathText text={t} /></p>);
      para = [];
    }
  };
  const flushBullets = () => {
    if (bullets.length) {
      blocks.push(
        <ul key={blocks.length} className="list-disc space-y-1 pl-5">
          {bullets.map((b, i) => <li key={i}><MathText text={b} /></li>)}
        </ul>,
      );
      bullets = [];
    }
  };
  const flushTable = () => {
    if (table.length) {
      const rows = table
        .filter((r) => !/^\|\s*-+/.test(r.trim()))
        .map((r) => r.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim()));
      const [head, ...body] = rows;
      blocks.push(
        <div key={blocks.length} className="overflow-x-auto">
          <table className="my-1 border-collapse text-sm">
            <thead><tr>{head.map((c, i) => <th key={i} className="border border-line bg-slate-50 px-3 py-1.5 text-left font-semibold"><MathText text={c} /></th>)}</tr></thead>
            <tbody>{body.map((r, i) => <tr key={i}>{r.map((c, j) => <td key={j} className="border border-line px-3 py-1.5"><MathText text={c} /></td>)}</tr>)}</tbody>
          </table>
        </div>,
      );
      table = [];
    }
  };

  for (const raw of lines) {
    const line = raw.trimEnd();
    if (line.trim().startsWith("|")) { flushPara(); flushBullets(); table.push(line); continue; }
    flushTable();
    if (line.trim().startsWith("•")) { flushPara(); bullets.push(line.trim().slice(1).trim()); continue; }
    flushBullets();
    if (!line.trim()) { flushPara(); continue; }
    if (/^Text \d$/.test(line.trim())) { flushPara(); para.push(line.trim()); flushPara(); continue; }
    para.push(line.trim());
  }
  flushPara(); flushBullets(); flushTable();
  return <div className={`space-y-3 leading-relaxed ${className}`}>{blocks}</div>;
}
