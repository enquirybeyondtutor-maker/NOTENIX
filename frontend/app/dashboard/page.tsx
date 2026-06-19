"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Brain, Flame, Trophy, Clock, Target, BookOpen, Plus, Star, Zap, TrendingUp, Share2, Mail, AlertCircle, X, Copy, Check } from "lucide-react";
import { progressAPI, api } from "@/lib/api";
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";

export default function DashboardPage() {
  const router = useRouter();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [shareUrl, setShareUrl] = useState("");
  const [sharing, setSharing] = useState(false);
  const [copied, setCopied] = useState(false);
  const [resendLoading, setResendLoading] = useState(false);
  const [resendSent, setResendSent] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("notenix_token");
    if (!token) { router.push("/login"); return; }
    progressAPI.dashboard().then((res) => { setData(res.data); setLoading(false); }).catch(() => { router.push("/login"); });
  }, [router]);

  const handleShare = async () => {
    setSharing(true);
    try {
      const res = await api.post("/social/share");
      setShareUrl(res.data.share_url);
    } catch {
      // ignore
    } finally {
      setSharing(false);
    }
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(shareUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleResendVerification = async () => {
    setResendLoading(true);
    try {
      await api.post("/auth/resend-verification");
      setResendSent(true);
    } catch {
      // ignore
    } finally {
      setResendLoading(false);
    }
  };

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="w-16 h-16 border-2 border-purple-500/30 border-t-purple-500 rounded-full animate-spin mx-auto mb-4" />
        <p className="text-slate-400 text-sm">Loading your dashboard...</p>
      </div>
    </div>
  );

  const user = data?.user || {};
  const stats = data?.stats || {};
  const subjectProgress = data?.subject_progress || [];
  const recentAttempts = data?.recent_attempts || [];
  const badges = data?.badges || [];

  const isSubscribed = user.subscription_status === "active";
  const freeRemaining = Math.max(0, (user.free_quiz_limit || 3) - (user.free_quizzes_used || 0));
  const isVerified = user.is_verified !== false;

  const radarData = subjectProgress.slice(0, 6).map((s: any) => ({
    subject: s.subject.replace("_", " ").replace(/\b\w/g, (c: string) => c.toUpperCase()).slice(0, 8),
    score: Math.round(s.average_score),
  }));

  const scoreData = recentAttempts.filter((a: any) => a.score != null).reverse().map((a: any, i: number) => ({
    quiz: `#${i + 1}`, score: Math.round(a.score), subject: a.subject,
  }));

  return (
    <div className="min-h-screen grid-bg px-4 sm:px-6 py-8 max-w-7xl mx-auto">
      <div className="orb w-96 h-96 bg-purple-600/10 top-0 right-0" />

      {/* Email verification banner */}
      {!isVerified && (
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} className="glass-card border-blue-500/30 bg-blue-500/5 p-4 mb-5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div className="flex items-center gap-3">
            <Mail size={18} className="text-blue-400 flex-shrink-0" />
            <div>
              <p className="text-sm font-medium text-white">Verify your email address</p>
              <p className="text-xs text-slate-400">Check your inbox for a verification link to unlock all features.</p>
            </div>
          </div>
          {resendSent ? (
            <span className="text-xs text-green-400 flex items-center gap-1 whitespace-nowrap"><Check size={12} /> Sent!</span>
          ) : (
            <button onClick={handleResendVerification} disabled={resendLoading}
              className="text-xs font-semibold text-blue-400 hover:text-blue-300 transition-colors whitespace-nowrap disabled:opacity-50">
              {resendLoading ? "Sending..." : "Resend email →"}
            </button>
          )}
        </motion.div>
      )}

      {/* Header */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-orbitron font-bold text-white">
            Welcome back, <span className="gradient-text">{user.full_name?.split(" ")[0] || "Student"}</span>
          </h1>
          <p className="text-slate-400 text-sm mt-1">Ready to level up today?</p>
        </div>
        <div className="flex items-center gap-3 flex-wrap">
          <button onClick={handleShare} disabled={sharing}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-white/12 text-slate-300 hover:text-white hover:border-white/20 text-sm font-medium transition-all">
            <Share2 size={15} /> {sharing ? "Generating..." : "Share Progress"}
          </button>
          <Link href="/quiz/create">
            <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }}
              className="btn-neon relative flex items-center gap-2 px-6 py-3 rounded-xl text-white font-semibold z-10">
              <span className="relative z-10 flex items-center gap-2"><Plus size={18} /> New Quiz</span>
            </motion.button>
          </Link>
        </div>
      </motion.div>

      {/* Share URL panel */}
      {shareUrl && (
        <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} className="glass-card border-purple-500/25 bg-purple-500/5 p-4 mb-5 flex items-center gap-3">
          <div className="flex-1 min-w-0">
            <p className="text-xs text-slate-400 mb-1">Your shareable progress link (parents/teachers can view without logging in):</p>
            <p className="text-sm text-purple-300 truncate font-mono">{shareUrl}</p>
          </div>
          <button onClick={handleCopy} className="flex-shrink-0 text-xs flex items-center gap-1 text-slate-400 hover:text-white transition-colors">
            {copied ? <><Check size={14} className="text-green-400" /> Copied</> : <><Copy size={14} /> Copy</>}
          </button>
          <button onClick={() => setShareUrl("")} className="flex-shrink-0 text-slate-600 hover:text-slate-400">
            <X size={16} />
          </button>
        </motion.div>
      )}

      {/* Subscription banner */}
      {!isSubscribed && (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass-card border-yellow-500/20 bg-yellow-500/5 p-4 mb-6 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <Star size={18} className="text-yellow-400" />
            <span className="text-sm text-slate-300">{freeRemaining > 0 ? `${freeRemaining} free quiz${freeRemaining !== 1 ? "zes" : ""} remaining` : "Free quizzes used up"}</span>
          </div>
          <Link href="/pricing" className="text-xs font-semibold text-yellow-400 hover:text-yellow-300 transition-colors whitespace-nowrap">
            Upgrade →
          </Link>
        </motion.div>
      )}

      {/* Stats row */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          { label: "Quizzes Done", value: stats.total_quizzes || 0, icon: Brain, color: "text-purple-400", bg: "bg-purple-500/10" },
          { label: "Avg Score", value: `${stats.average_score || 0}%`, icon: Target, color: "text-cyan-400", bg: "bg-cyan-500/10" },
          { label: "Study Time", value: `${stats.total_time_minutes || 0}m`, icon: Clock, color: "text-blue-400", bg: "bg-blue-500/10" },
          { label: "Day Streak", value: `${user.streak_days || 0} 🔥`, icon: Flame, color: "text-orange-400", bg: "bg-orange-500/10" },
        ].map((s, i) => (
          <motion.div key={s.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }}>
            <div className="glass-card p-5">
              <div className={`w-10 h-10 rounded-xl ${s.bg} flex items-center justify-center mb-3`}>
                <s.icon size={20} className={s.color} />
              </div>
              <div className="text-2xl font-orbitron font-bold text-white">{s.value}</div>
              <div className="text-xs text-slate-500 mt-1">{s.label}</div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* XP bar */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }} className="glass-card p-5 mb-6">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2 text-sm font-medium text-white">
            <Zap size={16} className="text-yellow-400" />
            XP Points
          </div>
          <div className="flex items-center gap-3">
            <Link href="/leaderboard" className="text-xs text-purple-400 hover:text-purple-300">View Leaderboard →</Link>
            <span className="text-xl font-orbitron font-bold gradient-text">{(user.xp_points || 0).toLocaleString()}</span>
          </div>
        </div>
        <div className="h-2 bg-white/5 rounded-full overflow-hidden">
          <motion.div initial={{ width: 0 }} animate={{ width: `${Math.min(100, ((user.xp_points || 0) % 1000) / 10)}%` }}
            transition={{ duration: 1, delay: 0.5 }} className="h-full progress-bar" />
        </div>
        <div className="text-xs text-slate-500 mt-1">Level {Math.floor((user.xp_points || 0) / 1000) + 1} — {(user.xp_points || 0) % 1000}/1000 XP to next level</div>
      </motion.div>

      <div className="grid lg:grid-cols-2 gap-6 mb-6">
        {radarData.length > 0 && (
          <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.4 }} className="glass-card p-6">
            <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
              <TrendingUp size={18} className="text-purple-400" /> Subject Performance
            </h3>
            <ResponsiveContainer width="100%" height={220}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="rgba(255,255,255,0.05)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: "#64748b", fontSize: 11 }} />
                <Radar name="Score" dataKey="score" stroke="#a855f7" fill="#a855f7" fillOpacity={0.2} strokeWidth={2} />
              </RadarChart>
            </ResponsiveContainer>
          </motion.div>
        )}

        {scoreData.length > 1 && (
          <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.5 }} className="glass-card p-6">
            <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
              <TrendingUp size={18} className="text-cyan-400" /> Score Trend
            </h3>
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={scoreData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                <XAxis dataKey="quiz" tick={{ fill: "#64748b", fontSize: 11 }} />
                <YAxis domain={[0, 100]} tick={{ fill: "#64748b", fontSize: 11 }} />
                <Tooltip contentStyle={{ background: "#0f0f1a", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 8, color: "#f1f5f9" }} />
                <Line type="monotone" dataKey="score" stroke="#06b6d4" strokeWidth={2} dot={{ fill: "#06b6d4", strokeWidth: 0, r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </motion.div>
        )}
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }} className="glass-card p-6">
          <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
            <BookOpen size={18} className="text-blue-400" /> Recent Quizzes
          </h3>
          {recentAttempts.length === 0 ? (
            <div className="text-center py-8">
              <Brain size={32} className="text-slate-600 mx-auto mb-3" />
              <p className="text-slate-500 text-sm">No quizzes yet. Start your first one!</p>
              <Link href="/quiz/create" className="text-purple-400 hover:text-purple-300 text-sm font-medium mt-2 inline-block">Create Quiz →</Link>
            </div>
          ) : (
            <div className="space-y-3">
              {recentAttempts.slice(0, 5).map((a: any) => (
                <Link key={a.id} href={`/quiz/result/${a.id}`}>
                  <div className="flex items-center justify-between p-3 rounded-lg bg-white/3 hover:bg-white/5 border border-white/5 hover:border-white/10 transition-all cursor-pointer">
                    <div>
                      <p className="text-sm font-medium text-white capitalize">{a.topic}</p>
                      <p className="text-xs text-slate-500">{a.subject?.replace("_", " ")} · {a.level?.replace("_", "-")}</p>
                    </div>
                    <div className="text-right">
                      <div className={`text-sm font-bold ${(a.score || 0) >= 70 ? "text-green-400" : (a.score || 0) >= 50 ? "text-yellow-400" : "text-red-400"}`}>
                        {a.score != null ? `${Math.round(a.score)}%` : "In progress"}
                      </div>
                      <div className="text-xs text-slate-600">{a.num_questions}q</div>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          )}
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.7 }} className="glass-card p-6">
          <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
            <Trophy size={18} className="text-yellow-400" /> Badges Earned
          </h3>
          {badges.length === 0 ? (
            <div className="text-center py-8">
              <Trophy size={32} className="text-slate-600 mx-auto mb-3" />
              <p className="text-slate-500 text-sm">Complete quizzes to earn badges!</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 gap-3">
              {badges.map((b: any) => (
                <div key={b.type} className="glass-card p-3 border-yellow-500/20 bg-yellow-500/5 text-center">
                  <Trophy size={20} className="text-yellow-400 mx-auto mb-2" />
                  <p className="text-xs font-semibold text-white">{b.name}</p>
                  <p className="text-xs text-slate-500 mt-1">{b.description}</p>
                </div>
              ))}
            </div>
          )}
        </motion.div>
      </div>
    </div>
  );
}
