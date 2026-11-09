"use client";
import { Target } from "lucide-react";
import { ReviewList } from "@/components/sat/Report";
import { fmt, type ExamInfo, type ExamReport as Report } from "@/lib/examApi";

/** Exam-engine score report (e.g. TMUA): overall and per-paper estimates on the exam's
 *  scale (or bands, for a diagnostic), weakest skills, skills by area, and the review. */
export default function ExamReport({ info, r, target, note }: {
  info: ExamInfo; r: Report; target?: number | null; note?: React.ReactNode;
}) {
  const max = fmt(info.scale.max, info);
  const show = (score: number, band?: [number, number]) => (band ? `${fmt(band[0], info)}–${fmt(band[1], info)}` : fmt(score, info));
  const sections = Object.entries(r.sections);
  return (
    <div className="space-y-8">
      <div className="card overflow-hidden">
        <div className={`grid gap-px bg-line ${sections.length >= 2 ? "sm:grid-cols-3" : "sm:grid-cols-2"}`}>
          <div className="bg-gradient-to-br from-brand-600 to-brand-700 p-6 text-white">
            <div className="text-xs font-semibold uppercase tracking-wide text-white/70">{r.band ? "Estimated score band" : "Estimated overall score"}</div>
            <div className="mt-1 text-4xl font-bold tabular-nums">{show(r.score, r.band)}</div>
            <div className="text-sm text-white/70">out of {max} · {r.right} of {r.total} right</div>
            {target ? (
              <div className="mt-3 inline-flex items-center gap-1.5 rounded-full bg-white/15 px-2.5 py-1 text-xs font-semibold">
                <Target size={12} /> Target {fmt(target, info)}: {r.score >= target ? "you're there" : `${fmt(target - r.score, info)} to go`}
              </div>
            ) : null}
          </div>
          {sections.map(([key, s]) => (
            <div key={key} className="bg-white p-6">
              <div className="text-xs font-semibold uppercase tracking-wide text-ink-subtle">{info.sections[key] ?? key}</div>
              <div className="mt-1 text-3xl font-bold tabular-nums text-ink">{show(s.score, s.band)}</div>
              <div className="text-sm text-ink-muted">out of {max} · {s.right} of {s.total} right</div>
            </div>
          ))}
        </div>
        <div className="border-t border-line bg-slate-50 px-6 py-3 text-xs text-ink-muted">{note ?? info.about_score}</div>
      </div>

      {r.weakest.length > 0 && (
        <div className="card p-6">
          <h2 className="font-semibold text-ink">Where your marks are going</h2>
          <p className="mt-1 text-sm text-ink-muted">The skills that cost you the most questions. Start your practice here.</p>
          <div className="mt-4 grid gap-3 sm:grid-cols-3">
            {r.weakest.map((w) => (
              <div key={w.skill} className="rounded-xl border border-amber-200 bg-amber-50 p-4">
                <div className="text-xs font-semibold text-amber-800">{w.domain}</div>
                <div className="mt-0.5 font-semibold text-ink">{w.skill}</div>
                <div className="mt-1 text-sm text-ink-muted">{w.right} of {w.total} right</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="card p-6">
        <h2 className="font-semibold text-ink">Your skills</h2>
        <div className="mt-4 grid gap-5 md:grid-cols-2">
          {Object.keys(info.domains).map((d) => {
            const rows = r.skills.filter((x) => x.domain === d);
            if (!rows.length) return null;
            const right = rows.reduce((n, x) => n + x.right, 0), tot = rows.reduce((n, x) => n + x.total, 0);
            return (
              <div key={d}>
                <div className="mb-1 flex justify-between text-sm">
                  <span className="font-medium text-ink">{d}</span>
                  <span className="text-ink-subtle">{right}/{tot}</span>
                </div>
                <div className="h-2 overflow-hidden rounded-full bg-slate-100">
                  <div className={`h-full rounded-full ${right / tot >= 0.75 ? "bg-emerald-500" : right / tot >= 0.5 ? "bg-amber-400" : "bg-red-400"}`}
                    style={{ width: `${Math.round((100 * right) / tot)}%` }} />
                </div>
                <div className="mt-1.5 flex flex-wrap gap-x-3 gap-y-0.5 text-xs text-ink-subtle">
                  {rows.map((x) => <span key={x.skill}>{x.skill}: {x.right}/{x.total}</span>)}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <ReviewList modules={r.modules} />
    </div>
  );
}
