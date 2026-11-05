import Link from "next/link";
import { Logo } from "./ui/Logo";
import { LEGAL_LINKS } from "./LegalPage";

const COLS = [
  {
    title: "International",
    links: [
      { label: "SAT practice", href: "/sat" },
      { label: "ESAT practice", href: "/esat" },
      { label: "TMUA practice", href: "/tmua" },
      { label: "IGCSE practice", href: "/igcse" },
      { label: "GCSE Maths", href: "/gcse-maths" },
      { label: "A-Level Maths", href: "/a-level-maths" },
    ],
  },
  {
    title: "Australia & NZ",
    links: [
      { label: "HSC practice (NSW)", href: "/hsc" },
      { label: "VCE practice (VIC)", href: "/vce" },
      { label: "QCE practice (QLD)", href: "/qce" },
      { label: "WACE practice (WA)", href: "/wace" },
      { label: "NCEA practice (NZ)", href: "/ncea" },
    ],
  },
  {
    title: "Company",
    links: [
      { label: "Request a test", href: "/request" },
      { label: "Pricing", href: "/pricing" },
      { label: "Sign in", href: "/login" },
      { label: "Contact", href: "mailto:support@notenix.com" },
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
              Practice tests for students anywhere: sit timed mocks online, get instant marks,
              and have full papers marked by tutors from Beyond Tutors.
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
          <p className="text-xs text-ink-subtle">© {new Date().getFullYear()} Notenix, a unit of Beyond Groups. All rights reserved.</p>
          <div className="flex items-center gap-5 text-xs text-ink-subtle">
            {LEGAL_LINKS.map((l) => (
              <Link key={l.href} href={l.href} className="hover:text-ink">{l.label}</Link>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
}
