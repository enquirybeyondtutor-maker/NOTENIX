"use client";
import { useCallback, useEffect, useState } from "react";
import { Clock, ArrowRight, BarChart3 } from "lucide-react";
import { satAPI, type SatModule } from "@/lib/satApi";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import Runner from "@/components/sat/Runner";
import Report from "@/components/sat/Report";
import TrialSignup from "@/components/sat/TrialSignup";

const KEY = "notenix_sat_diag";
type Saved = { stage: number; answers: Record<string, string>; marked: string[]; startedAt: number | null; result?: any };

// Free SAT diagnostic: no account. Progress is kept in this browser so a refresh doesn't lose it.
export default function SatDiagnostic() {
  const [mods, setMods] = useState<SatModule[] | null>(null);
  const [s, setS] = useState<Saved>({ stage: -1, answers: {}, marked: [], startedAt: null });
  const [scoring, setScoring] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    satAPI.diagnostic().then((r) => setMods(r.data.modules)).catch(() => setError("The diagnostic isn't available right now."));
    try { const saved = JSON.parse(localStorage.getItem(KEY) || "null"); if (saved) setS(saved); } catch { /* fresh start */ }
  }, []);
  const persist = (next: Saved) => { setS(next); try { localStorage.setItem(KEY, JSON.stringify(next)); } catch { /* private mode */ } };

  const finishModule = useCallback(async () => {
    if (!mods) return;
    if (s.stage < mods.length - 1) return persist({ ...s, stage: s.stage + 1, startedAt: null });
    setScoring(true);
    try {
      const { data } = await satAPI.scoreDiagnostic(s.answers);
      persist({ ...s, stage: mods.length, startedAt: null, result: data });
      window.scrollTo(0, 0);
    } catch {
      setError("Couldn't score the diagnostic. Check your connection and try again.");
    } finally {
      setScoring(false);
    }
  }, [mods, s]); // eslint-disable-line react-hooks/exhaustive-deps

  if (error) return <div className="mx-auto max-w-lg p-10 text-center text-sm text-red-600">{error}</div>;
  if (!mods) return <Spinner label="Loading the diagnostic…" />;

  // Results
  if (s.result) {
    const r = s.result;
    return (
      <PageContainer>
        <h1 className="text-2xl font-bold text-ink sm:text-3xl">Your SAT diagnostic</h1>
        <p className="mt-1 text-sm text-ink-muted">A first estimate from 26 questions. A full practice test narrows it down.</p>
        <div className="mt-6 grid gap-8 lg:grid-cols-[1fr_380px]">
          <Report total={r.total_band} rw={{ band: r.rw.band, right: r.rw.right, total: r.rw.total }}
            math={{ band: r.math.band, right: r.math.right, total: r.math.total }} skills={r.skills} weakest={r.weakest}
            modules={[{ key: "rw", title: "Reading and Writing", questions: r.review.filter((q: any) => q.section === "rw") },
                      { key: "m", title: "Math", questions: r.review.filter((q: any) => q.section === "math") }]}
            note="A short diagnostic gives a band, not an exact score." />
          <div className="lg:sticky lg:top-24 lg:self-start">
            <TrialSignup diagnosticAnswers={s.answers} onDone={() => { try { localStorage.removeItem(KEY); } catch { /* ignore */ } }} />
            <button onClick={() => persist({ stage: -1, answers: {}, marked: [], startedAt: null })}
              className="mt-3 w-full text-center text-xs text-ink-subtle hover:text-ink">Take the diagnostic again</button>
          </div>
        </div>
      </PageContainer>
    );
  }

  const mod = s.stage >= 0 ? mods[s.stage] : null;
  // Intro / between modules
  if (!mod || s.startedAt === null) {
    const next = mods[Math.max(0, s.stage)];
    return (
      <div className="mx-auto max-w-xl px-4 py-16">
        <div className="card p-8 text-center">
          <span className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-brand-50 text-brand-600">{s.stage < 0 ? <BarChart3 size={22} /> : <Clock size={22} />}</span>
          <h1 className="mt-4 text-2xl font-bold text-ink">{s.stage < 0 ? "Free SAT diagnostic" : "Part 2: Math"}</h1>
          <p className="mt-2 text-sm text-ink-muted">
            {s.stage < 0
              ? "26 questions in two timed parts, about 34 minutes. You'll get an estimated score band out of 1600 and the skills costing you the most points. No account needed."
              : "Reading and Writing done. The Math part has a Desmos calculator and the reference sheet, like the real test."}
          </p>
          <div className="mt-6 rounded-xl border border-line p-4 text-left text-sm">
            <div className="font-semibold text-ink">{next.title}</div>
            <div className="mt-1 text-ink-muted">{next.questions.length} questions · {next.minutes} minutes</div>
          </div>
          <Button className="mt-6" onClick={() => persist({ ...s, stage: Math.max(0, s.stage), startedAt: Date.now() })}>
            Start {next.title} <ArrowRight size={16} />
          </Button>
        </div>
      </div>
    );
  }

  const left = Math.round(mod.minutes * 60 - (Date.now() - s.startedAt) / 1000);
  return (
    <Runner
      key={mod.key}
      heading={`SAT diagnostic: part ${s.stage + 1} of ${mods.length}`}
      module={mod}
      answers={s.answers}
      marked={s.marked}
      secondsLeft={left}
      submitting={scoring}
      onAnswer={(qid, v) => persist({ ...s, answers: { ...s.answers, [qid]: v } })}
      onToggleMark={(qid) => persist({ ...s, marked: s.marked.includes(qid) ? s.marked.filter((x) => x !== qid) : [...s.marked, qid] })}
      onSubmit={() => finishModule()}
    />
  );
}
