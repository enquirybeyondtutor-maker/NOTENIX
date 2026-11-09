import type { Metadata } from "next";
import { Check, ArrowRight, ClipboardCheck, Camera, Gauge, LineChart, Mail, Layers, Clock, PenLine } from "lucide-react";
import { Button } from "@/components/ui/Button";
import LocalPrice from "@/components/LocalPrice";

export const metadata: Metadata = {
  title: "Starting a Kent Grammar School in Sept 2027? Get Grammar-Ready for Year 7",
  description:
    "Passed the Kent Test? Notenix KS3 checks your child against grammar-school Year 7 expectations in Maths, Science and English, closes Year 6 gaps before September, and emails you a progress report every month. Free for a week.",
  alternates: { canonical: "https://www.notenix.com/kent-grammar" },
};

const TRIAL = "/ks3/trial?year=6&src=kent-grammar";

const WORRIES = [
  { icon: Layers, title: "Top of the class to the middle", desc: "Every child in the room passed the 11+. Being 'bright' at primary is now the starting line." },
  { icon: Gauge, title: "Setting can happen early", desc: "Many grammar schools set Maths, and sometimes Science, after early Year 7 assessments." },
  { icon: Clock, title: "Faster pace, more homework", desc: "Lessons move quickly and independent homework starts from week one." },
  { icon: PenLine, title: "Gaps the 11+ didn't cover", desc: "11+ prep drilled reasoning. Fractions, algebra basics and written English often got squeezed." },
];

const WHAT = [
  { icon: ClipboardCheck, title: "Grammar-ready baseline", desc: "Year 7 Maths, Science and English tests, marked instantly with worked explanations." },
  { icon: Gauge, title: "Grammar-level benchmark", desc: "Each subject compared with a grammar-school Year 7 bar, not the national average." },
  { icon: Camera, title: "Homework help", desc: "Stuck on Year 7 homework? Send a photo, a Beyond Tutors tutor explains the method." },
  { icon: LineChart, title: "Monthly parent report", desc: "Scores, strong topics and the 3 topics to fix next, in your inbox every month." },
];

const TIMELINE = [
  { when: "Now – Feb 2027", text: "Free week: baseline tests and a report showing where your child stands for Year 7." },
  { when: "Mar – Aug 2027", text: "After offers: close the Year 6 gaps and get comfortable with Year 7 work over the summer." },
  { when: "Sept 2027", text: "Year 7 starts. A timed test every half-term, so you see slipping before school reports do." },
  { when: "Year 8 → GCSE", text: "Moves up automatically each September, with every result kept on one progress line." },
];

const PLAN = [
  "Year 7 tests in Maths, Science and English, every half-term",
  "Grammar-level benchmark in every report",
  "Monthly progress report emailed to you",
  "Homework help from Beyond Tutors tutors (up to 30 questions a month)",
  "Year 7 notes with worked examples",
  "Stays on Year 7 work through September, then moves up each year",
  "Pay once a year, no auto-renewal",
];

const FAQ = [
  ["My child is in Year 6. Is it too early?", "No. Choose 'Year 6 (starting Year 7 in September)' when you sign up. Your child works on Year 7 material now and stays on Year 7 when they start secondary, so nothing is skipped."],
  ["We haven't had our school offer yet. Should we wait?", "The Kent Test result tells you your child was assessed suitable for grammar school. Offers come on National Offer Day (1 March 2027). The free week is useful either way: the Year 7 baseline shows gaps from primary whichever school your child goes to."],
  ["Is this more 11+ tutoring?", "No. The 11+ is done. Notenix is short, regular Year 7 practice and tracking, about 20–30 minutes a test, so your child starts secondary confident instead of catching up."],
  ["What is the grammar-level benchmark?", "We compare each subject with a higher bar (75%+) than the national average, because grammar classes move faster. The report shows 'Grammar-ready' or how many points to go."],
  ["Are you linked to Kent County Council or any school?", "No. Notenix is an independent practice platform from Beyond Tutors. It follows the National Curriculum for Year 7, which all Kent grammar schools teach."],
  ["What does the free week cost?", "Nothing, and no card details. It ends by itself after 7 days and your child's results are kept if you continue."],
];

function SampleReport() {
  const rows = [["Maths", 68, "7 points to go"], ["Science", 79, "Grammar-ready"], ["English", 72, "3 points to go"]] as const;
  return (
    <div className="card mx-auto max-w-md p-6 text-left shadow-xl">
      <div className="flex items-center gap-2 text-sm"><Mail size={15} className="text-brand-600" /><span className="font-semibold text-ink">Oliver&apos;s grammar-ready report</span><span className="ml-auto text-xs text-ink-subtle">Sample</span></div>
      <div className="mt-4 space-y-3">
        {rows.map(([name, pct, label]) => {
          const ok = pct >= 75;
          return (
            <div key={name} className="flex items-center gap-3 text-sm">
              <span className="w-16 font-medium text-ink">{name}</span>
              <span className="relative h-2 flex-1 rounded-full bg-slate-100">
                <span className="block h-2 rounded-full" style={{ width: `${pct}%`, background: ok ? "#059669" : "#d97706" }} />
                <span className="absolute -top-1 h-4 w-0.5 bg-ink" style={{ left: "75%" }} />
              </span>
              <span className={`w-28 text-right text-xs font-semibold ${ok ? "text-emerald-700" : "text-amber-700"}`}>{pct}% · {label}</span>
            </div>
          );
        })}
      </div>
      <p className="mt-2 text-xs text-ink-subtle">Line = grammar-school Year 7 bar (75%)</p>
      <p className="mt-4 text-xs font-bold uppercase tracking-wide text-red-600">Fix before September</p>
      <p className="text-sm text-ink-muted">Fractions of amounts · Negative numbers · Paragraph structure</p>
    </div>
  );
}

export default function KentGrammarLanding() {
  return (
    <div>
      <section className="bg-gradient-to-b from-brand-50 to-white">
        <div className="mx-auto grid max-w-6xl items-center gap-12 px-4 py-16 sm:px-6 lg:grid-cols-2 lg:py-24">
          <div>
            <span className="eyebrow">For children starting Kent grammar schools · Sept 2027</span>
            <h1 className="mt-3 text-4xl font-bold tracking-tight text-ink sm:text-5xl">They passed the 11+. Now start Year 7 confident, not catching up.</h1>
            <p className="mt-5 text-lg text-ink-muted">
              Grammar school moves faster, and every classmate passed the same test. Notenix checks your child against
              grammar-level Year 7 expectations, closes the Year 6 gaps before September, and keeps you posted every month.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Button href={TRIAL} size="lg">Start a free week <ArrowRight size={16} /></Button>
              <Button href="#plans" size="lg" variant="secondary">See the plan</Button>
            </div>
            <p className="mt-3 text-sm text-ink-subtle">Free for 7 days · no card · ends by itself</p>
          </div>
          <SampleReport />
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">What changes in Year 7</span>
          <h2 className="mt-3 text-3xl font-bold tracking-tight text-ink">What grammar-school parents tell us they worry about</h2>
        </div>
        <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {WORRIES.map((f) => (
            <div key={f.title} className="card p-6">
              <span className="grid h-10 w-10 place-items-center rounded-xl bg-amber-50 text-amber-600"><f.icon size={20} /></span>
              <h3 className="mt-4 font-semibold text-ink">{f.title}</h3>
              <p className="mt-1 text-sm text-ink-muted">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-slate-50">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
          <div className="mx-auto max-w-2xl text-center">
            <span className="eyebrow">What you get</span>
            <h2 className="mt-3 text-3xl font-bold tracking-tight text-ink">Know where your child stands for grammar Year 7</h2>
          </div>
          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {WHAT.map((f) => (
              <div key={f.title} className="card p-6">
                <span className="grid h-10 w-10 place-items-center rounded-xl bg-brand-50 text-brand-600"><f.icon size={20} /></span>
                <h3 className="mt-4 font-semibold text-ink">{f.title}</h3>
                <p className="mt-1 text-sm text-ink-muted">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">The year ahead</span>
          <h2 className="mt-3 text-3xl font-bold tracking-tight text-ink">From Year 6 to a strong first term</h2>
        </div>
        <div className="mt-10 grid gap-4 md:grid-cols-4">
          {TIMELINE.map((p) => (
            <div key={p.when} className="card p-6">
              <div className="flex items-center gap-2 font-semibold text-ink"><span className="h-2.5 w-2.5 rounded-full bg-brand-600" /> {p.when}</div>
              <p className="mt-2 text-sm text-ink-muted">{p.text}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="plans" className="bg-slate-50 scroll-mt-20">
        <div className="mx-auto max-w-5xl px-4 py-16 sm:px-6">
          <div className="mx-auto max-w-2xl text-center">
            <span className="eyebrow">Plans</span>
            <h2 className="mt-3 text-3xl font-bold tracking-tight text-ink">Start free. Continue for a year.</h2>
          </div>
          <div className="mx-auto mt-10 grid max-w-4xl gap-6 md:grid-cols-2">
            <div className="card flex flex-col p-8">
              <h3 className="text-lg font-semibold text-ink">Free week</h3>
              <div className="mt-2 text-4xl font-bold text-ink">£0</div>
              <p className="mt-1 text-sm text-ink-muted">7 days, no card details.</p>
              <ul className="mt-6 flex-1 space-y-3 text-sm text-ink-muted">
                {["Year 7 baseline in Maths, Science and English", "Grammar-ready report on day 7", "5 homework-help questions", "Year 7 notes"].map((f) => (
                  <li key={f} className="flex items-start gap-2"><Check size={16} className="mt-0.5 shrink-0 text-brand-600" /> {f}</li>
                ))}
              </ul>
              <Button href={TRIAL} variant="secondary" className="mt-8 w-full">Start a free week</Button>
            </div>
            <div className="card flex flex-col border-brand-300 p-8 ring-2 ring-brand-600/20">
              <h3 className="text-lg font-semibold text-ink">Notenix KS3</h3>
              <div className="mt-2 flex items-baseline gap-1">
                <LocalPrice gbp={149} className="text-4xl font-bold text-ink" subClassName="text-sm text-ink-subtle" />
                <span className="text-sm text-ink-subtle">/ year</span>
              </div>
              <p className="mt-1 text-sm text-ink-muted">Covers the summer before Year 7 and the whole first year.</p>
              <ul className="mt-6 flex-1 space-y-3 text-sm text-ink-muted">
                {PLAN.map((f) => (
                  <li key={f} className="flex items-start gap-2"><Check size={16} className="mt-0.5 shrink-0 text-brand-600" /> {f}</li>
                ))}
              </ul>
              <Button href={TRIAL} className="mt-8 w-full">Try it free first <ArrowRight size={16} /></Button>
              <a href="/ks3/continue" className="mt-3 text-center text-sm font-medium text-brand-600 hover:underline">Already had your free week? Continue here</a>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-3xl px-4 py-16 sm:px-6">
        <h2 className="text-center text-2xl font-bold text-ink">Questions Kent parents ask</h2>
        <div className="mt-8 space-y-3">
          {FAQ.map(([q, a]) => (
            <details key={q} className="card group p-5">
              <summary className="cursor-pointer list-none font-semibold text-ink">{q}</summary>
              <p className="mt-2 text-sm text-ink-muted">{a}</p>
            </details>
          ))}
        </div>
        <div className="mt-12 text-center">
          <Button href={TRIAL} size="lg">Start a free week <ArrowRight size={16} /></Button>
          <p className="mt-3 text-sm text-ink-subtle">Notenix is independent and not affiliated with Kent County Council, the Kent Test or any school.</p>
        </div>
      </section>

      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
        "@context": "https://schema.org", "@type": "FAQPage",
        mainEntity: FAQ.map(([q, a]) => ({ "@type": "Question", name: q, acceptedAnswer: { "@type": "Answer", text: a } })),
      }) }} />
    </div>
  );
}
