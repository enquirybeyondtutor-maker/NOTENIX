import Link from "next/link";
import { Fragment } from "react";

/** Renders **bold** and [text](/path) inside a plain string (guides, notes). Server-safe, no HTML injection. */
export function RichText({ text }: { text: string }) {
  const parts = text.split(/(\*\*[^*]+\*\*|\[[^\]]+\]\([^)]+\))/g);
  return (
    <>
      {parts.map((p, i) => {
        const bold = p.match(/^\*\*([^*]+)\*\*$/);
        if (bold) return <strong key={i} className="font-semibold text-ink">{bold[1]}</strong>;
        const link = p.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
        if (link) {
          const internal = link[2].startsWith("/");
          return internal ? (
            <Link key={i} href={link[2]} className="font-medium text-brand-700 underline decoration-brand-300 underline-offset-2 hover:decoration-brand-600">{link[1]}</Link>
          ) : (
            <a key={i} href={link[2]} rel="noopener" className="font-medium text-brand-700 underline">{link[1]}</a>
          );
        }
        return <Fragment key={i}>{p}</Fragment>;
      })}
    </>
  );
}
