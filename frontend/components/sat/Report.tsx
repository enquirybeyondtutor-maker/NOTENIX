"use client";
import { useState } from "react";
import { CheckCircle2, XCircle, MinusCircle, ChevronDown, ChevronUp, Target, UserRound, ArrowRight } from "lucide-react";
import { MathText } from "@/components/MathText";
import SatText from "./SatText";
import { SAT_DOMAINS, type ReviewQuestion, type SkillRow } from "@/lib/satApi";

type Section = { score?: number; band?: [number, number]; right?: number; total?: number };

/** SAT score report: total out of 1600 (or a band), section scores, skills, weakest skills
 *  and a question-by-question review with explanations. Used for mocks and the diagnostic. */
export default function Report({
  total, rw, math, target, skills, weakest, modules, note,
}: {
  total: number | [number, number];
  rw: Section;
  math: Section;
  target?: number | null;
  skills: SkillRow[];
  weakest: SkillRow[];
  modules: { key: string; title: string; questions: ReviewQuestion[] }[];
  note?: React.ReactNode;
}) {
  const show = (s: Section) => (s.band ? `${s.band[0]}–${s.band[1]}` : String(s.score ?? "–"));
  const mid = Array.isArray(total) ? Math.round((total[0] + total[1]) / 2) : total;
  return (
    <div className="space-y-8">
      <div className="card overflow-hidden">
        <div className="grid gap-px bg-line sm:grid-cols-3">
          <div className="bg-gradient-to-br from-brand-600 to-brand-700 p-6 text-white">
            <div className="text-xs font-semibold uppercase tracking-wide text-white/70">{Array.isArray(total) ? "Estimated score band" : "Estimated total score"}</div>
            <div className="mt-1 text-4xl font-bold tabular-nums">{Array.isArray(total) ? `${total[0]}–${total[1]}` : total}</div>
            <div className="text-sm text-white/70">out of 1600</div>
            {target ? (
              <div className="mt-3 inline-flex items-center gap-1.5 rounded-full bg-white/15 px-2.5 py-1 text-xs font-semibold">
                <Target size={12} /> Target {target}: {mid >= target ? "you're there" : `${target - mid} points to go`}
              </div>
            ) : null}
          </div>
          {([["Reading and Writing", rw], ["Math", math]] as const).map(([label, s]) => (
            <div key={label} className="bg-white p-6">
              <div className="text-xs font-semibold uppercase tracking-wide text-ink-subtle">{label}</div>
              <div className="mt-1 text-3xl font-bold tabular-nums text-ink">{show(s)}</div>
              <div className="text-sm text-ink-muted">out of 800{s.total ? ` · ${s.right} of ${s.total} right` : ""}</div>
            </div>
          ))}
        </div>
        {note && <div className="border-t border-line bg-slate-50 px-6 py-3 text-xs text-ink-muted">{note}</div>}
      </div>

      <div className="card flex flex-wrap items-center justify-between gap-4 border-brand-200 bg-brand-50 p-5">
        <div className="min-w-0">
          <div className="flex items-center gap-2 font-semibold text-ink"><UserRound size={16} className="text-brand-600" /> Go through this test with a tutor</div>
          <p className="mt-1 text-sm text-ink-muted">A Beyond Tutors SAT tutor reviews your mistakes with you and tells you exactly what to fix before test day.</p>
        </div>
        <a href="https://www.thebeyondtutors.com/book?utm_source=notenix&utm_medium=sat_report&utm_campaign=tutor_review"
          target="_blank" rel="noopener"
          className="inline-flex shrink-0 items-center gap-1.5 rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700">
          Book a tutor review of your mock <ArrowRight size={15} />
        </a>
      </div>

      {weakest.length > 0 && (
        <div className="card p-6">
          <h2 className="font-semibold text-ink">Where your points are going</h2>
          <p className="mt-1 text-sm text-ink-muted">The skills that cost you the most questions. Start your practice here.</p>
          <div className="mt-4 grid gap-3 sm:grid-cols-3">
            {weakest.map((w) => (
              <div key={w.skill} className="rounded-xl border border-amber-200 bg-amber-50 p-4">
                <div className="text-xs font-semibold text-amber-800">{w.domain}</div>
                <div className="mt-0.5 font-semibold text-ink">{w.skill}</div>
                <div className="mt-1 text-sm text-ink-muted">{w.right} of {w.total} right</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        {(["rw", "math"] as const).map((sec) => (
          <div key={sec} className="card p-6">
            <h2 className="font-semibold text-ink">{sec === "rw" ? "Reading and Writing" : "Math"} skills</h2>
            <div className="mt-4 space-y-4">
              {SAT_DOMAINS[sec].map((d) => {
                const rows = skills.filter((r) => r.section === sec && r.domain === d);
                if (!rows.length) return null;
                const right = rows.reduce((n, r) => n + r.right, 0), tot = rows.reduce((n, r) => n + r.total, 0);
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
                      {rows.map((r) => <span key={r.skill}>{r.skill}: {r.right}/{r.total}</span>)}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      <ReviewList modules={modules} />
    </div>
  );
}

export function ReviewList({ modules }: { modules: { key: string; title: string; questions: ReviewQuestion[] }[] }) {
  const [onlyWrong, setOnlyWrong] = useState(true);
  const [open, setOpen] = useState<string | null>(null);
  return (
    <div className="card p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="font-semibold text-ink">Review your answers</h2>
        <label className="inline-flex items-center gap-2 text-sm text-ink-muted">
          <input type="checkbox" checked={onlyWrong} onChange={(e) => setOnlyWrong(e.target.checked)} /> Only questions I missed
        </label>
      </div>
      {modules.map((m) => {
        const list = m.questions.map((q, n) => ({ q, n })).filter(({ q }) => !onlyWrong || !q.correct);
        return (
          <div key={m.key} className="mt-6">
            <h3 className="text-sm font-semibold uppercase tracking-wide text-ink-subtle">{m.title}</h3>
            {list.length === 0 ? <p className="mt-2 text-sm text-emerald-700">Every question right in this module.</p> : (
              <div className="mt-2 divide-y divide-line rounded-xl border border-line">
                {list.map(({ q, n }) => {
                  const isOpen = open === q.id;
                  const blank = !q.given;
                  const right = Array.isArray(q.answer) ? q.answer[0] : q.answer;
                  return (
                    <div key={q.id}>
                      <button onClick={() => setOpen(isOpen ? null : q.id)} className="flex w-full items-center justify-between gap-3 px-4 py-3 text-left hover:bg-slate-50">
                        <span className="flex min-w-0 items-center gap-3">
                          {q.correct ? <CheckCircle2 size={17} className="shrink-0 text-emerald-600" /> : blank ? <MinusCircle size={17} className="shrink-0 text-slate-400" /> : <XCircle size={17} className="shrink-0 text-red-500" />}
                          <span className="text-sm font-medium text-ink">Question {n + 1}</span>
                          <span className="truncate text-xs text-ink-subtle">{q.skill}</span>
                        </span>
                        {isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                      </button>
                      {isOpen && (
                        <div className="space-y-4 border-t border-line bg-slate-50/50 px-4 py-4 text-sm">
                          {q.passage && <div className="rounded-lg bg-white p-3 text-ink"><SatText text={q.passage} /></div>}
                          <SatText text={q.question} className="text-ink" />
                          {q.options && (
                            <ul className="space-y-1.5">
                              {q.options.map((o, k) => {
                                const L = "ABCDEFGH"[k];
                                return (
                                  <li key={L} className={`rounded-lg px-3 py-2 ${L === right ? "bg-emerald-50 font-medium text-emerald-900" : L === q.given ? "bg-red-50 text-red-900" : "text-ink-muted"}`}>
                                    {L}. <MathText text={o} />{L === right ? "  ✓" : L === q.given ? "  (your answer)" : ""}
                                  </li>
                                );
                              })}
                            </ul>
                          )}
                          {!q.options && (
                            <p>Your answer: <b>{q.given || "blank"}</b> · Correct: <b>{right}</b></p>
                          )}
                          <div className="rounded-lg border border-brand-100 bg-white p-3">
                            <div className="text-xs font-semibold uppercase tracking-wide text-brand-700">Explanation</div>
                            <SatText text={q.explanation} className="mt-1 text-ink" />
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
