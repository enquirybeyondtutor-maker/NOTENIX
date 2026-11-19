import type { Metadata } from "next";
import { Check, ArrowRight, ClipboardCheck, Camera, BookOpen, LineChart, Mail, TrendingUp } from "lucide-react";
import { Button } from "@/components/ui/Button";

// Notenix Middle School: the KS3 product for US families, Grades 5-7, Common Core Math and ELA.
// Same machinery as /ks3 (free week, parent emails, monthly report); priced in USD ($189/yr).

export const metadata: Metadata = {
  title: "Middle School Math & ELA Practice for Grades 5–7 | Progress Reports for Parents",
  description:
    "Notenix Middle School for Grades 5, 6 and 7: Common Core Math and English Language Arts tests, homework help from Beyond Tutors tutors, grade-level notes and a monthly progress report emailed to parents. Try it free for a week.",
  alternates: { canonical: "https://www.notenix.com/middle-school" },
};

const TRIAL = "/middle-school/trial";
const ENROL = "/middle-school/trial?pay=1";   // the same sign-up, then straight on to payment
const PRICE = "$189";

const FREE_WEEK = [
  { icon: ClipboardCheck, title: "Baseline tests", desc: "Math and English Language Arts, about 30 minutes each, scored instantly." },
  { icon: Camera, title: "Homework help", desc: "Stuck on homework? Send a photo and a Beyond Tutors tutor explains the method." },
  { icon: BookOpen, title: "Grade-level notes", desc: "Short Common Core review notes with worked examples for your child's grade." },
  { icon: LineChart, title: "Your progress report", desc: "Emailed to you on day 7: scores, strong topics and what to work on first." },
];

const PATH = [
  { year: "Grade 5", text: "Decimals, fractions, volume; main idea, inference and figurative language." },
  { year: "Grade 6", text: "Ratios, negative numbers, equations; citing evidence, arguments and roots." },
  { year: "Grade 7", text: "Proportions, percents, rational numbers; theme, text structure and complex sentences." },
  { year: "Every year", text: "Moves up a grade automatically each fall, with every result kept." },
];

const PLAN = [
  "Common Core Math and ELA tests for your child's grade",
  "Instant scoring with a worked explanation for every question",
  "A progress report in your inbox every month",
  "Homework help from Beyond Tutors tutors (up to 30 questions a month)",
  "Review notes for your child's grade",
  "Moves up a grade automatically each fall",
  "Pay once a year, no auto-renewal",
];

const FAQ = [
  ["Who is it for?", "Children in Grades 5, 6 and 7 (about age 10–13). The tests and notes follow the Common Core State Standards for Math and English Language Arts, so they work alongside most US schools and American-curriculum schools abroad."],
  ["What does the free week cost?", "Nothing, and we don't ask for card details. It ends by itself after 7 days. Your child's results are saved if you decide to continue."],
  ["How does homework help work?", "Your child takes a photo of a homework question they're stuck on. A Beyond Tutors tutor replies with the method, step by step, so your child can finish it themselves."],
  ["What's in the monthly report?", "Scores in Math and ELA and how they're changing, the topics your child is strong in, the 3 topics to work on next, and any tests not yet taken."],
  ["How much is it, and how do I pay?", `${PRICE} a year, paid once by bank transfer. There's no subscription that renews by itself.`],
  ["Is it the same as tutoring?", "No. Notenix is practice and progress tracking. If the report shows your child needs more, you can book a free trial class with a Beyond Tutors tutor."],
];

function SampleReport() {
  const subjects = [["Math", 64, "#d97706", "▲ 8"], ["ELA", 79, "#059669", "▲ 3"]] as const;
  return (
    <div className="card mx-auto max-w-md p-6 text-left shadow-xl">
      <div className="flex items-center gap-2 text-sm"><Mail size={15} className="text-brand-600" /><span className="font-semibold text-ink">Ethan&apos;s progress report</span><span className="ml-auto text-xs text-ink-subtle">Sample</span></div>
      <div className="mt-4 space-y-3">
        {subjects.map(([name, pct, color, delta]) => (
          <div key={name} className="flex items-center gap-3 text-sm">
            <span className="w-16 font-medium text-ink">{name}</span>
            <span className="h-2 flex-1 rounded-full bg-slate-100"><span className="block h-2 rounded-full" style={{ width: `${pct}%`, background: color }} /></span>
            <span className="w-16 text-right font-semibold text-ink">{pct}% <span className="text-xs text-emerald-600">{delta}</span></span>
          </div>
        ))}
      </div>
      <p className="mt-5 text-xs font-bold uppercase tracking-wide text-emerald-700">Strong topics</p>
      <p className="text-sm text-ink-muted">Ratios &amp; rates · Inference · Figurative language</p>
      <p className="mt-3 text-xs font-bold uppercase tracking-wide text-red-600">Work on first</p>
      <p className="text-sm text-ink-muted">Dividing fractions · Negative numbers · Pronouns</p>
    </div>
  );
}

export default function MiddleSchoolLanding() {
  return (
    <div>
      <section className="bg-gradient-to-b from-brand-50 to-white">
        <div className="mx-auto grid max-w-6xl items-center gap-12 px-4 py-16 sm:px-6 lg:grid-cols-2 lg:py-24">
          <div>
            <span className="eyebrow">Notenix Middle School · Grades 5, 6 and 7</span>
            <h1 className="mt-3 text-4xl font-bold tracking-tight text-ink sm:text-5xl">Stay ahead in middle school.</h1>
            <p className="mt-5 text-lg text-ink-muted">
              Harder math, longer reading, more independent homework: Grades 5 to 7 are where many kids quietly slip.
              Notenix shows you exactly where your child stands in Math and English Language Arts, helps with homework
              straight away, and tracks progress all year.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Button href={TRIAL} size="lg">Start a free week <ArrowRight size={16} /></Button>
              <Button href="#plans" size="lg" variant="secondary">See the plan</Button>
              <Button href={ENROL} size="lg" variant="secondary">Enrol &amp; pay</Button>
            </div>
            <p className="mt-3 text-sm text-ink-subtle">Free for 7 days · no card · ends by itself</p>
          </div>
          <SampleReport />
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">The free week</span>
          <h2 className="mt-3 text-3xl font-bold tracking-tight text-ink">Know where your child stands in 7 days</h2>
        </div>
        <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {FREE_WEEK.map((f) => (
            <div key={f.title} className="card p-6">
              <span className="grid h-10 w-10 place-items-center rounded-xl bg-brand-50 text-brand-600"><f.icon size={20} /></span>
              <h3 className="mt-4 font-semibold text-ink">{f.title}</h3>
              <p className="mt-1 text-sm text-ink-muted">{f.desc}</p>
            </div>
          ))}
        </div>
        <ol className="mx-auto mt-12 grid max-w-4xl gap-6 text-sm sm:grid-cols-3">
          {["Enter your child's name, grade and your email. Confirm the code we send you.",
            "We give your child a Notenix login. You choose the password.",
            "Your child takes the baseline tests. Your report arrives on day 7."].map((t, i) => (
            <li key={i} className="flex gap-3">
              <span className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-brand-600 text-xs font-bold text-white">{i + 1}</span>
              <span className="text-ink-muted">{t}</span>
            </li>
          ))}
        </ol>
      </section>

      <section className="bg-slate-50">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
          <div className="mx-auto max-w-2xl text-center">
            <span className="eyebrow">Common Core, grade by grade</span>
            <h2 className="mt-3 text-3xl font-bold tracking-tight text-ink">What we check in each grade</h2>
            <p className="mt-3 text-ink-muted">Every test adds to the same record, so you see the trend, not just one score.</p>
          </div>
          <div className="mt-10 grid gap-4 md:grid-cols-4">
            {PATH.map((p, i) => (
              <div key={p.year} className="card relative p-6">
                <div className="flex items-center gap-2 font-semibold text-ink">
                  {i === 3 ? <TrendingUp size={18} className="text-emerald-600" /> : <span className="h-2.5 w-2.5 rounded-full bg-brand-600" />} {p.year}
                </div>
                <p className="mt-2 text-sm text-ink-muted">{p.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="plans" className="mx-auto max-w-5xl scroll-mt-20 px-4 py-16 sm:px-6">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">Plans</span>
          <h2 className="mt-3 text-3xl font-bold tracking-tight text-ink">Start free. Continue for a year.</h2>
        </div>
        <div className="mx-auto mt-10 grid max-w-4xl gap-6 md:grid-cols-2">
          <div className="card flex flex-col p-8">
            <h3 className="text-lg font-semibold text-ink">Free week</h3>
            <div className="mt-2 text-4xl font-bold text-ink">$0</div>
            <p className="mt-1 text-sm text-ink-muted">7 days, no card details.</p>
            <ul className="mt-6 flex-1 space-y-3 text-sm text-ink-muted">
              {["Baseline tests in Math and English Language Arts", "5 homework-help questions", "Review notes for your child's grade", "A progress report on day 7"].map((f) => (
                <li key={f} className="flex items-start gap-2"><Check size={16} className="mt-0.5 shrink-0 text-brand-600" /> {f}</li>
              ))}
            </ul>
            <Button href={TRIAL} variant="secondary" className="mt-8 w-full">Start a free week</Button>
          </div>
          <div className="card flex flex-col border-brand-300 p-8 ring-2 ring-brand-600/20">
            <h3 className="text-lg font-semibold text-ink">Notenix Middle School</h3>
            <div className="mt-2 flex items-baseline gap-1">
              <span className="text-4xl font-bold text-ink">{PRICE}</span>
              <span className="text-sm text-ink-subtle">/ year</span>
            </div>
            <p className="mt-1 text-sm text-ink-muted">Paid once a year by bank transfer. No auto-renewal.</p>
            <ul className="mt-6 flex-1 space-y-3 text-sm text-ink-muted">
              {PLAN.map((f) => (
                <li key={f} className="flex items-start gap-2"><Check size={16} className="mt-0.5 shrink-0 text-brand-600" /> {f}</li>
              ))}
            </ul>
            <Button href={TRIAL} className="mt-8 w-full">Try it free first <ArrowRight size={16} /></Button>
            <Button href={ENROL} variant="secondary" className="mt-3 w-full">Enrol &amp; pay now</Button>
            <a href="/middle-school/continue" className="mt-3 text-center text-sm font-medium text-brand-600 hover:underline">Already had your free week? Continue here</a>
          </div>
        </div>
      </section>

      <section className="bg-slate-50">
        <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6">
          <h2 className="text-center text-2xl font-bold text-ink">Questions parents ask</h2>
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
            <p className="mt-3 text-sm text-ink-subtle">Notenix Middle School is provided with Beyond Tutors.</p>
          </div>
        </div>
      </section>

      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify({
        "@context": "https://schema.org", "@type": "FAQPage",
        mainEntity: FAQ.map(([q, a]) => ({ "@type": "Question", name: q, acceptedAnswer: { "@type": "Answer", text: a } })),
      }) }} />
    </div>
  );
}
