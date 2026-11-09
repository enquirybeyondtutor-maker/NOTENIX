"use client";
import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Clock, ArrowRight, BarChart3, LogIn, Send } from "lucide-react";
import { examAPI, hasEngine, diagKey, type ExamInfo, type ExamReport as Report } from "@/lib/examApi";
import type { SatModule } from "@/lib/satApi";
import { requestHref } from "@/lib/exams";
import { getUser } from "@/lib/api";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import Runner from "@/components/sat/Runner";
import ExamReport from "@/components/exam/ExamReport";

type Saved = { stage: number; answers: Record<string, string>; marked: string[]; startedAt: number | null; result?: Report };

// Free diagnostic for an exam-engine exam (e.g. TMUA): no account needed. Progress stays in
// this browser; after signing in, the practice home saves it to the account.
export default function ExamDiagnostic() {
  const { exam } = useParams<{ exam: string }>();
  const [user, setUser] = useState<any>(null);
  const key = diagKey(exam);
  const [info, setInfo] = useState<ExamInfo | null>(null);
  const [mods, setMods] = useState<SatModule[] | null>(null);
  const [s, setS] = useState<Saved>({ stage: -1, answers: {}, marked: [], startedAt: null });
  const [scoring, setScoring] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setUser(getUser());
    if (!hasEngine(exam)) { setError("There's no diagnostic for this exam yet."); return; }
    Promise.all([examAPI.info(exam), examAPI.diagnostic(exam)])
      .then(([i, d]) => { setInfo(i.data); setMods(d.data.modules); })
      .catch(() => setError("The diagnostic isn't available right now."));
    try { const saved = JSON.parse(localStorage.getItem(key) || "null"); if (saved) setS(saved); } catch { /* fresh start */ }
  }, [exam, key]);
  const persist = (next: Saved) => { setS(next); try { localStorage.setItem(key, JSON.stringify(next)); } catch { /* private mode */ } };

  const finishModule = useCallback(async () => {
    if (!mods) return;
    if (s.stage < mods.length - 1) return persist({ ...s, stage: s.stage + 1, startedAt: null });
    setScoring(true);
    try {
      const { data } = await examAPI.scoreDiagnostic(exam, s.answers);
      persist({ ...s, stage: mods.length, startedAt: null, result: data });
      window.scrollTo(0, 0);
    } catch {
      setError("Couldn't score the diagnostic. Check your connection and try again.");
    } finally {
      setScoring(false);
    }
  }, [mods, s, exam]); // eslint-disable-line react-hooks/exhaustive-deps

  if (error) return <div className="mx-auto max-w-lg p-10 text-center text-sm text-red-600">{error}</div>;
  if (!mods || !info) return <Spinner label="Loading the diagnostic…" />;
  const nQs = mods.reduce((n, m) => n + m.questions.length, 0);
  const mins = mods.reduce((n, m) => n + m.minutes, 0);

  if (s.result) {
    return (
      <PageContainer>
        <h1 className="text-2xl font-bold text-ink sm:text-3xl">Your {info.name} diagnostic</h1>
        <p className="mt-1 text-sm text-ink-muted">A first estimate from {nQs} questions. A full practice test narrows it down.</p>
        <div className="mt-6 grid gap-8 lg:grid-cols-[1fr_340px]">
          <ExamReport info={info} r={s.result} note={`A short diagnostic gives a band, not an exact score. ${info.about_score}`} />
          <div className="lg:sticky lg:top-24 lg:self-start">
            <div className="card p-6">
              <h2 className="font-semibold text-ink">Keep going with Notenix {info.name}</h2>
              <ul className="mt-3 space-y-1.5 text-sm text-ink-muted">
                <li>{info.mocks > 0 ? `${info.mocks} full practice tests` : "Full practice tests"} with real timings ({info.mock_detail})</li>
                <li>A score estimate after every test</li>
                <li>Your skill map and a weekly study plan to test day</li>
                <li>Skill drills with worked explanations</li>
              </ul>
              {user ? (
                <Button href={`/${exam}/practice`} className="mt-5 w-full">Save this and open practice <ArrowRight size={16} /></Button>
              ) : (
                <>
                  <Button href={requestHref(exam)} className="mt-5 w-full"><Send size={15} /> Ask for access</Button>
                  <Button href="/login" variant="secondary" className="mt-2 w-full"><LogIn size={15} /> I have a Notenix account</Button>
                  <p className="mt-3 text-xs text-ink-subtle">Your diagnostic is kept in this browser and saved to your account when you sign in.</p>
                </>
              )}
            </div>
            <button onClick={() => persist({ stage: -1, answers: {}, marked: [], startedAt: null })}
              className="mt-3 w-full text-center text-xs text-ink-subtle hover:text-ink">Take the diagnostic again</button>
          </div>
        </div>
      </PageContainer>
    );
  }

  const mod = s.stage >= 0 ? mods[s.stage] : null;
  if (!mod || s.startedAt === null) {
    const next = mods[Math.max(0, s.stage)];
    return (
      <div className="mx-auto max-w-xl px-4 py-16">
        <div className="card p-8 text-center">
          <span className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-brand-50 text-brand-600">{s.stage < 0 ? <BarChart3 size={22} /> : <Clock size={22} />}</span>
          <h1 className="mt-4 text-2xl font-bold text-ink">{s.stage < 0 ? `Free ${info.name} diagnostic` : `Part ${s.stage + 1} of ${mods.length}`}</h1>
          <p className="mt-2 text-sm text-ink-muted">
            {s.stage < 0
              ? `${nQs} questions in ${mods.length} timed parts, about ${mins} minutes${info.calculator ? "" : ", no calculator"}. You'll get an estimated score band out of ${info.scale.max.toFixed(1)} and the skills costing you the most marks. No account needed.`
              : "Part done. Take a breath, then start the next part when you're ready: its clock starts when you press Start."}
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
      heading={`${info.name} diagnostic: part ${s.stage + 1} of ${mods.length}`}
      module={mod}
      answers={s.answers}
      marked={s.marked}
      secondsLeft={left}
      submitting={scoring}
      calculator={info.calculator}
      reference={false}
      onAnswer={(qid, v) => persist({ ...s, answers: { ...s.answers, [qid]: v } })}
      onToggleMark={(qid) => persist({ ...s, marked: s.marked.includes(qid) ? s.marked.filter((x) => x !== qid) : [...s.marked, qid] })}
      onSubmit={() => finishModule()}
    />
  );
}
