"use client";
import { useEffect, useState } from "react";
import { LineChart, Brain, FileText } from "lucide-react";
import { quizAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, EmptyState, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { humanize, formatDate } from "@/lib/utils";

export default function Progress() {
  const { ready } = useAuthGuard();
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!ready) return;
    quizAPI.history().then((r) => setHistory(r.data)).catch(() => setHistory([])).finally(() => setLoading(false));
  }, [ready]);

  if (!ready || loading) return <Spinner label="Loading your progress…" />;

  return (
    <PageContainer>
      <PageHeader icon={LineChart} title="Your progress" subtitle="Every quiz and practice session you've completed." />

      {history.length === 0 ? (
        <EmptyState
          icon={Brain}
          title="No practice yet"
          desc="Take your first quiz to start tracking your progress over time."
          action={<Button href="/quiz"><Brain size={16} /> Start a quiz</Button>}
        />
      ) : (
        <div className="card divide-y divide-line">
          {history.map((h) => (
            <div key={h.id} className="flex items-center justify-between gap-3 p-4">
              <div className="flex items-center gap-3">
                <span className="grid h-9 w-9 place-items-center rounded-lg bg-brand-50 text-brand-600">
                  {h.mode === "exam" ? <FileText size={16} /> : <Brain size={16} />}
                </span>
                <div>
                  <div className="text-sm font-medium text-ink">{humanize(h.subject)} · {humanize(h.topic)}</div>
                  <div className="text-xs text-ink-subtle">
                    {h.mode === "exam" ? "Exam mode" : "Quiz"} · {h.completed_at ? formatDate(h.completed_at) : ""}
                  </div>
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm font-semibold text-ink">{h.score}%</div>
                <div className="text-xs text-ink-subtle">+{h.xp_earned} XP</div>
              </div>
            </div>
          ))}
        </div>
      )}
    </PageContainer>
  );
}
