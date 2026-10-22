import type { Metadata } from "next";
import { Send, ClipboardCheck, PenLine, UserCheck, CheckCircle2 } from "lucide-react";
import { SITE } from "@/lib/site";
import RequestForm from "@/components/RequestForm";

export const metadata: Metadata = {
  title: "Request a Tutor-Marked Mock Test (SAT, ESAT, TMUA, JEE, NEET, CBSE…)",
  description:
    "Request a full practice test for SAT, ESAT, TMUA, GCSE, IGCSE, A-Level, CBSE, ICSE, JEE or NEET. Sit it online under timed conditions and get it marked by real tutors with feedback.",
  alternates: { canonical: `${SITE}/request` },
};

const STEPS = [
  { icon: Send, title: "Request", desc: "Choose your exam and tell us what you need." },
  { icon: ClipboardCheck, title: "We send it", desc: "A tutor picks a suitable mock and it appears in your account." },
  { icon: PenLine, title: "You sit it", desc: "Timed and exam-style, on any device." },
  { icon: UserCheck, title: "Tutor marks it", desc: "Score, written feedback and what to work on next." },
];

export default function RequestPage() {
  return (
    <div className="mx-auto max-w-5xl px-4 py-14 sm:px-6">
      <div className="max-w-2xl">
        <span className="eyebrow">Tutor-marked tests</span>
        <h1 className="mt-3 text-3xl font-bold tracking-tight text-ink sm:text-4xl">Request a test, marked by our team</h1>
        <p className="mt-4 text-lg text-ink-muted">
          Real exam conditions, marked by experienced tutors. For students anywhere in the world.
        </p>
      </div>

      <div className="mt-10 grid gap-10 lg:grid-cols-[1.2fr_0.8fr]">
        <RequestForm />
        <div>
          <ol className="space-y-6">
            {STEPS.map((s, i) => (
              <li key={s.title} className="flex gap-4">
                <span className="grid h-10 w-10 shrink-0 place-items-center rounded-lg bg-brand-600 text-white"><s.icon size={18} /></span>
                <div>
                  <div className="text-xs font-bold text-ink-subtle">STEP {i + 1}</div>
                  <div className="font-semibold text-ink">{s.title}</div>
                  <p className="text-sm text-ink-muted">{s.desc}</p>
                </div>
              </li>
            ))}
          </ol>
          <ul className="mt-8 space-y-2 border-t border-line pt-6">
            {["Original questions written by tutors", "Instant marks for multiple-choice", "Written answers marked by hand", "Pay from any country"].map((x) => (
              <li key={x} className="flex items-center gap-2 text-sm text-ink-muted">
                <CheckCircle2 size={15} className="text-emerald-600" /> {x}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
