"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { ArrowLeft, ArrowRight, CheckCircle2, XCircle, RotateCcw } from "lucide-react";
import { useAuthGuard } from "@/lib/guard";
import { satAPI, type SatQuestion } from "@/lib/satApi";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { MathText } from "@/components/MathText";
import SatText from "@/components/sat/SatText";

type Feedback = { correct: boolean; answer: string | string[]; explanation: string };

// A 6-question skill drill: answer, see straight away whether it's right and why, move on.
export default function SatDrill() {
  const { ready } = useAuthGuard("student");
  const { slug } = useParams<{ slug: string }>();
  const [d, setD] = useState<any>(null);
  const [error, setError] = useState("");
  const [i, setI] = useState(0);
  const [given, setGiven] = useState("");
  const [fb, setFb] = useState<Feedback | null>(null);
  const [score, setScore] = useState<boolean[]>([]);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (ready) satAPI.drill(slug).then((r) => setD(r.data)).catch((e) => setError(e.response?.data?.detail || "Couldn't load this drill."));
  }, [ready, slug]);

  if (error) return <div className="mx-auto max-w-lg p-10 text-center text-sm text-red-600">{error}</div>;
  if (!ready || !d) return <Spinner label="Loading the drill…" />;

  const qs: SatQuestion[] = d.questions;
  const finished = i >= qs.length;
  const q = qs[Math.min(i, qs.length - 1)];

  const check = async () => {
    if (!given.trim()) return;
    setBusy(true);
    try {
      const { data } = await satAPI.drillAnswer(slug, q.id, given);
      setFb(data);
      setScore((s) => [...s, data.correct]);
    } finally {
      setBusy(false);
    }
  };
  const next = () => {
    setI(i + 1); setGiven(""); setFb(null);
  };
  const restart = () => { setI(0); setGiven(""); setFb(null); setScore([]); };
  const right = Array.isArray(fb?.answer) ? fb?.answer[0] : fb?.answer;

  return (
    <PageContainer className="max-w-4xl">
      <a href="/sat/practice" className="mb-4 inline-flex items-center gap-1 text-sm font-medium text-brand-600 hover:text-brand-700"><ArrowLeft size={15} /> SAT practice</a>
      <div className="flex flex-wrap items-end justify-between gap-3">
        <div>
          <div className="text-xs font-semibold uppercase tracking-wide text-brand-700">{d.domain}</div>
          <h1 className="text-2xl font-bold text-ink">{d.skill}</h1>
          <p className="mt-1 text-sm text-ink-muted"><MathText text={d.about} /></p>
        </div>
        {!finished && <span className="text-sm font-semibold text-ink-muted">Question {i + 1} of {qs.length}</span>}
      </div>

      {finished ? (
        <div className="card mt-6 p-8 text-center">
          <div className="text-4xl font-bold text-ink">{score.filter(Boolean).length} / {qs.length}</div>
          <p className="mt-2 text-sm text-ink-muted">
            {score.filter(Boolean).length === qs.length ? "Every one right. This skill is looking strong." :
              score.filter(Boolean).length >= qs.length / 2 ? "Good work. Read the explanations for the ones you missed, then try again tomorrow." :
              "This skill needs more practice. Go back over the explanations, then try the drill again."}
          </p>
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            <Button href="/sat/practice">Back to your plan</Button>
            <Button variant="secondary" onClick={restart}><RotateCcw size={15} /> Try again</Button>
          </div>
        </div>
      ) : (
        <div className={`card mt-6 grid gap-6 p-6 ${q.passage ? "lg:grid-cols-2" : ""}`}>
          {q.passage && <div className="border-line text-[15px] text-ink lg:border-r lg:pr-6"><SatText text={q.passage} /></div>}
          <div>
            <SatText text={q.question} className="text-[15px] text-ink" />
            {q.type === "mcq" ? (
              <div className="mt-5 space-y-2.5">
                {(q.options ?? []).map((opt, k) => {
                  const L = "ABCD"[k];
                  const isRight = fb && L === right, isMine = given === L;
                  return (
                    <button key={L} disabled={!!fb} onClick={() => setGiven(L)}
                      className={`flex w-full items-center gap-3 rounded-xl border-2 px-4 py-3 text-left text-[15px] transition-colors
                        ${isRight ? "border-emerald-500 bg-emerald-50" : fb && isMine ? "border-red-400 bg-red-50" : isMine ? "border-brand-600 bg-brand-50" : "border-line hover:border-slate-300"}`}>
                      <span className={`grid h-7 w-7 shrink-0 place-items-center rounded-full border-2 text-sm font-semibold ${isMine && !fb ? "border-brand-600 bg-brand-600 text-white" : "border-slate-400"}`}>{L}</span>
                      <MathText text={opt} />
                    </button>
                  );
                })}
              </div>
            ) : (
              <input value={given} disabled={!!fb} onChange={(e) => setGiven(e.target.value.replace(/[^0-9./-]/g, "").slice(0, 6))}
                inputMode="decimal" placeholder="Your answer"
                className="mt-5 block w-48 rounded-lg border-2 border-line px-3 py-2.5 font-mono text-lg outline-none focus:border-brand-600" />
            )}

            {fb ? (
              <div className={`mt-5 rounded-xl border p-4 ${fb.correct ? "border-emerald-200 bg-emerald-50/70" : "border-red-200 bg-red-50/70"}`}>
                <div className={`flex items-center gap-2 font-semibold ${fb.correct ? "text-emerald-800" : "text-red-700"}`}>
                  {fb.correct ? <CheckCircle2 size={18} /> : <XCircle size={18} />} {fb.correct ? "Correct" : `Not quite: the answer is ${right}`}
                </div>
                <SatText text={fb.explanation} className="mt-2 text-sm text-ink" />
                <Button className="mt-4" onClick={next}>{i + 1 < qs.length ? <>Next question <ArrowRight size={15} /></> : "See my score"}</Button>
              </div>
            ) : (
              <Button className="mt-5" loading={busy} disabled={!given.trim()} onClick={check}>Check answer</Button>
            )}
          </div>
        </div>
      )}
    </PageContainer>
  );
}
