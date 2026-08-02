"use client";
import { useEffect, useState } from "react";
import { ClipboardList, Users, CheckCircle2, TrendingUp, FilePlus2, ArrowRight } from "lucide-react";
import { teacherAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, StatCard, Spinner, EmptyState } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { relativeTime } from "@/lib/utils";

interface Overview {
  tests: number;
  assignments: number;
  completed: number;
  avg_score: number | null;
  recent: { student: string; test: string; score: number; grade: string; completed_at: string }[];
}

export default function TeacherOverviewPage() {
  const { user, ready } = useAuthGuard("teacher");
  const [data, setData] = useState<Overview | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!ready) return;
    teacherAPI
      .overview()
      .then(({ data }) => setData(data))
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [ready]);

  if (!ready || loading) return <Spinner label="Loading your dashboard…" />;

  return (
    <PageContainer>
      <PageHeader
        title={`Welcome back, ${user?.full_name?.split(" ")[0] || "teacher"}`}
        subtitle="Your assessment activity at a glance."
        actions={
          <Button href="/teacher/tests/new">
            <FilePlus2 size={16} /> Create test
          </Button>
        }
      />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard label="Tests created" value={data?.tests ?? 0} icon={ClipboardList} />
        <StatCard label="Assignments" value={data?.assignments ?? 0} icon={Users} />
        <StatCard label="Completed" value={data?.completed ?? 0} icon={CheckCircle2} />
        <StatCard label="Avg score" value={data?.avg_score != null ? `${data.avg_score}%` : "—"} icon={TrendingUp} />
      </div>

      <div className="mt-8 grid gap-6 lg:grid-cols-3">
        {/* Recent activity */}
        <div className="lg:col-span-2">
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-ink-subtle">Recent submissions</h2>
          {!data?.recent?.length ? (
            <EmptyState
              icon={CheckCircle2}
              title="No submissions yet"
              desc="Once students complete their assigned tests, their results will show up here."
            />
          ) : (
            <div className="card divide-y divide-line">
              {data.recent.map((r, i) => (
                <div key={i} className="flex items-center justify-between gap-3 p-4">
                  <div className="flex items-center gap-3">
                    <span className="grid h-9 w-9 place-items-center rounded-lg bg-brand-50 text-xs font-semibold text-brand-700">
                      {(r.student?.[0] || "S").toUpperCase()}
                    </span>
                    <div>
                      <div className="text-sm font-medium text-ink">{r.student}</div>
                      <div className="text-xs text-ink-subtle">{r.test} · {relativeTime(r.completed_at)}</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-semibold text-ink">{r.score}%</div>
                    <div className="text-xs text-ink-subtle">Grade {r.grade}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Quick actions */}
        <div>
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-ink-subtle">Quick actions</h2>
          <div className="space-y-3">
            {[
              { href: "/teacher/tests/new", label: "Create a new test", desc: "Build or AI-generate", icon: FilePlus2 },
              { href: "/teacher/tests", label: "Manage tests", desc: "Assign & review", icon: ClipboardList },
              { href: "/teacher/students", label: "View students", desc: "Track performance", icon: Users },
            ].map((a) => (
              <Button key={a.href} href={a.href} variant="secondary" className="w-full justify-between">
                <span className="flex items-center gap-2.5">
                  <a.icon size={16} className="text-brand-600" />
                  <span className="text-left">
                    <span className="block text-sm font-medium text-ink">{a.label}</span>
                    <span className="block text-xs font-normal text-ink-subtle">{a.desc}</span>
                  </span>
                </span>
                <ArrowRight size={15} className="text-ink-subtle" />
              </Button>
            ))}
          </div>
        </div>
      </div>
    </PageContainer>
  );
}
