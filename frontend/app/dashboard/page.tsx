"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { Star, Flame, Brain, Target, ArrowRight, ClipboardList, CalendarClock, CheckCircle2, Trophy, BookOpen, NotebookText, Bell } from "lucide-react";
import { progressAPI } from "@/lib/api";
import { loadInbox, type Inbox, type InboxItem } from "@/lib/inbox";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, StatCard, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { humanize, formatDate } from "@/lib/utils";

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
  const [inbox, setInbox] = useState<Inbox | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!ready) return;
    Promise.all([
      progressAPI.dashboard().then((r) => r.data).catch(() => ({})),
      loadInbox(),
    ])
      .then(([d, box]) => {
        setData(d || {});
        setInbox(box);
      })
      .finally(() => setLoading(false));
  }, [ready]);

  if (!ready || loading) return <Spinner label="Loading your dashboard…" />;

  const todo = inbox?.todo ?? [];
  const newCount = todo.filter((i) => i.isNew).length;
  const completedCount = (inbox?.tests ?? []).filter((a) => a.status === "completed").length;
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

      {/* From your tutor: new notes, homework to hand in, tests to sit — what students must not miss */}
      <section className="mt-8">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-ink-subtle">
            From your tutor {todo.length > 0 && `· ${todo.length} to do`}
            {newCount > 0 && <span className="rounded-full bg-brand-600 px-2 py-0.5 text-[11px] font-semibold normal-case tracking-normal text-white">{newCount} new</span>}
          </h2>
          <div className="flex gap-4 text-sm font-medium">
            <Link href="/homework" className="text-brand-600 hover:text-brand-700">Homework</Link>
            <Link href="/tests" className="text-brand-600 hover:text-brand-700">Tests</Link>
          </div>
        </div>

        {newCount > 0 && (
          <div className="mb-4 flex items-center gap-3 rounded-xl border border-brand-200 bg-brand-50 p-4 text-sm text-ink">
            <Bell size={18} className="shrink-0 text-brand-600" />
            <span>
              Your tutor has added <b>{newCount} new {newCount === 1 ? "item" : "items"}</b> since you last looked
              {todo.some((i) => i.isNew && i.kind === "homework") ? ", including homework" : ""}.
            </span>
          </div>
        )}

        {todo.length === 0 ? (
          <div className="card flex items-center gap-4 p-6">
            <span className="grid h-11 w-11 shrink-0 place-items-center rounded-lg bg-emerald-50 text-emerald-600">
              <CheckCircle2 size={20} />
            </span>
            <div>
              <div className="font-medium text-ink">You're all caught up</div>
              <div className="text-sm text-ink-muted">No homework or tests waiting. Practise a quiz to keep your streak going.</div>
            </div>
          </div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {todo.slice(0, 6).map((t) => <TodoCard key={t.key} item={t} />)}
          </div>
        )}
        {todo.length > 6 && (
          <p className="mt-3 text-sm text-ink-muted">and {todo.length - 6} more on your <Link href="/homework" className="font-medium text-brand-600">Homework</Link> and <Link href="/tests" className="font-medium text-brand-600">Tests</Link> pages.</p>
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

const KIND = {
  homework: { label: "Homework", icon: BookOpen, cls: "bg-amber-100 text-amber-800" },
  notes: { label: "Class notes", icon: NotebookText, cls: "bg-sky-100 text-sky-800" },
  test: { label: "Test", icon: ClipboardList, cls: "bg-brand-50 text-brand-700" },
} as const;

function TodoCard({ item }: { item: InboxItem }) {
  const k = KIND[item.kind];
  const due = item.kind === "notes" ? null : dueLabel(item.due_at ?? null);
  return (
    <div className={`card card-hover flex flex-col p-5 ${item.isNew ? "ring-2 ring-brand-200" : ""}`}>
      <div className="flex flex-wrap items-center gap-2">
        {item.isNew && <span className="rounded-full bg-brand-600 px-2 py-0.5 text-xs font-semibold text-white">New</span>}
        <span className={`inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs font-semibold ${k.cls}`}><k.icon size={12} /> {k.label}</span>
        {item.subject && <span className="badge-neutral">{humanize(item.subject)}</span>}
      </div>
      <h3 className="mt-3 font-semibold text-ink">{item.title}</h3>
      {due && (
        <div className={`mt-2 inline-flex items-center gap-1 text-xs ${due.danger ? "text-amber-600" : "text-ink-subtle"}`}>
          <CalendarClock size={13} /> {due.text}
        </div>
      )}
      <div className="mt-auto pt-4">
        <Button href={item.href} size="sm" className="w-full">
          {item.action} <ArrowRight size={14} />
        </Button>
      </div>
    </div>
  );
}
