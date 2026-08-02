"use client";
import { useEffect, useState } from "react";
import { Trophy } from "lucide-react";
import { leaderboardAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, EmptyState, Spinner } from "@/components/ui/Page";
import { cn } from "@/lib/utils";

export default function Leaderboard() {
  const { ready } = useAuthGuard();
  const [tab, setTab] = useState<"weekly" | "global">("global");
  const [rows, setRows] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!ready) return;
    setLoading(true);
    const call = tab === "weekly" ? leaderboardAPI.weekly() : leaderboardAPI.global();
    call.then((r) => setRows(r.data)).catch(() => setRows([])).finally(() => setLoading(false));
  }, [tab, ready]);

  const medal = (rank: number) => (rank === 1 ? "🥇" : rank === 2 ? "🥈" : rank === 3 ? "🥉" : null);

  if (!ready) return <Spinner />;

  return (
    <PageContainer className="max-w-2xl">
      <PageHeader icon={Trophy} title="Leaderboard" subtitle="See how you rank against other students." />

      <div className="mb-5 inline-flex rounded-lg border border-line bg-white p-1">
        {(["global", "weekly"] as const).map((t) => (
          <button
            key={t}
            onClick={() => setTab(t)}
            className={cn(
              "rounded-md px-4 py-1.5 text-sm font-medium capitalize transition-colors",
              tab === t ? "bg-brand-600 text-white" : "text-ink-muted hover:text-ink"
            )}
          >
            {t}
          </button>
        ))}
      </div>

      {loading ? (
        <Spinner />
      ) : rows.length === 0 ? (
        <EmptyState icon={Trophy} title="No rankings yet" desc="Complete quizzes and tests to earn XP and climb the board." />
      ) : (
        <div className="card divide-y divide-line">
          {rows.map((r) => (
            <div key={r.rank} className={cn("flex items-center justify-between p-4", r.rank <= 3 && "bg-brand-50/30")}>
              <div className="flex items-center gap-3">
                <span className="grid h-8 w-8 place-items-center text-center font-bold text-ink-subtle">
                  {medal(r.rank) || r.rank}
                </span>
                <span className="text-sm font-medium text-ink">{r.name}</span>
              </div>
              <span className="text-sm font-semibold text-brand-600">{r.xp} XP</span>
            </div>
          ))}
        </div>
      )}
    </PageContainer>
  );
}
