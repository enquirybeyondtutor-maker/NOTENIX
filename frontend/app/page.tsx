"use client";
import { motion } from "framer-motion";
import Link from "next/link";
import { ArrowRight, Zap, Brain, Target, TrendingUp, Star, CheckCircle, BookOpen, BarChart3, Repeat, Clock, Trophy, Sparkles } from "lucide-react";

const SUBJECTS = [
  { label: "Mathematics", icon: "∑", color: "bg-purple-100 text-purple-700" },
  { label: "Biology", icon: "🧬", color: "bg-green-100 text-green-700" },
  { label: "Chemistry", icon: "⚗️", color: "bg-blue-100 text-blue-700" },
  { label: "Physics", icon: "⚡", color: "bg-yellow-100 text-yellow-700" },
  { label: "Computer Science", icon: "💻", color: "bg-pink-100 text-pink-700" },
  { label: "Economics", icon: "📈", color: "bg-teal-100 text-teal-700" },
  { label: "English Literature", icon: "📚", color: "bg-rose-100 text-rose-700" },
  { label: "Geography", icon: "🌍", color: "bg-sky-100 text-sky-700" },
  { label: "History", icon: "🏛️", color: "bg-amber-100 text-amber-700" },
  { label: "Psychology", icon: "🧠", color: "bg-violet-100 text-violet-700" },
  { label: "Business", icon: "💼", color: "bg-slate-100 text-slate-700" },
];

const FEATURES = [
  { icon: Brain, title: "AI-Generated Questions", desc: "Claude AI creates unique questions from the exact spec of your exam board — AQA, Edexcel, OCR and more.", color: "bg-purple-100 text-purple-600" },
  { icon: Target, title: "Instant Analysis", desc: "Get a grade estimate (GCSE 1–9 or A-Level A*–E), strengths, weaknesses and subtopic breakdown after every quiz.", color: "bg-pink-100 text-pink-600" },
  { icon: Repeat, title: "Spaced Repetition", desc: "Our SM-2 algorithm resurfaces your weakest topics at the optimal time so nothing slips through the cracks.", color: "bg-blue-100 text-blue-600" },
  { icon: TrendingUp, title: "Progress Tracking", desc: "Beautiful dashboards show your score trends, subject radar charts, XP points and daily streaks.", color: "bg-green-100 text-green-600" },
  { icon: Clock, title: "Mock Exam Mode", desc: "Timed sessions that simulate real exam conditions and build confidence before the big day.", color: "bg-amber-100 text-amber-600" },
  { icon: Trophy, title: "Leaderboards & Badges", desc: "Compete with students across the UK, earn badges and climb the weekly leaderboard.", color: "bg-rose-100 text-rose-600" },
];

const BOARDS = ["AQA", "Edexcel", "OCR", "Cambridge", "WJEC", "CCEA"];

const STATS = [
  { value: "10+", label: "Subjects covered" },
  { value: "6", label: "Exam boards" },
  { value: "AI", label: "Powered by Claude" },
  { value: "Free", label: "To get started" },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen">

      {/* Hero */}
      <section className="grid-bg relative overflow-hidden pt-20 pb-24 px-4">
        <div className="orb w-[500px] h-[500px] bg-purple-300/30 top-[-100px] right-[-100px]" />
        <div className="orb w-[300px] h-[300px] bg-pink-300/20 bottom-0 left-[-50px]" />

        <div className="max-w-7xl mx-auto relative z-10">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left */}
            <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7 }}>
              <div className="badge-pill mb-6">
                <Sparkles size={14} className="text-purple-500" />
                AI-powered quiz platform · GCSE & A-Level
              </div>

              <h1 className="text-5xl sm:text-6xl font-bold leading-tight mb-6 text-[#1E1B4B]">
                Master Your<br />
                <span className="text-pink-500">Exams</span> with AI
              </h1>

              <p className="text-lg text-gray-500 mb-8 leading-relaxed max-w-lg">
                Generate unlimited practice quizzes from your exact exam board spec. Get instant AI feedback, track your progress and climb from Grade 4 to Grade 9.
              </p>

              <div className="flex flex-wrap gap-4 mb-8">
                <Link href="/register">
                  <motion.button whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }} className="btn-primary text-base py-3.5 px-7">
                    Start for Free →
                  </motion.button>
                </Link>
                <Link href="/login">
                  <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} className="btn-secondary text-base py-3.5 px-7">
                    Sign in
                  </motion.button>
                </Link>
              </div>

              <div className="flex items-center gap-6 flex-wrap">
                <div className="flex items-center gap-1.5">
                  {[...Array(5)].map((_, i) => <Star key={i} size={16} className="text-yellow-400 fill-yellow-400" />)}
                  <span className="text-sm text-gray-500 ml-1">4.9/5 from students</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <CheckCircle size={15} className="text-green-500" />
                  No credit card required
                </div>
              </div>
            </motion.div>

            {/* Right — hero visual */}
            <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.8, delay: 0.2 }}
              className="relative flex items-center justify-center py-16">

              <div className="animate-float">
                <div className="w-72 h-72 sm:w-80 sm:h-80 rounded-[40px] bg-gradient-to-br from-purple-600 via-purple-500 to-pink-500 flex items-center justify-center shadow-[0_30px_80px_rgba(124,58,237,0.4)]">
                  <div className="text-center text-white p-8">
                    <div className="text-6xl mb-4">🧠</div>
                    <div className="text-xl font-bold mb-1">Quiz Generated!</div>
                    <div className="text-purple-200 text-sm">10 questions · Algebra · AQA</div>
                    <div className="mt-4 bg-white/20 rounded-full px-4 py-2 text-sm font-semibold backdrop-blur-sm">
                      Start Quiz →
                    </div>
                  </div>
                </div>
              </div>

              <motion.div initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.6 }}
                className="stat-card absolute top-8 -left-4 sm:-left-8">
                <div className="text-xs text-gray-500 mb-0.5">Grade Estimate</div>
                <div className="text-2xl font-bold text-purple-600">A*</div>
              </motion.div>

              <motion.div initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: 0.7 }}
                className="stat-card absolute bottom-16 -right-4 sm:-right-8">
                <div className="text-xs text-gray-500 mb-0.5">Score</div>
                <div className="text-2xl font-bold text-pink-500">92%</div>
              </motion.div>

              <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.8 }}
                className="stat-card absolute bottom-2 left-8">
                <div className="flex items-center gap-2">
                  <span className="text-xl">🔥</span>
                  <div>
                    <div className="text-xs text-gray-500">Streak</div>
                    <div className="font-bold text-[#1E1B4B]">7 days</div>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Exam boards */}
      <section className="bg-white border-y border-purple-100 py-5 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="flex flex-wrap items-center justify-center gap-3 sm:gap-5">
            <span className="text-sm text-gray-400 font-medium">Aligned to every major exam board:</span>
            {BOARDS.map((b) => (
              <span key={b} className="px-4 py-1.5 rounded-full bg-purple-50 text-purple-700 text-sm font-semibold border border-purple-100">{b}</span>
            ))}
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-4xl mx-auto grid grid-cols-2 sm:grid-cols-4 gap-6">
          {STATS.map((s, i) => (
            <motion.div key={s.label} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }} viewport={{ once: true }} className="text-center">
              <div className="text-4xl font-bold gradient-text mb-1">{s.value}</div>
              <div className="text-sm text-gray-500">{s.label}</div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* Subjects */}
      <section id="subjects" className="grid-bg py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <div className="section-label mb-3">Subjects</div>
            <h2 className="text-3xl sm:text-4xl font-bold text-[#1E1B4B]">Every subject covered</h2>
            <p className="text-gray-500 mt-3 max-w-lg mx-auto">From Maths to Psychology — practise any topic, any difficulty, any exam board.</p>
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
            {SUBJECTS.map((s, i) => (
              <motion.div key={s.label} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }} viewport={{ once: true }}>
                <Link href="/register">
                  <div className="card card-hover p-5 cursor-pointer">
                    <div className={`w-11 h-11 rounded-xl ${s.color} flex items-center justify-center text-xl mb-3`}>{s.icon}</div>
                    <p className="font-semibold text-sm text-[#1E1B4B]">{s.label}</p>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="bg-white py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <div className="section-label mb-3">Features</div>
            <h2 className="text-3xl sm:text-4xl font-bold text-[#1E1B4B]">Everything you need to <span className="text-pink-500">ace your exams</span></h2>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map((f, i) => (
              <motion.div key={f.title} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.08 }} viewport={{ once: true }}>
                <div className="card card-hover p-6 h-full">
                  <div className={`w-12 h-12 rounded-2xl ${f.color} flex items-center justify-center mb-4`}>
                    <f.icon size={22} />
                  </div>
                  <h3 className="font-bold text-[#1E1B4B] mb-2">{f.title}</h3>
                  <p className="text-sm text-gray-500 leading-relaxed">{f.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="grid-bg py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <div className="section-label mb-3">How it works</div>
            <h2 className="text-3xl sm:text-4xl font-bold text-[#1E1B4B]">From zero to Grade 9 in 3 steps</h2>
          </div>
          <div className="grid sm:grid-cols-3 gap-8">
            {[
              { step: "01", title: "Choose your topic", desc: "Pick your subject, exam board and the specific topic you want to practise.", icon: BookOpen },
              { step: "02", title: "AI generates your quiz", desc: "Claude AI creates unique, board-aligned multiple choice questions in seconds.", icon: Zap },
              { step: "03", title: "Get your results", desc: "Receive a grade estimate, detailed breakdown and personalised study tips.", icon: BarChart3 },
            ].map((s, i) => (
              <motion.div key={s.step} initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.15 }} viewport={{ once: true }} className="text-center">
                <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-600 to-pink-500 flex items-center justify-center mx-auto mb-4 shadow-purple">
                  <s.icon size={24} className="text-white" />
                </div>
                <div className="text-xs font-bold text-purple-400 mb-1">Step {s.step}</div>
                <h3 className="font-bold text-[#1E1B4B] mb-2">{s.title}</h3>
                <p className="text-sm text-gray-500 leading-relaxed">{s.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="bg-white py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <div className="section-label mb-3">Pricing</div>
            <h2 className="text-3xl sm:text-4xl font-bold text-[#1E1B4B]">Simple, transparent pricing</h2>
          </div>
          <div className="grid sm:grid-cols-2 gap-6 max-w-2xl mx-auto">
            {[
              { name: "Free", price: "£0", desc: "3 quizzes to try it out", features: ["3 AI quizzes", "Basic analysis", "Progress tracking"], cta: "Get Started Free", href: "/register", highlight: false },
              { name: "Unlimited", price: "£100", period: "/month", desc: "Everything you need to excel", features: ["Unlimited quizzes", "Full AI analysis", "Spaced repetition", "AI study planner", "Leaderboard access"], cta: "Start Free Trial", href: "/register", highlight: true },
            ].map((plan) => (
              <div key={plan.name} className={`card p-8 relative ${plan.highlight ? "border-purple-300 shadow-card-lg" : ""}`}>
                {plan.highlight && (
                  <div className="absolute -top-3.5 left-1/2 -translate-x-1/2 whitespace-nowrap">
                    <span className="btn-primary text-xs py-1.5 px-4">Most Popular</span>
                  </div>
                )}
                <div className="text-sm font-semibold text-purple-600 mb-2">{plan.name}</div>
                <div className="flex items-baseline gap-1 mb-1">
                  <span className="text-4xl font-bold text-[#1E1B4B]">{plan.price}</span>
                  {plan.period && <span className="text-gray-500 text-sm">{plan.period}</span>}
                </div>
                <p className="text-sm text-gray-500 mb-6">{plan.desc}</p>
                <div className="space-y-3 mb-8">
                  {plan.features.map((f) => (
                    <div key={f} className="flex items-center gap-2 text-sm text-gray-600">
                      <CheckCircle size={15} className="text-green-500 flex-shrink-0" /> {f}
                    </div>
                  ))}
                </div>
                <Link href={plan.href} className="block">
                  <button className={`w-full py-3 rounded-2xl font-semibold text-sm transition-all ${plan.highlight ? "btn-primary justify-center" : "btn-secondary justify-center"}`}>
                    {plan.cta}
                  </button>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="grid-bg py-20 px-4">
        <motion.div initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} className="max-w-2xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold text-[#1E1B4B] mb-4">
            Ready to unlock your <span className="text-pink-500">potential?</span>
          </h2>
          <p className="text-gray-500 mb-8">Join students across the UK using AI to go from predicted grades to actual grades.</p>
          <Link href="/register">
            <motion.button whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.97 }} className="btn-primary text-base py-4 px-10">
              Start for Free — No card needed →
            </motion.button>
          </Link>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-purple-100 py-8 px-4">
        <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-purple-600 to-pink-500 flex items-center justify-center">
              <Zap size={14} className="text-white" />
            </div>
            <span className="font-bold text-[#1E1B4B]"><span className="text-purple-600">Note</span>nix</span>
          </div>
          <p className="text-xs text-gray-400">© 2025 Notenix. Built for UK students. Powered by Claude AI.</p>
          <div className="flex items-center gap-4 text-xs text-gray-400">
            <Link href="/pricing" className="hover:text-purple-600">Pricing</Link>
            <Link href="/login" className="hover:text-purple-600">Login</Link>
            <Link href="/register" className="hover:text-purple-600">Sign up</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
