"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { Star, Flame, Brain, Target, ArrowRight, ClipboardList, CalendarClock, CheckCircle2, Trophy } from "lucide-react";
import { progressAPI, testsAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, StatCard, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { humanize, formatDate } from "@/lib/utils";

interface Assignment {
  assignment_id: number;
  title: string;
  subject: string;
  topic: string;
  exam_board: string;
  num_questions: number;
  due_at: string | null;
  status: string;
  assigned_by: string;
}

function dueLabel(due: string | null) {
  if (!due) return { text: "No deadline", danger: false };
  const diff = new Date(due).getTime() - Date.now();
  const days = Math.ceil(diff / 86400000);
  if (diff < 0) return { text: "Overdue", danger: true };
  if (days <= 1) return { text: "Due tomorrow", danger: true };
  if (days <= 3) return { text: `Due in ${days} days`, danger: false };
  return { text: `Due ${formatDate(due)}`, danger: false };
}

export default function StudentDashboard() {
  const { user, ready } = useAuthGuard("student");
  const [data, setData] = useState<any>(null);
  const [assignments, setAssignments] = useState<Assignment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!ready) return;
    Promise.all([
      progressAPI.dashboard().then((r) => r.data).catch(() => ({})),
      testsAPI.mine().then((r) => r.data).catch(() => []),
    ])
      .then(([d, a]) => {
        setData(d || {});
        setAssignments(Array.isArray(a) ? a : []);
      })
      .finally(() => setLoading(false));
  }, [ready]);

  if (!ready || loading) return <Spinner label="Loading your dashboard…" />;

  const pending = assignments.filter((a) => a.status !== "completed");
  const completedCount = assignments.filter((a) => a.status === "completed").length;
  const subjectStats: any[] = data?.subject_stats || [];
  const recent: any[] = data?.recent || [];

  return (
    <PageContainer>
      <PageHeader
        title={`Welcome back, ${user?.full_name?.split(" ")[0] || "there"}`}
        subtitle={data?.plan === "pro" ? "Pro member" : "Free plan"}
        actions={<Button href="/quiz" variant="secondary"><Brain size={16} /> Practise a quiz</Button>}
      />

      {/* Stats */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard label="Total XP" value={data?.xp ?? 0} icon={Star} />
        <StatCard label="Day streak" value={data?.streak ?? 0} icon={Flame} />
        <StatCard label="Tests done" value={completedCount} icon={CheckCircle2} />
        <StatCard label="Avg score" value={data?.avg_score != null ? `${data.avg_score}%` : "—"} icon={Target} />
      </div>

      {/* Assigned tests — primary focus */}
      <section className="mt-8">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-ink-subtle">
            Assigned to you {pending.length > 0 && `· ${pending.length}`}
          </h2>
          <Link href="/tests" className="text-sm font-medium text-brand-600 hover:text-brand-700">View all</Link>
        </div>

        {pending.length === 0 ? (
          <div className="card flex items-center gap-4 p-6">
            <span className="grid h-11 w-11 shrink-0 place-items-center rounded-lg bg-emerald-50 text-emerald-600">
              <CheckCircle2 size={20} />
            </span>
            <div>
              <div className="font-medium text-ink">You're all caught up</div>
              <div className="text-sm text-ink-muted">No tests due right now. Practise a quiz to keep your streak going.</div>
            </div>
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {pending.slice(0, 6).map((t) => {
              const due = dueLabel(t.due_at);
              return (
                <div key={t.assignment_id} className="card card-hover flex flex-col p-5">
                  <div className="flex items-center gap-2">
                    <span className="badge-brand">{humanize(t.subject)}</span>
                    <span className="badge-neutral">{t.exam_board}</span>
                  </div>
                  <h3 className="mt-3 font-semibold text-ink">{t.title}</h3>
                  <p className="mt-0.5 text-sm text-ink-muted">{humanize(t.topic)}</p>
                  <div className="mt-3 flex items-center gap-3 text-xs text-ink-subtle">
                    <span className="inline-flex items-center gap-1"><ClipboardList size={13} /> {t.num_questions} Q</span>
                    <span className={`inline-flex items-center gap-1 ${due.danger ? "text-amber-600" : ""}`}>
                      <CalendarClock size={13} /> {due.text}
                    </span>
                  </div>
                  <div className="mt-4 border-t border-line pt-4">
                    <Button href={`/tests/${t.assignment_id}`} size="sm" className="w-full">
                      Start test <ArrowRight size={14} />
                    </Button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </section>

      {/* Performance + activity */}
      <div className="mt-8 grid gap-6 lg:grid-cols-2">
        <div className="card p-6">
          <h2 className="flex items-center gap-2 font-semibold text-ink">
            <Target size={17} className="text-brand-600" /> Subject performance
          </h2>
          {subjectStats.length === 0 ? (
            <p className="mt-4 text-sm text-ink-muted">Complete a test or quiz to see your subject breakdown.</p>
          ) : (
            <div className="mt-5 space-y-4">
              {subjectStats.map((s: any) => (
                <div key={s.subject}>
                  <div className="mb-1 flex justify-between text-sm">
                    <span className="font-medium text-ink">{humanize(s.subject)}</span>
                    <span className="text-ink-subtle">{s.avg}% · {s.count}</span>
                  </div>
                  <div className="h-2 overflow-hidden rounded-full bg-slate-100">
                    <div className="h-full rounded-full bg-brand-600" style={{ width: `${s.avg}%` }} />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="card p-6">
          <h2 className="flex items-center gap-2 font-semibold text-ink">
            <Trophy size={17} className="text-brand-600" /> Recent activity
          </h2>
          {recent.length === 0 ? (
            <p className="mt-4 text-sm text-ink-muted">Your recent quizzes and tests will appear here.</p>
          ) : (
            <div className="mt-4 divide-y divide-line">
              {recent.map((r: any, i: number) => (
                <div key={i} className="flex items-center justify-between py-2.5">
                  <div className="text-sm">
                    <span className="font-medium text-ink">{humanize(r.subject)}</span>
                    <span className="text-ink-subtle"> · {humanize(r.topic)}</span>
                    {r.mode === "exam" && <span className="ml-1 text-xs text-brand-600">(exam)</span>}
                  </div>
                  <span className="text-sm font-semibold text-ink">{r.score}%</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </PageContainer>
  );
}
