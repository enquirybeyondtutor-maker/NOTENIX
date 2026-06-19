"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Trophy, Flame, Zap, Crown, Brain, Plus } from "lucide-react";
import { api } from "@/lib/api";

type Tab = "global" | "weekly";

export default function LeaderboardPage() {
  const router = useRouter();
  const [tab, setTab] = useState<Tab>("global");
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("notenix_token");
    if (!token) { router.push("/login"); return; }
  }, [router]);

  useEffect(() => {
    setLoading(true);
    api.get(`/leaderboard/${tab}`)
      .then((res) => { setData(res.data); setLoading(false); })
      .catch(() => setLoading(false));
  }, [tab]);

  const leaderboard = data?.leaderboard || [];
  const yourRank = data?.your_rank;

  return (
    <div className="min-h-screen grid-bg px-4 sm:px-6 py-8 max-w-3xl mx-auto">
      <div className="orb w-80 h-80 bg-yellow-600/10 top-0 right-0" />

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-orbitron font-bold text-white flex items-center gap-3">
            <Trophy size={28} className="text-yellow-400" /> Leaderboard
          </h1>
          <p className="text-slate-400 text-sm mt-1">Compete with students across the UK</p>
        </div>
        <Link href="/quiz/create">
          <button className="btn-neon relative flex items-center gap-2 px-5 py-2.5 rounded-xl text-white font-semibold text-sm z-10">
            <span className="relative z-10 flex items-center gap-2"><Plus size={15} /> New Quiz</span>
          </button>
        </Link>
      </motion.div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        {(["global", "weekly"] as Tab[]).map((t) => (
          <button key={t} onClick={() => setTab(t)}
            className={`px-5 py-2.5 rounded-xl text-sm font-medium transition-all capitalize ${tab === t ? "bg-purple-500/20 border border-purple-500/40 text-purple-300" : "border border-white/8 text-slate-400 hover:text-white hover:border-white/15"}`}>
            {t === "global" ? "🌍 All Time" : "📅 This Week"}
          </button>
        ))}
      </div>

      {/* Your rank banner */}
      {yourRank && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-card border-purple-500/30 bg-purple-500/5 p-4 mb-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Crown size={18} className="text-purple-400" />
            <span className="text-sm text-white font-medium">Your rank: <span className="gradient-text font-bold">#{yourRank}</span></span>
          </div>
          <span className="text-xs text-slate-500">Keep quizzing to climb higher!</span>
        </motion.div>
      )}

      {/* Leaderboard list */}
      <div className="glass-card p-6 relative z-10">
        {loading ? (
          <div className="flex items-center justify-center py-16">
            <div className="w-10 h-10 border-2 border-purple-500/30 border-t-purple-500 rounded-full animate-spin" />
          </div>
        ) : leaderboard.length === 0 ? (
          <div className="text-center py-16">
            <Trophy size={40} className="text-slate-700 mx-auto mb-3" />
            <p className="text-white font-semibold mb-1">No data yet</p>
            <p className="text-slate-500 text-sm">
              {tab === "weekly" ? "Complete quizzes this week to appear here." : "Complete your first quiz to appear here."}
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            {leaderboard.map((entry: any, i: number) => (
              <motion.div key={i} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.04 }}>
                <div className={`flex items-center gap-4 p-4 rounded-xl border transition-all ${
                  entry.is_you
                    ? "border-purple-500/40 bg-purple-500/10"
                    : entry.rank <= 3
                    ? "border-yellow-500/20 bg-yellow-500/5"
                    : "border-white/5 bg-white/2 hover:bg-white/4"
                }`}>
                  {/* Rank */}
                  <div className="w-10 text-center flex-shrink-0">
                    {entry.badge ? (
                      <span className="text-xl">{entry.badge}</span>
                    ) : (
                      <span className="text-slate-500 font-orbitron text-sm font-bold">#{entry.rank}</span>
                    )}
                  </div>

                  {/* Avatar placeholder */}
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 text-sm font-bold ${
                    entry.is_you ? "bg-purple-500/30 text-purple-300" : "bg-white/8 text-slate-400"
                  }`}>
                    {entry.name.charAt(0).toUpperCase()}
                  </div>

                  {/* Name */}
                  <div className="flex-1 min-w-0">
                    <p className={`font-semibold text-sm truncate ${entry.is_you ? "text-white" : "text-slate-200"}`}>
                      {entry.name} {entry.is_you && <span className="text-xs text-purple-400 font-normal">(you)</span>}
                    </p>
                    {tab === "weekly" && entry.quizzes_this_week && (
                      <p className="text-xs text-slate-500">{entry.quizzes_this_week} quiz{entry.quizzes_this_week !== 1 ? "zes" : ""} · avg {entry.avg_score}%</p>
                    )}
                    {tab === "global" && entry.streak > 0 && (
                      <p className="text-xs text-slate-500 flex items-center gap-1"><Flame size={10} className="text-orange-400" />{entry.streak} day streak</p>
                    )}
                  </div>

                  {/* XP */}
                  <div className="text-right flex-shrink-0">
                    <div className="flex items-center gap-1 text-sm font-orbitron font-bold">
                      <Zap size={13} className="text-yellow-400" />
                      <span className={entry.is_you ? "gradient-text" : "text-white"}>{(entry.xp || 0).toLocaleString()}</span>
                    </div>
                    <div className="text-xs text-slate-600">XP</div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>

      <p className="text-center text-xs text-slate-600 mt-6">Names are partially hidden to protect privacy.</p>
    </div>
  );
}
