"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";
import { Trophy, Target, Zap, CheckCircle, XCircle, ChevronDown, ChevronUp, ArrowRight, Brain, Loader2 } from "lucide-react";
import { quizAPI } from "@/lib/api";
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer } from "recharts";

export default function ResultPage() {
  const { id } = useParams() as { id: string };
  const router = useRouter();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [expandedQ, setExpandedQ] = useState<string | null>(null);

  useEffect(() => {
    quizAPI.result(id).then((res) => { setData(res.data); setLoading(false); }).catch(() => router.push("/dashboard"));
  }, [id, router]);

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <Loader2 size={32} className="text-purple-400 animate-spin mx-auto mb-3" />
        <p className="text-slate-400 text-sm">Loading your results...</p>
      </div>
    </div>
  );

  const analysis = data?.analysis;
  const attempt = data?.attempt;
  if (!analysis) return null;

  const score = Math.round(analysis.overall_score || 0);
  const grade = analysis.estimated_grade || "N/A";
  const scoreColor = score >= 70 ? "text-green-400" : score >= 50 ? "text-yellow-400" : "text-red-400";
  const scoreGlow = score >= 70 ? "shadow-[0_0_30px_rgba(16,185,129,0.4)]" : score >= 50 ? "shadow-[0_0_30px_rgba(234,179,8,0.4)]" : "shadow-[0_0_30px_rgba(239,68,68,0.4)]";

  const radarData = Object.entries(analysis.subtopic_scores || {}).slice(0, 8).map(([k, v]) => ({
    subject: k.replace(/_/g, " ").slice(0, 12),
    score: Math.round(v as number),
  }));

  const breakdown = analysis.question_breakdown || [];

  return (
    <div className="min-h-screen grid-bg px-4 sm:px-6 py-8 max-w-4xl mx-auto">
      <div className="orb w-80 h-80 bg-purple-600/15 top-0 right-0" />

      {/* Score hero */}
      <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.6 }} className="text-center mb-8">
        <div className={`inline-flex items-center justify-center w-36 h-36 rounded-full border-4 ${score >= 70 ? "border-green-500/50" : score >= 50 ? "border-yellow-500/50" : "border-red-500/50"} mb-6 relative ${scoreGlow}`}>
          <div className="text-center">
            <div className={`text-4xl font-orbitron font-black ${scoreColor}`}>{score}%</div>
            <div className="text-xs text-slate-400">score</div>
          </div>
        </div>
        <h1 className="text-3xl font-orbitron font-bold text-white mb-2">
          {score >= 80 ? "Excellent Work!" : score >= 60 ? "Good Job!" : score >= 40 ? "Keep Going!" : "Keep Practising!"}
        </h1>
        <p className="text-slate-400 capitalize mb-4">{attempt?.topic} · {attempt?.subject?.replace("_", " ")} · {attempt?.exam_board}</p>

        <div className="flex items-center justify-center gap-4 flex-wrap">
          <div className="glass-card px-6 py-3 text-center">
            <div className="text-2xl font-orbitron font-bold gradient-text">{grade}</div>
            <div className="text-xs text-slate-500">Estimated Grade</div>
          </div>
          <div className="glass-card px-6 py-3 text-center">
            <div className="text-2xl font-orbitron font-bold text-green-400">{breakdown.filter((q: any) => q.is_correct).length}</div>
            <div className="text-xs text-slate-500">Correct</div>
          </div>
          <div className="glass-card px-6 py-3 text-center">
            <div className="text-2xl font-orbitron font-bold text-red-400">{breakdown.filter((q: any) => !q.is_correct).length}</div>
            <div className="text-xs text-slate-500">Incorrect</div>
          </div>
          {attempt?.time_taken_seconds && (
            <div className="glass-card px-6 py-3 text-center">
              <div className="text-2xl font-orbitron font-bold text-cyan-400">{Math.floor(attempt.time_taken_seconds / 60)}m</div>
              <div className="text-xs text-slate-500">Time Taken</div>
            </div>
          )}
        </div>
      </motion.div>

      {/* AI Feedback */}
      {analysis.ai_feedback && (
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="glass-card p-6 mb-6 border-purple-500/20 bg-purple-500/5">
          <div className="flex items-center gap-2 mb-3">
            <Brain size={18} className="text-purple-400" />
            <h3 className="font-semibold text-white">AI Feedback</h3>
          </div>
          <p className="text-slate-300 text-sm leading-relaxed">{analysis.ai_feedback}</p>
          {analysis.improvement_tips?.length > 0 && (
            <div className="mt-4 space-y-2">
              {analysis.improvement_tips.map((tip: string, i: number) => (
                <div key={i} className="flex items-start gap-2 text-sm text-slate-400">
                  <span className="text-purple-400 font-bold mt-0.5">→</span> {tip}
                </div>
              ))}
            </div>
          )}
        </motion.div>
      )}

      <div className="grid md:grid-cols-2 gap-6 mb-6">
        {/* Strengths & Weaknesses */}
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.4 }} className="glass-card p-6">
          <h3 className="font-semibold text-white mb-4 flex items-center gap-2"><Target size={18} className="text-cyan-400" /> Topic Breakdown</h3>
          <div className="space-y-2 mb-4">
            {analysis.strength_areas?.length > 0 && (
              <div>
                <p className="text-xs text-green-400 font-medium mb-2">Strong Areas</p>
                {analysis.strength_areas.map((a: string) => (
                  <div key={a} className="flex items-center gap-2 text-sm text-slate-300 mb-1">
                    <CheckCircle size={14} className="text-green-400" /> {a}
                  </div>
                ))}
              </div>
            )}
            {analysis.weak_areas?.length > 0 && (
              <div>
                <p className="text-xs text-red-400 font-medium mb-2 mt-3">Needs Work</p>
                {analysis.weak_areas.map((a: string) => (
                  <div key={a} className="flex items-center gap-2 text-sm text-slate-300 mb-1">
                    <XCircle size={14} className="text-red-400" /> {a}
                  </div>
                ))}
              </div>
            )}
          </div>
        </motion.div>

        {/* Radar chart */}
        {radarData.length > 2 && (
          <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.5 }} className="glass-card p-6">
            <h3 className="font-semibold text-white mb-4 flex items-center gap-2"><Zap size={18} className="text-yellow-400" /> Subtopic Scores</h3>
            <ResponsiveContainer width="100%" height={200}>
              <RadarChart data={radarData}>
                <PolarGrid stroke="rgba(255,255,255,0.05)" />
                <PolarAngleAxis dataKey="subject" tick={{ fill: "#64748b", fontSize: 10 }} />
                <Radar dataKey="score" stroke="#a855f7" fill="#a855f7" fillOpacity={0.25} strokeWidth={2} />
              </RadarChart>
            </ResponsiveContainer>
          </motion.div>
        )}
      </div>

      {/* Question breakdown */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.6 }} className="glass-card p-6 mb-8">
        <h3 className="font-semibold text-white mb-4">Question by Question Review</h3>
        <div className="space-y-3">
          {breakdown.map((item: any, i: number) => (
            <div key={item.question_id} className={`rounded-xl border p-4 ${item.is_correct ? "border-green-500/20 bg-green-500/5" : "border-red-500/20 bg-red-500/5"}`}>
              <button className="w-full flex items-start justify-between gap-4 text-left" onClick={() => setExpandedQ(expandedQ === item.question_id ? null : item.question_id)}>
                <div className="flex items-start gap-3">
                  {item.is_correct ? <CheckCircle size={18} className="text-green-400 flex-shrink-0 mt-0.5" /> : <XCircle size={18} className="text-red-400 flex-shrink-0 mt-0.5" />}
                  <div>
                    <p className="text-sm text-white font-medium">Q{i + 1}: {item.question.slice(0, 80)}{item.question.length > 80 ? "..." : ""}</p>
                    <p className="text-xs text-slate-500 mt-0.5">{item.marks_earned}/{item.marks_available} marks · {item.subtopic}</p>
                  </div>
                </div>
                {expandedQ === item.question_id ? <ChevronUp size={16} className="text-slate-500 flex-shrink-0 mt-1" /> : <ChevronDown size={16} className="text-slate-500 flex-shrink-0 mt-1" />}
              </button>

              {expandedQ === item.question_id && (
                <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: "auto" }} className="mt-4 pt-4 border-t border-white/5 space-y-2">
                  <p className="text-sm text-white">{item.question}</p>
                  <div className="flex gap-4 text-xs">
                    <span className="text-slate-400">Your answer: <span className={item.is_correct ? "text-green-400 font-semibold" : "text-red-400 font-semibold"}>{item.user_answer || "Not answered"}</span></span>
                    {!item.is_correct && <span className="text-slate-400">Correct: <span className="text-green-400 font-semibold">{item.correct_answer}</span></span>}
                  </div>
                  {item.explanation && <p className="text-sm text-slate-400 leading-relaxed bg-white/3 rounded-lg p-3">{item.explanation}</p>}
                </motion.div>
              )}
            </div>
          ))}
        </div>
      </motion.div>

      {/* CTA */}
      <div className="flex flex-col sm:flex-row gap-4 justify-center">
        <Link href="/quiz/create">
          <motion.button whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.97 }} className="btn-neon relative flex items-center gap-2 px-8 py-3 rounded-xl text-white font-semibold z-10">
            <span className="relative z-10 flex items-center gap-2"><Brain size={18} /> New Quiz <ArrowRight size={16} /></span>
          </motion.button>
        </Link>
        <Link href="/dashboard">
          <button className="flex items-center gap-2 px-8 py-3 rounded-xl border border-white/10 text-slate-300 hover:text-white hover:border-white/20 transition-all font-semibold">
            <Trophy size={18} /> View Dashboard
          </button>
        </Link>
      </div>
    </div>
  );
}
