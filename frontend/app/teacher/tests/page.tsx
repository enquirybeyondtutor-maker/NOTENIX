"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { ClipboardList, FilePlus2, Users, CheckCircle2, ArrowRight } from "lucide-react";
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
  num_questions: number;
  duration_minutes: number | null;
  created_at: string;
  assigned_count: number;
  completed_count: number;
  avg_score: number | null;
}

export default function TeacherTestsPage() {
  const { ready } = useAuthGuard("teacher");
  const [tests, setTests] = useState<TestRow[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!ready) return;
    teacherAPI
      .listTests()
      .then(({ data }) => setTests(data))
      .catch(() => setTests([]))
      .finally(() => setLoading(false));
  }, [ready]);

  if (!ready || loading) return <Spinner label="Loading tests…" />;

  return (
    <PageContainer>
      <PageHeader
        icon={ClipboardList}
        title="Tests"
        subtitle="Create, assign and review your assessments."
        actions={
          <Button href="/teacher/tests/new">
            <FilePlus2 size={16} /> Create test
          </Button>
        }
      />

      {tests.length === 0 ? (
        <EmptyState
          icon={ClipboardList}
          title="No tests yet"
          desc="Create your first assessment — build it by hand or let AI generate board-aligned questions in seconds."
          action={<Button href="/teacher/tests/new"><FilePlus2 size={16} /> Create your first test</Button>}
        />
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {tests.map((t) => (
            <Link key={t.id} href={`/teacher/tests/${t.id}`} className="card card-hover flex flex-col p-5">
              <div className="flex flex-wrap items-center gap-2">
                <span className="badge-brand">{humanize(t.subject)}</span>
                <span className="badge-neutral">{t.level}</span>
                <span className="badge-neutral">{t.exam_board}</span>
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
