"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { TrendingUp, Brain, BookOpen, Clock, Target, Trophy, Flame, Calendar, Plus } from "lucide-react";
import { progressAPI } from "@/lib/api";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";

export default function ProgressPage() {
  const router = useRouter();
  const [data, setData] = useState<any>(null);
  const [srsData, setSrsData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("notenix_token");
    if (!token) { router.push("/login"); return; }
    Promise.all([progressAPI.dashboard(), progressAPI.srsdue()]).then(([dash, srs]) => {
      setData(dash.data);
      setSrsData(srs.data);
      setLoading(false);
    }).catch(() => router.push("/login"));
  }, [router]);

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="w-12 h-12 border-2 border-purple-500/30 border-t-purple-500 rounded-full animate-spin" />
    </div>
  );

  const subjectProgress = data?.subject_progress || [];
  const user = data?.user || {};
  const stats = data?.stats || {};
  const badges = data?.badges || [];
  const dueCards = srsData?.due_count || 0;

  const barData = subjectProgress.map((s: any) => ({
    name: s.subject.replace("_", " ").replace(/\b\w/g, (c: string) => c.toUpperCase()).slice(0, 10),
    avg: Math.round(s.average_score),
    best: Math.round(s.best_score),
  }));

  return (
    <div className="min-h-screen grid-bg px-4 sm:px-6 py-8 max-w-6xl mx-auto">
      <div className="orb w-80 h-80 bg-cyan-600/10 top-0 right-0" />

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-orbitron font-bold text-white">Progress Tracker</h1>
          <p className="text-slate-400 text-sm mt-1">Your complete learning journey</p>
        </div>
        <Link href="/quiz/create">
          <button className="btn-neon relative flex items-center gap-2 px-5 py-2.5 rounded-xl text-white font-semibold text-sm z-10">
            <span className="relative z-10 flex items-center gap-2"><Plus size={16} /> New Quiz</span>
          </button>
        </Link>
      </motion.div>

      {/* Summary stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          { label: "Total Quizzes", value: stats.total_quizzes || 0, icon: Brain, color: "text-purple-400", bg: "bg-purple-500/10" },
          { label: "Avg Score", value: `${stats.average_score || 0}%`, icon: Target, color: "text-cyan-400", bg: "bg-cyan-500/10" },
          { label: "Study Time", value: `${stats.total_time_minutes || 0}m`, icon: Clock, color: "text-blue-400", bg: "bg-blue-500/10" },
          { label: "Streak", value: `${user.streak_days || 0} days`, icon: Flame, color: "text-orange-400", bg: "bg-orange-500/10" },
        ].map((s, i) => (
          <motion.div key={s.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}>
            <div className="glass-card p-5">
              <div className={`w-10 h-10 rounded-xl ${s.bg} flex items-center justify-center mb-3`}><s.icon size={20} className={s.color} /></div>
              <div className="text-2xl font-orbitron font-bold text-white">{s.value}</div>
              <div className="text-xs text-slate-500 mt-1">{s.label}</div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* SRS reminder */}
      {dueCards > 0 && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-card border-orange-500/30 bg-orange-500/5 p-4 mb-6 flex items-center gap-4">
          <Calendar size={20} className="text-orange-400 flex-shrink-0" />
          <div>
            <p className="text-sm font-medium text-white">{dueCards} topic{dueCards > 1 ? "s" : ""} due for review today</p>
            <p className="text-xs text-slate-500">Your spaced repetition system has flagged these for revision</p>
          </div>
          <Link href="/quiz/create" className="ml-auto text-xs text-orange-400 hover:text-orange-300 font-semibold whitespace-nowrap">
            Review Now →
          </Link>
        </motion.div>
      )}

      {/* Bar chart */}
      {barData.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="glass-card p-6 mb-6">
          <h3 className="font-semibold text-white mb-4 flex items-center gap-2"><TrendingUp size={18} className="text-purple-400" /> Performance by Subject</h3>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={barData} barGap={4}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
              <XAxis dataKey="name" tick={{ fill: "#64748b", fontSize: 11 }} />
              <YAxis domain={[0, 100]} tick={{ fill: "#64748b", fontSize: 11 }} />
              <Tooltip contentStyle={{ background: "#0f0f1a", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8, color: "#f1f5f9" }} />
              <Bar dataKey="avg" name="Avg Score" fill="#a855f7" radius={[4, 4, 0, 0]} opacity={0.8} />
              <Bar dataKey="best" name="Best Score" fill="#06b6d4" radius={[4, 4, 0, 0]} opacity={0.6} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      )}

      {/* Subject cards */}
      {subjectProgress.length > 0 && (
        <div className="grid md:grid-cols-2 gap-4 mb-8">
          {subjectProgress.map((s: any, i: number) => (
            <motion.div key={s.subject} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 + i * 0.07 }}>
              <div className="glass-card p-5">
                <div className="flex items-center justify-between mb-3">
                  <div>
                    <h4 className="font-semibold text-white capitalize">{s.subject.replace("_", " ")}</h4>
                    <p className="text-xs text-slate-500">{s.level?.replace("_", "-")} · {s.exam_board}</p>
                  </div>
                  <div className="text-right">
                    <div className={`text-xl font-orbitron font-bold ${s.average_score >= 70 ? "text-green-400" : s.average_score >= 50 ? "text-yellow-400" : "text-red-400"}`}>
                      {Math.round(s.average_score)}%
                    </div>
                    <div className="text-xs text-slate-500">avg</div>
                  </div>
                </div>

                <div className="h-1.5 bg-white/5 rounded-full mb-3 overflow-hidden">
                  <div className="h-full progress-bar rounded-full" style={{ width: `${s.average_score}%` }} />
                </div>

                <div className="flex items-center justify-between text-xs text-slate-500">
                  <span>{s.total_quizzes} quiz{s.total_quizzes !== 1 ? "zes" : ""}</span>
                  <span>Best: {Math.round(s.best_score)}%</span>
                </div>

                {/* Topic breakdown */}
                {Object.keys(s.topic_scores || {}).length > 0 && (
                  <div className="mt-3 pt-3 border-t border-white/5">
                    <p className="text-xs text-slate-500 mb-2">Topic scores</p>
                    <div className="space-y-1.5">
                      {Object.entries(s.topic_scores).slice(0, 4).map(([topic, score]: [string, any]) => (
                        <div key={topic} className="flex items-center gap-2">
                          <span className="text-xs text-slate-400 capitalize w-28 truncate">{topic.replace("_", " ")}</span>
                          <div className="flex-1 h-1 bg-white/5 rounded-full overflow-hidden">
                            <div className={`h-full rounded-full ${score >= 70 ? "bg-green-400" : score >= 50 ? "bg-yellow-400" : "bg-red-400"}`} style={{ width: `${score}%` }} />
                          </div>
                          <span className="text-xs text-slate-500 w-8 text-right">{Math.round(score)}%</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </div>
      )}

      {subjectProgress.length === 0 && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center py-16">
          <BookOpen size={48} className="text-slate-700 mx-auto mb-4" />
          <h3 className="text-white font-semibold mb-2">No progress yet</h3>
          <p className="text-slate-500 text-sm mb-6">Complete your first quiz to start tracking your progress.</p>
          <Link href="/quiz/create">
            <button className="btn-neon relative px-8 py-3 rounded-xl text-white font-semibold z-10">
              <span className="relative z-10">Start First Quiz</span>
            </button>
          </Link>
        </motion.div>
      )}

      {/* Badges */}
      {badges.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.7 }} className="glass-card p-6">
          <h3 className="font-semibold text-white mb-4 flex items-center gap-2"><Trophy size={18} className="text-yellow-400" /> Earned Badges</h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
            {badges.map((b: any) => (
              <div key={b.type} className="glass-card p-4 border-yellow-500/15 bg-yellow-500/5 text-center">
                <Trophy size={24} className="text-yellow-400 mx-auto mb-2" />
                <p className="text-xs font-semibold text-white">{b.name}</p>
                <p className="text-xs text-slate-500 mt-1">{b.description}</p>
              </div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
}
