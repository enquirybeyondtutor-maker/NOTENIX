"use client";
import { motion } from "framer-motion";
import Link from "next/link";
import { Brain, Zap, Target, BarChart3, BookOpen, Shield, Star, ArrowRight, CheckCircle, Sparkles, Flame, Trophy } from "lucide-react";

const subjects = [
  { name: "Mathematics", icon: "∑", color: "from-purple-500 to-indigo-600", boards: "AQA · Edexcel · OCR" },
  { name: "Biology", icon: "🧬", color: "from-green-500 to-emerald-600", boards: "AQA · Edexcel · OCR" },
  { name: "Chemistry", icon: "⚗️", color: "from-blue-500 to-cyan-600", boards: "AQA · Edexcel · OCR" },
  { name: "Physics", icon: "⚡", color: "from-yellow-500 to-orange-600", boards: "AQA · Edexcel · OCR" },
  { name: "Computer Science", icon: "💻", color: "from-pink-500 to-rose-600", boards: "AQA · OCR · Cambridge" },
  { name: "Economics", icon: "📈", color: "from-teal-500 to-cyan-600", boards: "AQA · Edexcel · OCR" },
];

const features = [
  { icon: Brain, title: "RAG-Powered Questions", desc: "Questions generated from real exam board specifications and past paper knowledge base.", color: "text-purple-400" },
  { icon: Target, title: "Personalised Difficulty", desc: "AI adapts question difficulty based on your performance history and weak areas.", color: "text-cyan-400" },
  { icon: BarChart3, title: "Deep Analytics", desc: "Per-topic radar charts, grade estimates, and trend analysis over time.", color: "text-blue-400" },
  { icon: Flame, title: "Spaced Repetition", desc: "SM-2 algorithm resurfaces weak topics at optimal intervals to maximise retention.", color: "text-orange-400" },
  { icon: Trophy, title: "XP & Badges", desc: "Earn XP, maintain streaks, unlock badges and compete on leaderboards.", color: "text-yellow-400" },
  { icon: BookOpen, title: "Mock Exam Mode", desc: "Full timed mock exams with official marking schemes and PDF export.", color: "text-green-400" },
];

const stats = [
  { value: "10+", label: "Subjects covered" },
  { value: "4", label: "Exam boards" },
  { value: "GCSE & A-Level", label: "Both levels" },
  { value: "AI-powered", label: "Analysis engine" },
];

export default function LandingPage() {
  return (
    <div className="relative min-h-screen overflow-hidden grid-bg">
      {/* Ambient orbs */}
      <div className="orb w-[600px] h-[600px] bg-purple-600/20 top-[-200px] left-[-200px]" />
      <div className="orb w-[500px] h-[500px] bg-cyan-600/15 top-[200px] right-[-150px]" />
      <div className="orb w-[400px] h-[400px] bg-blue-600/10 bottom-[100px] left-[30%]" />

      {/* Hero */}
      <section className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 pt-24 pb-20 text-center">
        <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}>
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-purple-500/30 bg-purple-500/10 text-purple-300 text-sm font-medium mb-8">
            <Sparkles size={14} />
            <span>Powered by Claude AI + RAG Technology</span>
          </div>

          <h1 className="text-5xl sm:text-6xl md:text-7xl font-orbitron font-bold leading-tight mb-6">
            <span className="gradient-text">MASTER YOUR</span>
            <br />
            <span className="text-white">EXAMS WITH AI</span>
          </h1>

          <p className="text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            Generate unlimited GCSE & A-Level quizzes on any topic, get AI-powered analysis,
            track your progress and revise smarter — not harder.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <Link href="/register">
              <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }} className="btn-neon relative flex items-center gap-2 px-8 py-4 rounded-xl text-white font-semibold text-lg z-10">
                <span className="relative z-10 flex items-center gap-2">
                  Start for Free <ArrowRight size={18} />
                </span>
              </motion.button>
            </Link>
            <Link href="/pricing">
              <button className="flex items-center gap-2 px-8 py-4 rounded-xl border border-white/10 text-slate-300 hover:border-white/20 hover:text-white transition-all font-semibold text-lg">
                View Plans <ArrowRight size={18} />
              </button>
            </Link>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 max-w-3xl mx-auto">
            {stats.map((s) => (
              <div key={s.label} className="glass-card p-4 text-center">
                <div className="text-2xl font-orbitron font-bold gradient-text">{s.value}</div>
                <div className="text-xs text-slate-500 mt-1">{s.label}</div>
              </div>
            ))}
          </div>
        </motion.div>
      </section>

      {/* Subjects */}
      <section className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 py-20">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6 }}>
          <h2 className="text-3xl font-orbitron font-bold text-center text-white mb-4">All Major Subjects</h2>
          <p className="text-slate-400 text-center mb-12">Covering AQA, Edexcel, OCR and Cambridge specifications</p>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {subjects.map((s, i) => (
              <motion.div key={s.name} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.1 }} whileHover={{ y: -4 }}>
                <div className="glass-card p-6 cursor-pointer group hover:border-white/15 transition-all">
                  <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${s.color} flex items-center justify-center text-2xl mb-4 group-hover:scale-110 transition-transform`}>
                    {s.icon}
                  </div>
                  <h3 className="font-semibold text-white mb-1">{s.name}</h3>
                  <p className="text-xs text-slate-500">{s.boards}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </section>

      {/* Features */}
      <section className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 py-20">
        <motion.div initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }}>
          <h2 className="text-3xl font-orbitron font-bold text-center text-white mb-4">Everything You Need to Ace Your Exams</h2>
          <p className="text-slate-400 text-center mb-12 max-w-xl mx-auto">Advanced AI features designed specifically for UK exam preparation</p>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f, i) => (
              <motion.div key={f.title} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.08 }} whileHover={{ y: -4 }}>
                <div className="glass-card p-6 h-full">
                  <f.icon size={28} className={`${f.color} mb-4`} />
                  <h3 className="font-semibold text-white mb-2">{f.title}</h3>
                  <p className="text-sm text-slate-400 leading-relaxed">{f.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </section>

      {/* How it works */}
      <section className="relative z-10 max-w-5xl mx-auto px-4 sm:px-6 py-20">
        <h2 className="text-3xl font-orbitron font-bold text-center text-white mb-4">How It Works</h2>
        <p className="text-slate-400 text-center mb-12">Get quiz-ready in under 60 seconds</p>
        <div className="grid md:grid-cols-3 gap-8">
          {[
            { step: "01", title: "Choose Your Topic", desc: "Select subject, exam board, level and enter any topic from your syllabus.", icon: BookOpen },
            { step: "02", title: "AI Generates Quiz", desc: "Claude AI creates exam-style questions from our RAG knowledge base instantly.", icon: Brain },
            { step: "03", title: "Get Deep Analysis", desc: "Receive grade estimate, per-topic breakdown, AI feedback and study tips.", icon: BarChart3 },
          ].map((step, i) => (
            <motion.div key={step.step} initial={{ opacity: 0, x: -20 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.15 }}>
              <div className="glass-card p-6 text-center relative">
                <div className="text-5xl font-orbitron font-black gradient-text opacity-20 absolute top-4 right-4">{step.step}</div>
                <div className="w-14 h-14 rounded-2xl bg-purple-500/20 border border-purple-500/30 flex items-center justify-center mx-auto mb-4">
                  <step.icon size={24} className="text-purple-400" />
                </div>
                <h3 className="font-semibold text-white mb-2">{step.title}</h3>
                <p className="text-sm text-slate-400 leading-relaxed">{step.desc}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Pricing preview */}
      <section className="relative z-10 max-w-4xl mx-auto px-4 sm:px-6 py-20 text-center">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}>
          <div className="glass-card p-12 relative overflow-hidden">
            <div className="orb w-64 h-64 bg-purple-600/20 top-[-50px] right-[-50px]" />
            <h2 className="text-3xl font-orbitron font-bold text-white mb-4 relative z-10">Start Free, Scale When Ready</h2>
            <p className="text-slate-400 mb-8 relative z-10">3 free quizzes to get started. Unlimited access from £100/month.</p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-6 mb-8 relative z-10">
              <div className="glass-card px-8 py-4 border-purple-500/20">
                <div className="text-xs text-slate-500 mb-1">FREE TIER</div>
                <div className="text-2xl font-bold text-white">£0</div>
                <div className="text-xs text-slate-400">3 quizzes</div>
              </div>
              <div className="text-slate-600 font-bold text-xl hidden sm:block">→</div>
              <div className="glass-card px-8 py-4 border-purple-500/40 bg-purple-500/10">
                <div className="text-xs text-purple-400 mb-1">MONTHLY</div>
                <div className="text-2xl font-bold gradient-text">£100/mo</div>
                <div className="text-xs text-slate-400">Unlimited</div>
              </div>
              <div className="text-slate-600 font-bold text-xl hidden sm:block">or</div>
              <div className="glass-card px-8 py-4 border-cyan-500/40 bg-cyan-500/10">
                <div className="text-xs text-cyan-400 mb-1">YEARLY</div>
                <div className="text-2xl font-bold text-cyan-400">£1100/yr</div>
                <div className="text-xs text-slate-400">Save £100</div>
              </div>
            </div>
            <Link href="/register" className="relative z-10">
              <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.98 }} className="btn-neon relative px-10 py-4 rounded-xl text-white font-semibold text-lg z-10">
                <span className="relative z-10">Start Free — No Card Required</span>
              </motion.button>
            </Link>
          </div>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 border-t border-white/5 py-8 text-center">
        <div className="flex items-center justify-center gap-2 mb-2">
          <div className="w-6 h-6 rounded bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center">
            <Zap size={12} className="text-white" />
          </div>
          <span className="font-orbitron text-sm font-bold gradient-text">NOTENIX</span>
        </div>
        <p className="text-xs text-slate-600">© 2025 Notenix. AI-powered exam preparation for UK students.</p>
      </footer>
    </div>
  );
}
