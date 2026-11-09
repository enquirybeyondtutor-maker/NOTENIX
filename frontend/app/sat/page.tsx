import type { Metadata } from "next";
import { BarChart3, Timer, Calculator, Shuffle, Target, BookOpenCheck, ArrowRight, Check } from "lucide-react";
import { EXAM_BY_SLUG } from "@/lib/exams";
import { SITE } from "@/lib/site";
import SampleQuiz from "@/components/SampleQuiz";
import { Button } from "@/components/ui/Button";
import SatPrice from "@/components/sat/SatPrice";

const exam = EXAM_BY_SLUG["sat"];
const url = `${SITE}/sat`;
const title = "Digital SAT Practice Tests with a Free Diagnostic | Notenix SAT";
const description =
  "Free 34-minute SAT diagnostic, then full-length adaptive Digital SAT practice tests with the real module timings, built-in Desmos, a score out of 1600 and worked explanations. Free for 7 days.";

export const metadata: Metadata = {
  title, description,
  keywords: [...exam.keywords, "SAT diagnostic test", "adaptive SAT practice test", "SAT score estimate"],
  alternates: { canonical: url },
  openGraph: { type: "website", url, siteName: "Notenix", title, description },
  twitter: { card: "summary_large_image", title, description },
};

const FEATURES = [
  { icon: Shuffle, title: "Adaptive, like test day", desc: "Two modules per section. How you do in Module 1 decides whether Module 2 is easier or harder, as on the real Digital SAT." },
  { icon: Timer, title: "The real timings", desc: "Reading and Writing: 2 × 32 minutes. Math: 2 × 35 minutes. A 10-minute break between sections." },
  { icon: Calculator, title: "Desmos built in", desc: "The graphing calculator and the reference sheet are on screen for every Math question." },
  { icon: BarChart3, title: "Score out of 1600", desc: "Section scores out of 800, and a breakdown of all eight skill areas the SAT reports." },
  { icon: Target, title: "Your weakest skills", desc: "See exactly which skills cost you the most points, so you know what to practise next." },
  { icon: BookOpenCheck, title: "Every question explained", desc: "Worked explanations for every question, right or wrong, written by our tutors." },
];

const FAQS = [
  { q: "How accurate is the diagnostic?", a: "It is 26 questions across every SAT skill area, so it gives an estimated score band rather than an exact score. A full practice test narrows your estimate down." },
  { q: "Are these official College Board questions?", a: "No. Every Notenix SAT question is original, written by our tutors to match the Digital SAT's style, skills and difficulty. Use the College Board's Bluebook practice tests too." },
  { q: "How is my score worked out?", a: "Your section scores are Notenix estimates on the official 200–800 scale, based on how many questions you get right and which Module 2 you reached. The real SAT uses the College Board's own scoring, so treat ours as a close guide." },
  { q: "What happens after the free week?", a: "Your account stays, with your scores. To keep practising, choose a year of Notenix SAT. Nothing renews by itself." },
  { q: "Can I get help from a tutor?", a: "Yes. Beyond Tutors runs live 1:1 SAT classes, and you can request a tutor review of a practice test." },
];

export default function SatLanding() {
  const jsonLd = {
    "@context": "https://schema.org",
    "@graph": [
      { "@type": "Course", name: "Notenix Digital SAT practice", description, url,
        provider: { "@type": "Organization", name: "Notenix", url: SITE }, educationalLevel: "SAT",
        hasCourseInstance: { "@type": "CourseInstance", courseMode: "online", courseWorkload: "PT2H14M" } },
      { "@type": "FAQPage", mainEntity: FAQS.map((f) => ({ "@type": "Question", name: f.q, acceptedAnswer: { "@type": "Answer", text: f.a } })) },
    ],
  };
  return (
    <div>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      <section className="border-b border-line bg-gradient-to-b from-brand-50/70 to-white">
        <div className="mx-auto grid max-w-6xl gap-10 px-4 py-16 sm:px-6 lg:grid-cols-[1.15fr_0.85fr] lg:items-center">
          <div>
            <span className="eyebrow">Notenix SAT</span>
            <h1 className="mt-3 text-4xl font-bold tracking-tight text-ink sm:text-5xl">Digital SAT practice that feels like test day</h1>
            <p className="mt-4 text-lg text-ink-muted">
              Start with a free 34-minute diagnostic. Get an estimated score out of 1600 and the skills costing you the most points.
              Then practise with full adaptive tests, Desmos and worked explanations.
            </p>
            <div className="mt-7 flex flex-wrap gap-3">
              <Button href="/sat/diagnostic" size="lg">Take the free diagnostic <ArrowRight size={18} /></Button>
              <Button href="/sat/diagnostic" size="lg" variant="secondary">Start a free week</Button>
            </div>
            <p className="mt-3 text-sm text-ink-subtle">No sign-up for the diagnostic · Free for 7 days after · No card needed</p>
          </div>
          <div className="card p-6">
            <div className="text-xs font-semibold uppercase tracking-wide text-ink-subtle">Sample score report</div>
            <div className="mt-3 flex items-end gap-6">
              <div><div className="text-4xl font-bold text-ink">1340</div><div className="text-sm text-ink-muted">out of 1600</div></div>
              <div className="text-sm text-ink-muted"><div>Reading and Writing <b className="text-ink">660</b></div><div>Math <b className="text-ink">680</b></div></div>
            </div>
            <div className="mt-5 space-y-3">
              {[["Algebra", 86], ["Advanced Math", 64], ["Information and Ideas", 78], ["Standard English Conventions", 52]].map(([d, p]) => (
                <div key={d as string}>
                  <div className="mb-1 flex justify-between text-sm"><span className="text-ink">{d}</span><span className="text-ink-subtle">{p}%</span></div>
                  <div className="h-2 rounded-full bg-slate-100"><div className={`h-full rounded-full ${(p as number) >= 75 ? "bg-emerald-500" : (p as number) >= 60 ? "bg-amber-400" : "bg-red-400"}`} style={{ width: `${p}%` }} /></div>
                </div>
              ))}
            </div>
            <div className="mt-4 rounded-lg bg-amber-50 p-3 text-sm text-ink">Work on next: <b>Boundaries</b> and <b>Nonlinear functions</b></div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
        <h2 className="text-2xl font-bold text-ink sm:text-3xl">Built like the real Digital SAT</h2>
        <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((f) => (
            <div key={f.title} className="card p-6">
              <span className="grid h-10 w-10 place-items-center rounded-lg bg-brand-600 text-white"><f.icon size={18} /></span>
              <h3 className="mt-4 font-semibold text-ink">{f.title}</h3>
              <p className="mt-1 text-sm text-ink-muted">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="border-y border-line bg-slate-50/60">
        <div className="mx-auto grid max-w-6xl gap-10 px-4 py-16 sm:px-6 lg:grid-cols-2">
          <div>
            <h2 className="text-2xl font-bold text-ink">Try a few questions now</h2>
            <p className="mt-2 text-ink-muted">Answer each question and check it instantly. Worked solutions included.</p>
            <div className="mt-6"><SampleQuiz examName="SAT" questions={exam.samples} requestHref="/sat/diagnostic" /></div>
          </div>
          <div id="plans" className="lg:pt-14">
            <div className="card p-8">
              <div className="text-sm font-semibold text-brand-700">Notenix SAT · 1 year</div>
              <div className="mt-2"><SatPrice className="text-4xl font-bold text-ink" /> <span className="text-sm text-ink-subtle">/ year</span></div>
              <ul className="mt-6 space-y-2.5 text-sm text-ink-muted">
                {["Full-length adaptive practice tests", "Score out of 1600 after every test", "All eight SAT skill areas tracked",
                  "Worked explanations for every question", "Countdown to your test date", "Free for the first 7 days"]
                  .map((x) => <li key={x} className="flex gap-2"><Check size={16} className="mt-0.5 shrink-0 text-emerald-600" /> {x}</li>)}
              </ul>
              <Button href="/sat/diagnostic" className="mt-8 w-full">Start with the free diagnostic <ArrowRight size={16} /></Button>
              <p className="mt-3 text-center text-xs text-ink-subtle">Pay once by bank transfer from any country. Nothing renews by itself.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-3xl px-4 py-16 sm:px-6">
        <h2 className="text-2xl font-bold text-ink">Questions students ask</h2>
        <div className="mt-6 divide-y divide-line">
          {FAQS.map((f) => (
            <details key={f.q} className="group py-4">
              <summary className="cursor-pointer list-none font-medium text-ink">{f.q}</summary>
              <p className="mt-2 text-sm text-ink-muted">{f.a}</p>
            </details>
          ))}
        </div>
      </section>
    </div>
  );
}
