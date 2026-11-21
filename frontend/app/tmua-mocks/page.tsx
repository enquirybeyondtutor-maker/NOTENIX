import Link from "next/link";
import { ArrowRight, CalendarClock, CheckCircle2, ClipboardList, Gauge, Lock, MessageSquarePlus, Monitor, Trophy } from "lucide-react";
import { Button } from "@/components/ui/Button";
import TmuaSeriesPrice from "@/components/TmuaSeriesPrice";
import { SERIES, SCHEDULE } from "@/lib/tmuaSeries";

// Public page for the Notenix TMUA Mock Series (January 2027). Everything sits behind enrolment
// and payment: /tmua-mocks/enrol creates a locked account that opens once the payment is confirmed.

const ENROL = "/tmua-mocks/enrol";

const FORMAT = [
  { t: "Paper 1 · 75 min", d: "20 questions · Applications of Mathematical Knowledge" },
  { t: "10 min break", d: "then straight on, like the real day" },
  { t: "Paper 2 · 75 min", d: "20 questions · Mathematical Reasoning" },
  { t: "Instant score", d: "then your rank and worked solutions" },
];

const GETS = [
  { icon: Gauge, t: "Baseline Mock, any time", d: "Opens as soon as your place is confirmed. A hard diagnostic that shows your starting score and weakest topics." },
  { icon: ClipboardList, t: "10 full mocks on a schedule", d: "Mock 1 on Wed 25 Nov, then weekends up to Sat 2 Jan. Mocks 1–7 are hard; 8–10 are at real exam level." },
  { icon: Trophy, t: "Rankings and worked solutions", d: "Each mock is ranked for 24 hours from 10:00 UK. After that it stays open as practice." },
  { icon: MessageSquarePlus, t: "Topic sets on request", d: `Stuck on inequalities, logic or calculus? Request a topic and our team sends a targeted set with worked solutions within 48 hours (up to ${SERIES.requestsPerWeek} a week).` },
];

const STEPS = [
  "Enrol: create your Notenix account and pay.",
  "We confirm your payment, usually within a few hours, and email you.",
  "Sign in: the Baseline Mock is waiting in Tests.",
  `Each mock appears in Tests at ${SERIES.opensAt} on its date.`,
];

const TERMS = [
  "Not affiliated with UAT-UK, Pearson VUE or any university. Estimated scores are a guide, not a prediction.",
  "Your account opens only after payment is confirmed. One account per student; sharing logins, questions or solutions ends access without a refund.",
  "Full refund before Mock 1 opens, or within 48 hours of enrolling if you haven't started a mock; none afterwards.",
  "Each mock is ranked within its 24-hour window only. Later attempts are unranked practice.",
  `Topic requests: up to ${SERIES.requestsPerWeek} a week, normally answered within 48 hours. No live classes or tuition are included.`,
  "Use a laptop or desktop with a stable connection. Students under 18 need a parent's consent.",
  "Access ends after the January 2027 test window. You must book your own TMUA by 21 Dec 2026.",
];

const ROW_STYLE = {
  mock: "border-brand-100 bg-brand-50/50",
  deadline: "border-orange-200 bg-orange-50",
  exam: "border-pink-200 bg-pink-50",
} as const;
const TAG_STYLE = {
  mock: "bg-brand-600 text-white",
  deadline: "bg-orange-600 text-white",
  exam: "bg-pink-600 text-white",
} as const;

export default function TmuaMocksPage() {
  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden border-b border-line">
        <div className="dotted-grid absolute inset-0 opacity-70" />
        <div className="relative mx-auto max-w-5xl px-4 py-14 sm:px-6 lg:py-20">
          <nav aria-label="Breadcrumb" className="text-xs text-ink-subtle">
            <Link href="/" className="hover:text-ink">Notenix</Link> <span className="mx-1">/</span> TMUA Mock Series
          </nav>
          <p className="mt-4 text-sm font-semibold uppercase tracking-wider text-brand-600">TMUA Mock Series · {SERIES.sitting}</p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight text-ink sm:text-5xl">
            10 full mocks before your TMUA on <span className="text-brand-600">{SERIES.examWindow}</span>
          </h1>
          <p className="mt-5 max-w-2xl text-lg text-ink-muted">
            Computer-based mocks that feel like the real test: on screen, timed, no calculator. Open to every TMUA candidate.
          </p>
          <div className="mt-6"><TmuaSeriesPrice /></div>
          <div className="mt-6 flex flex-wrap gap-3">
            <Button href={ENROL} size="lg">Enrol now <ArrowRight size={18} /></Button>
            <Button href="#schedule" variant="secondary" size="lg"><CalendarClock size={18} /> See the schedule</Button>
          </div>
          <p className="mt-3 flex items-center gap-1.5 text-sm text-ink-muted">
            <Lock size={14} /> Everything, including the Baseline Mock, opens once you&apos;ve enrolled and your payment is confirmed.
          </p>
          <dl className="mt-10 grid grid-cols-2 gap-3 sm:grid-cols-4">
            {FORMAT.map((f) => (
              <div key={f.t} className="rounded-xl border border-line bg-white px-4 py-3">
                <dt className="text-sm font-semibold text-ink">{f.t}</dt>
                <dd className="mt-1 text-xs text-ink-muted">{f.d}</dd>
              </div>
            ))}
          </dl>
        </div>
      </section>

      {/* What you get */}
      <section className="mx-auto max-w-5xl px-4 py-14 sm:px-6">
        <h2 className="text-2xl font-bold tracking-tight text-ink">What you get</h2>
        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          {GETS.map(({ icon: Icon, t, d }) => (
            <div key={t} className="card p-5">
              <span className="grid h-10 w-10 place-items-center rounded-lg bg-brand-50 text-brand-600"><Icon size={20} /></span>
              <h3 className="mt-3 font-semibold text-ink">{t}</h3>
              <p className="mt-1 text-sm text-ink-muted">{d}</p>
            </div>
          ))}
        </div>
        <div className="mt-6 flex items-start gap-3 rounded-xl border border-line bg-slate-50 p-4 text-sm text-ink-muted">
          <Monitor size={18} className="mt-0.5 shrink-0 text-brand-600" />
          <p>The real TMUA is taken on a computer. Our mocks run in fullscreen with a countdown timer that submits automatically, a question navigator and a review screen, so test day feels familiar.</p>
        </div>
      </section>

      {/* Schedule */}
      <section id="schedule" className="scroll-mt-20 border-y border-line bg-slate-50/60">
        <div className="mx-auto max-w-5xl px-4 py-14 sm:px-6">
          <h2 className="text-2xl font-bold tracking-tight text-ink">Mock schedule</h2>
          <p className="mt-2 text-ink-muted">
            Every mock opens at <b className="text-ink">{SERIES.opensAt}</b> and is ranked for 24 hours. The Baseline Mock is open any time after you enrol.
          </p>
          <ol className="mt-6 space-y-2">
            {SCHEDULE.map((r) => (
              <li key={r.title} className={`grid grid-cols-[4.5rem,1fr] items-center gap-3 rounded-xl border px-4 py-3 sm:grid-cols-[5.5rem,1fr,auto] ${ROW_STYLE[r.kind]}`}>
                <div><p className="font-semibold text-ink">{r.day}</p><p className="text-xs text-ink-muted">{r.date}</p></div>
                <div>
                  <p className="font-medium text-ink">
                    <span className={`mr-2 rounded-full px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider ${TAG_STYLE[r.kind]}`}>{r.kind}</span>
                    {r.title}
                  </p>
                  {r.detail && <p className="mt-0.5 text-xs text-ink-muted">{r.detail}</p>}
                </div>
                {r.kind === "mock" && <p className="col-span-2 text-xs text-ink-muted sm:col-span-1 sm:text-right">Opens {SERIES.opensAt}</p>}
              </li>
            ))}
          </ol>
        </div>
      </section>

      {/* How it works + price */}
      <section className="mx-auto grid max-w-5xl gap-8 px-4 py-14 sm:px-6 md:grid-cols-2">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-ink">How it works</h2>
          <ol className="mt-5 space-y-3">
            {STEPS.map((s, i) => (
              <li key={s} className="flex gap-3 text-ink-muted">
                <span className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-brand-600 text-sm font-bold text-white">{i + 1}</span>
                <span className="pt-0.5">{s}</span>
              </li>
            ))}
          </ol>
        </div>
        <div className="card p-6">
          <p className="text-sm font-semibold text-brand-600">Full Series</p>
          <div className="mt-2"><TmuaSeriesPrice /></div>
          <ul className="mt-4 space-y-2 text-sm text-ink-muted">
            {["Baseline Mock", "10 full mocks (Paper 1 + Paper 2)", "Rankings and worked solutions", `Topic sets on request (up to ${SERIES.requestsPerWeek} a week)`, "Access until the end of the January 2027 test window"].map((x) => (
              <li key={x} className="flex gap-2"><CheckCircle2 size={16} className="mt-0.5 shrink-0 text-emerald-600" />{x}</li>
            ))}
          </ul>
          <Button href={ENROL} size="lg" className="mt-6 w-full">Enrol now <ArrowRight size={18} /></Button>
          <p className="mt-2 text-center text-xs text-ink-muted">Pay by card (Wise) or bank transfer. One price, no single mocks.</p>
        </div>
      </section>

      {/* Terms */}
      <section id="terms" className="scroll-mt-20 border-t border-line">
        <div className="mx-auto max-w-5xl px-4 py-12 sm:px-6">
          <h2 className="text-xl font-bold tracking-tight text-ink">Terms in brief</h2>
          <ul className="mt-4 list-disc space-y-1.5 pl-5 text-sm text-ink-muted">
            {TERMS.map((t) => <li key={t}>{t}</li>)}
          </ul>
          <p className="mt-4 text-sm text-ink-muted">
            Full terms: <Link href="/terms" className="font-medium text-brand-600 hover:underline">notenix.com/terms</Link> ·{" "}
            <Link href="/refunds" className="font-medium text-brand-600 hover:underline">refunds</Link>
          </p>
        </div>
      </section>
    </div>
  );
}
