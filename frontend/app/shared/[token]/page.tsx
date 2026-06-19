"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useParams } from "next/navigation";
import Link from "next/link";
import { Zap, Trophy, Flame, Target, BookOpen, CheckCircle, BarChart3 } from "lucide-react";
import { api } from "@/lib/api";
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer } from "recharts";

export default function SharedProgressPage() {
  const { token } = useParams() as { token: string };
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    api.get(`/social/shared/${token}`)
      .then((res) => { setData(res.data); setLoading(false); })
      .catch(() => { setError(true); setLoading(false); });
  }, [token]);

  if (loading) return (
    <div className="min-h-screen grid-bg flex items-center justify-center">
      <div className="w-12 h-12 border-2 border-purple-500/30 border-t-purple-500 rounded-full animate-spin" />
    </div>
  );

  if (error || !data) return (
    <div className="min-h-screen grid-bg flex items-center justify-center text-center px-4">
      <div>
        <Zap size={40} className="text-slate-600 mx-auto mb-4" />
        <h2 className="text-white font-semibold mb-2">Link not found</h2>
        <p className="text-slate-400 text-sm mb-4">This share link is invalid or has expired.</p>
        <Link href="/" className="text-purple-400 hover:text-purple-300 text-sm">Go to Notenix →</Link>
      </div>
    </div>
  );

  const radarData = data.subject_progress.slice(0, 6).map((s: any) => ({
    subject: s.subject.replace("_", " ").replace(/\b\w/g, (c: string) => c.toUpperCase()).slice(0, 8),
    score: Math.round(s.average_score),
  }));

  return (
    <div className="min-h-screen grid-bg px-4 sm:px-6 py-8 max-w-4xl mx-auto">
      <div className="orb w-80 h-80 bg-purple-600/15 top-0 right-0" />

      {/* Header */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-8">
        <Link href="/" className="inline-flex items-center gap-2 mb-6">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center">
            <Zap size={14} className="text-white" />
          </div>
          <span className="font-orbitron text-base font-bold gradient-text tracking-wider">NOTENIX</span>
        </Link>
        <div className="w-20 h-20 rounded-full bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center text-3xl font-bold text-white mx-auto mb-4">
          {data.student_name.charAt(0).toUpperCase()}
        </div>
        <h1 className="text-2xl font-orbitron font-bold text-white">{data.student_name}</h1>
        <p className="text-slate-400 text-sm mt-1">Student Progress Report</p>

        <div className="flex items-center justify-center gap-4 mt-4 flex-wrap">
          <div className="glass-card px-5 py-2.5 flex items-center gap-2">
            <Zap size={16} className="text-yellow-400" />
            <span className="font-orbitron font-bold text-white">{(data.xp_points || 0).toLocaleString()}</span>
            <span className="text-xs text-slate-500">XP</span>
          </div>
          <div className="glass-card px-5 py-2.5 flex items-center gap-2">
            <Flame size={16} className="text-orange-400" />
            <span className="font-orbitron font-bold text-white">{data.streak_days || 0}</span>
            <span className="text-xs text-slate-500">day streak</span>
          </div>
          {data.badges?.length > 0 && (
            <div className="glass-card px-5 py-2.5 flex items-center gap-2">
              <Trophy size={16} className="text-yellow-400" />
              <span className="font-orbitron font-bold text-white">{data.badges.length}</span>
              <span className="text-xs text-slate-500">badges</span>
            </div>
          )}
        </div>
      </motion.div>

      <div className="grid md:grid-cols-2 gap-6 mb-6">
        {/* Radar */}
        {radarData.length > 2 && (
          <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.2 }} className="glass-card p-6">
            <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
              <BarChart3 size={18} className="text-purple-400" /> Subject Performance
            </h3>
            <ResponsiveContainer width="100%" height={220}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="rgba(255,255,255,0.05)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: "#64748b", fontSize: 11 }} />
                <Radar dataKey="score" stroke="#a855f7" fill="#a855f7" fillOpacity={0.2} strokeWidth={2} />
              </RadarChart>
            </ResponsiveContainer>
          </motion.div>
        )}

        {/* Subject scores */}
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.3 }} className="glass-card p-6">
          <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
            <Target size={18} className="text-cyan-400" /> Subject Scores
          </h3>
          {data.subject_progress.length === 0 ? (
            <p className="text-slate-500 text-sm text-center py-4">No quizzes completed yet.</p>
          ) : (
            <div className="space-y-3">
              {data.subject_progress.map((s: any) => (
                <div key={s.subject}>
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-slate-300 capitalize">{s.subject.replace("_", " ")}</span>
                    <span className={`text-sm font-bold ${s.average_score >= 70 ? "text-green-400" : s.average_score >= 50 ? "text-yellow-400" : "text-red-400"}`}>
                      {Math.round(s.average_score)}%
                    </span>
                  </div>
                  <div className="h-1.5 bg-white/5 rounded-full overflow-hidden">
                    <div className="h-full progress-bar rounded-full" style={{ width: `${s.average_score}%` }} />
                  </div>
                </div>
              ))}
            </div>
          )}
        </motion.div>
      </div>

      {/* Recent activity */}
      {data.recent_activity.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }} className="glass-card p-6 mb-6">
          <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
            <BookOpen size={18} className="text-blue-400" /> Recent Activity
          </h3>
          <div className="space-y-2">
            {data.recent_activity.map((a: any, i: number) => (
              <div key={i} className="flex items-center justify-between p-3 rounded-lg bg-white/3 border border-white/5">
                <div>
                  <p className="text-sm font-medium text-white capitalize">{a.topic}</p>
                  <p className="text-xs text-slate-500 capitalize">{a.subject?.replace("_", " ")}</p>
                </div>
                {a.score != null && (
                  <span className={`text-sm font-bold ${a.score >= 70 ? "text-green-400" : a.score >= 50 ? "text-yellow-400" : "text-red-400"}`}>
                    {Math.round(a.score)}%
                  </span>
                )}
              </div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Badges */}
      {data.badges.length > 0 && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }} className="glass-card p-6 mb-8">
          <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
            <Trophy size={18} className="text-yellow-400" /> Badges Earned
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {data.badges.map((b: any) => (
              <div key={b.name} className="glass-card p-3 border-yellow-500/15 bg-yellow-500/5 text-center">
                <Trophy size={20} className="text-yellow-400 mx-auto mb-2" />
                <p className="text-xs font-semibold text-white">{b.name}</p>
                <p className="text-xs text-slate-500 mt-1">{b.description}</p>
              </div>
            ))}
          </div>
        </motion.div>
      )}

      <div className="text-center">
        <p className="text-slate-500 text-sm mb-3">Want to track your own progress?</p>
        <Link href="/register">
          <motion.button whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.97 }}
            className="btn-neon relative px-8 py-3 rounded-xl text-white font-semibold z-10">
            <span className="relative z-10">Try Notenix Free</span>
          </motion.button>
        </Link>
      </div>
    </div>
  );
}
