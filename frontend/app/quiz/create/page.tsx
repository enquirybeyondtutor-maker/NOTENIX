"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { Brain, ChevronRight, Sparkles, Loader2, BookOpen, Target, GraduationCap, LayoutGrid, CheckCircle2 } from "lucide-react";
import { quizAPI } from "@/lib/api";

const SUBJECTS = [
  { id: "maths", label: "Mathematics", icon: "∑", color: "from-purple-500 to-indigo-600" },
  { id: "biology", label: "Biology", icon: "🧬", color: "from-green-500 to-emerald-600" },
  { id: "chemistry", label: "Chemistry", icon: "⚗️", color: "from-blue-500 to-cyan-600" },
  { id: "physics", label: "Physics", icon: "⚡", color: "from-yellow-500 to-orange-600" },
  { id: "computer_science", label: "Computer Science", icon: "💻", color: "from-pink-500 to-rose-600" },
  { id: "economics", label: "Economics", icon: "📈", color: "from-teal-500 to-cyan-600" },
  { id: "english_literature", label: "English Lit.", icon: "📚", color: "from-rose-500 to-pink-600" },
  { id: "geography", label: "Geography", icon: "🌍", color: "from-sky-500 to-blue-600" },
  { id: "history", label: "History", icon: "🏛️", color: "from-amber-500 to-yellow-600" },
  { id: "psychology", label: "Psychology", icon: "🧠", color: "from-violet-500 to-purple-600" },
  { id: "business", label: "Business", icon: "💼", color: "from-slate-500 to-slate-600" },
];

const LEVELS = [
  { id: "gcse", label: "GCSE", desc: "Year 10–11" },
  { id: "a_level", label: "A-Level", desc: "Year 12–13" },
];

const BOARDS = ["AQA", "Edexcel", "OCR", "Cambridge"];
const DIFFICULTIES = [
  { id: "easy", label: "Easy", desc: "1-2 mark recall questions" },
  { id: "medium", label: "Medium", desc: "Application questions" },
  { id: "hard", label: "Hard", desc: "Analysis & evaluation" },
  { id: "mixed", label: "Mixed", desc: "Variety of difficulty" },
];
const QN_OPTIONS = [5, 10, 15, 20, 30];

export default function CreateQuizPage() {
  const router = useRouter();
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({ subject: "", topic: "", level: "gcse", exam_board: "AQA", num_questions: 10, difficulty: "mixed", is_mock_exam: false });
  const [loading, setLoading] = useState(false);
  const [loadStep, setLoadStep] = useState(0);
  const [error, setError] = useState("");

  const canProceed = () => {
    if (step === 1) return !!form.subject;
    if (step === 2) return !!form.level && !!form.exam_board;
    if (step === 3) return !!form.topic.trim();
    return true;
  };

  const GEN_STEPS = [
    { label: "Searching knowledge base", icon: BookOpen },
    { label: "Generating questions with AI", icon: Brain },
    { label: "Formatting your quiz", icon: Sparkles },
  ];

  const handleCreate = async () => {
    setLoading(true);
    setLoadStep(1);
    setError("");

    const stepTimer = setInterval(() => {
      setLoadStep((s) => (s < 3 ? s + 1 : s));
    }, 6000);

    try {
      const res = await quizAPI.create(form);
      clearInterval(stepTimer);
      setLoadStep(3);
      localStorage.setItem(`quiz_${res.data.attempt_id}`, JSON.stringify(res.data));
      router.push(`/quiz/${res.data.attempt_id}`);
    } catch (err: any) {
      clearInterval(stepTimer);
      const detail = err.response?.data?.detail;
      if (err.response?.status === 402) {
        router.push("/pricing");
      } else {
        setError(detail || "Failed to generate quiz. Please try again.");
        setLoading(false);
        setLoadStep(0);
      }
    }
  };

  const steps = ["Subject", "Level & Board", "Topic & Settings", "Generate"];

  return (
    <div className="min-h-screen grid-bg px-4 sm:px-6 py-8 max-w-4xl mx-auto">
      <div className="orb w-80 h-80 bg-purple-600/10 top-0 right-0" />

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <div className="text-center mb-8">
          <h1 className="text-2xl font-orbitron font-bold text-white mb-2">Create a Quiz</h1>
          <p className="text-slate-400 text-sm">AI-generated questions from your exact exam board spec</p>
        </div>

        {/* Step indicator */}
        <div className="flex items-center justify-center gap-2 mb-8">
          {steps.map((s, i) => (
            <div key={s} className="flex items-center gap-2">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-all ${i + 1 === step ? "bg-purple-500 text-white" : i + 1 < step ? "bg-green-500/20 text-green-400 border border-green-500/30" : "bg-white/5 text-slate-500 border border-white/10"}`}>
                {i + 1 < step ? "✓" : i + 1}
              </div>
              <span className={`text-xs hidden sm:block ${i + 1 === step ? "text-white" : "text-slate-600"}`}>{s}</span>
              {i < steps.length - 1 && <div className="w-8 h-px bg-white/10 hidden sm:block" />}
            </div>
          ))}
        </div>

        <div className="glass-card p-8 relative z-10">
          {/* Step 1: Subject */}
          {step === 1 && (
            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}>
              <h2 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
                <LayoutGrid size={20} className="text-purple-400" /> Choose Subject
              </h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                {SUBJECTS.map((s) => (
                  <motion.button key={s.id} whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}
                    onClick={() => setForm({ ...form, subject: s.id })}
                    className={`p-4 rounded-xl border text-left transition-all ${form.subject === s.id ? "border-purple-500/50 bg-purple-500/15 shadow-neon-purple" : "border-white/8 bg-white/3 hover:border-white/15 hover:bg-white/5"}`}>
                    <div className={`w-10 h-10 rounded-lg bg-gradient-to-br ${s.color} flex items-center justify-center text-lg mb-3`}>{s.icon}</div>
                    <p className={`text-xs font-medium ${form.subject === s.id ? "text-white" : "text-slate-400"}`}>{s.label}</p>
                  </motion.button>
                ))}
              </div>
            </motion.div>
          )}

          {/* Step 2: Level & Board */}
          {step === 2 && (
            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}>
              <h2 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
                <GraduationCap size={20} className="text-cyan-400" /> Level & Exam Board
              </h2>
              <div className="mb-6">
                <p className="text-sm text-slate-400 mb-3">Qualification Level</p>
                <div className="grid grid-cols-2 gap-3">
                  {LEVELS.map((l) => (
                    <button key={l.id} onClick={() => setForm({ ...form, level: l.id })}
                      className={`p-4 rounded-xl border text-left transition-all ${form.level === l.id ? "border-cyan-500/50 bg-cyan-500/10" : "border-white/8 bg-white/3 hover:border-white/15"}`}>
                      <p className={`font-bold text-lg ${form.level === l.id ? "text-cyan-300" : "text-white"}`}>{l.label}</p>
                      <p className="text-xs text-slate-500">{l.desc}</p>
                    </button>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-sm text-slate-400 mb-3">Exam Board</p>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  {BOARDS.map((b) => (
                    <button key={b} onClick={() => setForm({ ...form, exam_board: b })}
                      className={`py-3 rounded-xl border font-semibold text-sm transition-all ${form.exam_board === b ? "border-purple-500/50 bg-purple-500/15 text-purple-300" : "border-white/8 bg-white/3 text-slate-400 hover:border-white/15 hover:text-white"}`}>
                      {b}
                    </button>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {/* Step 3: Topic & Settings */}
          {step === 3 && (
            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}>
              <h2 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
                <BookOpen size={20} className="text-blue-400" /> Topic & Settings
              </h2>
              <div className="mb-6">
                <label className="text-xs text-slate-400 font-medium mb-2 block uppercase tracking-wider">Topic Name</label>
                <input
                  type="text" value={form.topic} onChange={(e) => setForm({ ...form, topic: e.target.value })}
                  placeholder={`e.g. Quadratic equations, Cell division, Organic chemistry...`}
                  className="w-full bg-white/5 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-slate-600 focus:outline-none focus:border-purple-500/50 transition-all"
                />
              </div>
              <div className="grid sm:grid-cols-2 gap-6">
                <div>
                  <p className="text-xs text-slate-400 font-medium mb-3 uppercase tracking-wider">Number of Questions</p>
                  <div className="flex flex-wrap gap-2">
                    {QN_OPTIONS.map((n) => (
                      <button key={n} onClick={() => setForm({ ...form, num_questions: n })}
                        className={`px-4 py-2 rounded-lg border text-sm font-medium transition-all ${form.num_questions === n ? "border-purple-500/50 bg-purple-500/15 text-purple-300" : "border-white/8 text-slate-400 hover:border-white/15 hover:text-white"}`}>
                        {n}
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <p className="text-xs text-slate-400 font-medium mb-3 uppercase tracking-wider">Difficulty</p>
                  <div className="space-y-2">
                    {DIFFICULTIES.map((d) => (
                      <button key={d.id} onClick={() => setForm({ ...form, difficulty: d.id })}
                        className={`w-full flex items-center justify-between px-4 py-2.5 rounded-lg border text-sm transition-all ${form.difficulty === d.id ? "border-purple-500/50 bg-purple-500/15" : "border-white/8 bg-white/3 hover:border-white/15"}`}>
                        <span className={form.difficulty === d.id ? "text-white font-medium" : "text-slate-400"}>{d.label}</span>
                        <span className="text-xs text-slate-600">{d.desc}</span>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
              <div className="mt-4">
                <label className="flex items-center gap-3 cursor-pointer">
                  <div onClick={() => setForm({ ...form, is_mock_exam: !form.is_mock_exam })}
                    className={`w-10 h-6 rounded-full transition-all relative ${form.is_mock_exam ? "bg-purple-500" : "bg-white/10"}`}>
                    <div className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-all ${form.is_mock_exam ? "left-5" : "left-1"}`} />
                  </div>
                  <span className="text-sm text-slate-300">Mock Exam Mode (timed)</span>
                </label>
              </div>
            </motion.div>
          )}

          {/* Step 4: Review & Generate */}
          {step === 4 && (
            <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}>
              <h2 className="text-lg font-semibold text-white mb-6 flex items-center gap-2">
                <Sparkles size={20} className="text-yellow-400" /> Ready to Generate
              </h2>
              <div className="grid sm:grid-cols-2 gap-4 mb-8">
                {[
                  { label: "Subject", value: SUBJECTS.find(s => s.id === form.subject)?.label || form.subject },
                  { label: "Topic", value: form.topic },
                  { label: "Level", value: form.level === "a_level" ? "A-Level" : "GCSE" },
                  { label: "Exam Board", value: form.exam_board },
                  { label: "Questions", value: form.num_questions.toString() },
                  { label: "Difficulty", value: form.difficulty.charAt(0).toUpperCase() + form.difficulty.slice(1) },
                ].map(({ label, value }) => (
                  <div key={label} className="bg-white/3 rounded-lg p-4 border border-white/5">
                    <p className="text-xs text-slate-500 mb-1">{label}</p>
                    <p className="text-sm font-medium text-white capitalize">{value}</p>
                  </div>
                ))}
              </div>
              {error && <div className="text-red-400 text-sm mb-4 bg-red-500/10 border border-red-500/20 rounded-lg p-3">{error}</div>}

              {loading ? (
                <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="py-6">
                  <p className="text-center text-sm text-slate-400 mb-6 font-medium">Claude AI is generating your quiz...</p>
                  <div className="space-y-4">
                    {GEN_STEPS.map((s, i) => {
                      const done = loadStep > i + 1;
                      const active = loadStep === i + 1;
                      return (
                        <motion.div key={s.label} initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.15 }}
                          className={`flex items-center gap-4 p-4 rounded-xl border transition-all ${done ? "border-green-500/25 bg-green-500/5" : active ? "border-purple-500/40 bg-purple-500/8" : "border-white/5 opacity-40"}`}>
                          <div className={`w-9 h-9 rounded-lg flex items-center justify-center flex-shrink-0 ${done ? "bg-green-500/20" : active ? "bg-purple-500/20" : "bg-white/5"}`}>
                            {done ? <CheckCircle2 size={18} className="text-green-400" /> : active ? <Loader2 size={18} className="text-purple-400 animate-spin" /> : <s.icon size={18} className="text-slate-600" />}
                          </div>
                          <span className={`text-sm font-medium ${done ? "text-green-300" : active ? "text-white" : "text-slate-600"}`}>{s.label}</span>
                        </motion.div>
                      );
                    })}
                  </div>
                  <p className="text-center text-xs text-slate-600 mt-5">Typically 15–30 seconds. Don&apos;t navigate away.</p>
                </motion.div>
              ) : (
                <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} onClick={handleCreate}
                  className="btn-neon relative w-full py-4 rounded-xl text-white font-semibold text-lg flex items-center justify-center gap-3 z-10">
                  <span className="relative z-10 flex items-center gap-3"><Brain size={20} /> Generate Quiz with AI</span>
                </motion.button>
              )}
            </motion.div>
          )}

          {/* Navigation */}
          <div className="flex items-center justify-between mt-8 pt-6 border-t border-white/5">
            <button onClick={() => setStep(step - 1)} disabled={step === 1}
              className="px-5 py-2.5 rounded-lg border border-white/10 text-sm text-slate-400 hover:text-white hover:border-white/20 transition-all disabled:opacity-30 disabled:cursor-not-allowed">
              ← Back
            </button>
            {step < 4 ? (
              <motion.button whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }} onClick={() => setStep(step + 1)} disabled={!canProceed()}
                className="btn-neon relative px-6 py-2.5 rounded-lg text-white font-semibold text-sm flex items-center gap-2 disabled:opacity-30 disabled:cursor-not-allowed z-10">
                <span className="relative z-10 flex items-center gap-2">Continue <ChevronRight size={16} /></span>
              </motion.button>
            ) : null}
          </div>
        </div>
      </motion.div>
    </div>
  );
}
