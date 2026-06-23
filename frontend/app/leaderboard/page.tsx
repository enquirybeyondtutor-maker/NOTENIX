"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Trophy, Medal } from "lucide-react";
import { leaderboardAPI, getUser } from "@/lib/api";

export default function Leaderboard() {
  const router = useRouter();
  const [tab, setTab] = useState<"weekly" | "global">("global");
  const [rows, setRows] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!getUser()) { router.push("/login"); return; }
    setLoading(true);
    const call = tab === "weekly" ? leaderboardAPI.weekly() : leaderboardAPI.global();
    call.then((r) => setRows(r.data)).finally(() => setLoading(false));
  }, [tab, router]);

  const medal = (rank: number) => rank === 1 ? "🥇" : rank === 2 ? "🥈" : rank === 3 ? "🥉" : null;

  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 py-10">
      <h1 className="text-3xl font-bold mb-2 flex items-center gap-2"><Trophy className="text-pink-500" /> Leaderboard</h1>
      <p className="text-gray-500 mb-6">See how you rank against other students.</p>

      <div className="flex gap-2 mb-6">
        {(["global", "weekly"] as const).map((t) => (
          <button key={t} onClick={() => setTab(t)} className={`px-4 py-2 rounded-xl text-sm font-medium capitalize border ${tab === t ? "bg-purple-600 text-white border-purple-600" : "border-purple-200 text-gray-600"}`}>{t}</button>
        ))}
      </div>

      {loading ? <p className="text-gray-400">Loading…</p> :
        rows.length === 0 ? <div className="card p-10 text-center text-gray-400">No rankings yet.</div> : (
          <div className="card divide-y divide-purple-50">
            {rows.map((r) => (
              <div key={r.rank} className="flex items-center justify-between p-4">
                <div className="flex items-center gap-3">
                  <span className="w-8 text-center font-bold text-gray-400">{medal(r.rank) || r.rank}</span>
                  <span className="font-medium">{r.name}</span>
                </div>
                <span className="font-bold text-purple-600">{r.xp} XP</span>
              </div>
            ))}
          </div>
        )}
    </div>
  );
}
