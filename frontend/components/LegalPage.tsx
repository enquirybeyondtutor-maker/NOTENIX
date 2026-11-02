import Link from "next/link";

// Shared layout for /terms, /privacy and /refunds. Keep these documents in step with what the
// product actually does (retention in backend/config.py, prices in PRO_PRICE / REQUEST_PRICE).
export const LEGAL_UPDATED = "25 October 2026";

export const LEGAL_LINKS = [
  { label: "Terms", href: "/terms" },
  { label: "Privacy", href: "/privacy" },
  { label: "Refunds", href: "/refunds" },
];

export default function LegalPage({ title, intro, children }: { title: string; intro: string; children: React.ReactNode }) {
  return (
    <div className="mx-auto max-w-3xl px-4 py-14 sm:px-6">
      <span className="eyebrow">Policies</span>
      <h1 className="mt-3 text-3xl font-bold tracking-tight text-ink sm:text-4xl">{title}</h1>
      <p className="mt-2 text-sm text-ink-subtle">Last updated {LEGAL_UPDATED}</p>
      <p className="mt-6 text-lg leading-relaxed text-ink-muted">{intro}</p>
      <div className="mt-10 space-y-8 text-[15px] leading-relaxed text-ink-muted [&_h2]:text-lg [&_h2]:font-semibold [&_h2]:text-ink [&_li]:ml-5 [&_li]:list-disc [&_p+p]:mt-3 [&_ul]:mt-3 [&_ul]:space-y-1.5">
        {children}
      </div>
      <nav className="mt-14 flex flex-wrap gap-4 border-t border-line pt-6 text-sm">
        {LEGAL_LINKS.map((l) => (
          <Link key={l.href} href={l.href} className="font-medium text-brand-600 hover:underline">{l.label}</Link>
        ))}
        <a href="mailto:hello@notenix.com" className="font-medium text-brand-600 hover:underline">hello@notenix.com</a>
      </nav>
    </div>
  );
}
