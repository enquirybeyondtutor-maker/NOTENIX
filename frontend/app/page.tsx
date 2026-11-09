import type { Metadata } from "next";
import Link from "next/link";
import {
  ArrowRight,
  ClipboardList,
  Brain,
  BarChart3,
  ShieldCheck,
  Clock,
  Users,
  CheckCircle2,
  Sparkles,
  GraduationCap,
  PenSquare,
  Send,
  UserCheck,
  Globe2,
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { EXAMS } from "@/lib/exams";
import { SITE } from "@/lib/site";

export const metadata: Metadata = {
  alternates: { canonical: SITE },
};

const REQUEST_STEPS = [
  { icon: Send, title: "Request a test", desc: "Pick your exam: SAT, ESAT, TMUA, GCSE, A-Level, HSC, VCE, NCEA and more." },
  { icon: ClipboardList, title: "We send it", desc: "A tutor chooses a full mock that fits and it lands in your account." },
  { icon: GraduationCap, title: "Sit it online", desc: "Timed, exam-style, on any device, from anywhere." },
  { icon: UserCheck, title: "A tutor marks it", desc: "Your score, written feedback and exactly what to work on next." },
];

const STEPS = [
  { n: "01", title: "Get your tests", desc: "Your tutor sets homework and timed tests, or you pick practice for your exam.", icon: ClipboardList },
  { n: "02", title: "Sit them anywhere", desc: "Exam-style, timed, on any device, from wherever you study.", icon: GraduationCap },
  { n: "03", title: "Get marked fast", desc: "Instant marks and grade estimates, with tutor feedback on full mocks.", icon: UserCheck },
  { n: "04", title: "Watch your progress", desc: "See your weak topics, track your scores and know exactly what to revise next.", icon: BarChart3 },
];

const STATS = [
  { value: String(EXAMS.length), label: "Exams covered" },
  { value: "Free", label: "Sample questions" },
  { value: "Tutor", label: "Marked mocks" },
  { value: "Global", label: "Pay from anywhere" },
];

export default function LandingPage() {
  return (
    <div>
      {/* ── Hero ─────────────────────────────────────────────── */}
      <section className="relative overflow-hidden border-b border-line">
        <div className="dotted-grid absolute inset-0 opacity-70" />
        <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-brand-200 to-transparent" />
        <div className="relative mx-auto grid max-w-7xl items-center gap-14 px-4 py-20 sm:px-6 lg:grid-cols-[1.05fr_0.95fr] lg:py-28">
          <div className="animate-slide-up">
            <h1 className="text-4xl font-bold leading-[1.08] tracking-tight text-ink sm:text-5xl lg:text-[3.4rem]">
              <span className="block text-brand-600">Notenix</span>
              Practice tests,<br className="hidden sm:block" /> marked by real tutors.
            </h1>
            <p className="mt-6 max-w-xl text-lg leading-relaxed text-ink-muted">
              Sit timed, exam-style mocks online and get instant marks. Want more? Request a full test
              and our tutors mark it with feedback. For students anywhere in the world.
            </p>
            <div className="mt-8 flex flex-wrap items-center gap-3">
              <Button href="#exams" size="lg">
                Try free questions <ArrowRight size={18} />
              </Button>
              <Button href="/request" variant="secondary" size="lg">
                Request a marked test
              </Button>
            </div>
            <div className="mt-8 flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-ink-muted">
              <span className="inline-flex items-center gap-1.5">
                <CheckCircle2 size={15} className="text-emerald-500" /> Free to start
              </span>
              <span className="inline-flex items-center gap-1.5">
                <CheckCircle2 size={15} className="text-emerald-500" /> No sign-up for samples
              </span>
              <span className="inline-flex items-center gap-1.5">
                <Globe2 size={15} className="text-emerald-500" /> Pay from any country
              </span>
            </div>
          </div>

          {/* Product mockup */}
          <div className="relative animate-fade-in">
            <div className="rounded-2xl border border-line bg-white shadow-xl">
              <div className="flex items-center gap-1.5 border-b border-line px-4 py-3">
                <span className="h-2.5 w-2.5 rounded-full bg-slate-200" />
                <span className="h-2.5 w-2.5 rounded-full bg-slate-200" />
                <span className="h-2.5 w-2.5 rounded-full bg-slate-200" />
                <span className="ml-3 text-xs text-ink-subtle">notenix.com/tests</span>
              </div>
              <div className="p-5">
                <div className="mb-4 flex items-center justify-between">
                  <div>
                    <div className="text-sm font-semibold text-ink">Assigned to you</div>
                    <div className="text-xs text-ink-subtle">3 tests · 1 due soon</div>
                  </div>
                  <span className="badge-brand">Year 11</span>
                </div>
                <div className="space-y-3">
                  {[
                    { t: "Algebra — Quadratics", b: "AQA · 12 Q", tone: "due", meta: "Due tomorrow" },
                    { t: "Cell Biology", b: "Edexcel · 15 Q", tone: "open", meta: "Due Fri" },
                    { t: "Forces & Motion", b: "OCR · 10 Q", tone: "done", meta: "Grade 7" },
                  ].map((row) => (
                    <div key={row.t} className="flex items-center justify-between rounded-xl border border-line px-4 py-3">
                      <div className="flex items-center gap-3">
                        <span className="grid h-9 w-9 place-items-center rounded-lg bg-brand-50 text-brand-600">
                          <ClipboardList size={16} />
                        </span>
                        <div>
                          <div className="text-sm font-medium text-ink">{row.t}</div>
                          <div className="text-xs text-ink-subtle">{row.b}</div>
                        </div>
                      </div>
                      <span className={row.tone === "due" ? "badge-warning" : row.tone === "done" ? "badge-success" : "badge-neutral"}>
                        {row.meta}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <div className="absolute -bottom-5 -left-5 hidden rounded-xl border border-line bg-white px-4 py-3 shadow-lg sm:block">
              <div className="text-xs text-ink-subtle">Class average</div>
              <div className="text-xl font-bold text-brand-600">Grade 6.8</div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Exams ──────────────────────────────────────────── */}
      <section id="exams" className="scroll-mt-20 border-b border-line bg-white">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6">
          <div className="max-w-2xl">
            <span className="eyebrow">Choose your exam</span>
            <h2 className="mt-3 text-3xl font-bold tracking-tight text-ink">Free practice for every major exam</h2>
            <p className="mt-3 text-ink-muted">Each page has free sample questions you can answer right now, with worked solutions.</p>
          </div>
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {EXAMS.map((e) => (
              <Link key={e.slug} href={`/${e.slug}`} className="card card-hover group p-5">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-bold text-ink">{e.name}</h3>
                  <ArrowRight size={16} className="text-ink-subtle transition-transform group-hover:translate-x-0.5 group-hover:text-brand-600" />
                </div>
                <p className="mt-1 text-xs font-medium text-ink-subtle">{e.fullName}</p>
                <p className="mt-3 text-sm text-ink-muted">{e.tagline}</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* ── Request a test ───────────────────────────────────── */}
      <section className="mx-auto max-w-7xl px-4 py-20 sm:px-6">
        <div className="mx-auto max-w-2xl text-center">
          <span className="eyebrow">Tutor-marked tests</span>
          <h2 className="mt-3 text-3xl font-bold tracking-tight text-ink sm:text-4xl">Request a test. We mark it.</h2>
          <p className="mt-4 text-lg text-ink-muted">Real exam conditions and real feedback from experienced tutors, not just a number.</p>
        </div>
        <div className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          {REQUEST_STEPS.map((st, i) => (
            <div key={st.title}>
              <span className="grid h-11 w-11 place-items-center rounded-lg bg-brand-600 text-white"><st.icon size={18} /></span>
              <div className="mt-3 text-xs font-bold text-ink-subtle">0{i + 1}</div>
              <h3 className="mt-1 text-base font-semibold text-ink">{st.title}</h3>
              <p className="mt-1 text-sm leading-relaxed text-ink-muted">{st.desc}</p>
            </div>
          ))}
        </div>
        <div className="mt-10 text-center">
          <Button href="/request" size="lg">Request a test <ArrowRight size={18} /></Button>
        </div>
      </section>

      {/* ── How it works ─────────────────────────────────────── */}
      <section id="how" className="border-y border-line bg-white">
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:py-24">
          <div className="mx-auto max-w-2xl text-center">
            <span className="eyebrow">How it works</span>
            <h2 className="mt-3 text-3xl font-bold tracking-tight text-ink sm:text-4xl">
              From practice to progress in four steps
            </h2>
          </div>
          <div className="mt-14 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
            {STEPS.map((s) => (
              <div key={s.n}>
                <div className="flex items-center gap-3">
                  <span className="grid h-11 w-11 place-items-center rounded-lg bg-brand-600 text-white">
                    <s.icon size={18} />
                  </span>
                  <span className="text-sm font-bold text-ink-subtle">{s.n}</span>
                </div>
                <h3 className="mt-4 text-base font-semibold text-ink">{s.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-ink-muted">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Stats band ───────────────────────────────────────── */}
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6">
        <div className="grid grid-cols-2 gap-6 rounded-2xl border border-line bg-white p-8 sm:grid-cols-4">
          {STATS.map((s) => (
            <div key={s.label} className="text-center">
              <div className="text-2xl font-bold text-ink sm:text-3xl">{s.value}</div>
              <div className="mt-1 text-sm text-ink-muted">{s.label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── CTA ──────────────────────────────────────────────── */}
      <section className="border-t border-line bg-brand-600">
        <div className="mx-auto max-w-4xl px-4 py-16 text-center sm:px-6">
          <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Your next mock, marked by a tutor
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-lg text-brand-100">
            Join Beyond Tutors and get Notenix included, wherever you study: UK, US, India, the Middle East and beyond.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            <Button href="/request" variant="inverse" size="lg">
              Request a test <ArrowRight size={18} />
            </Button>
            <Button href="https://www.thebeyondtutors.com/book" variant="outline-inverse" size="lg">
              Book a free trial class
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
