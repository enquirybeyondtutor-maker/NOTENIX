"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { ClipboardList, BookOpen, Clock, CheckCircle2, ArrowRight, CalendarClock, PenLine, Hourglass, type LucideIcon } from "lucide-react";
import { testsAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, EmptyState, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { humanize, formatDate } from "@/lib/utils";

interface Assignment {
  assignment_id: number;
  title: string;
  subject: string;
  topic: string;
  level: string;
  exam_board: string;
  mode?: "mcq" | "written";
  kind?: "test" | "homework";
  num_questions: number;
  duration_minutes: number | null;
  class_label: string | null;
  assigned_by: string;
  due_at: string | null;
  status: "assigned" | "completed";
  marking_status?: "graded" | "awaiting_marking" | null;
  score: number | null;
  grade: string | null;
}

function dueLabel(due: string | null): { text: string; tone: "warning" | "neutral" | "danger" } {
  if (!due) return { text: "No deadline", tone: "neutral" };
  const diff = new Date(due).getTime() - Date.now();
  const days = Math.ceil(diff / 86400000);
  if (diff < 0) return { text: "Overdue", tone: "danger" };
  if (days <= 1) return { text: "Due tomorrow", tone: "warning" };
  if (days <= 3) return { text: `Due in ${days} days`, tone: "warning" };
  return { text: `Due ${formatDate(due)}`, tone: "neutral" };
}

export default function AssignmentBoard({ kind }: { kind: "test" | "homework" }) {
  const { ready } = useAuthGuard("student");
  const [items, setItems] = useState<Assignment[]>([]);
  const [loading, setLoading] = useState(true);

  const homework = kind === "homework";
  const icon: LucideIcon = homework ? BookOpen : ClipboardList;

  useEffect(() => {
    if (!ready) return;
    testsAPI
      .mine()
      .then(({ data }) => setItems(data.filter((a: Assignment) => (a.kind || "test") === kind)))
      .catch(() => setItems([]))
      .finally(() => setLoading(false));
  }, [ready, kind]);

  const todo = items.filter((i) => i.status !== "completed");
  const done = items.filter((i) => i.status === "completed");

  const startLabel = (t: Assignment) =>
    homework ? "Start homework" : t.mode === "written" ? "Write answers" : "Start test";

  if (!ready || loading) return <Spinner label={homework ? "Loading your homework…" : "Loading your tests…"} />;

  return (
    <PageContainer>
      <PageHeader
        icon={icon}
        title={homework ? "My homework" : "My tests"}
        subtitle={homework ? "Homework set by your teachers — take your time, no exam timer." : "Assessments assigned to you by your teachers."}
      />

      {items.length === 0 ? (
        <EmptyState
          icon={icon}
          title={homework ? "No homework yet" : "No tests assigned yet"}
          desc={homework
            ? "When a teacher sets you homework, it'll appear here for you to complete."
            : "When a teacher assigns you a test, it'll appear here. In the meantime, you can practise on your own."}
          action={homework ? undefined : <Button href="/quiz">Practise a quiz</Button>}
        />
      ) : (
        <div className="space-y-8">
          <section>
            <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-ink-subtle">
              To do · {todo.length}
            </h2>
            {todo.length === 0 ? (
              <div className="card p-6 text-sm text-ink-muted">You're all caught up. 🎉</div>
            ) : (
              <div className="grid gap-4 sm:grid-cols-2">
                {todo.map((t) => {
                  const due = dueLabel(t.due_at);
                  return (
                    <div key={t.assignment_id} className="card card-hover flex flex-col p-5">
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <div className="flex flex-wrap items-center gap-2">
                            <span className="badge-brand">{humanize(t.subject)}</span>
                            {t.exam_board && <span className="badge-neutral">{t.exam_board}</span>}
                            {t.mode === "written" && (
                              <span className="inline-flex items-center gap-1 badge-neutral"><PenLine size={11} /> Written</span>
                            )}
                            {t.class_label && <span className="badge-neutral">{t.class_label}</span>}
                          </div>
                          <h3 className="mt-3 font-semibold text-ink">{t.title}</h3>
                          <p className="mt-0.5 text-sm text-ink-muted">{humanize(t.topic)}</p>
                        </div>
                      </div>
                      <div className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-ink-subtle">
                        <span className="inline-flex items-center gap-1">
                          <ClipboardList size={13} /> {t.num_questions} questions
                        </span>
                        {t.duration_minutes && (
                          <span className="inline-flex items-center gap-1">
                            <Clock size={13} /> {t.duration_minutes} min
                          </span>
                        )}
                        <span className={`inline-flex items-center gap-1 ${due.tone === "danger" ? "text-red-600" : due.tone === "warning" ? "text-amber-600" : ""}`}>
                          <CalendarClock size={13} /> {due.text}
                        </span>
                      </div>
                      <div className="mt-4 flex items-center justify-between border-t border-line pt-4">
                        <span className="text-xs text-ink-subtle">Set by {t.assigned_by}</span>
                        <Button href={`/tests/${t.assignment_id}`} size="sm">
                          {startLabel(t)} <ArrowRight size={14} />
                        </Button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </section>

          {done.length > 0 && (
            <section>
              <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-ink-subtle">
                Completed · {done.length}
              </h2>
              <div className="card divide-y divide-line">
                {done.map((t) => {
                  const awaiting = t.marking_status === "awaiting_marking";
                  return (
                    <Link
                      key={t.assignment_id}
                      href={`/tests/${t.assignment_id}/result`}
                      className="flex items-center justify-between gap-3 p-4 transition-colors hover:bg-slate-50"
                    >
                      <div className="flex items-center gap-3">
                        <span className={`grid h-9 w-9 place-items-center rounded-lg ${awaiting ? "bg-amber-50 text-amber-600" : "bg-emerald-50 text-emerald-600"}`}>
                          {awaiting ? <Hourglass size={16} /> : <CheckCircle2 size={16} />}
                        </span>
                        <div>
                          <div className="text-sm font-medium text-ink">{t.title}</div>
                          <div className="text-xs text-ink-subtle">
                            {humanize(t.subject)}{t.exam_board ? ` · ${t.exam_board}` : ""}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        {awaiting ? (
                          <span className="text-xs font-medium text-amber-600">Awaiting marking</span>
                        ) : (
                          <div className="text-right">
                            <div className="text-sm font-semibold text-ink">{t.score}%</div>
                            <div className="text-xs text-ink-subtle">Grade {t.grade}</div>
                          </div>
                        )}
                        <ArrowRight size={16} className="text-ink-subtle" />
                      </div>
                    </Link>
                  );
                })}
              </div>
            </section>
          )}
        </div>
      )}
    </PageContainer>
  );
}
