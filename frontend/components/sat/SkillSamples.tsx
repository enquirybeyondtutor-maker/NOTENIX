"use client";
import { useState } from "react";
import { CheckCircle2, XCircle } from "lucide-react";
import { MathText } from "@/components/MathText";
import SatText from "./SatText";
import { numericEqual } from "@/lib/answers";

type Q = { id: string; type: "mcq" | "spr"; passage?: string; question: string; options?: string[]; answer: string | string[]; explanation: string };

/** Free sample questions on a public SAT skill page, checked in the browser. */
export default function SkillSamples({ questions }: { questions: Q[] }) {
  const [given, setGiven] = useState<Record<string, string>>({});
  const [shown, setShown] = useState<Record<string, boolean>>({});
  return (
    <div className="space-y-5">
      {questions.map((q, n) => {
        const g = given[q.id] ?? "";
        const ok = q.type === "mcq" ? g === q.answer : (q.answer as string[]).some((a) => numericEqual(g, a));
        const right = Array.isArray(q.answer) ? q.answer[0] : q.answer;
        return (
          <div key={q.id} className="card p-6">
            <div className="text-xs font-semibold uppercase tracking-wide text-ink-subtle">Question {n + 1}</div>
            {q.passage && <div className="mt-3 rounded-lg bg-slate-50 p-4 text-[15px] text-ink"><SatText text={q.passage} /></div>}
            <SatText text={q.question} className="mt-3 text-[15px] text-ink" />
            {q.type === "mcq" ? (
              <div className="mt-4 space-y-2">
                {(q.options ?? []).map((o, k) => {
                  const L = "ABCD"[k];
                  const cls = shown[q.id] && L === right ? "border-emerald-500 bg-emerald-50" : shown[q.id] && L === g ? "border-red-400 bg-red-50" : g === L ? "border-brand-600 bg-brand-50" : "border-line hover:border-slate-300";
                  return (
                    <button key={L} disabled={shown[q.id]} onClick={() => setGiven({ ...given, [q.id]: L })}
                      className={`flex w-full items-center gap-3 rounded-xl border-2 px-4 py-2.5 text-left text-sm ${cls}`}>
                      <span className="font-semibold">{L}.</span> <MathText text={o} />
                    </button>
                  );
                })}
              </div>
            ) : (
              <input value={g} disabled={shown[q.id]} onChange={(e) => setGiven({ ...given, [q.id]: e.target.value })} placeholder="Your answer"
                className="mt-4 block w-40 rounded-lg border-2 border-line px-3 py-2 font-mono outline-none focus:border-brand-600" />
            )}
            {shown[q.id] ? (
              <div className={`mt-4 rounded-xl border p-4 text-sm ${ok ? "border-emerald-200 bg-emerald-50/60" : "border-red-200 bg-red-50/60"}`}>
                <div className={`flex items-center gap-2 font-semibold ${ok ? "text-emerald-800" : "text-red-700"}`}>
                  {ok ? <CheckCircle2 size={16} /> : <XCircle size={16} />} {ok ? "Correct" : `The answer is ${right}`}
                </div>
                <SatText text={q.explanation} className="mt-1.5 text-ink" />
              </div>
            ) : (
              <button disabled={!g.trim()} onClick={() => setShown({ ...shown, [q.id]: true })}
                className="mt-4 rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-40">Check answer</button>
            )}
          </div>
        );
      })}
    </div>
  );
}
