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
} from "lucide-react";
import { Button } from "@/components/ui/Button";

const BOARDS = ["AQA", "Edexcel", "OCR", "Cambridge", "WJEC", "CCEA"];

const FEATURES = [
  { icon: PenSquare, title: "Build tests in minutes", desc: "Assemble board-aligned assessments by hand or let Claude AI draft questions from any topic and specification." },
  { icon: Users, title: "Assign to classes", desc: "Push a test to a whole class or individual students with a deadline. Everyone sees exactly what's due." },
  { icon: ShieldCheck, title: "Controlled conditions", desc: "Timed sittings, single-attempt locks and randomised order keep assessments fair and exam-realistic." },
  { icon: Brain, title: "Automatic marking", desc: "Responses are graded the moment a student submits, with a GCSE 1–9 or A-Level A*–E estimate." },
  { icon: BarChart3, title: "Mastery analytics", desc: "See cohort and per-student breakdowns by topic — spot the weak areas before the real exam does." },
  { icon: Clock, title: "Save hours every week", desc: "No more writing papers or marking by hand. Reclaim the time and give students faster feedback." },
];

const STEPS = [
  { n: "01", title: "Create or generate", desc: "A teacher builds a test from scratch or generates questions with AI, aligned to the board and topic.", icon: PenSquare },
  { n: "02", title: "Assign to students", desc: "Set a deadline and assign to a class. Students see the test appear in their portal instantly.", icon: ClipboardList },
  { n: "03", title: "Students attempt", desc: "Learners sit the test under controlled conditions, on any device, within the window.", icon: GraduationCap },
  { n: "04", title: "Track mastery", desc: "AI grades on submit. Teachers get cohort analytics; students get personalised feedback.", icon: BarChart3 },
];

const STATS = [
  { value: "11", label: "Subjects" },
  { value: "6", label: "Exam boards" },
  { value: "1–9 / A*–E", label: "Grade estimates" },
  { value: "AI", label: "Auto-marked" },
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
            <span className="badge-brand">
              <Sparkles size={13} /> AI-powered assessment · GCSE &amp; A-Level
            </span>
            <h1 className="mt-6 text-4xl font-bold leading-[1.08] tracking-tight text-ink sm:text-5xl lg:text-[3.4rem]">
              Assessment that runs<br className="hidden sm:block" /> itself, end to end.
            </h1>
            <p className="mt-6 max-w-xl text-lg leading-relaxed text-ink-muted">
              Notenix lets teachers create board-aligned tests, assign them to students, and track
              mastery — while AI handles the marking. One portal for setting, sitting and scoring.
            </p>
            <div className="mt-8 flex flex-wrap items-center gap-3">
              <Button href="/register" size="lg">
                Get started free <ArrowRight size={18} />
              </Button>
              <Button href="/pricing" variant="secondary" size="lg">
                Book a demo
              </Button>
            </div>
            <div className="mt-8 flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-ink-muted">
              <span className="inline-flex items-center gap-1.5">
                <CheckCircle2 size={15} className="text-emerald-500" /> Free for individual students
              </span>
              <span className="inline-flex items-center gap-1.5">
                <CheckCircle2 size={15} className="text-emerald-500" /> No card required
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

      {/* ── Board trust bar ──────────────────────────────────── */}
      <section className="border-b border-line bg-white">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-center gap-x-6 gap-y-3 px-4 py-6 sm:px-6">
          <span className="text-sm font-medium text-ink-subtle">Aligned to every major exam board</span>
          {BOARDS.map((b) => (
            <span key={b} className="text-sm font-semibold text-ink-muted">{b}</span>
          ))}
        </div>
      </section>

      {/* ── Features ─────────────────────────────────────────── */}
      <section id="features" className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:py-24">
        <div className="max-w-2xl">
          <span className="eyebrow">Platform</span>
          <h2 className="mt-3 text-3xl font-bold tracking-tight text-ink sm:text-4xl">
            Everything a department needs to assess
          </h2>
          <p className="mt-4 text-lg text-ink-muted">
            From setting the paper to reading the analytics — Notenix replaces a stack of tools with
            one coherent workflow.
          </p>
        </div>
        <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map((f) => (
            <div key={f.title} className="card card-hover p-6">
              <span className="grid h-11 w-11 place-items-center rounded-lg bg-brand-50 text-brand-600">
                <f.icon size={20} />
              </span>
              <h3 className="mt-4 text-base font-semibold text-ink">{f.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-ink-muted">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── How it works ─────────────────────────────────────── */}
      <section id="how" className="border-y border-line bg-white">
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:py-24">
          <div className="mx-auto max-w-2xl text-center">
            <span className="eyebrow">How it works</span>
            <h2 className="mt-3 text-3xl font-bold tracking-tight text-ink sm:text-4xl">
              Set, sit and score in four steps
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

      {/* ── Audience split ───────────────────────────────────── */}
      <section className="mx-auto max-w-7xl px-4 pb-20 sm:px-6">
        <div className="grid gap-6 lg:grid-cols-2">
          <div className="card p-8">
            <span className="grid h-11 w-11 place-items-center rounded-lg bg-brand-50 text-brand-600">
              <PenSquare size={20} />
            </span>
            <h3 className="mt-4 text-xl font-bold text-ink">For teachers</h3>
            <p className="mt-2 text-ink-muted">Build once, assign to every class, and let the marking take care of itself.</p>
            <ul className="mt-5 space-y-2.5">
              {["AI question generation", "Class & student assignment", "Cohort mastery analytics", "Deadline & attempt controls"].map((x) => (
                <li key={x} className="flex items-center gap-2 text-sm text-ink-muted">
                  <CheckCircle2 size={16} className="text-brand-600" /> {x}
                </li>
              ))}
            </ul>
            <Button href="/register" variant="secondary" className="mt-6">Create a teacher account</Button>
          </div>
          <div className="card p-8">
            <span className="grid h-11 w-11 place-items-center rounded-lg bg-emerald-50 text-emerald-600">
              <GraduationCap size={20} />
            </span>
            <h3 className="mt-4 text-xl font-bold text-ink">For students</h3>
            <p className="mt-2 text-ink-muted">See what's due, sit it anywhere, and get feedback that actually moves your grade.</p>
            <ul className="mt-5 space-y-2.5">
              {["One place for all assigned tests", "Instant grade estimates", "Topic-by-topic feedback", "Progress you can watch climb"].map((x) => (
                <li key={x} className="flex items-center gap-2 text-sm text-ink-muted">
                  <CheckCircle2 size={16} className="text-emerald-600" /> {x}
                </li>
              ))}
            </ul>
            <Button href="/register" variant="secondary" className="mt-6">Start as a student</Button>
          </div>
        </div>
      </section>

      {/* ── CTA ──────────────────────────────────────────────── */}
      <section className="border-t border-line bg-brand-600">
        <div className="mx-auto max-w-4xl px-4 py-16 text-center sm:px-6">
          <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Bring your assessments into one place
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-lg text-brand-100">
            Join teachers and students across the UK using Notenix to set, sit and score smarter.
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            <Button href="/register" variant="inverse" size="lg">
              Get started free <ArrowRight size={18} />
            </Button>
            <Button href="/login" variant="outline-inverse" size="lg">
              Sign in
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}
