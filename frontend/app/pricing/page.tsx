import { Check, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/Button";
import LocalPrice from "@/components/LocalPrice";

const BOOK = "https://www.thebeyondtutors.com/book";

const FEATURES = [
  "Your own Notenix login (name@beyondtutors.com)",
  "Homework and timed tests set by your tutor",
  "Class notes from every lesson",
  "Instant marking, grade estimates and progress reports",
  "Per course: e.g. IGCSE Chemistry, A-Level Maths or TMUA",
  "Add another course any time for the same yearly price",
];

const OPEN_FEATURES = [
  "One course for a whole year (e.g. IGCSE Chemistry, A-Level Maths, TMUA)",
  "Revision notes, worksheets and topic questions",
  "Timed, exam-style practice tests on any device",
  "Instant marking with worked solutions",
  "Tutor-marked mocks on request, with written feedback",
  "Grade estimates and topic-by-topic progress reports",
  "See your weak topics and what to revise next",
  "GCSE, IGCSE, A-Level, HSC, VCE, QCE, WACE, NCEA, SAT, ESAT, TMUA and TARA courses",
  "Add more courses any time",
  "Pay once by bank transfer, from any country",
  "No auto-renewal: you choose whether to renew",
];

// Yearly prices for students outside Beyond Tutors. Keep in step with backend/services/pricing.py
// (GCSE_PRICES, GCSE_BUNDLE_PRICES, SAT_PRICES, KS3_PRICES), config.revision_price and services/doubt.py.
const COURSE_PRICES: { name: string; detail: string; gbp: number; per: string; href: string; tag?: string }[] = [
  { name: "GCSE, one subject", detail: "Maths, Biology, Chemistry or Physics: diagnostic, topic drills and practice papers", gbp: 99, per: "/ year", href: "/gcse-maths" },
  { name: "GCSE, all four subjects", detail: "Maths, Biology, Chemistry and Physics together", gbp: 349, per: "/ year", href: "/gcse-maths", tag: "Save £47" },
  { name: "SAT", detail: "Full adaptive SAT practice tests, score reports and worked explanations", gbp: 99, per: "/ year", href: "/sat" },
  { name: "Any other course", detail: "IGCSE, A-Level, TMUA, ESAT, TARA, HSC, VCE, QCE, WACE, NCEA", gbp: 149, per: "/ year per course", href: "/revision/checkout" },
  { name: "KS3 (Years 7 to 9)", detail: "A test every half-term, homework help, notes and a monthly progress report. Free trial first", gbp: 149, per: "/ year", href: "/ks3" },
  { name: "Ask a Tutor", detail: "Homework questions answered step by step by a tutor. Plus £49 / 30 days, or £149 a year", gbp: 25, per: "/ 30 days", href: "/ask-a-tutor", tag: "From" },
];

export default function Pricing() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-16 sm:px-6">
      <div className="mx-auto max-w-2xl text-center">
        <span className="eyebrow">Pricing</span>
        <h1 className="mt-3 text-3xl font-bold tracking-tight text-ink sm:text-4xl">
          Simple yearly pricing
        </h1>
        <p className="mt-4 text-lg text-ink-muted">
          <LocalPrice gbp={49} /> a year per course for Beyond Tutors students. Not with Beyond Tutors? From <LocalPrice gbp={99} /> a year: GCSE and SAT <LocalPrice gbp={99} />, other courses <LocalPrice gbp={149} />.
        </p>
      </div>

      <div className="mx-auto mt-12 grid max-w-4xl gap-6 md:grid-cols-2">
        <div className="card flex flex-col p-8">
          <h3 className="text-lg font-semibold text-ink">Beyond Tutors students</h3>
          <div className="mt-2 flex items-baseline gap-1">
            <LocalPrice gbp={49} className="text-4xl font-bold text-ink" subClassName="text-sm text-ink-subtle" />
            <span className="text-sm text-ink-subtle">/ year per course</span>
          </div>
          <p className="mt-1 text-sm text-ink-muted">
            Paid once when you join Beyond Tutors, renewed each year. Your login is issued by our team.
          </p>
          <ul className="mt-6 flex-1 space-y-3">
            {FEATURES.map((f) => (
              <li key={f} className="flex items-start gap-2 text-sm text-ink-muted">
                <Check size={16} className="mt-0.5 shrink-0 text-brand-600" /> {f}
              </li>
            ))}
          </ul>
          <Button href={BOOK} variant="secondary" className="mt-8 w-full">Join Beyond Tutors <ArrowRight size={16} /></Button>
        </div>

        <div className="relative flex flex-col rounded-2xl p-8 text-white shadow-lg" style={{ background: "#5444DC" }}>
          <span className="absolute -top-3 left-8 rounded-full bg-white px-3 py-1 text-xs font-semibold shadow-sm" style={{ color: "#5444DC" }}>
            Any student
          </span>
          <h3 className="text-lg font-semibold">Notenix course</h3>
          <div className="mt-2 flex items-baseline gap-1">
            <span className="text-sm text-white/70">from</span>
            <LocalPrice gbp={99} className="text-4xl font-bold" subClassName="text-sm text-white/70" />
            <span className="text-sm text-white/70">/ year per course</span>
          </div>
          <p className="mt-1 text-sm text-white/80">
            For any student, anywhere. Everything Notenix offers for your course, for a whole year.
            GCSE and SAT <LocalPrice gbp={99} />, other courses <LocalPrice gbp={149} />. <a href="#all-prices" className="underline underline-offset-2">See every price</a>.
          </p>
          <ul className="mt-6 flex-1 space-y-3">
            {OPEN_FEATURES.map((f) => (
              <li key={f} className="flex items-start gap-2 text-sm text-white/90">
                <Check size={16} className="mt-0.5 shrink-0 text-white" /> {f}
              </li>
            ))}
          </ul>
          <Button href="/revision/checkout" variant="inverse" className="mt-8 w-full">Choose your course <ArrowRight size={16} /></Button>
        </div>
      </div>

      <section id="all-prices" className="mx-auto mt-16 max-w-4xl scroll-mt-24">
        <h2 className="text-2xl font-bold tracking-tight text-ink">Every price, if you&apos;re not with Beyond Tutors</h2>
        <p className="mt-2 text-sm text-ink-muted">
          Paid once by bank transfer. The exact amount in your currency is shown before you pay, and nothing renews automatically.
          Beyond Tutors students pay <LocalPrice gbp={49} /> a year per course instead.
        </p>
        <div className="card mt-6 divide-y divide-line">
          {COURSE_PRICES.map((p) => (
            <a key={p.name} href={p.href}
              className="flex flex-col gap-2 p-5 transition-colors hover:bg-slate-50 sm:flex-row sm:items-center sm:justify-between sm:gap-6">
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2 font-semibold text-ink">
                  {p.name}
                  {p.tag && p.tag !== "From" && (
                    <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-xs font-semibold text-emerald-700">{p.tag}</span>
                  )}
                </div>
                <div className="mt-0.5 text-sm text-ink-muted">{p.detail}</div>
              </div>
              <div className="shrink-0 whitespace-nowrap sm:text-right">
                {p.tag === "From" && <span className="mr-1 text-sm text-ink-subtle">from</span>}
                <LocalPrice gbp={p.gbp} className="text-xl font-bold text-ink" subClassName="text-xs text-ink-subtle" />
                <span className="ml-1 text-sm text-ink-subtle">{p.per}</span>
              </div>
            </a>
          ))}
        </div>
      </section>

      <p className="mt-8 text-center text-sm text-ink-muted">
        Already have a login? <a href="/login" className="font-semibold text-brand-600 hover:text-brand-700">Sign in</a>
      </p>
    </div>
  );
}
