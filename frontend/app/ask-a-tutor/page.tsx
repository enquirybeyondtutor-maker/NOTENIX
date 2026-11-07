import type { Metadata } from "next";
import { Camera, MessageSquareText, Clock, Check } from "lucide-react";
import { SITE } from "@/lib/site";
import SignUp from "./SignUp";

export const metadata: Metadata = {
  title: "Ask a Tutor: Send a Photo of Any Question, Get a Step-by-Step Explanation (Singapore Sec 1–4, JC)",
  description: "Stuck on Science or Maths after studying? Your child sends a photo of the question and a Beyond Tutors tutor replies with a clear explanation, usually the same evening (Singapore time). S$249 a year. Free trial: 5 questions.",
  alternates: { canonical: `${SITE}/ask-a-tutor` },
};

const STEPS = [
  { icon: Camera, title: "Snap the question", desc: "Your child photographs the question or the topic they don't understand, and says what's confusing." },
  { icon: MessageSquareText, title: "A tutor explains it", desc: "A Beyond Tutors tutor replies step by step, so your child understands the method, not just the answer." },
  { icon: Clock, title: "Usually the same evening", desc: "Questions sent after school are normally answered the same evening, Singapore time." },
];

const PLANS = [
  { name: "1 year", price: "S$249", per: "/ year", highlight: true, note: "About S$21 a month", points: ["Up to 20 questions every month, all year", "Step-by-step written explanations", "Science, Maths, English (Sec 1–2); Physics, Chemistry, Biology, E-Math, A-Math (Sec 3–4)", "All answers saved to revise from"] },
  { name: "Monthly", price: "S$39", per: "/ month", points: ["Up to 20 questions every 30 days", "Step-by-step written explanations", "Science, Maths, English (Sec 1–2); Physics, Chemistry, Biology, E-Math, A-Math (Sec 3–4)", "All answers saved to revise from"] },
  { name: "Monthly Plus", price: "S$79", per: "/ month", points: ["Up to 50 questions every 30 days", "Everything in Doubt Help", "2 live 30-minute doubt-clearing calls each month", "Best before tests and exams"] },
];

const FAQ: [string, string][] = [
  ["Which levels and subjects do you cover?", "Secondary 1 to 4 (and 5): Science, Maths and English at lower secondary; Physics, Chemistry, Biology, Combined Science, E-Math and A-Math at upper secondary. JC H2 Maths and Sciences are also available."],
  ["Will the tutor just give the answer?", "No. Tutors explain the method step by step so your child can do the next question on their own. That's what actually helps in tests."],
  ["How fast is the reply?", "Questions sent after school are usually answered the same evening, Singapore time. Our tutors work across Singapore evening hours."],
  ["How does payment work?", "By bank transfer: S$249 covers a whole year, or pay monthly from S$39. Nothing renews automatically, and we remind you before the end."],
  ["Who are the tutors?", "Notenix is run with Beyond Tutors, whose tutors teach Maths and Science up to university-admissions level."],
];

export default function AskATutor() {
  return (
    <div>
      <section className="bg-gradient-to-b from-brand-50 to-white">
        <div className="mx-auto grid max-w-6xl items-start gap-10 px-4 py-14 sm:px-6 lg:grid-cols-[1.1fr_1fr] lg:py-20">
          <div>
            <span className="eyebrow">Ask a Tutor · Singapore Sec 1–4 &amp; JC</span>
            <h1 className="mt-3 text-4xl font-bold tracking-tight text-ink sm:text-5xl">Stuck after studying? Ask a tutor tonight.</h1>
            <p className="mt-5 text-lg text-ink-muted">
              Your child sends a photo of any Science or Maths question they don&apos;t understand, and a Beyond Tutors tutor
              replies with a clear, step-by-step explanation, usually the same evening.
            </p>
            <ul className="mt-6 space-y-2 text-sm text-ink">
              {["5 free questions to try it", "S$249 for a whole year (about S$21 a month)", "Costs less than one hour of home tuition a month"].map((t) => (
                <li key={t} className="flex items-center gap-2"><Check size={16} className="text-brand-600" /> {t}</li>
              ))}
            </ul>
          </div>
          <SignUp />
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
        <h2 className="text-center text-3xl font-bold tracking-tight text-ink">How it works</h2>
        <div className="mt-10 grid gap-6 md:grid-cols-3">
          {STEPS.map((s) => (
            <div key={s.title} className="card p-6">
              <span className="grid h-10 w-10 place-items-center rounded-xl bg-brand-50 text-brand-600"><s.icon size={20} /></span>
              <h3 className="mt-4 font-semibold text-ink">{s.title}</h3>
              <p className="mt-1 text-sm text-ink-muted">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="plans" className="bg-slate-50">
        <div className="mx-auto max-w-5xl scroll-mt-20 px-4 py-16 sm:px-6">
          <h2 className="text-center text-3xl font-bold tracking-tight text-ink">Simple plans</h2>
          <p className="mt-2 text-center text-ink-muted">Start with the free trial. Pay only if it helps.</p>
          <div className="mx-auto mt-10 grid max-w-5xl gap-6 md:grid-cols-3">
            {PLANS.map((p) => (
              <div key={p.name} className={`card flex flex-col p-8 ${p.highlight ? "border-brand-300 ring-2 ring-brand-600/20" : ""}`}>
                <h3 className="flex items-center gap-2 text-lg font-semibold text-ink">{p.name} {p.highlight && <span className="rounded-full bg-brand-600 px-2 py-0.5 text-[11px] font-semibold text-white">Best value</span>}</h3>
                <div className="mt-2 flex items-baseline gap-1"><span className="text-4xl font-bold text-ink">{p.price}</span><span className="text-sm text-ink-subtle">{p.per}</span></div>
                {"note" in p && p.note && <div className="mt-1 text-sm font-medium text-emerald-700">{p.note}</div>}
                <ul className="mt-6 flex-1 space-y-3 text-sm text-ink-muted">
                  {p.points.map((x) => <li key={x} className="flex items-start gap-2"><Check size={16} className="mt-0.5 shrink-0 text-brand-600" /> {x}</li>)}
                </ul>
                <a href="#start" className="mt-8 rounded-lg bg-brand-600 px-4 py-2.5 text-center text-sm font-semibold text-white hover:bg-brand-700">Try it free first</a>
              </div>
            ))}
          </div>
          <p className="mt-6 text-center text-sm text-ink-muted">Already had your trial? <a href="/ask-a-tutor/continue" className="font-semibold text-brand-600 hover:underline">Choose a plan here</a>.</p>
        </div>
      </section>

      <section className="mx-auto max-w-3xl px-4 py-16 sm:px-6">
        <h2 className="text-center text-2xl font-bold text-ink">Questions parents ask</h2>
        <div className="mt-8 space-y-3">
          {FAQ.map(([q, a]) => (
            <details key={q} className="card p-5"><summary className="cursor-pointer font-semibold text-ink">{q}</summary><p className="mt-2 text-sm text-ink-muted">{a}</p></details>
          ))}
        </div>
      </section>

      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
        "@context": "https://schema.org", "@type": "FAQPage",
        mainEntity: FAQ.map(([q, a]) => ({ "@type": "Question", name: q, acceptedAnswer: { "@type": "Answer", text: a } })),
      }) }} />
    </div>
  );
}
