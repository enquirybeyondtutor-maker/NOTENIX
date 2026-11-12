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
  "Pay once by card or bank transfer, from any country",
  "No auto-renewal: you choose whether to renew",
];

// Yearly prices for students outside Beyond Tutors. Keep in step with backend/services/pricing.py
// (GCSE_PRICES, GCSE_BUNDLE_PRICES, SAT_PRICES, KS3_PRICES), config.revision_price and services/doubt.py.
type Plan = {
  name: string; who: string; gbp: number; per: string; from?: boolean; tag?: string;
  includes: string[]; pay: string; cta: string; href: string; more?: { label: string; href: string };
};

const PLANS: Plan[] = [
  {
    name: "GCSE, one subject", who: "Year 10 and 11 students taking GCSE Maths, Biology, Chemistry or Physics (AQA, Edexcel, OCR).",
    gbp: 99, per: "/ year",
    includes: [
      "Free diagnostic test with a 9â€“1 grade estimate and a skill map",
      "Topic drills for every skill, with worked explanations",
      "Two full practice papers, timed and marked instantly",
      "Tutor-marked past papers on request, with written feedback",
    ],
    pay: "One payment, one subject, 12 months of access. Card or bank transfer, from any country.",
    cta: "Buy one GCSE subject", href: "/revision/checkout?course=gcse-maths",
    more: { label: "Try the free GCSE diagnostic", href: "/gcse-maths/diagnostic" },
  },
  {
    name: "GCSE, all four subjects", who: "Students taking GCSE Maths and the three separate sciences.",
    gbp: 349, per: "/ year", tag: "Save Â£47",
    includes: [
      "Everything in the one-subject plan, for Maths, Biology, Chemistry and Physics",
      "One payment unlocks all four courses at once",
      "Â£47 less than buying the four subjects one by one (Â£396)",
    ],
    pay: "One payment, 12 months of access to all four. Card or bank transfer, from any country.",
    cta: "Buy all four GCSEs", href: "/revision/checkout?course=gcse-bundle",
  },
  {
    name: "SAT", who: "Students preparing for the digital SAT, anywhere in the world.",
    gbp: 99, per: "/ year",
    includes: [
      "Full-length adaptive practice tests that work like the real digital SAT",
      "Score reports with your estimated SAT score and weakest skills",
      "Skill drills with worked explanations for Reading & Writing and Maths",
      "Access until your SAT date (12 months)",
    ],
    pay: "One payment, 12 months of access. Card or bank transfer, from any country.",
    cta: "Buy SAT", href: "/revision/checkout?course=sat",
    more: { label: "Start with a free SAT diagnostic", href: "/sat" },
  },
  {
    name: "Any other course", who: "IGCSE, A-Level, TMUA, ESAT, TARA, HSC, VCE, QCE, WACE and NCEA students.",
    gbp: 149, per: "/ year per course",
    includes: [
      "Practice papers and topic questions for your course",
      "Revision notes and worksheets",
      "Tutor-marked mocks on request, with written feedback",
      "Grade estimates and topic-by-topic progress reports",
    ],
    pay: "One payment per course, 12 months of access. Card or bank transfer.",
    cta: "Choose your course", href: "/revision/checkout",
  },
  {
    name: "KS3 (Years 7 to 9)", who: "Parents of students in Years 7, 8 and 9 who want regular checks on progress.",
    gbp: 149, per: "/ year",
    includes: [
      "A timed test in Maths, Science and English every half-term",
      "Homework help from Beyond Tutors tutors",
      "KS3 notes for every topic",
      "A progress report for parents every month",
    ],
    pay: "Starts with a free one-week trial; continue for a year only if you want to.",
    cta: "Start the free trial", href: "/ks3/trial",
    more: { label: "How Notenix KS3 works", href: "/ks3" },
  },
  {
    name: "Ask a Tutor", who: "Any student stuck on homework who wants a tutor's step-by-step answer.",
    gbp: 25, per: "/ 30 days", from: true,
    includes: [
      "30 days: up to 20 questions, answered step by step by a tutor (Â£25)",
      "Plus, 30 days: up to 50 questions and two live 30-minute calls with a tutor (Â£49)",
      "A whole year: up to 20 questions every month (Â£149)",
    ],
    pay: "Starts with a free 7-day trial (5 questions). No auto-renewal.",
    cta: "Try Ask a Tutor free", href: "/ask-a-tutor",
  },
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
          The exact amount in your currency is shown before you pay, and nothing renews automatically.
          Beyond Tutors students pay <LocalPrice gbp={49} /> a year per course instead, through their tuition invoice.
        </p>
        <div className="mt-6 grid gap-5 md:grid-cols-2">
          {PLANS.map((p) => (
            <div key={p.name} className="card flex flex-col p-6">
              <div className="flex flex-wrap items-center gap-2">
                <h3 className="font-semibold text-ink">{p.name}</h3>
                {p.tag && <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-xs font-semibold text-emerald-700">{p.tag}</span>}
              </div>
              <div className="mt-2 flex flex-wrap items-baseline gap-1">
                {p.from && <span className="text-sm text-ink-subtle">from</span>}
                <LocalPrice gbp={p.gbp} className="text-3xl font-bold text-ink" subClassName="text-xs text-ink-subtle" />
                <span className="text-sm text-ink-subtle">{p.per}</span>
              </div>
              <p className="mt-2 text-sm text-ink-muted">{p.who}</p>
              <ul className="mt-4 flex-1 space-y-2">
                {p.includes.map((f) => (
                  <li key={f} className="flex items-start gap-2 text-sm text-ink-muted">
                    <Check size={15} className="mt-0.5 shrink-0 text-brand-600" /> {f}
                  </li>
                ))}
              </ul>
              <p className="mt-4 text-xs text-ink-subtle">{p.pay}</p>
              <Button href={p.href} className="mt-4 w-full">{p.cta} <ArrowRight size={16} /></Button>
              {p.more && (
                <a href={p.more.href} className="mt-2 text-center text-sm font-medium text-brand-600 hover:text-brand-700">{p.more.label}</a>
              )}
            </div>
          ))}
        </div>
      </section>

      <p className="mt-8 text-center text-sm text-ink-muted">
        Already have a login? <a href="/login" className="font-semibold text-brand-600 hover:text-brand-700">Sign in</a>
      </p>
    </div>
  );
}
