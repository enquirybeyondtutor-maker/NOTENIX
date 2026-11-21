import Link from "next/link";
import { AlarmClock, ArrowRight, CalendarDays, CheckCircle2, ClipboardList, Gauge, Lock, MessageSquarePlus, Monitor, Trophy } from "lucide-react";
import { Button } from "@/components/ui/Button";
import FactValue from "@/components/FactValue";
import TmuaSeriesPrice from "@/components/TmuaSeriesPrice";
import { SERIES, SCHEDULE } from "@/lib/tmuaSeries";

// Public page for the Notenix TMUA Mock Series (January 2027). Everything sits behind enrolment
// and payment: /tmua-mocks/enrol creates a locked account that opens once the payment is confirmed.

const ENROL = "/tmua-mocks/enrol";

const FACTS = [
  { label: "Mocks", value: "10 + a Baseline Mock" },
  { label: "Each mock", value: "2 papers · 75 min each" },
  { label: "First mock", value: "Wed 25 Nov · 10 a.m. UK" },
  { label: "Your TMUA", value: "4–8 January 2027" },
];

const GETS = [
  { icon: Gauge, t: "Baseline Mock, any time", d: "Opens as soon as your place is confirmed. A hard diagnostic that shows your starting score and weakest topics." },
  { icon: ClipboardList, t: "10 full mocks", d: "From Wed 25 Nov, then every weekend until Sat 2 Jan. Mocks 1–7 are hard; 8–10 are at real exam level." },
  { icon: Trophy, t: "Rankings and worked solutions", d: "Instant score when you submit, then your rank and full solutions. Each mock is ranked for 24 hours." },
  { icon: MessageSquarePlus, t: "Topic sets on request", d: `Stuck on inequalities, logic or calculus? Ask for a topic and our team sends a set with worked solutions within 48 hours (up to ${SERIES.requestsPerWeek} a week).` },
];

const STEPS = [
  { t: "Enrol and pay", d: "Create your Notenix account and pay by card or bank transfer." },
  { t: "We confirm", d: "Usually within a few hours. We email you when your account is open." },
  { t: "Take the Baseline Mock", d: "It's waiting in Tests the moment you sign in." },
  { t: "Sit each mock", d: `Each one appears in Tests at ${SERIES.opensAt} on its date.` },
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

const MONTHS = [
  { name: "November", match: "Nov" },
  { name: "December", match: "Dec" },
  { name: "January", match: "Jan" },
];

export default function TmuaMocksPage() {
  const mocks = SCHEDULE.filter((r) => r.kind === "mock");
  const keyDates = SCHEDULE.filter((r) => r.kind !== "mock");
  return (
    <div>
      {/* Hero */}
      <section className="relative overflow-hidden border-b border-line">
        <div className="dotted-grid absolute inset-0 opacity-70" />
        <div className="relative mx-auto max-w-5xl px-4 py-14 sm:px-6 lg:py-20">
          <nav aria-label="Breadcrumb" className="text-xs text-ink-subtle">
            <Link href="/" className="hover:text-ink">Notenix</Link> <span className="mx-1">/</span>{" "}
            <Link href="/tmua" className="hover:text-ink">TMUA</Link> <span className="mx-1">/</span> Mock Series
          </nav>
          <p className="mt-5 text-xs font-semibold uppercase tracking-[0.14em] text-brand-600">TMUA Mock Series · {SERIES.sitting} sitting</p>
          <h1 className="mt-3 text-3xl font-bold tracking-tight text-ink sm:text-5xl">
            TMUA mocks that feel like <span className="whitespace-nowrap text-brand-600 sm:block">the real test</span>
          </h1>
          <p className="mt-5 max-w-2xl text-lg text-ink-muted">
            10 full computer-based mocks before your TMUA: on screen, timed, no calculator. With a Baseline Mock, rankings,
            worked solutions and topic sets on request.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Button href={ENROL} size="lg">Enrol now <ArrowRight size={18} /></Button>
            <Button href="#schedule" variant="secondary" size="lg">See the schedule</Button>
          </div>
          <p className="mt-3 text-sm text-ink-muted"><TmuaSeriesPrice variant="line" /> · open to every TMUA candidate</p>
          <dl className="mt-10 grid grid-cols-2 gap-3 sm:grid-cols-4">
            {FACTS.map((f) => (
              <div key={f.label} className="rounded-xl border border-line bg-white px-4 py-3">
                <dt className="text-xs font-medium text-ink-subtle">{f.label}</dt>
                <dd className="mt-1 text-sm font-semibold text-ink"><FactValue value={f.value} /></dd>
              </div>
            ))}
          </dl>
        </div>
      </section>

      {/* What you get */}
      <section className="mx-auto max-w-5xl px-4 py-16 sm:px-6">
        <h2 className="text-2xl font-bold tracking-tight text-ink sm:text-3xl">Everything in the series</h2>
        <p className="mt-2 max-w-2xl text-ink-muted">One payment covers it all, until the end of the January 2027 test window.</p>
        <div className="mt-8 grid gap-4 sm:grid-cols-2">
          {GETS.map(({ icon: Icon, t, d }) => (
            <div key={t} className="card flex gap-4 p-5">
              <span className="grid h-10 w-10 shrink-0 place-items-center rounded-lg bg-brand-50 text-brand-600"><Icon size={20} /></span>
              <div>
                <h3 className="font-semibold text-ink">{t}</h3>
                <p className="mt-1 text-sm text-ink-muted">{d}</p>
              </div>
            </div>
          ))}
        </div>
        <div className="mt-4 flex items-start gap-3 rounded-xl border border-line bg-slate-50 p-4 text-sm text-ink-muted">
          <Monitor size={18} className="mt-0.5 shrink-0 text-brand-600" />
          <p>The real TMUA is sat on a computer. Our mocks run fullscreen with a countdown timer that submits automatically, a question navigator and a review screen, so the day itself feels familiar.</p>
        </div>
      </section>

      {/* Schedule */}
      <section id="schedule" className="scroll-mt-20 border-y border-line bg-slate-50/60">
        <div className="mx-auto max-w-5xl px-4 py-16 sm:px-6">
          <h2 className="text-2xl font-bold tracking-tight text-ink sm:text-3xl">Mock schedule</h2>
          <p className="mt-2 max-w-2xl text-ink-muted">
            Every mock opens at <b className="font-semibold text-ink">{SERIES.opensAt}</b> and is ranked for 24 hours, then stays open as practice.
            The Baseline Mock is open any time after you enrol.
          </p>

          <div className="mt-8 space-y-8">
            {MONTHS.map((m) => {
              const rows = mocks.filter((r) => r.date.endsWith(m.match));
              if (!rows.length) return null;
              return (
                <div key={m.name}>
                  <h3 className="text-xs font-semibold uppercase tracking-[0.14em] text-ink-subtle">{m.name}</h3>
                  <div className="mt-3 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                    {rows.map((r) => (
                      <div key={r.title} className="rounded-xl border border-line bg-white p-4">
                        <div className="flex items-center justify-between gap-2">
                          <p className="font-semibold text-ink">{r.title.replace(" · Final mock", "")}</p>
                          <span className={`rounded-full px-2 py-0.5 text-[11px] font-semibold ${r.detail?.startsWith("Real") ? "bg-emerald-50 text-emerald-700" : "bg-brand-50 text-brand-700"}`}>
                            {r.detail?.includes("Real") ? "Exam level" : "Hard"}
                          </span>
                        </div>
                        <p className="mt-2 flex items-center gap-1.5 text-sm text-ink-muted"><CalendarDays size={14} /> {r.day} {r.date} · 10 a.m. UK time</p>
                        {(r.title.includes("Final") || r.detail?.includes("Launch")) && (
                          <p className="mt-1 text-xs font-medium text-brand-600">{r.title.includes("Final") ? "Final mock" : "Launch mock"}</p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>

          <h3 className="mt-10 text-xs font-semibold uppercase tracking-[0.14em] text-ink-subtle">Key dates</h3>
          <div className="mt-3 grid gap-3 sm:grid-cols-3">
            {keyDates.map((r) => (
              <div key={r.title} className={`rounded-xl border p-4 ${r.kind === "exam" ? "border-brand-200 bg-brand-50" : "border-orange-200 bg-orange-50"}`}>
                <p className={`flex items-center gap-1.5 text-sm font-semibold ${r.kind === "exam" ? "text-brand-700" : "text-orange-700"}`}>
                  <AlarmClock size={14} /> {r.day} {r.date}
                </p>
                <p className="mt-1 text-sm text-ink">{r.kind === "exam" ? "Your TMUA: 4–8 January 2027" : r.title.replace("UAT-UK deadline: ", "")}</p>
                {r.kind === "deadline" && <p className="mt-0.5 text-xs text-ink-muted">{r.title.startsWith("UAT-UK") ? "UAT-UK deadline" : "Book your test before this"}</p>}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works + price */}
      <section className="mx-auto grid max-w-5xl gap-10 px-4 py-16 sm:px-6 md:grid-cols-[1fr,22rem]">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-ink sm:text-3xl">How it works</h2>
          <ol className="mt-6 space-y-5">
            {STEPS.map((s, i) => (
              <li key={s.t} className="flex gap-4">
                <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-brand-600 text-sm font-bold text-white">{i + 1}</span>
                <div>
                  <p className="font-semibold text-ink">{s.t}</p>
                  <p className="text-sm text-ink-muted">{s.d}</p>
                </div>
              </li>
            ))}
          </ol>
        </div>
        <div className="card self-start p-6">
          <p className="text-sm font-semibold text-brand-600">TMUA Mock Series</p>
          <div className="mt-3"><TmuaSeriesPrice variant="card" /></div>
          <ul className="mt-5 space-y-2 text-sm text-ink-muted">
            {["Baseline Mock", "10 full mocks (Paper 1 + Paper 2)", "Rankings and worked solutions", `Topic sets on request (up to ${SERIES.requestsPerWeek} a week)`, "Access until the end of the test window"].map((x) => (
              <li key={x} className="flex gap-2"><CheckCircle2 size={16} className="mt-0.5 shrink-0 text-emerald-600" />{x}</li>
            ))}
          </ul>
          <Button href={ENROL} size="lg" className="mt-6 w-full">Enrol now <ArrowRight size={18} /></Button>
          <p className="mt-3 flex items-center justify-center gap-1.5 text-xs text-ink-muted"><Lock size={12} /> Opens once your payment is confirmed</p>
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
