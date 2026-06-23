"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";
import { Brain, Flame, Star, Trophy, Target, ArrowRight, Award } from "lucide-react";
import { progressAPI, getUser } from "@/lib/api";

export default function Dashboard() {
  const router = useRouter();
  const [data, setData] = useState<any>(null);
  const user = typeof window !== "undefined" ? getUser() : null;

  useEffect(() => {
    if (!getUser()) { router.push("/login"); return; }
    progressAPI.dashboard().then((r) => setData(r.data)).catch(() => {});
  }, [router]);

  if (!data) return <div className="max-w-6xl mx-auto px-4 py-20 text-center text-gray-400">Loading…</div>;

  const stats = [
    { label: "Total XP", value: data.xp, icon: Star, color: "text-purple-600 bg-purple-50" },
    { label: "Streak", value: `${data.streak} 🔥`, icon: Flame, color: "text-pink-500 bg-pink-50" },
    { label: "Quizzes", value: data.quiz_count, icon: Brain, color: "text-blue-500 bg-blue-50" },
    { label: "Avg Score", value: `${data.avg_score}%`, icon: Target, color: "text-green-500 bg-green-50" },
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-10">
      <div className="flex items-center justify-between mb-8 flex-wrap gap-4">
        <div>
          <h1 className="text-3xl font-bold">Welcome back, {user?.full_name?.split(" ")[0]} 👋</h1>
          <p className="text-gray-500 mt-1">{data.plan === "pro" ? "Pro member" : `Free plan · ${Math.max(0, 3 - data.quiz_count)} quizzes left`}</p>
        </div>
        <Link href="/quiz"><button className="btn-primary">New Quiz <ArrowRight size={16} /></button></Link>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {stats.map((s, i) => (
          <motion.div key={s.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }} className="card p-5">
            <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-3 ${s.color}`}><s.icon size={18} /></div>
            <div className="text-2xl font-bold">{s.value}</div>
            <div className="text-xs text-gray-400">{s.label}</div>
          </motion.div>
        ))}
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <div className="card p-6">
          <h2 className="font-bold mb-4 flex items-center gap-2"><Target size={18} className="text-purple-600" /> Subject performance</h2>
          {data.subject_stats.length === 0 ? <p className="text-sm text-gray-400">Take a quiz to see your stats.</p> : (
            <div className="space-y-4">
              {data.subject_stats.map((s: any) => (
                <div key={s.subject}>
                  <div className="flex justify-between text-sm mb-1"><span className="font-medium">{s.subject}</span><span className="text-gray-400">{s.avg}% · {s.count} quizzes</span></div>
                  <div className="h-2 bg-purple-100 rounded-full overflow-hidden"><div className="h-full bg-gradient-to-r from-purple-600 to-pink-500" style={{ width: `${s.avg}%` }} /></div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="card p-6">
          <h2 className="font-bold mb-4 flex items-center gap-2"><Award size={18} className="text-purple-600" /> Badges</h2>
          {data.badges.length === 0 ? <p className="text-sm text-gray-400">Earn badges by taking quizzes and building streaks.</p> : (
            <div className="flex flex-wrap gap-2">
              {data.badges.map((b: any) => (
                <div key={b.id} className="badge-pill"><Trophy size={14} className="text-pink-500" /> {b.name}</div>
              ))}
            </div>
          )}
        </div>
      </div>

      {data.recent.length > 0 && (
        <div className="card p-6 mt-6">
          <h2 className="font-bold mb-4">Recent quizzes</h2>
          <div className="space-y-2">
            {data.recent.map((r: any, i: number) => (
              <div key={i} className="flex items-center justify-between py-2 border-b border-purple-50 last:border-0">
                <div><span className="font-medium text-sm">{r.subject}</span> <span className="text-gray-400 text-sm">· {r.topic}</span> {r.mode === "exam" && <span className="text-xs text-purple-600">(exam)</span>}</div>
                <span className="font-bold text-sm text-purple-600">{r.score}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
