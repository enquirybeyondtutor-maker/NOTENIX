"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Coffee, Clock, ArrowRight } from "lucide-react";
import { useAuthGuard } from "@/lib/guard";
import { satAPI, type SatModule } from "@/lib/satApi";
import { Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import Runner from "@/components/sat/Runner";

type State = {
  status: "in_progress" | "done"; title: string; stage: number; stages: number; module: SatModule;
  seconds_left: number | null; started: boolean; answers: Record<string, string>; marked: string[]; break_before: boolean;
};

// One sitting of a Notenix SAT practice test. The server keeps the clock, the answers
// (autosaved every few seconds) and which Module 2 each section gets.
export default function SatTestPage() {
  const { ready } = useAuthGuard("student");
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [st, setSt] = useState<State | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [marked, setMarked] = useState<string[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const dirty = useRef(false);

  const load = useCallback(async (openModule = false) => {
    try {
      const { data } = await satAPI.attempt(id, openModule);
      if (data.status === "done") return router.replace(`/sat/test/${id}/result`);
      setSt(data);
      setAnswers(data.answers || {});
      setMarked(data.marked || []);
      dirty.current = false;
    } catch (e: any) {
      setError(e.response?.data?.detail || "Couldn't load this test.");
    }
  }, [id, router]);

  useEffect(() => { if (ready) load(); }, [ready, load]);

  // Autosave every 5 seconds while answers change.
  useEffect(() => {
    if (!st?.started) return;
    const t = setInterval(() => {
      if (!dirty.current) return;
      dirty.current = false;
      satAPI.save(id, { module: st.module.key, answers, marked }).catch(() => { dirty.current = true; });
    }, 5000);
    return () => clearInterval(t);
  }, [st, id, answers, marked]);

  const submit = useCallback(async () => {
    if (!st || submitting) return;
    setSubmitting(true);
    try {
      const { data } = await satAPI.submit(id, { module: st.module.key, answers, marked });
      if (data.status === "done") return router.replace(`/sat/test/${id}/result`);
      await load();
    } catch (e: any) {
      setError(e.response?.data?.detail || "Couldn't submit. Check your connection and try again.");
    } finally {
      setSubmitting(false);
    }
  }, [st, submitting, id, answers, marked, router, load]);

  if (error) return <div className="mx-auto max-w-lg p-10 text-center text-sm text-red-600">{error}</div>;
  if (!ready || !st) return <Spinner label="Loading your test…" />;

  const section = st.module.section === "rw" ? "Section 1: Reading and Writing" : "Section 2: Math";
  const moduleNo = st.stage % 2 === 0 ? 1 : 2;

  if (!st.started) {
    return (
      <div className="mx-auto max-w-xl px-4 py-16">
        <div className="card p-8 text-center">
          {st.break_before ? (
            <>
              <span className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-amber-50 text-amber-600"><Coffee size={22} /></span>
              <h1 className="mt-4 text-2xl font-bold text-ink">Reading and Writing done</h1>
              <p className="mt-2 text-sm text-ink-muted">
                On test day you get a 10-minute break here. Stand up, drink some water, then start Math when you&apos;re ready.
                The Math clock doesn&apos;t start until you press Start.
              </p>
            </>
          ) : (
            <>
              <span className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-brand-50 text-brand-600"><Clock size={22} /></span>
              <h1 className="mt-4 text-2xl font-bold text-ink">{st.title}</h1>
            </>
          )}
          <div className="mt-6 rounded-xl border border-line p-4 text-left text-sm">
            <div className="font-semibold text-ink">{section}, Module {moduleNo}</div>
            <div className="mt-1 text-ink-muted">{st.module.questions.length} questions · {st.module.minutes} minutes</div>
            {st.module.section === "math" && <div className="mt-1 text-ink-muted">Calculator (Desmos) and reference sheet available for every question.</div>}
            {moduleNo === 2 && <div className="mt-1 text-ink-muted">Module 2 has been chosen from how you did in Module 1, as on the real test.</div>}
          </div>
          <Button className="mt-6" onClick={() => load(true)}>Start Module {moduleNo} <ArrowRight size={16} /></Button>
        </div>
      </div>
    );
  }

  return (
    <Runner
      key={st.module.key}
      heading={`${section}, Module ${moduleNo}`}
      module={st.module}
      answers={answers}
      marked={marked}
      secondsLeft={st.seconds_left ?? st.module.minutes * 60}
      submitting={submitting}
      onAnswer={(qid, v) => { setAnswers((a) => ({ ...a, [qid]: v })); dirty.current = true; }}
      onToggleMark={(qid) => { setMarked((m) => (m.includes(qid) ? m.filter((x) => x !== qid) : [...m, qid])); dirty.current = true; }}
      onSubmit={() => submit()}
    />
  );
}
