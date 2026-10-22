"use client";
import { useState } from "react";
import { CheckCircle2, XCircle, ArrowRight, RotateCcw } from "lucide-react";
import { MathText } from "./MathText";
import { Button } from "./ui/Button";
import { Input } from "./ui/Input";
import { cn } from "@/lib/utils";
import { numericEqual } from "@/lib/answers";
import type { SampleQuestion } from "@/lib/exams";

// Free, no-account sample questions on the public exam pages. Answers are checked in the browser.
export default function SampleQuiz({ examName, questions }: { examName: string; questions: SampleQuestion[] }) {
  const [picked, setPicked] = useState<Record<number, string>>({});
  const [typed, setTyped] = useState<Record<number, string>>({});
  const [checked, setChecked] = useState<Record<number, boolean>>({});

  const isRight = (i: number) => {
    const q = questions[i];
    return q.options ? picked[i] === q.answer : numericEqual(typed[i] ?? "", q.answer);
  };
  const done = Object.keys(checked).length;
  const score = Object.keys(checked).filter((k) => isRight(Number(k))).length;

  const reset = () => { setPicked({}); setTyped({}); setChecked({}); };

  return (
    <div className="space-y-5">
      {questions.map((q, i) => {
        const shown = !!checked[i];
        const right = shown && isRight(i);
        const ready = q.options ? picked[i] != null : (typed[i] ?? "").trim() !== "";
        return (
          <div key={i} className="card p-5 sm:p-6">
            <div className="flex items-start gap-3">
              <span className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-brand-50 text-xs font-bold text-brand-700">{i + 1}</span>
              <p className="whitespace-pre-line text-[15px] leading-relaxed text-ink"><MathText text={q.question} /></p>
            </div>

            {q.options ? (
              <div className="mt-4 grid gap-2 sm:grid-cols-2">
                {q.options.map((opt) => {
                  const sel = picked[i] === opt;
                  const isAns = shown && opt === q.answer;
                  const isWrongPick = shown && sel && opt !== q.answer;
                  return (
                    <button
                      key={opt}
                      type="button"
                      disabled={shown}
                      onClick={() => setPicked((p) => ({ ...p, [i]: opt }))}
                      className={cn("option-btn text-left", sel && !shown && "selected", isAns && "correct", isWrongPick && "incorrect")}
                    >
                      <MathText text={opt} />
                    </button>
                  );
                })}
              </div>
            ) : (
              <div className="mt-4 flex max-w-xs items-center gap-2">
                <Input
                  inputMode="decimal"
                  aria-label={`Answer to question ${i + 1}`}
                  placeholder="Type your answer"
                  disabled={shown}
                  value={typed[i] ?? ""}
                  onChange={(e) => setTyped((t) => ({ ...t, [i]: e.target.value }))}
                  onKeyDown={(e) => { if (e.key === "Enter" && ready) setChecked((c) => ({ ...c, [i]: true })); }}
                />
              </div>
            )}

            <div className="mt-4 flex flex-wrap items-center gap-3">
              {!shown ? (
                <Button size="sm" disabled={!ready} onClick={() => setChecked((c) => ({ ...c, [i]: true }))}>
                  Check answer
                </Button>
              ) : (
                <span className={cn("inline-flex items-center gap-1.5 text-sm font-semibold", right ? "text-emerald-600" : "text-red-600")}>
                  {right ? <CheckCircle2 size={16} /> : <XCircle size={16} />}
                  {right ? "Correct" : <>Not quite. The answer is&nbsp;<MathText text={q.answer} /></>}
                </span>
              )}
            </div>
            {shown && (
              <p className="mt-3 rounded-lg bg-slate-50 px-4 py-3 text-sm leading-relaxed text-ink-muted">
                <MathText text={q.explanation} />
              </p>
            )}
          </div>
        );
      })}

      {done === questions.length && (
        <div className="card flex flex-col items-start gap-4 border-brand-200 bg-brand-50 p-6 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <div className="text-lg font-bold text-ink">You scored {score} / {questions.length}</div>
            <p className="text-sm text-ink-muted">Ready for a full timed {examName} mock? Create a free account or request a tutor-marked test.</p>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button href="/request" size="sm">Request a full mock <ArrowRight size={14} /></Button>
            <Button variant="secondary" size="sm" onClick={reset}><RotateCcw size={14} /> Try again</Button>
          </div>
        </div>
      )}
    </div>
  );
}
