"use client";
import { useState } from "react";
import Link from "next/link";
import { CheckCircle2, Circle, ChevronDown, ChevronUp, ListChecks } from "lucide-react";
import { SAT_DOMAINS, type SkillStatus, type StudyPlan as Plan } from "@/lib/satApi";
import { formatDate } from "@/lib/utils";

/** This week's tasks with progress, and an outline of the weeks up to the SAT. */
export function StudyPlan({ plan }: { plan: Plan }) {
  const [open, setOpen] = useState(false);
  const done = plan.tasks.filter((t) => t.done).length;
  return (
    <div className="card p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="flex items-center gap-2 font-semibold text-ink"><ListChecks size={18} className="text-brand-600" /> This week</h2>
        <span className="text-sm text-ink-muted">{done} of {plan.tasks.length} done</span>
      </div>
      {plan.tasks.length === 0 ? (
        <p className="mt-3 text-sm text-ink-muted">Take the diagnostic or a practice test so we can plan your week.</p>
      ) : (
        <ul className="mt-4 space-y-2">
          {plan.tasks.map((t) => (
            <li key={t.title}>
              <Link href={t.href} className={`flex items-center justify-between gap-3 rounded-xl border px-4 py-3 transition-colors ${t.done ? "border-emerald-200 bg-emerald-50/60" : "border-line hover:border-brand-200 hover:bg-brand-50/40"}`}>
                <span className="flex items-center gap-3">
                  {t.done ? <CheckCircle2 size={18} className="shrink-0 text-emerald-600" /> : <Circle size={18} className="shrink-0 text-slate-300" />}
                  <span>
                    <span className={`block text-sm font-semibold ${t.done ? "text-emerald-900" : "text-ink"}`}>{t.title}</span>
                    <span className="block text-xs text-ink-subtle">{t.detail}</span>
                  </span>
                </span>
                <span className="text-xs font-semibold tabular-nums text-ink-muted">{t.progress}</span>
              </Link>
            </li>
          ))}
        </ul>
      )}
      {plan.weeks.length > 1 && (
        <>
          <button onClick={() => setOpen(!open)} className="mt-4 inline-flex items-center gap-1 text-sm font-medium text-brand-600 hover:text-brand-700">
            {open ? <ChevronUp size={15} /> : <ChevronDown size={15} />} {open ? "Hide" : "See"} your plan to test day ({plan.weeks.length} weeks)
          </button>
          {open && (
            <ol className="mt-3 space-y-2">
              {plan.weeks.map((w, i) => (
                <li key={w.week_of} className={`rounded-lg border px-4 py-2.5 text-sm ${w.current ? "border-brand-200 bg-brand-50/50" : "border-line"}`}>
                  <span className="font-semibold text-ink">Week {i + 1}</span>
                  <span className="text-ink-subtle"> · from {formatDate(w.week_of)}</span>
                  <div className="mt-0.5 text-ink-muted">{w.items.join(" · ")}</div>
                </li>
              ))}
            </ol>
          )}
        </>
      )}
    </div>
  );
}

const COLOURS: Record<SkillStatus["status"], string> = {
  strong: "bg-emerald-500 text-white",
  building: "bg-amber-300 text-amber-950",
  weak: "bg-red-400 text-white",
  untried: "bg-slate-100 text-ink-muted",
};

/** All 30 SAT skills, coloured by how the student is doing; each opens its drill. */
export function SkillMap({ skills }: { skills: SkillStatus[] }) {
  return (
    <div className="card p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="font-semibold text-ink">Your SAT skills</h2>
        <div className="flex flex-wrap gap-3 text-xs text-ink-muted">
          {(["strong", "building", "weak", "untried"] as const).map((s) => (
            <span key={s} className="inline-flex items-center gap-1.5"><span className={`h-3 w-3 rounded-sm ${COLOURS[s]}`} /> {s === "untried" ? "Not tried yet" : s[0].toUpperCase() + s.slice(1)}</span>
          ))}
        </div>
      </div>
      <p className="mt-1 text-sm text-ink-muted">From your practice tests, diagnostic and drills. Pick any skill to drill it.</p>
      <div className="mt-5 grid gap-6 lg:grid-cols-2">
        {(["rw", "math"] as const).map((sec) => (
          <div key={sec}>
            <h3 className="text-xs font-semibold uppercase tracking-wide text-ink-subtle">{sec === "rw" ? "Reading and Writing" : "Math"}</h3>
            <div className="mt-3 space-y-3">
              {SAT_DOMAINS[sec].map((d) => (
                <div key={d}>
                  <div className="mb-1.5 text-sm font-medium text-ink">{d}</div>
                  <div className="flex flex-wrap gap-1.5">
                    {skills.filter((s) => s.domain === d).map((s) => (
                      <Link key={s.slug} href={`/sat/drills/${s.slug}`}
                        title={s.accuracy === null ? "Not tried yet" : `${s.right} of ${s.total} right`}
                        className={`rounded-lg px-2.5 py-1.5 text-xs font-semibold transition-transform hover:-translate-y-0.5 ${COLOURS[s.status]}`}>
                        {s.skill}{s.accuracy !== null ? ` · ${Math.round(s.accuracy * 100)}%` : ""}
                      </Link>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
