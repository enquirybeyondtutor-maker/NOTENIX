"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { CheckCircle2, XCircle, ArrowLeft, Trophy, Clock, Hourglass, PenLine } from "lucide-react";
import { testsAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { cn, humanize } from "@/lib/utils";

interface QResult {
  question: string;
  options?: string[];
  image?: string | null;
  answer_images?: string[] | null;
  your_answer: string | null;
  // MCQ
  correct_answer?: string;
  is_correct?: boolean;
  explanation?: string;
  // written
  marks?: number;
  marks_awarded?: number | null;
  feedback?: string | null;
  model_answer?: string | null;
}
interface Result {
  title: string;
  subject: string;
  topic: string;
  level: string;
  mode?: "mcq" | "written";
  status?: "graded" | "awaiting_marking";
  score: number | null;
  grade: string | null;
  time_taken_seconds: number | null;
  results: QResult[];
}

export default function TestResultPage() {
  const params = useParams();
  const id = params?.id as string;
  const { ready } = useAuthGuard("student");
  const [data, setData] = useState<Result | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!ready) return;
    testsAPI
      .result(id)
      .then(({ data }) => setData(data))
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [ready, id]);

  if (!ready || loading) return <Spinner label="Loading your result…" />;
  if (!data) {
    return (
      <PageContainer>
        <div className="card p-10 text-center text-ink-muted">Result not found.</div>
      </PageContainer>
    );
  }

  const isWritten = data.mode === "written";
  const pending = data.status === "awaiting_marking";

  // ── Written, awaiting a teacher/admin to mark ──
  if (isWritten && pending) {
    return (
      <PageContainer>
        <Link href="/tests" className="mb-4 inline-flex items-center gap-1.5 text-sm text-ink-muted hover:text-ink">
          <ArrowLeft size={15} /> Back to my tests
        </Link>
        <div className="card overflow-hidden">
          <div className="flex items-start gap-4 border-b border-line p-6 sm:p-8">
            <span className="grid h-12 w-12 shrink-0 place-items-center rounded-xl bg-amber-50 text-amber-600">
              <Hourglass size={22} />
            </span>
            <div>
              <div className="badge-brand mb-2">{humanize(data.subject)}</div>
              <h1 className="text-xl font-bold text-ink">{data.title}</h1>
              <p className="mt-1.5 text-sm text-ink-muted">
                Your answers were submitted and are <span className="font-semibold text-ink">awaiting marking</span>.
                You'll see your marks and feedback here once your teacher has marked them.
              </p>
            </div>
          </div>
        </div>

        <h2 className="mb-3 mt-8 text-sm font-semibold uppercase tracking-wide text-ink-subtle">Your answers</h2>
        <div className="space-y-4">
          {data.results.map((r, i) => (
            <div key={i} className="card p-5">
              <div className="flex items-center justify-between">
                <div className="text-xs font-medium text-ink-subtle">Question {i + 1}</div>
                {r.marks != null && (
                  <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-semibold text-ink-muted">
                    {r.marks} {r.marks === 1 ? "mark" : "marks"}
                  </span>
                )}
              </div>
              <p className="mt-1 whitespace-pre-line font-medium text-ink">{r.question}</p>
              {r.image && <img src={r.image} alt="Question figure" className="mt-3 max-h-80 w-auto max-w-full rounded-lg border border-line" />}
              {(r.your_answer || !(r.answer_images?.length)) && (
                <div className="mt-3 whitespace-pre-line rounded-lg bg-slate-50 p-3 text-sm text-ink-muted">
                  {r.your_answer || "— (not answered)"}
                </div>
              )}
              {(r.answer_images?.length ?? 0) > 0 && (
                <div className="mt-3 flex flex-wrap gap-3">
                  {r.answer_images!.map((src, j) => (
                    <img key={j} src={src} alt={`Your answer photo ${j + 1}`} className="max-h-72 w-auto max-w-full rounded-lg border border-line" />
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
        <div className="mt-8 flex justify-center">
          <Button href="/tests" variant="secondary">Back to my tests</Button>
        </div>
      </PageContainer>
    );
  }

  const scoreTone = (data.score ?? 0) >= 70 ? "text-emerald-600" : (data.score ?? 0) >= 50 ? "text-amber-600" : "text-red-600";

  // ── Written, marked ──
  if (isWritten) {
    const totalMarks = data.results.reduce((s, r) => s + (r.marks ?? 0), 0);
    const totalAwarded = data.results.reduce((s, r) => s + (r.marks_awarded ?? 0), 0);
    return (
      <PageContainer>
        <Link href="/tests" className="mb-4 inline-flex items-center gap-1.5 text-sm text-ink-muted hover:text-ink">
          <ArrowLeft size={15} /> Back to my tests
        </Link>

        <div className="card overflow-hidden">
          <div className="grid gap-6 border-b border-line p-6 sm:grid-cols-[1.4fr_1fr_1fr] sm:p-8">
            <div>
              <div className="badge-brand mb-2">{humanize(data.subject)}</div>
              <h1 className="text-xl font-bold text-ink">{data.title}</h1>
              <p className="mt-1 text-sm text-ink-muted">{humanize(data.topic)}</p>
            </div>
            <div className="flex flex-col items-start justify-center sm:items-center">
              <div className="text-xs uppercase tracking-wide text-ink-subtle">Marks</div>
              <div className={cn("text-4xl font-bold", scoreTone)}>{totalAwarded}<span className="text-2xl text-ink-subtle">/{totalMarks}</span></div>
              <div className="mt-1 text-xs text-ink-subtle">{data.score}%</div>
            </div>
            <div className="flex flex-col items-start justify-center sm:items-center">
              <div className="text-xs uppercase tracking-wide text-ink-subtle">Estimated grade</div>
              <div className="flex items-center gap-1.5 text-4xl font-bold text-brand-600">
                <Trophy size={26} /> {data.grade}
              </div>
            </div>
          </div>
        </div>

        <h2 className="mb-3 mt-8 text-sm font-semibold uppercase tracking-wide text-ink-subtle">Examiner feedback</h2>
        <div className="space-y-4">
          {data.results.map((r, i) => {
            const full = (r.marks_awarded ?? 0) >= (r.marks ?? 0);
            return (
              <div key={i} className="card p-5">
                <div className="flex items-center justify-between">
                  <div className="text-xs font-medium text-ink-subtle">Question {i + 1}</div>
                  <span className={cn("rounded-full px-2.5 py-0.5 text-xs font-semibold",
                    full ? "bg-emerald-50 text-emerald-700" : "bg-amber-50 text-amber-700")}>
                    {r.marks_awarded ?? 0} / {r.marks ?? 0} marks
                  </span>
                </div>
                <p className="mt-1 whitespace-pre-line font-medium text-ink">{r.question}</p>
                {r.image && <img src={r.image} alt="Question figure" className="mt-3 max-h-80 w-auto max-w-full rounded-lg border border-line" />}

                <div className="mt-3 whitespace-pre-line rounded-lg bg-slate-50 p-3 text-sm text-ink-muted">
                  <span className="mb-1 flex items-center gap-1.5 font-medium text-ink"><PenLine size={13} /> Your answer</span>
                  {r.your_answer || (r.answer_images?.length ? "(see uploaded photo)" : "— (not answered)")}
                  {(r.answer_images?.length ?? 0) > 0 && (
                    <div className="mt-2 flex flex-wrap gap-3">
                      {r.answer_images!.map((src, j) => (
                        <img key={j} src={src} alt={`Your answer photo ${j + 1}`} className="max-h-72 w-auto max-w-full rounded-lg border border-line" />
                      ))}
                    </div>
                  )}
                </div>

                {r.feedback && (
                  <div className="mt-3 rounded-lg border border-brand-100 bg-brand-50/60 p-3 text-sm text-ink-muted">
                    <span className="font-medium text-ink">Feedback: </span>{r.feedback}
                  </div>
                )}
                {r.model_answer && (
                  <div className="mt-3 whitespace-pre-line rounded-lg bg-slate-50 p-3 text-sm text-ink-muted">
                    <span className="font-medium text-ink">Model answer: </span>{r.model_answer}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <div className="mt-8 flex justify-center">
          <Button href="/tests" variant="secondary">Back to my tests</Button>
        </div>
      </PageContainer>
    );
  }

  // ── MCQ (unchanged) ──
  const correct = data.results.filter((r) => r.is_correct).length;

  return (
    <PageContainer>
      <Link href="/tests" className="mb-4 inline-flex items-center gap-1.5 text-sm text-ink-muted hover:text-ink">
        <ArrowLeft size={15} /> Back to my tests
      </Link>

      {/* Score summary */}
      <div className="card overflow-hidden">
        <div className="grid gap-6 border-b border-line p-6 sm:grid-cols-[1.4fr_1fr_1fr] sm:p-8">
          <div>
            <div className="badge-brand mb-2">{humanize(data.subject)}</div>
            <h1 className="text-xl font-bold text-ink">{data.title}</h1>
            <p className="mt-1 text-sm text-ink-muted">{humanize(data.topic)}</p>
          </div>
          <div className="flex flex-col items-start justify-center sm:items-center">
            <div className="text-xs uppercase tracking-wide text-ink-subtle">Score</div>
            <div className={cn("text-4xl font-bold", scoreTone)}>{data.score}%</div>
            <div className="mt-1 text-xs text-ink-subtle">{correct} of {data.results.length} correct</div>
          </div>
          <div className="flex flex-col items-start justify-center sm:items-center">
            <div className="text-xs uppercase tracking-wide text-ink-subtle">Estimated grade</div>
            <div className="flex items-center gap-1.5 text-4xl font-bold text-brand-600">
              <Trophy size={26} /> {data.grade}
            </div>
            {data.time_taken_seconds != null && (
              <div className="mt-1 inline-flex items-center gap-1 text-xs text-ink-subtle">
                <Clock size={12} /> {Math.floor(data.time_taken_seconds / 60)}m {data.time_taken_seconds % 60}s
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Question breakdown */}
      <h2 className="mb-3 mt-8 text-sm font-semibold uppercase tracking-wide text-ink-subtle">
        Question review
      </h2>
      <div className="space-y-4">
        {data.results.map((r, i) => (
          <div key={i} className="card p-5">
            <div className="flex items-start gap-3">
              <span className={cn("mt-0.5 grid h-6 w-6 shrink-0 place-items-center rounded-full",
                r.is_correct ? "bg-emerald-50 text-emerald-600" : "bg-red-50 text-red-600")}>
                {r.is_correct ? <CheckCircle2 size={16} /> : <XCircle size={16} />}
              </span>
              <div className="flex-1">
                <div className="text-xs font-medium text-ink-subtle">Question {i + 1}</div>
                <p className="mt-1 font-medium text-ink">{r.question}</p>
                {r.image && <img src={r.image} alt="Question figure" className="mt-3 max-h-80 w-auto max-w-full rounded-lg border border-line" />}

                <div className="mt-3 space-y-1.5 text-sm">
                  {!r.is_correct && (
                    <div className="text-red-600">
                      <span className="text-ink-subtle">Your answer:</span> {r.your_answer || "— (not answered)"}
                    </div>
                  )}
                  <div className="text-emerald-700">
                    <span className="text-ink-subtle">Correct answer:</span> {r.correct_answer}
                  </div>
                </div>

                {r.explanation && (
                  <div className="mt-3 rounded-lg bg-slate-50 p-3 text-sm text-ink-muted">
                    <span className="font-medium text-ink">Why: </span>{r.explanation}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 flex justify-center">
        <Button href="/tests" variant="secondary">Back to my tests</Button>
      </div>
    </PageContainer>
  );
}
