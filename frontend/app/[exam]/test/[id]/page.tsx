"use client";
import { useCallback, useEffect, useRef, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Coffee, Clock, ArrowRight } from "lucide-react";
import { useAuthGuard } from "@/lib/guard";
import { examAPI } from "@/lib/examApi";
import type { SatModule } from "@/lib/satApi";
import { Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import Runner from "@/components/sat/Runner";

type State = {
  status: "in_progress" | "done"; exam: string; name: string; title: string; kind: string; stage: number; stages: number;
  module: SatModule; seconds_left: number | null; started: boolean; calculator: boolean;
  answers: Record<string, string>; marked: string[]; break_before: boolean;
};

// One sitting of an exam-engine practice test (e.g. TMUA Paper 1 then Paper 2). The server
// keeps the clock and the answers (autosaved every few seconds).
export default function ExamTestPage() {
  const { ready } = useAuthGuard("student");
  const { exam, id } = useParams<{ exam: string; id: string }>();
  const router = useRouter();
  const [st, setSt] = useState<State | null>(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [marked, setMarked] = useState<string[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const dirty = useRef(false);

  const load = useCallback(async (openModule = false) => {
    try {
      const { data } = await examAPI.attempt(id, openModule);
      if (data.status === "done") return router.replace(`/${data.exam || exam}/test/${id}/result`);
      setSt(data);
      setAnswers(data.answers || {});
      setMarked(data.marked || []);
      dirty.current = false;
    } catch (e: any) {
      setError(e.response?.data?.detail || "Couldn't load this test.");
    }
  }, [id, exam, router]);

  useEffect(() => { if (ready) load(); }, [ready, load]);

  useEffect(() => {
    if (!st?.started) return;
    const t = setInterval(() => {
      if (!dirty.current) return;
      dirty.current = false;
      examAPI.save(id, { module: st.module.key, answers, marked }).catch(() => { dirty.current = true; });
    }, 5000);
    return () => clearInterval(t);
  }, [st, id, answers, marked]);

  const submit = useCallback(async () => {
    if (!st || submitting) return;
    setSubmitting(true);
    try {
      const { data } = await examAPI.submit(id, { module: st.module.key, answers, marked });
      if (data.status === "done") return router.replace(`/${st.exam}/test/${id}/result`);
      await load();
    } catch (e: any) {
      setError(e.response?.data?.detail || "Couldn't submit. Check your connection and try again.");
    } finally {
      setSubmitting(false);
    }
  }, [st, submitting, id, answers, marked, router, load]);

  if (error) return <div className="mx-auto max-w-lg p-10 text-center text-sm text-red-600">{error}</div>;
  if (!ready || !st) return <Spinner label="Loading your test…" />;

  const part = st.stages > 1 ? ` (part ${st.stage + 1} of ${st.stages})` : "";
  if (!st.started) {
    return (
      <div className="mx-auto max-w-xl px-4 py-16">
        <div className="card p-8 text-center">
          {st.break_before ? (
            <>
              <span className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-amber-50 text-amber-600"><Coffee size={22} /></span>
              <h1 className="mt-4 text-2xl font-bold text-ink">Part {st.stage} done</h1>
              <p className="mt-2 text-sm text-ink-muted">Take a short break if you need one. The next clock doesn&apos;t start until you press Start.</p>
            </>
          ) : (
            <>
              <span className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-brand-50 text-brand-600"><Clock size={22} /></span>
              <h1 className="mt-4 text-2xl font-bold text-ink">{st.title}</h1>
            </>
          )}
          <div className="mt-6 rounded-xl border border-line p-4 text-left text-sm">
            <div className="font-semibold text-ink">{st.module.title}{part}</div>
            <div className="mt-1 text-ink-muted">{st.module.questions.length} questions · {st.module.minutes} minutes</div>
            {!st.calculator && <div className="mt-1 text-ink-muted">No calculator, as in the real {st.name}. Have paper and a pen ready.</div>}
          </div>
          <Button className="mt-6" onClick={() => load(true)}>Start {st.module.title} <ArrowRight size={16} /></Button>
        </div>
      </div>
    );
  }

  return (
    <Runner
      key={st.module.key}
      heading={`${st.title}${part}`}
      module={st.module}
      answers={answers}
      marked={marked}
      secondsLeft={st.seconds_left ?? st.module.minutes * 60}
      submitting={submitting}
      calculator={st.calculator}
      reference={false}
      onAnswer={(qid, v) => { setAnswers((a) => ({ ...a, [qid]: v })); dirty.current = true; }}
      onToggleMark={(qid) => { setMarked((m) => (m.includes(qid) ? m.filter((x) => x !== qid) : [...m, qid])); dirty.current = true; }}
      onSubmit={() => submit()}
    />
  );
}
