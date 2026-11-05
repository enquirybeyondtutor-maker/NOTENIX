import { Check, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/Button";
import LocalPrice from "@/components/LocalPrice";

const BOOK = "https://www.thebeyondtutors.com/book";

const FEATURES = [
  "Your own Notenix login (name@thebeyondtutors.com)",
  "Homework and timed tests set by your tutor",
  "Class notes from every lesson",
  "Instant marking, grade estimates and progress reports",
  "TMUA, ESAT, TARA, HSC, GCSE, A-Level and more",
];

const OPEN_FEATURES = [
  "Full access for a whole year",
  "Revision notes, worksheets and topic questions",
  "Timed, exam-style practice tests on any device",
  "Instant marking with worked solutions",
  "Tutor-marked mocks on request, with written feedback",
  "Grade estimates and topic-by-topic progress reports",
  "See your weak topics and what to revise next",
  "GCSE, IGCSE and A-Level, all major boards",
  "SAT, ESAT, TMUA, HSC, VCE, QCE, WACE and NCEA",
  "Pay once by card or bank transfer, from any country",
  "No auto-renewal: you choose whether to renew",
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
          <LocalPrice gbp={49} /> a year for Beyond Tutors students. Not with Beyond Tutors? Full access is <LocalPrice gbp={149} /> a year.
        </p>
      </div>

      <div className="mx-auto mt-12 grid max-w-4xl gap-6 md:grid-cols-2">
        <div className="card flex flex-col p-8">
          <h3 className="text-lg font-semibold text-ink">Beyond Tutors students</h3>
          <div className="mt-2 flex items-baseline gap-1">
            <LocalPrice gbp={49} className="text-4xl font-bold text-ink" subClassName="text-sm text-ink-subtle" />
            <span className="text-sm text-ink-subtle">/ year</span>
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
            Full access
          </span>
          <h3 className="text-lg font-semibold">Notenix full access</h3>
          <div className="mt-2 flex items-baseline gap-1">
            <LocalPrice gbp={149} className="text-4xl font-bold" subClassName="text-sm text-white/70" />
            <span className="text-sm text-white/70">/ year</span>
          </div>
          <p className="mt-1 text-sm text-white/80">
            For any student, anywhere. Everything Notenix offers, for a whole year.
          </p>
          <ul className="mt-6 flex-1 space-y-3">
            {OPEN_FEATURES.map((f) => (
              <li key={f} className="flex items-start gap-2 text-sm text-white/90">
                <Check size={16} className="mt-0.5 shrink-0 text-white" /> {f}
              </li>
            ))}
          </ul>
          <Button href="/revision/checkout" variant="inverse" className="mt-8 w-full">Get full access <ArrowRight size={16} /></Button>
        </div>
      </div>

      <p className="mt-8 text-center text-sm text-ink-muted">
        Already have a login? <a href="/login" className="font-semibold text-brand-600 hover:text-brand-700">Sign in</a>
      </p>
    </div>
  );
}
