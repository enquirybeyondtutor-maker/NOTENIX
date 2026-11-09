"use client";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Bookmark, Calculator, ChevronLeft, ChevronRight, Clock, Eye, EyeOff, FileText, LayoutGrid, X } from "lucide-react";
import { MathText } from "@/components/MathText";
import SatText from "./SatText";
import ReferenceSheet from "./ReferenceSheet";
import type { SatModule } from "@/lib/satApi";

/** One timed SAT module, laid out like the Digital SAT app. The parent owns answers/marks
 *  (so it can autosave) and handles submit; the timer calls onSubmit itself at 0:00. */
export default function Runner({
  heading, module, answers, marked, secondsLeft, onAnswer, onToggleMark, onSubmit, submitting, calculator, reference,
}: {
  heading: string;
  module: SatModule;
  answers: Record<string, string>;
  marked: string[];
  secondsLeft: number;
  onAnswer: (qid: string, value: string) => void;
  onToggleMark: (qid: string) => void;
  onSubmit: (auto: boolean) => void;
  submitting?: boolean;
  /** Show the Desmos calculator / reference sheet buttons (default: in SAT Math modules). */
  calculator?: boolean;
  reference?: boolean;
}) {
  const qs = module.questions;
  const [i, setI] = useState(0);          // current question; qs.length = review page
  const [left, setLeft] = useState(secondsLeft);
  const [showTime, setShowTime] = useState(true);
  const [grid, setGrid] = useState(false);
  const [calc, setCalc] = useState(false);
  const [ref, setRef] = useState(false);
  const [crossed, setCrossed] = useState<Record<string, string[]>>({});
  const fired = useRef(false);
  const isMath = module.section === "math";
  const showCalc = calculator ?? isMath, showRef = reference ?? isMath;
  const onReview = i >= qs.length;
  const q = qs[Math.min(i, qs.length - 1)];

  useEffect(() => { setLeft(secondsLeft); }, [secondsLeft]);
  useEffect(() => {
    const t = setInterval(() => setLeft((s) => s - 1), 1000);
    return () => clearInterval(t);
  }, []);
  useEffect(() => {
    if (left <= 0 && !fired.current) { fired.current = true; onSubmit(true); }
  }, [left, onSubmit]);

  const mm = Math.max(0, Math.floor(left / 60)), ss = Math.max(0, left % 60);
  const lowTime = left <= 300;
  const answeredCount = useMemo(() => qs.filter((x) => (answers[x.id] ?? "").trim() !== "").length, [qs, answers]);

  const cross = useCallback((qid: string, letter: string) => {
    setCrossed((c) => {
      const cur = c[qid] ?? [];
      return { ...c, [qid]: cur.includes(letter) ? cur.filter((x) => x !== letter) : [...cur, letter] };
    });
  }, []);

  return (
    <div className="fixed inset-0 z-[60] flex flex-col bg-white">
      {/* Top bar */}
      <header className="flex items-center justify-between gap-3 border-b border-line px-4 py-2.5 sm:px-6">
        <div className="min-w-0">
          <div className="truncate text-sm font-semibold text-ink">{heading}</div>
          <div className="text-xs text-ink-subtle">{module.title}</div>
        </div>
        <div className="flex flex-col items-center">
          {showTime ? (
            <span className={`font-mono text-lg font-bold tabular-nums ${lowTime ? "text-red-600" : "text-ink"}`}>
              {mm}:{ss.toString().padStart(2, "0")}
            </span>
          ) : <Clock size={20} className="text-ink-subtle" />}
          <button onClick={() => setShowTime(!showTime)} className="inline-flex items-center gap-1 text-[11px] font-medium text-ink-subtle hover:text-ink">
            {showTime ? <><EyeOff size={11} /> Hide</> : <><Eye size={11} /> Show</>}
          </button>
        </div>
        <div className="flex items-center gap-1.5">
          {showCalc && (
              <button onClick={() => setCalc(!calc)} className={`inline-flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-xs font-semibold ${calc ? "bg-brand-600 text-white" : "border border-line text-ink hover:bg-slate-50"}`}>
                <Calculator size={14} /> <span className="hidden sm:inline">Calculator</span>
              </button>
          )}
          {showRef && (
              <button onClick={() => setRef(true)} className="inline-flex items-center gap-1.5 rounded-lg border border-line px-2.5 py-1.5 text-xs font-semibold text-ink hover:bg-slate-50">
                <FileText size={14} /> <span className="hidden sm:inline">Reference</span>
              </button>
          )}
        </div>
      </header>

      {/* Body */}
      <div className="flex min-h-0 flex-1">
        {calc && showCalc && (
          <aside className="hidden w-[min(44vw,560px)] shrink-0 border-r border-line md:block">
            <iframe src="https://www.desmos.com/calculator" title="Desmos graphing calculator" className="h-full w-full" />
          </aside>
        )}
        <main className="min-w-0 flex-1 overflow-y-auto">
          {onReview ? (
            <div className="mx-auto max-w-3xl p-6">
              <h2 className="text-xl font-bold text-ink">Check your work</h2>
              <p className="mt-1 text-sm text-ink-muted">
                {answeredCount} of {qs.length} answered. Select a question to go back to it. When you submit, you can&apos;t return to this module.
              </p>
              <QuestionGrid qs={qs} answers={answers} marked={marked} current={-1} onPick={(n) => setI(n)} />
              <button onClick={() => onSubmit(false)} disabled={submitting}
                className="mt-8 rounded-xl bg-brand-600 px-6 py-3 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-60">
                {submitting ? "Submitting…" : "Submit this module"}
              </button>
            </div>
          ) : (
            <div className={`mx-auto grid gap-6 p-5 sm:p-8 ${q.passage ? "max-w-6xl lg:grid-cols-2" : "max-w-3xl"}`}>
              {q.passage && (
                <div className="border-line text-[15px] text-ink lg:border-r lg:pr-8">
                  <SatText text={q.passage} />
                </div>
              )}
              <div>
                <div className="mb-4 flex items-center justify-between gap-3 border-b border-dashed border-line pb-3">
                  <span className="grid h-8 w-8 place-items-center rounded-md bg-ink text-sm font-bold text-white">{i + 1}</span>
                  <button onClick={() => onToggleMark(q.id)}
                    className={`inline-flex items-center gap-1.5 text-sm font-medium ${marked.includes(q.id) ? "text-red-600" : "text-ink-muted hover:text-ink"}`}>
                    <Bookmark size={15} fill={marked.includes(q.id) ? "currentColor" : "none"} /> Mark for review
                  </button>
                </div>
                <SatText text={q.question} className="text-[15px] text-ink" />
                {q.type === "mcq" ? (
                  <div className="mt-5 space-y-2.5">
                    {(q.options ?? []).map((opt, k) => {
                      const letter = "ABCDEFGH"[k];
                      const chosen = answers[q.id] === letter;
                      const out = (crossed[q.id] ?? []).includes(letter);
                      return (
                        <div key={letter} className="flex items-center gap-2">
                          <button onClick={() => onAnswer(q.id, chosen ? "" : letter)}
                            className={`flex flex-1 items-center gap-3 rounded-xl border-2 px-4 py-3 text-left text-[15px] transition-colors ${chosen ? "border-brand-600 bg-brand-50" : "border-line hover:border-slate-300"} ${out ? "opacity-40" : ""}`}>
                            <span className={`grid h-7 w-7 shrink-0 place-items-center rounded-full border-2 text-sm font-semibold ${chosen ? "border-brand-600 bg-brand-600 text-white" : "border-slate-400 text-ink"}`}>{letter}</span>
                            <span className={out ? "line-through" : ""}><MathText text={opt} /></span>
                          </button>
                          <button onClick={() => cross(q.id, letter)} title={out ? "Undo cross out" : "Cross out this option"}
                            className="grid h-7 w-7 shrink-0 place-items-center rounded-full text-xs font-semibold text-ink-subtle hover:bg-slate-100">
                            {out ? "↺" : <span className="line-through">{letter}</span>}
                          </button>
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <div className="mt-5">
                    <label className="text-sm font-medium text-ink">Your answer</label>
                    <input value={answers[q.id] ?? ""} onChange={(e) => onAnswer(q.id, e.target.value.replace(/[^0-9./-]/g, "").slice(0, 6))}
                      inputMode="decimal" placeholder="e.g. 12, 0.75 or 3/4"
                      className="mt-1.5 block w-48 rounded-lg border-2 border-line px-3 py-2.5 font-mono text-lg outline-none focus:border-brand-600" />
                    <p className="mt-2 text-xs text-ink-subtle">Type a number: a whole number, a decimal or a fraction such as 3/4. Up to 5 characters, plus a minus sign.</p>
                  </div>
                )}
              </div>
            </div>
          )}
        </main>
      </div>

      {/* Bottom bar */}
      <footer className="relative flex items-center justify-between gap-3 border-t border-line px-4 py-2.5 sm:px-6">
        <span className="hidden text-xs text-ink-subtle sm:inline">{answeredCount}/{qs.length} answered</span>
        <button onClick={() => setGrid(!grid)} className="inline-flex items-center gap-1.5 rounded-lg bg-ink px-3 py-1.5 text-sm font-semibold text-white">
          <LayoutGrid size={14} /> {onReview ? "Review" : `Question ${i + 1} of ${qs.length}`}
        </button>
        <div className="flex gap-2">
          <button onClick={() => setI(Math.max(0, i - 1))} disabled={i === 0}
            className="inline-flex items-center gap-1 rounded-lg border border-line px-3 py-1.5 text-sm font-semibold text-ink disabled:opacity-40">
            <ChevronLeft size={15} /> Back
          </button>
          {!onReview && (
            <button onClick={() => setI(i + 1)} className="inline-flex items-center gap-1 rounded-lg bg-brand-600 px-3 py-1.5 text-sm font-semibold text-white hover:bg-brand-700">
              Next <ChevronRight size={15} />
            </button>
          )}
        </div>
        {grid && (
          <div className="absolute bottom-14 left-1/2 w-[min(92vw,520px)] -translate-x-1/2 rounded-2xl border border-line bg-white p-4 shadow-xl">
            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold text-ink">{module.title}</span>
              <button onClick={() => setGrid(false)} aria-label="Close"><X size={16} /></button>
            </div>
            <QuestionGrid qs={qs} answers={answers} marked={marked} current={i} onPick={(n) => { setI(n); setGrid(false); }} />
            <button onClick={() => { setI(qs.length); setGrid(false); }} className="mt-3 w-full rounded-lg border border-brand-200 py-2 text-sm font-semibold text-brand-700 hover:bg-brand-50">
              Go to review page
            </button>
          </div>
        )}
      </footer>
      {ref && <ReferenceSheet onClose={() => setRef(false)} />}
    </div>
  );
}

function QuestionGrid({ qs, answers, marked, current, onPick }: {
  qs: SatModule["questions"]; answers: Record<string, string>; marked: string[]; current: number; onPick: (n: number) => void;
}) {
  return (
    <>
      <div className="mt-4 grid grid-cols-8 gap-2 sm:grid-cols-10">
        {qs.map((x, n) => {
          const done = (answers[x.id] ?? "").trim() !== "";
          return (
            <button key={x.id} onClick={() => onPick(n)}
              className={`relative grid h-9 place-items-center rounded-md border-2 text-sm font-semibold
                ${n === current ? "ring-2 ring-ink ring-offset-1" : ""}
                ${done ? "border-brand-600 bg-brand-600 text-white" : "border-dashed border-slate-400 text-ink"}`}>
              {n + 1}
              {marked.includes(x.id) && <Bookmark size={11} className="absolute -right-1 -top-1.5 text-red-600" fill="currentColor" />}
            </button>
          );
        })}
      </div>
      <div className="mt-3 flex flex-wrap gap-4 text-xs text-ink-subtle">
        <span className="inline-flex items-center gap-1"><span className="h-3 w-3 rounded-sm bg-brand-600" /> Answered</span>
        <span className="inline-flex items-center gap-1"><span className="h-3 w-3 rounded-sm border-2 border-dashed border-slate-400" /> Unanswered</span>
        <span className="inline-flex items-center gap-1"><Bookmark size={11} className="text-red-600" fill="currentColor" /> For review</span>
      </div>
    </>
  );
}
