"use client";
import { useEffect, useState, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useRouter, useParams } from "next/navigation";
import { Clock, ChevronRight, ChevronLeft, Flag, Brain, Loader2 } from "lucide-react";
import { quizAPI } from "@/lib/api";

interface Question {
  id: number;
  question: string;
  options: { A: string; B: string; C: string; D: string };
  marks: number;
  difficulty: string;
}

export default function QuizPage() {
  const router = useRouter();
  const { id } = useParams() as { id: string };
  const [questions, setQuestions] = useState<Question[]>([]);
  const [metadata, setMetadata] = useState<any>({});
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [currentQ, setCurrentQ] = useState(0);
  const [timeSeconds, setTimeSeconds] = useState(0);
  const [submitting, setSubmitting] = useState(false);
  const [loading, setLoading] = useState(true);
  const timerRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    const stored = localStorage.getItem(`quiz_${id}`);
    if (stored) {
      const data = JSON.parse(stored);
      setQuestions(data.questions);
      setMetadata({ subject: data.subject, topic: data.topic, level: data.level, exam_board: data.exam_board });
      setLoading(false);
      timerRef.current = setInterval(() => setTimeSeconds((t) => t + 1), 1000);
    } else {
      setLoading(false);
    }
    return () => { if (timerRef.current) clearInterval(timerRef.current); };
  }, [id]);

  const formatTime = (s: number) => `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
  const answered = Object.keys(answers).length;
  const progress = questions.length > 0 ? (answered / questions.length) * 100 : 0;

  const handleAnswer = (option: string) => {
    const qid = String(questions[currentQ].id);
    setAnswers({ ...answers, [qid]: option });
  };

  const handleSubmit = async () => {
    if (submitting) return;
    setSubmitting(true);
    if (timerRef.current) clearInterval(timerRef.current);
    try {
      await quizAPI.submit({ attempt_id: id, answers, time_taken_seconds: timeSeconds });
      localStorage.removeItem(`quiz_${id}`);
      router.push(`/quiz/result/${id}`);
    } catch (err) {
      setSubmitting(false);
    }
  };

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <Loader2 size={32} className="text-purple-400 animate-spin" />
    </div>
  );

  if (questions.length === 0) return (
    <div className="min-h-screen flex items-center justify-center text-center px-4">
      <div>
        <Brain size={48} className="text-slate-600 mx-auto mb-4" />
        <p className="text-white font-semibold mb-2">Quiz not found</p>
        <p className="text-slate-400 text-sm mb-4">This quiz may have expired or been completed already.</p>
        <button onClick={() => router.push("/quiz/create")} className="text-purple-400 hover:text-purple-300">Create a new quiz →</button>
      </div>
    </div>
  );

  const q = questions[currentQ];
  const currentAnswer = answers[String(q.id)];

  return (
    <div className="min-h-screen grid-bg px-4 sm:px-6 py-6 max-w-3xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="font-orbitron font-bold text-white text-sm capitalize">{metadata.topic}</h1>
          <p className="text-xs text-slate-500">{metadata.subject?.replace("_", " ")} · {metadata.exam_board}</p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 glass-card px-3 py-2">
            <Clock size={14} className="text-cyan-400" />
            <span className="font-orbitron text-sm text-white">{formatTime(timeSeconds)}</span>
          </div>
          <div className="text-sm text-slate-400">{answered}/{questions.length} answered</div>
        </div>
      </div>

      {/* Progress bar */}
      <div className="h-1.5 bg-white/5 rounded-full mb-6 overflow-hidden">
        <motion.div className="h-full progress-bar" animate={{ width: `${progress}%` }} transition={{ duration: 0.3 }} />
      </div>

      {/* Question dots */}
      <div className="flex flex-wrap gap-1.5 mb-6">
        {questions.map((_, i) => (
          <button key={i} onClick={() => setCurrentQ(i)}
            className={`w-7 h-7 rounded-md text-xs font-medium transition-all ${i === currentQ ? "bg-purple-500 text-white" : answers[String(questions[i].id)] ? "bg-purple-500/20 text-purple-400 border border-purple-500/30" : "bg-white/5 text-slate-500 hover:bg-white/10"}`}>
            {i + 1}
          </button>
        ))}
      </div>

      {/* Question card */}
      <AnimatePresence mode="wait">
        <motion.div key={currentQ} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} transition={{ duration: 0.25 }}>
          <div className="glass-card p-6 mb-6">
            <div className="flex items-start justify-between gap-4 mb-6">
              <div className="flex items-center gap-2">
                <span className="text-xs text-slate-500 font-medium">Q{currentQ + 1}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full border ${q.difficulty === "easy" ? "border-green-500/30 text-green-400 bg-green-500/10" : q.difficulty === "hard" ? "border-red-500/30 text-red-400 bg-red-500/10" : "border-yellow-500/30 text-yellow-400 bg-yellow-500/10"}`}>
                  {q.difficulty}
                </span>
              </div>
              <span className="text-xs text-slate-500">{q.marks} mark{q.marks !== 1 ? "s" : ""}</span>
            </div>

            <p className="text-white font-medium leading-relaxed mb-8">{q.question}</p>

            <div className="space-y-3">
              {(["A", "B", "C", "D"] as const).map((opt) => (
                <motion.button key={opt} whileHover={{ x: 4 }} whileTap={{ scale: 0.99 }} onClick={() => handleAnswer(opt)}
                  className={`option-btn w-full flex items-center gap-4 p-4 rounded-xl text-left ${currentAnswer === opt ? "selected" : ""}`}>
                  <span className={`w-8 h-8 rounded-lg flex-shrink-0 flex items-center justify-center text-sm font-bold transition-colors ${currentAnswer === opt ? "bg-purple-500 text-white" : "bg-white/5 text-slate-400"}`}>
                    {opt}
                  </span>
                  <span className={`text-sm leading-relaxed ${currentAnswer === opt ? "text-white" : "text-slate-300"}`}>
                    {q.options[opt]}
                  </span>
                </motion.button>
              ))}
            </div>
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Navigation */}
      <div className="flex items-center justify-between">
        <button onClick={() => setCurrentQ(Math.max(0, currentQ - 1))} disabled={currentQ === 0}
          className="flex items-center gap-2 px-5 py-2.5 rounded-lg border border-white/10 text-sm text-slate-400 hover:text-white hover:border-white/20 disabled:opacity-30 transition-all">
          <ChevronLeft size={16} /> Previous
        </button>

        {currentQ < questions.length - 1 ? (
          <button onClick={() => setCurrentQ(currentQ + 1)}
            className="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-white/5 border border-white/10 text-sm text-white hover:bg-white/10 transition-all">
            Next <ChevronRight size={16} />
          </button>
        ) : (
          <motion.button whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }} onClick={handleSubmit} disabled={submitting}
            className="btn-neon relative flex items-center gap-2 px-6 py-2.5 rounded-lg text-white font-semibold text-sm disabled:opacity-50 z-10">
            <span className="relative z-10 flex items-center gap-2">
              {submitting ? <><Loader2 size={16} className="animate-spin" /> Submitting...</> : <><Flag size={16} /> Submit Quiz</>}
            </span>
          </motion.button>
        )}
      </div>

      {answered === questions.length && currentQ < questions.length - 1 && (
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="mt-4 text-center">
          <button onClick={handleSubmit} disabled={submitting}
            className="text-sm text-green-400 hover:text-green-300 font-medium transition-colors">
            All answered — Submit now →
          </button>
        </motion.div>
      )}
    </div>
  );
}
