"use client";
import Link from "next/link";
import type { ExamInfo, ExamSkill } from "@/lib/examApi";

const COLOURS: Record<ExamSkill["status"], string> = {
  strong: "bg-emerald-500 text-white",
  building: "bg-amber-300 text-amber-950",
  weak: "bg-red-400 text-white",
  untried: "bg-slate-100 text-ink-muted",
};

/** Every skill of an exam, coloured by how the student is doing; each opens its drill. */
export default function ExamSkillMap({ info, skills }: { info: ExamInfo; skills: ExamSkill[] }) {
  return (
    <div className="card p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="font-semibold text-ink">Your {info.name} skills</h2>
        <div className="flex flex-wrap gap-3 text-xs text-ink-muted">
          {(["strong", "building", "weak", "untried"] as const).map((s) => (
            <span key={s} className="inline-flex items-center gap-1.5"><span className={`h-3 w-3 rounded-sm ${COLOURS[s]}`} /> {s === "untried" ? "Not tried yet" : s[0].toUpperCase() + s.slice(1)}</span>
          ))}
        </div>
      </div>
      <p className="mt-1 text-sm text-ink-muted">From your practice tests, diagnostic and drills. Pick any skill to drill it.</p>
      <div className="mt-5 grid gap-5 md:grid-cols-2">
        {Object.keys(info.domains).map((d) => (
          <div key={d}>
            <div className="mb-1.5 text-sm font-medium text-ink">{d}</div>
            <div className="flex flex-wrap gap-1.5">
              {skills.filter((s) => s.domain === d).map((s) => {
                const label = `${s.skill}${s.accuracy !== null ? ` · ${Math.round(s.accuracy * 100)}%` : ""}`;
                const cls = `rounded-lg px-2.5 py-1.5 text-xs font-semibold ${COLOURS[s.status]}`;
                return s.has_drill ? (
                  <Link key={s.slug} href={`/${info.exam}/drills/${s.slug}`} title={s.accuracy === null ? "Not tried yet" : `${s.right} of ${s.total} right`}
                    className={`${cls} transition-transform hover:-translate-y-0.5`}>{label}</Link>
                ) : <span key={s.slug} className={cls}>{label}</span>;
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
