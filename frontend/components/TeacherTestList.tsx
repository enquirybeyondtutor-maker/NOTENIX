"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { ClipboardList, BookOpen, FilePlus2, Users, CheckCircle2, ArrowRight, PenLine, type LucideIcon } from "lucide-react";
import { teacherAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, EmptyState, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { humanize, formatDate } from "@/lib/utils";

interface TestRow {
  id: number;
  title: string;
  subject: string;
  topic: string;
  level: string;
  exam_board: string;
  mode?: "mcq" | "written";
  kind?: "test" | "homework";
  num_questions: number;
  duration_minutes: number | null;
  created_at: string;
  assigned_count: number;
  completed_count: number;
  avg_score: number | null;
}

export default function TeacherTestList({ kind }: { kind: "test" | "homework" }) {
  const { ready } = useAuthGuard("teacher");
  const [tests, setTests] = useState<TestRow[]>([]);
  const [loading, setLoading] = useState(true);

  const homework = kind === "homework";
  const icon: LucideIcon = homework ? BookOpen : ClipboardList;
  const createHref = homework ? "/teacher/tests/new?kind=homework" : "/teacher/tests/new";

  useEffect(() => {
    if (!ready) return;
    teacherAPI
      .listTests()
      .then(({ data }) => setTests(data.filter((t: TestRow) => (t.kind || "test") === kind)))
      .catch(() => setTests([]))
      .finally(() => setLoading(false));
  }, [ready, kind]);

  if (!ready || loading) return <Spinner label={homework ? "Loading homework…" : "Loading tests…"} />;

  return (
    <PageContainer>
      <PageHeader
        icon={icon}
        title={homework ? "Homework" : "Tests"}
        subtitle={homework ? "Set and review homework — untimed, students can save and resume." : "Create, assign and review your assessments."}
        actions={
          <Button href={createHref}>
            <FilePlus2 size={16} /> {homework ? "Set homework" : "Create test"}
          </Button>
        }
      />

      {tests.length === 0 ? (
        <EmptyState
          icon={icon}
          title={homework ? "No homework yet" : "No tests yet"}
          desc={homework
            ? "Set your first homework — any question type works, it's untimed, and students can finish it in their own time."
            : "Create your first assessment — build it by hand or let AI generate board-aligned questions in seconds."}
          action={<Button href={createHref}><FilePlus2 size={16} /> {homework ? "Set your first homework" : "Create your first test"}</Button>}
        />
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {tests.map((t) => (
            <Link key={t.id} href={`/teacher/tests/${t.id}`} className="card card-hover flex flex-col p-5">
              <div className="flex flex-wrap items-center gap-2">
                <span className="badge-brand">{humanize(t.subject)}</span>
                <span className="badge-neutral">{t.level}</span>
                {t.exam_board && <span className="badge-neutral">{t.exam_board}</span>}
                {t.mode === "written" && <span className="inline-flex items-center gap-1 badge-neutral"><PenLine size={11} /> Written</span>}
              </div>
              <h3 className="mt-3 font-semibold text-ink">{t.title}</h3>
              <p className="mt-0.5 text-sm text-ink-muted">{humanize(t.topic)} · {t.num_questions} questions</p>

              <div className="mt-4 grid grid-cols-3 gap-2 border-t border-line pt-4 text-center">
                <div>
                  <div className="flex items-center justify-center gap-1 text-sm font-semibold text-ink">
                    <Users size={13} className="text-ink-subtle" /> {t.assigned_count}
                  </div>
                  <div className="text-[11px] text-ink-subtle">assigned</div>
                </div>
                <div>
                  <div className="flex items-center justify-center gap-1 text-sm font-semibold text-ink">
                    <CheckCircle2 size={13} className="text-ink-subtle" /> {t.completed_count}
                  </div>
                  <div className="text-[11px] text-ink-subtle">completed</div>
                </div>
                <div>
                  <div className="text-sm font-semibold text-ink">{t.avg_score != null ? `${t.avg_score}%` : "—"}</div>
                  <div className="text-[11px] text-ink-subtle">avg score</div>
                </div>
              </div>
              <div className="mt-4 flex items-center justify-between text-xs text-ink-subtle">
                <span>Created {formatDate(t.created_at)}</span>
                <span className="inline-flex items-center gap-1 text-brand-600">Manage <ArrowRight size={12} /></span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </PageContainer>
  );
}
