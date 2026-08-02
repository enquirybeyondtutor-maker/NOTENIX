import Link from "next/link";
import { Logo } from "./ui/Logo";

const COLS = [
  {
    title: "Product",
    links: [
      { label: "Features", href: "/#features" },
      { label: "How it works", href: "/#how" },
      { label: "Pricing", href: "/pricing" },
    ],
  },
  {
    title: "For educators",
    links: [
      { label: "Create tests", href: "/register" },
      { label: "Assign & track", href: "/register" },
      { label: "Book a demo", href: "/pricing" },
    ],
  },
  {
    title: "Company",
    links: [
      { label: "Sign in", href: "/login" },
      { label: "Get started", href: "/register" },
      { label: "Contact", href: "mailto:hello@notenix.com" },
    ],
  },
];

export default function Footer() {
  return (
    <footer className="border-t border-line bg-white">
      <div className="mx-auto max-w-7xl px-4 py-14 sm:px-6">
        <div className="grid gap-10 md:grid-cols-[1.4fr_1fr_1fr_1fr]">
          <div className="max-w-xs">
            <Logo />
            <p className="mt-4 text-sm leading-relaxed text-ink-muted">
              The assessment platform for UK schools. Create board-aligned tests, assign them to
              students, and track mastery — powered by AI.
            </p>
          </div>
          {COLS.map((col) => (
            <div key={col.title}>
              <h4 className="text-xs font-semibold uppercase tracking-wider text-ink-subtle">{col.title}</h4>
              <ul className="mt-4 space-y-2.5">
                {col.links.map((l) => (
                  <li key={l.label}>
                    <Link href={l.href} className="text-sm text-ink-muted transition-colors hover:text-brand-600">
                      {l.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="mt-12 flex flex-col items-center justify-between gap-3 border-t border-line pt-6 sm:flex-row">
          <p className="text-xs text-ink-subtle">© {new Date().getFullYear()} Notenix · Beyond Imagination. All rights reserved.</p>
          <div className="flex items-center gap-5 text-xs text-ink-subtle">
            <Link href="/pricing" className="hover:text-ink">Terms</Link>
            <Link href="/pricing" className="hover:text-ink">Privacy</Link>
            <span>Powered by Claude AI</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
