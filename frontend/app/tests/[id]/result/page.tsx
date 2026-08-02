"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { CheckCircle2, XCircle, ArrowLeft, Trophy, Clock } from "lucide-react";
import { testsAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { cn, humanize } from "@/lib/utils";

interface QResult {
  question: string;
  options?: string[];
  your_answer: string | null;
  correct_answer: string;
  is_correct: boolean;
  explanation?: string;
}
interface Result {
  title: string;
  subject: string;
  topic: string;
  level: string;
  score: number;
  grade: string;
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

  const correct = data.results.filter((r) => r.is_correct).length;
  const scoreTone = data.score >= 70 ? "text-emerald-600" : data.score >= 50 ? "text-amber-600" : "text-red-600";

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
