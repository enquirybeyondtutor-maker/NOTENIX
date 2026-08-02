"use client";
import { useEffect, useMemo, useState, useCallback } from "react";
import { useRouter, useParams } from "next/navigation";
import { Clock, ChevronLeft, ChevronRight, Flag, AlertCircle, CheckCircle2, Loader2 } from "lucide-react";
import { testsAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Logo } from "@/components/ui/Logo";
import { cn, humanize } from "@/lib/utils";

interface Question {
  question: string;
  options: string[];
}
interface TestData {
  assignment_id: number;
  title: string;
  subject: string;
  topic: string;
  level: string;
  exam_board: string;
  duration_minutes: number | null;
  questions: Question[];
}

function fmtTime(s: number) {
  const m = Math.floor(s / 60);
  const sec = s % 60;
  return `${m}:${sec.toString().padStart(2, "0")}`;
}

export default function AttemptTestPage() {
  const router = useRouter();
  const params = useParams();
  const id = params?.id as string;
  const { ready } = useAuthGuard("student");

  const [test, setTest] = useState<TestData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [remaining, setRemaining] = useState<number | null>(null);
  const [startedAt] = useState(() => Date.now());
  const [submitting, setSubmitting] = useState(false);
  const [reviewOpen, setReviewOpen] = useState(false);

  useEffect(() => {
    if (!ready) return;
    testsAPI
      .get(id)
      .then(({ data }) => {
        setTest(data);
        if (data.duration_minutes) setRemaining(data.duration_minutes * 60);
      })
      .catch((e) => setError(e.response?.data?.detail || "Could not load this test."))
      .finally(() => setLoading(false));
  }, [ready, id]);

  const handleSubmit = useCallback(async () => {
    if (!test || submitting) return;
    setSubmitting(true);
    const ordered = test.questions.map((_, i) => answers[i] ?? "");
    try {
      await testsAPI.submit(id, {
        answers: ordered,
        time_taken_seconds: Math.round((Date.now() - startedAt) / 1000),
      });
      router.replace(`/tests/${id}/result`);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Submission failed. Please try again.");
      setSubmitting(false);
    }
  }, [test, submitting, answers, id, startedAt, router]);

  // countdown
  useEffect(() => {
    if (remaining === null) return;
    if (remaining <= 0) {
      handleSubmit();
      return;
    }
    const t = setInterval(() => setRemaining((r) => (r === null ? r : r - 1)), 1000);
    return () => clearInterval(t);
  }, [remaining, handleSubmit]);

  const answeredCount = useMemo(() => Object.values(answers).filter(Boolean).length, [answers]);

  if (!ready || loading) return <Spinner label="Preparing your test…" />;

  if (error && !test) {
    return (
      <div className="mx-auto max-w-md px-4 py-24 text-center">
        <span className="mx-auto grid h-12 w-12 place-items-center rounded-xl bg-red-50 text-red-600">
          <AlertCircle size={22} />
        </span>
        <h1 className="mt-4 text-lg font-semibold text-ink">Can't open this test</h1>
        <p className="mt-1.5 text-sm text-ink-muted">{error}</p>
        <Button href="/tests" variant="secondary" className="mt-6">Back to my tests</Button>
      </div>
    );
  }
  if (!test) return null;

  const q = test.questions[current];
  const total = test.questions.length;
  const lowTime = remaining !== null && remaining <= 60;

  return (
    <div className="fixed inset-0 z-[60] flex flex-col bg-canvas">
      {/* Exam top bar */}
      <header className="flex items-center justify-between border-b border-line bg-white px-4 py-3 sm:px-6">
        <div className="flex items-center gap-3">
          <Logo href={null} />
          <div className="hidden border-l border-line pl-3 sm:block">
            <div className="text-sm font-semibold text-ink">{test.title}</div>
            <div className="text-xs text-ink-subtle">{humanize(test.subject)} · {test.exam_board}</div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          {remaining !== null && (
            <div className={cn("flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-sm font-semibold tabular-nums",
              lowTime ? "border-red-200 bg-red-50 text-red-600" : "border-line text-ink")}>
              <Clock size={15} /> {fmtTime(remaining)}
            </div>
          )}
          <Button size="sm" onClick={() => setReviewOpen(true)}>
            <Flag size={14} /> Finish
          </Button>
        </div>
      </header>

      {/* Progress */}
      <div className="h-1 w-full bg-slate-100">
        <div className="h-full bg-brand-600 transition-all" style={{ width: `${((current + 1) / total) * 100}%` }} />
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Question navigator */}
        <aside className="hidden w-52 shrink-0 overflow-y-auto border-r border-line bg-white p-4 lg:block">
          <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-ink-subtle">
            Questions
          </div>
          <div className="grid grid-cols-5 gap-2">
            {test.questions.map((_, i) => (
              <button
                key={i}
                onClick={() => setCurrent(i)}
                className={cn(
                  "grid h-9 place-items-center rounded-lg border text-sm font-medium transition-colors",
                  i === current
                    ? "border-brand-600 bg-brand-600 text-white"
                    : answers[i]
                    ? "border-brand-200 bg-brand-50 text-brand-700"
                    : "border-line text-ink-muted hover:bg-slate-50"
                )}
              >
                {i + 1}
              </button>
            ))}
          </div>
          <div className="mt-4 text-xs text-ink-subtle">{answeredCount} of {total} answered</div>
        </aside>

        {/* Question */}
        <main className="flex-1 overflow-y-auto">
          <div className="mx-auto max-w-2xl px-4 py-8 sm:px-6">
            <div className="text-sm font-medium text-ink-subtle">Question {current + 1} of {total}</div>
            <h2 className="mt-2 text-lg font-semibold leading-relaxed text-ink sm:text-xl">{q.question}</h2>

            <div className="mt-6 space-y-3">
              {q.options.map((opt) => {
                const selected = answers[current] === opt;
                return (
                  <button
                    key={opt}
                    onClick={() => setAnswers((a) => ({ ...a, [current]: opt }))}
                    className={cn("option-btn flex items-center gap-3", selected && "selected")}
                  >
                    <span className={cn("grid h-5 w-5 shrink-0 place-items-center rounded-full border",
                      selected ? "border-brand-600 bg-brand-600 text-white" : "border-line-strong")}>
                      {selected && <CheckCircle2 size={14} />}
                    </span>
                    <span>{opt}</span>
                  </button>
                );
              })}
            </div>

            <div className="mt-8 flex items-center justify-between">
              <Button variant="secondary" size="sm" disabled={current === 0} onClick={() => setCurrent((c) => Math.max(0, c - 1))}>
                <ChevronLeft size={16} /> Previous
              </Button>
              {current < total - 1 ? (
                <Button size="sm" onClick={() => setCurrent((c) => Math.min(total - 1, c + 1))}>
                  Next <ChevronRight size={16} />
                </Button>
              ) : (
                <Button size="sm" onClick={() => setReviewOpen(true)}>
                  Review &amp; submit <Flag size={14} />
                </Button>
              )}
            </div>
          </div>
        </main>
      </div>

      {/* Review / submit modal */}
      {reviewOpen && (
        <div className="fixed inset-0 z-[70] flex items-center justify-center bg-ink/30 p-4" onClick={() => !submitting && setReviewOpen(false)}>
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-lg font-semibold text-ink">Submit your test?</h3>
            <p className="mt-1.5 text-sm text-ink-muted">
              You've answered <span className="font-semibold text-ink">{answeredCount}</span> of {total} questions.
              {answeredCount < total && " Unanswered questions will be marked as incorrect."}
            </p>
            {error && (
              <div className="mt-4 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
                <AlertCircle size={16} /> {error}
              </div>
            )}
            <div className="mt-6 flex justify-end gap-2">
              <Button variant="secondary" onClick={() => setReviewOpen(false)} disabled={submitting}>
                Keep working
              </Button>
              <Button onClick={handleSubmit} loading={submitting}>
                {submitting ? "Submitting…" : "Submit test"}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
