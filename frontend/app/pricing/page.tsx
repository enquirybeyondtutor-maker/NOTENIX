import { Check, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/Button";

const BOOK = "https://www.thebeyondtutors.com/book";

const FEATURES = [
  "Your own Notenix login (name@thebeyondtutors.com)",
  "Homework and timed tests set by your tutor",
  "Class notes from every lesson",
  "Instant marking, grade estimates and progress reports",
  "TMUA, ESAT, TARA, HSC, GCSE, A-Level and more",
];

export default function Pricing() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-16 sm:px-6">
      <div className="mx-auto max-w-2xl text-center">
        <span className="eyebrow">Pricing</span>
        <h1 className="mt-3 text-3xl font-bold tracking-tight text-ink sm:text-4xl">
          One plan for every Beyond Tutors student
        </h1>
        <p className="mt-4 text-lg text-ink-muted">
          Notenix comes with your Beyond Tutors classes. Try it free during your trial class,
          then £49 a year when you join.
        </p>
      </div>

      <div className="mx-auto mt-12 grid max-w-3xl gap-6 md:grid-cols-2">
        <div className="card flex flex-col p-8">
          <h3 className="text-lg font-semibold text-ink">Trial class</h3>
          <div className="mt-2 flex items-baseline gap-1">
            <span className="text-4xl font-bold text-ink">£0</span>
          </div>
          <p className="mt-1 text-sm text-ink-muted">Full access while you try a class with us.</p>
          <ul className="mt-6 flex-1 space-y-3">
            {FEATURES.slice(0, 3).map((f) => (
              <li key={f} className="flex items-center gap-2 text-sm text-ink-muted">
                <Check size={16} className="text-emerald-500" /> {f}
              </li>
            ))}
          </ul>
          <Button href={BOOK} variant="secondary" className="mt-8 w-full">Book a free trial class</Button>
        </div>

        <div className="card flex flex-col border-brand-300 p-8 ring-1 ring-brand-200">
          <h3 className="text-lg font-semibold text-ink">Notenix subscription</h3>
          <div className="mt-2 flex items-baseline gap-1">
            <span className="text-4xl font-bold text-ink">£49</span>
            <span className="text-sm text-ink-subtle">/ year</span>
          </div>
          <p className="mt-1 text-sm text-ink-muted">
            Paid once when you join Beyond Tutors, renewed each year. Your login is issued by our team.
          </p>
          <ul className="mt-6 flex-1 space-y-3">
            {FEATURES.map((f) => (
              <li key={f} className="flex items-center gap-2 text-sm text-ink-muted">
                <Check size={16} className="text-brand-600" /> {f}
              </li>
            ))}
          </ul>
          <Button href={BOOK} className="mt-8 w-full">Join Beyond Tutors <ArrowRight size={16} /></Button>
        </div>
      </div>

      <p className="mt-8 text-center text-sm text-ink-muted">
        Already have a login? <a href="/login" className="font-semibold text-brand-600 hover:text-brand-700">Sign in</a>
      </p>
    </div>
  );
}
