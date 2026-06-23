"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Brain, BookOpen, Sparkles, Loader2, CheckCircle2, ArrowRight, ArrowLeft, Lock, RefreshCw, FileText } from "lucide-react";
import { quizAPI, getUser } from "@/lib/api";

type Stage = "setup" | "loading" | "taking" | "results";
const GEN_STEPS = [
  { label: "Finding real past-paper questions", icon: FileText },
  { label: "Generating your quiz with AI", icon: Brain },
  { label: "Formatting questions", icon: Sparkles },
];

export default function QuizPage() {
  const router = useRouter();
  const [stage, setStage] = useState<Stage>("setup");
  const [tree, setTree] = useState<any>({});
  const [level, setLevel] = useState("");
  const [subject, setSubject] = useState("");
  const [topic, setTopic] = useState("");
  const [mode, setMode] = useState<"quiz" | "exam">("quiz");
  const [difficulty, setDifficulty] = useState("medium");
  const [numQ, setNumQ] = useState(5);
  const [error, setError] = useState("");
  const [loadStep, setLoadStep] = useState(0);

  const [sessionId, setSessionId] = useState<number | null>(null);
  const [questions, setQuestions] = useState<any[]>([]);
  const [answers, setAnswers] = useState<any[]>([]);
  const [current, setCurrent] = useState(0);
  const [results, setResults] = useState<any>(null);

  const user = typeof window !== "undefined" ? getUser() : null;

  useEffect(() => {
    if (!getUser()) { router.push("/login"); return; }
    quizAPI.subjects().then((r) => setTree(r.data)).catch(() => {});
  }, [router]);

  useEffect(() => {
    if (stage !== "loading") return;
    setLoadStep(0);
    const t = setInterval(() => setLoadStep((s) => Math.min(s + 1, GEN_STEPS.length - 1)), 5000);
    return () => clearInterval(t);
  }, [stage]);

  const levels = Object.keys(tree);
  const subjects = level ? Object.keys(tree[level] || {}) : [];
  const topics = level && subject ? tree[level]?.[subject] || [] : [];

  const start = async () => {
    if (!level || !subject || !topic) { setError("Please select a level, subject and topic."); return; }
    setError(""); setStage("loading");
    try {
      const res = await quizAPI.create({ subject, topic, level, difficulty, mode, num_questions: numQ });
      setSessionId(res.data.session_id);
      setQuestions(res.data.questions);
      setAnswers(new Array(res.data.questions.length).fill(mode === "exam" ? "" : null));
      setCurrent(0);
      setStage("taking");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Could not create quiz.");
      setStage("setup");
    }
  };

  const submit = async () => {
    setStage("loading"); setLoadStep(1);
    try {
      const res = await quizAPI.submit({ session_id: sessionId, answers });
      setResults(res.data);
      setStage("results");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Could not submit quiz.");
      setStage("taking");
    }
  };

  // ---------- SETUP ----------
  if (stage === "setup") {
    return (
      <div className="max-w-3xl mx-auto px-4 sm:px-6 py-10">
        <h1 className="text-3xl font-bold mb-2">New Quiz</h1>
        <p className="text-gray-500 mb-8">Built from real GCSE & A-Level past papers.</p>
        {error && <div className="bg-red-50 border border-red-200 text-red-600 rounded-xl p-3 mb-5 text-sm">{error}</div>}

        <div className="card p-6 mb-5">
          <div className="section-label mb-3">1 · Level</div>
          <div className="flex flex-wrap gap-2">
            {levels.length === 0 && <span className="text-sm text-gray-400">Loading subjects…</span>}
            {levels.map((l) => (
              <button key={l} onClick={() => { setLevel(l); setSubject(""); setTopic(""); }}
                className={`px-4 py-2 rounded-xl text-sm font-medium border ${level === l ? "bg-purple-600 text-white border-purple-600" : "border-purple-200 text-gray-600 hover:border-purple-400"}`}>{l}</button>
            ))}
          </div>
        </div>

        {level && (
          <div className="card p-6 mb-5">
            <div className="section-label mb-3">2 · Subject</div>
            <div className="flex flex-wrap gap-2">
              {subjects.map((s) => (
                <button key={s} onClick={() => { setSubject(s); setTopic(""); }}
                  className={`px-4 py-2 rounded-xl text-sm font-medium border ${subject === s ? "bg-purple-600 text-white border-purple-600" : "border-purple-200 text-gray-600 hover:border-purple-400"}`}>{s}</button>
              ))}
            </div>
          </div>
        )}

        {subject && (
          <div className="card p-6 mb-5">
            <div className="section-label mb-3">3 · Topic</div>
            <div className="grid sm:grid-cols-2 gap-2 max-h-72 overflow-y-auto">
              {topics.map((t: string) => (
                <button key={t} onClick={() => setTopic(t)}
                  className={`select-card text-sm ${topic === t ? "selected" : ""}`}>{t}</button>
              ))}
            </div>
          </div>
        )}

        {topic && (
          <div className="card p-6 mb-5">
            <div className="section-label mb-3">4 · Options</div>
            <div className="grid sm:grid-cols-2 gap-4">
              <div>
                <div className="text-xs font-semibold text-gray-500 mb-2">Mode</div>
                <div className="flex gap-2">
                  <button onClick={() => setMode("quiz")} className={`flex-1 px-3 py-2 rounded-xl text-sm font-medium border ${mode === "quiz" ? "bg-purple-600 text-white border-purple-600" : "border-purple-200 text-gray-600"}`}>
                    <BookOpen size={14} className="inline mr-1" /> Quiz (MCQ)
                  </button>
                  <button onClick={() => setMode("exam")} disabled={user?.plan !== "pro"}
                    className={`flex-1 px-3 py-2 rounded-xl text-sm font-medium border ${mode === "exam" ? "bg-purple-600 text-white border-purple-600" : "border-purple-200 text-gray-600"} ${user?.plan !== "pro" ? "opacity-50 cursor-not-allowed" : ""}`}>
                    {user?.plan !== "pro" && <Lock size={12} className="inline mr-1" />} Exam mode
                  </button>
                </div>
                {user?.plan !== "pro" && <p className="text-xs text-gray-400 mt-1">Exam mode is a Pro feature.</p>}
              </div>
              <div>
                <div className="text-xs font-semibold text-gray-500 mb-2">Questions</div>
                <div className="flex gap-2">
                  {[5, 10, 15].map((n) => (
                    <button key={n} onClick={() => setNumQ(n)} className={`flex-1 px-3 py-2 rounded-xl text-sm font-medium border ${numQ === n ? "bg-purple-600 text-white border-purple-600" : "border-purple-200 text-gray-600"}`}>{n}</button>
                  ))}
                </div>
              </div>
              {mode === "quiz" && (
                <div className="sm:col-span-2">
                  <div className="text-xs font-semibold text-gray-500 mb-2">Difficulty</div>
                  <div className="flex gap-2">
                    {["easy", "medium", "hard"].map((d) => (
                      <button key={d} onClick={() => setDifficulty(d)} className={`flex-1 px-3 py-2 rounded-xl text-sm font-medium border capitalize ${difficulty === d ? "bg-purple-600 text-white border-purple-600" : "border-purple-200 text-gray-600"}`}>{d}</button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {topic && (
          <button onClick={start} className="btn-primary w-full justify-center py-3.5 text-base">
            Generate Quiz <ArrowRight size={18} />
          </button>
        )}
      </div>
    );
  }

  // ---------- LOADING ----------
  if (stage === "loading") {
    return (
      <div className="max-w-md mx-auto px-4 py-24">
        <div className="card p-8">
          <h2 className="text-lg font-bold mb-6 text-center">Preparing your quiz…</h2>
          <div className="space-y-4">
            {GEN_STEPS.map((s, i) => (
              <div key={i} className="flex items-center gap-3">
                {i < loadStep ? <CheckCircle2 size={20} className="text-green-500" /> :
                  i === loadStep ? <Loader2 size={20} className="text-purple-600 animate-spin" /> :
                  <div className="w-5 h-5 rounded-full border-2 border-gray-200" />}
                <span className={`text-sm ${i <= loadStep ? "text-gray-700 font-medium" : "text-gray-400"}`}>{s.label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  // ---------- TAKING ----------
  if (stage === "taking") {
    const q = questions[current];
    const isLast = current === questions.length - 1;
    const answered = mode === "exam" ? String(answers[current] || "").trim().length > 0 : answers[current] != null;
    return (
      <div className="max-w-2xl mx-auto px-4 sm:px-6 py-10">
        <div className="flex items-center justify-between mb-4">
          <span className="text-sm text-gray-500">{subject} · {topic}</span>
          <span className="badge-pill text-xs">{current + 1} / {questions.length}</span>
        </div>
        <div className="h-1.5 bg-purple-100 rounded-full mb-6 overflow-hidden">
          <div className="h-full bg-gradient-to-r from-purple-600 to-pink-500 transition-all" style={{ width: `${((current + 1) / questions.length) * 100}%` }} />
        </div>

        <AnimatePresence mode="wait">
          <motion.div key={current} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="card p-6 mb-5">
            {mode === "exam" && <div className="text-xs font-semibold text-purple-600 mb-2">{q.marks} marks</div>}
            <h3 className="font-semibold mb-5 leading-relaxed whitespace-pre-line">{q.question}</h3>
            {mode === "quiz" ? (
              <div className="space-y-2">
                {q.options.map((opt: string) => (
                  <button key={opt} onClick={() => { const a = [...answers]; a[current] = opt; setAnswers(a); }}
                    className={`option-btn ${answers[current] === opt ? "selected" : ""}`}>{opt}</button>
                ))}
              </div>
            ) : (
              <textarea value={answers[current] || ""} onChange={(e) => { const a = [...answers]; a[current] = e.target.value; setAnswers(a); }}
                rows={7} placeholder="Write your answer here…" className="input-field resize-none" />
            )}
          </motion.div>
        </AnimatePresence>

        <div className="flex gap-3">
          <button onClick={() => setCurrent((c) => Math.max(0, c - 1))} disabled={current === 0} className="btn-secondary disabled:opacity-40">
            <ArrowLeft size={16} /> Back
          </button>
          {isLast ? (
            <button onClick={submit} disabled={!answered} className="btn-primary flex-1 justify-center disabled:opacity-40">Submit Quiz</button>
          ) : (
            <button onClick={() => setCurrent((c) => c + 1)} disabled={!answered} className="btn-primary flex-1 justify-center disabled:opacity-40">Next <ArrowRight size={16} /></button>
          )}
        </div>
      </div>
    );
  }

  // ---------- RESULTS ----------
  return (
    <div className="max-w-2xl mx-auto px-4 sm:px-6 py-10">
      <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="card p-8 text-center mb-6">
        <div className="text-5xl font-extrabold gradient-text mb-2">{results.score}%</div>
        <p className="text-gray-500">+{results.xp_earned} XP · 🔥 {results.streak} day streak</p>
      </motion.div>

      <div className="space-y-4 mb-6">
        {results.results.map((r: any, i: number) => (
          <div key={i} className="card p-5">
            <div className="font-medium mb-3 whitespace-pre-line">{r.question}</div>
            {mode === "quiz" ? (
              <div className="space-y-1.5 text-sm">
                <div className={r.is_correct ? "text-green-600 font-medium" : "text-red-600"}>Your answer: {r.your_answer || "—"}</div>
                {!r.is_correct && <div className="text-green-600">Correct: {r.correct_answer}</div>}
                {r.explanation && <div className="text-gray-500 mt-2">{r.explanation}</div>}
              </div>
            ) : (
              <div className="text-sm space-y-2">
                <div className="font-semibold text-purple-600">{r.marks_awarded} / {r.marks} marks</div>
                <div className="text-gray-600"><span className="font-medium">Feedback:</span> {r.feedback}</div>
                {r.model_answer && <div className="bg-purple-50 rounded-xl p-3 text-gray-600"><span className="font-medium">Model answer:</span> {r.model_answer}</div>}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="flex gap-3">
        <button onClick={() => { setStage("setup"); setResults(null); setTopic(""); }} className="btn-secondary flex-1 justify-center"><RefreshCw size={16} /> New Quiz</button>
        <button onClick={() => router.push("/dashboard")} className="btn-primary flex-1 justify-center">Dashboard</button>
      </div>
    </div>
  );
}
