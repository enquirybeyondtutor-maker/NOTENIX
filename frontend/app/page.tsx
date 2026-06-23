"use client";
import Link from "next/link";
import { motion } from "framer-motion";
import { Brain, Target, TrendingUp, Clock, Trophy, FileText, ArrowRight, Sparkles } from "lucide-react";

const features = [
  { icon: FileText, title: "Real past papers", desc: "Quizzes built from authentic GCSE & A-Level exam questions, not generic content." },
  { icon: Brain, title: "AI question generation", desc: "Fresh multiple-choice questions on any topic, grounded in real exam material." },
  { icon: Target, title: "Exam mode (Pro)", desc: "Practise actual past-paper questions and get your written answers marked by AI." },
  { icon: TrendingUp, title: "Track progress", desc: "See your average scores per subject, streaks, and earned badges over time." },
  { icon: Clock, title: "Spaced practice", desc: "Build consistent revision habits with daily streaks and XP." },
  { icon: Trophy, title: "Leaderboards", desc: "Compete with other students on weekly and all-time XP rankings." },
];

const steps = [
  { n: "1", title: "Pick your topic", desc: "Choose your level, subject and exact topic from real exam specifications." },
  { n: "2", title: "Take the quiz", desc: "Answer AI-generated MCQs or real past-paper questions in exam mode." },
  { n: "3", title: "Learn & improve", desc: "Get instant marking, explanations, and track your progress over time." },
];

export default function Landing() {
  return (
    <div className="grid-bg">
      {/* Hero */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 pt-16 pb-20 relative overflow-hidden">
        <div className="orb w-96 h-96 bg-purple-300/20 top-0 right-0" />
        <div className="grid md:grid-cols-2 gap-12 items-center relative z-10">
          <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
            <div className="badge-pill mb-6"><Sparkles size={14} className="text-purple-600" /> AI quizzes from real past papers · GCSE & A-Level</div>
            <h1 className="text-4xl sm:text-5xl font-extrabold leading-tight mb-5">
              Master your exams with <span className="gradient-text">real past-paper</span> practice
            </h1>
            <p className="text-lg text-gray-600 mb-8 leading-relaxed">
              Notenix turns authentic GCSE & A-Level exam papers into smart quizzes — with AI marking, progress tracking, and instant explanations.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link href="/register"><button className="btn-primary text-base py-3 px-7">Start for Free <ArrowRight size={18} /></button></Link>
              <Link href="/login"><button className="btn-secondary text-base py-3 px-7">Sign in</button></Link>
            </div>
          </motion.div>
          <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.7 }} className="relative">
            <div className="rounded-3xl bg-gradient-to-br from-purple-600 to-pink-500 p-8 shadow-card-lg aspect-[4/3] flex flex-col justify-center text-white">
              <div className="text-sm opacity-80 mb-2">A-Level Biology · ATP</div>
              <div className="font-semibold mb-4">Which correctly describes the structure of ATP?</div>
              <div className="space-y-2 text-sm">
                <div className="bg-white/15 rounded-xl px-3 py-2">A pentose sugar, three phosphates, adenine ✓</div>
                <div className="bg-white/10 rounded-xl px-3 py-2 opacity-70">A hexose sugar, two phosphates, adenine</div>
              </div>
            </div>
            <div className="stat-card absolute -bottom-5 -left-5 animate-float"><div className="text-xs text-gray-400">Avg score</div><div className="text-xl font-bold text-purple-600">92%</div></div>
            <div className="stat-card absolute -top-5 -right-3 animate-float" style={{ animationDelay: "1s" }}><div className="text-xs text-gray-400">Streak</div><div className="text-xl font-bold text-pink-500">🔥 7 days</div></div>
          </motion.div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="max-w-7xl mx-auto px-4 sm:px-6 py-16">
        <div className="text-center mb-12">
          <div className="section-label mb-3">Why Notenix</div>
          <h2 className="text-3xl font-bold">Everything you need to revise smarter</h2>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {features.map((f, i) => (
            <motion.div key={f.title} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ delay: i * 0.05 }}
              className="card card-hover p-6">
              <div className="w-11 h-11 rounded-xl bg-purple-50 flex items-center justify-center mb-4"><f.icon size={20} className="text-purple-600" /></div>
              <h3 className="font-bold mb-2">{f.title}</h3>
              <p className="text-sm text-gray-500 leading-relaxed">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section id="how" className="max-w-7xl mx-auto px-4 sm:px-6 py-16">
        <div className="text-center mb-12">
          <div className="section-label mb-3">How it works</div>
          <h2 className="text-3xl font-bold">Three steps to better grades</h2>
        </div>
        <div className="grid md:grid-cols-3 gap-6">
          {steps.map((s) => (
            <div key={s.n} className="card p-7 text-center">
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-purple-600 to-pink-500 text-white flex items-center justify-center text-xl font-bold mx-auto mb-4">{s.n}</div>
              <h3 className="font-bold mb-2">{s.title}</h3>
              <p className="text-sm text-gray-500">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-5xl mx-auto px-4 sm:px-6 py-16">
        <div className="rounded-3xl bg-gradient-to-br from-purple-600 to-pink-500 p-10 sm:p-14 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">Ready to ace your exams?</h2>
          <p className="opacity-90 mb-8 max-w-xl mx-auto">Start with 3 free quizzes. No credit card required.</p>
          <Link href="/register"><button className="bg-white text-purple-600 font-bold rounded-full px-8 py-3.5 inline-flex items-center gap-2 hover:scale-105 transition-transform">Get Started Free <ArrowRight size={18} /></button></Link>
        </div>
      </section>

      <footer className="border-t border-purple-100 py-8 text-center text-sm text-gray-400">
        <span className="font-bold"><span className="text-purple-600">Note</span>nix</span> · AI exam practice for GCSE & A-Level
      </footer>
    </div>
  );
}
