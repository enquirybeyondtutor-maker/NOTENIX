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
import { MathText } from "@/components/MathText";

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
  purged?: boolean;
  retention_days?: number;
  score: number | null;
  grade: string | null;
  time_taken_seconds: number | null;
  results: QResult[];
  tmua?: Tmua | null;
}

// TMUA extras from the API: a 1.0–9.0 estimate for any TMUA paper; for the Mock Series also
// the combined two-paper score and the rank (see backend/services/series_results.py).
interface Rank { rank: number; of: number; average: number | null; ranked: boolean }
interface Tmua {
  paper_score: number;
  right: number;
  total: number;
  scale_max: number;
  about: string;
  series: null | {
    mock: string;
    paper: number;
    paper_rank: Rank;
    combined: { score: number; right: number; total: number } | null;
    combined_rank: Rank | null;
    other_paper: { paper: number; title: string; assignment_id: number | null; done: boolean } | null;
    window: { start: string; end: string; open: boolean } | null;
  };
}

const ordinal = (n: number) => {
  const s = n % 100 >= 11 && n % 100 <= 13 ? "th" : ({ 1: "st", 2: "nd", 3: "rd" } as Record<number, string>)[n % 10] ?? "th";
  return `${n}${s}`;
};

// The API sends UTC without a zone; show it as UK time, like the series page does.
const ukTime = (iso: string) =>
  new Date(iso.endsWith("Z") ? iso : `${iso}Z`).toLocaleString("en-GB", {
    timeZone: "Europe/London", weekday: "short", day: "numeric", month: "short", hour: "numeric", minute: "2-digit",
  }) + " UK";

function RankTile({ label, r }: { label: string; r: Rank }) {
  return (
    <div className="bg-white p-5">
      <div className="text-xs font-semibold uppercase tracking-wide text-ink-subtle">{label}</div>
      {r.ranked ? (
        <>
          <div className="mt-1 text-3xl font-bold text-ink">{ordinal(r.rank)} <span className="text-lg font-semibold text-ink-subtle">of {r.of}</span></div>
          {r.average != null && <div className="mt-1 text-xs text-ink-muted">Average of everyone ranked: {r.average.toFixed(1)}</div>}
        </>
      ) : (
        <>
          <div className="mt-1 text-lg font-bold text-ink">Unranked practice</div>
          <div className="mt-1 text-xs text-ink-muted">
            {r.of > 0 ? `You'd have placed ${ordinal(r.rank)} of ${r.of}.` : "Nobody was ranked on this one."}
            {r.average != null && ` Ranked average: ${r.average.toFixed(1)}.`}
          </div>
        </>
      )}
    </div>
  );
}

function SeriesPanel({ t }: { t: Tmua }) {
  const s = t.series!;
  const max = t.scale_max.toFixed(1);
  const other = s.other_paper;
  let note: string;
  if (!s.window) note = "Ranked against everyone on the Mock Series who has sat the Baseline Mock.";
  else if (s.window.open && s.paper_rank.ranked) note = `Ranking so far. The ranked window closes ${ukTime(s.window.end)}, so your place can still change.`;
  else if (s.paper_rank.ranked) note = `Final ranking: sittings finished between ${ukTime(s.window.start)} and ${ukTime(s.window.end)}.`;
  else note = `This mock was ranked for 24 hours from ${ukTime(s.window.start)}. Later sittings are practice: your score is yours, but it doesn't change the ranking.`;
  return (
    <div className="card mt-6 overflow-hidden">
      <div className="border-b border-line px-6 py-4">
        <h2 className="font-semibold text-ink">{s.mock}: your TMUA result</h2>
      </div>
      <div className={cn("grid gap-px bg-line", s.combined_rank ? "sm:grid-cols-3" : "sm:grid-cols-2")}>
        <div className="bg-gradient-to-br from-brand-600 to-brand-700 p-5 text-white">
          <div className="text-xs font-semibold uppercase tracking-wide text-white/70">Combined TMUA score</div>
          {s.combined ? (
            <>
              <div className="mt-1 text-3xl font-bold tabular-nums">{s.combined.score.toFixed(1)} <span className="text-lg font-semibold text-white/70">/ {max}</span></div>
              <div className="mt-1 text-xs text-white/70">{s.combined.right} of {s.combined.total} right across both papers</div>
            </>
          ) : other ? (
            <>
              <div className="mt-1 text-lg font-bold">Paper {other.paper} to go</div>
              <div className="mt-1 text-xs text-white/80">Sit Paper {other.paper} to get your combined score and overall rank.</div>
              {other.assignment_id && (
                <Link href={`/tests/${other.assignment_id}`} className="mt-3 inline-block rounded-lg bg-white px-3 py-1.5 text-xs font-semibold text-brand-700 hover:bg-white/90">
                  Start Paper {other.paper}
                </Link>
              )}
            </>
          ) : (
            <div className="mt-1 text-sm text-white/80">This paper's partner isn't available yet.</div>
          )}
        </div>
        <RankTile label={`Rank · Paper ${s.paper}`} r={s.paper_rank} />
        {s.combined_rank && <RankTile label="Rank · both papers" r={s.combined_rank} />}
      </div>
      <div className="border-t border-line bg-slate-50 px-6 py-3 text-xs text-ink-muted">{note} {t.about}</div>
    </div>
  );
}

function PurgeNote({ days }: { days?: number }) {
  const weeks = days ? Math.round(days / 7) : null;
  return (
    <div className="mb-6 rounded-xl border border-line bg-slate-50 p-4 text-sm text-ink-muted">
      Your submitted answers{weeks ? ` were removed ${weeks} week${weeks === 1 ? "" : "s"} after submission` : " were removed"} for privacy.
      Your marks, grade and feedback are kept.
    </div>
  );
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
        {data.purged && <PurgeNote days={data.retention_days} />}
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
              {r.question && <p className="mt-1 whitespace-pre-line font-medium text-ink"><MathText text={r.question} /></p>}
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
        {data.purged && <PurgeNote days={data.retention_days} />}
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
                {r.question && <p className="mt-1 whitespace-pre-line font-medium text-ink"><MathText text={r.question} /></p>}
                {r.image && <img src={r.image} alt="Question figure" className="mt-3 max-h-80 w-auto max-w-full rounded-lg border border-line" />}

                <div className="mt-3 whitespace-pre-line rounded-lg bg-slate-50 p-3 text-sm text-ink-muted">
                  <span className="mb-1 flex items-center gap-1.5 font-medium text-ink"><PenLine size={13} /> Your answer</span>
                  {r.your_answer || (data.purged ? "(removed for privacy)" : (r.answer_images?.length ? "(see uploaded photo)" : "— (not answered)"))}
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
                    <span className="font-medium text-ink">Model answer: </span><MathText text={r.model_answer} />
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
          {/* TMUA papers show the 1.0–9.0 estimate; other exams their grade; no box when there's neither. */}
          <div className="flex flex-col items-start justify-center sm:items-center">
            {data.tmua ? (
              <>
                <div className="text-xs uppercase tracking-wide text-ink-subtle">
                  TMUA estimate{data.tmua.series ? ` · Paper ${data.tmua.series.paper}` : ""}
                </div>
                <div className="flex items-baseline gap-1 text-4xl font-bold tabular-nums text-brand-600">
                  {data.tmua.paper_score.toFixed(1)}<span className="text-xl font-semibold text-ink-subtle">/ {data.tmua.scale_max.toFixed(1)}</span>
                </div>
              </>
            ) : data.grade ? (
              <>
                <div className="text-xs uppercase tracking-wide text-ink-subtle">Estimated grade</div>
                <div className="flex items-center gap-1.5 text-4xl font-bold text-brand-600">
                  <Trophy size={26} /> {data.grade}
                </div>
              </>
            ) : null}
            {data.time_taken_seconds != null && (
              <div className="mt-1 inline-flex items-center gap-1 text-xs text-ink-subtle">
                <Clock size={12} /> {Math.floor(data.time_taken_seconds / 60)}m {data.time_taken_seconds % 60}s
              </div>
            )}
          </div>
        </div>
        {data.tmua && !data.tmua.series && (
          <div className="bg-slate-50 px-6 py-3 text-xs text-ink-muted sm:px-8">{data.tmua.about}</div>
        )}
      </div>

      {data.tmua?.series && <SeriesPanel t={data.tmua} />}

      {/* Question breakdown */}
      <h2 className="mb-3 mt-8 text-sm font-semibold uppercase tracking-wide text-ink-subtle">
        Question review
      </h2>
      {data.purged && <PurgeNote days={data.retention_days} />}
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
                <p className="mt-1 whitespace-pre-line font-medium text-ink"><MathText text={r.question} /></p>
                {r.image && <img src={r.image} alt="Question figure" className="mt-3 max-h-80 w-auto max-w-full rounded-lg border border-line" />}

                <div className="mt-3 space-y-1.5 text-sm">
                  {!r.is_correct && (
                    <div className="text-red-600">
                      <span className="text-ink-subtle">Your answer:</span> {r.your_answer ? <MathText text={r.your_answer} /> : (data.purged ? "(removed for privacy)" : "— (not answered)")}
                    </div>
                  )}
                  <div className="text-emerald-700">
                    <span className="text-ink-subtle">Correct answer:</span> <MathText text={r.correct_answer} />
                  </div>
                </div>

                {r.explanation && (
                  <div className="mt-3 rounded-lg bg-slate-50 p-3 text-sm text-ink-muted">
                    <span className="font-medium text-ink">Why: </span><MathText text={r.explanation} />
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
