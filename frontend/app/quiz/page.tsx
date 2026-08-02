"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { Brain, BookOpen, Sparkles, Loader2, CheckCircle2, ArrowRight, ArrowLeft, Lock, RefreshCw, FileText } from "lucide-react";
import { quizAPI, getUser } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { cn, humanize } from "@/lib/utils";

type Stage = "setup" | "loading" | "taking" | "results";
const GEN_STEPS = [
  { label: "Finding real past-paper questions", icon: FileText },
  { label: "Building your questions", icon: Brain },
  { label: "Formatting questions", icon: Sparkles },
];

function Chip({ active, disabled, onClick, children }: { active: boolean; disabled?: boolean; onClick: () => void; children: React.ReactNode }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={cn(
        "rounded-lg border px-4 py-2 text-sm font-medium transition-colors",
        active ? "border-brand-600 bg-brand-600 text-white" : "border-line text-ink-muted hover:border-brand-400 hover:text-ink",
        disabled && "cursor-not-allowed opacity-50 hover:border-line"
      )}
    >
      {children}
    </button>
  );
}

export default function QuizPage() {
  const router = useRouter();
  const { ready } = useAuthGuard();
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
    if (!ready) return;
    quizAPI.subjects().then((r) => setTree(r.data)).catch(() => {});
  }, [ready]);

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
    if (!level || !subject || !topic) {
      setError("Please select a level, subject and topic.");
      return;
    }
    setError("");
    setStage("loading");
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
    setStage("loading");
    setLoadStep(1);
    try {
      const res = await quizAPI.submit({ session_id: sessionId, answers });
      setResults(res.data);
      setStage("results");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Could not submit quiz.");
      setStage("taking");
    }
  };

  if (!ready) return <Spinner />;

  // ---------- SETUP ----------
  if (stage === "setup") {
    return (
      <PageContainer className="max-w-3xl">
        <h1 className="text-2xl font-bold tracking-tight text-ink">Practise a quiz</h1>
        <p className="mt-1 text-sm text-ink-muted">Built from real GCSE &amp; A-Level past papers.</p>
        {error && <div className="mt-5 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">{error}</div>}

        <div className="card mt-6 p-6">
          <div className="eyebrow mb-3">1 · Level</div>
          <div className="flex flex-wrap gap-2">
            {levels.length === 0 && <span className="text-sm text-ink-subtle">Loading subjects…</span>}
            {levels.map((l) => (
              <Chip key={l} active={level === l} onClick={() => { setLevel(l); setSubject(""); setTopic(""); }}>{l}</Chip>
            ))}
          </div>
        </div>

        {level && (
          <div className="card mt-5 p-6">
            <div className="eyebrow mb-3">2 · Subject</div>
            <div className="flex flex-wrap gap-2">
              {subjects.map((s) => (
                <Chip key={s} active={subject === s} onClick={() => { setSubject(s); setTopic(""); }}>{humanize(s)}</Chip>
              ))}
            </div>
          </div>
        )}

        {subject && (
          <div className="card mt-5 p-6">
            <div className="eyebrow mb-3">3 · Topic</div>
            <div className="grid max-h-72 gap-2 overflow-y-auto sm:grid-cols-2">
              {topics.map((t: string) => (
                <button key={t} onClick={() => setTopic(t)} className={cn("select-card text-sm", topic === t && "selected")}>{t}</button>
              ))}
            </div>
          </div>
        )}

        {topic && (
          <div className="card mt-5 p-6">
            <div className="eyebrow mb-3">4 · Options</div>
            <div className="grid gap-5 sm:grid-cols-2">
              <div>
                <div className="mb-2 text-xs font-semibold text-ink-muted">Mode</div>
                <div className="flex gap-2">
                  <Chip active={mode === "quiz"} onClick={() => setMode("quiz")}>
                    <BookOpen size={14} className="mr-1 inline" /> Quiz (MCQ)
                  </Chip>
                  <Chip active={mode === "exam"} disabled={user?.plan !== "pro"} onClick={() => user?.plan === "pro" && setMode("exam")}>
                    {user?.plan !== "pro" && <Lock size={12} className="mr-1 inline" />} Exam mode
                  </Chip>
                </div>
                {user?.plan !== "pro" && <p className="mt-1.5 text-xs text-ink-subtle">Exam mode is a Pro feature.</p>}
              </div>
              <div>
                <div className="mb-2 text-xs font-semibold text-ink-muted">Questions</div>
                <div className="flex gap-2">
                  {[5, 10, 15].map((n) => (
                    <Chip key={n} active={numQ === n} onClick={() => setNumQ(n)}>{n}</Chip>
                  ))}
                </div>
              </div>
              {mode === "quiz" && (
                <div className="sm:col-span-2">
                  <div className="mb-2 text-xs font-semibold text-ink-muted">Difficulty</div>
                  <div className="flex gap-2">
                    {["easy", "medium", "hard"].map((d) => (
                      <Chip key={d} active={difficulty === d} onClick={() => setDifficulty(d)}>
                        <span className="capitalize">{d}</span>
                      </Chip>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {topic && (
          <Button onClick={start} size="lg" className="mt-6 w-full">
            Start quiz <ArrowRight size={18} />
          </Button>
        )}
      </PageContainer>
    );
  }

  // ---------- LOADING ----------
  if (stage === "loading") {
    return (
      <div className="mx-auto max-w-md px-4 py-24">
        <div className="card p-8">
          <h2 className="mb-6 text-center text-lg font-semibold text-ink">Preparing your quiz…</h2>
          <div className="space-y-4">
            {GEN_STEPS.map((s, i) => (
              <div key={i} className="flex items-center gap-3">
                {i < loadStep ? (
                  <CheckCircle2 size={20} className="text-emerald-500" />
                ) : i === loadStep ? (
                  <Loader2 size={20} className="animate-spin text-brand-600" />
                ) : (
                  <div className="h-5 w-5 rounded-full border-2 border-line-strong" />
                )}
                <span className={cn("text-sm", i <= loadStep ? "font-medium text-ink" : "text-ink-subtle")}>{s.label}</span>
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
      <PageContainer className="max-w-2xl">
        <div className="mb-4 flex items-center justify-between">
          <span className="text-sm text-ink-muted">{humanize(subject)} · {topic}</span>
          <span className="badge-neutral">{current + 1} / {questions.length}</span>
        </div>
        <div className="mb-6 h-1.5 overflow-hidden rounded-full bg-slate-100">
          <div className="h-full rounded-full bg-brand-600 transition-all" style={{ width: `${((current + 1) / questions.length) * 100}%` }} />
        </div>

        <AnimatePresence mode="wait">
          <motion.div key={current} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="card mb-5 p-6">
            {mode === "exam" && <div className="mb-2 text-xs font-semibold text-brand-600">{q.marks} marks</div>}
            <h3 className="mb-5 whitespace-pre-line font-semibold leading-relaxed text-ink">{q.question}</h3>
            {mode === "quiz" ? (
              <div className="space-y-2">
                {q.options.map((opt: string) => (
                  <button
                    key={opt}
                    onClick={() => { const a = [...answers]; a[current] = opt; setAnswers(a); }}
                    className={cn("option-btn", answers[current] === opt && "selected")}
                  >
                    {opt}
                  </button>
                ))}
              </div>
            ) : (
              <textarea
                value={answers[current] || ""}
                onChange={(e) => { const a = [...answers]; a[current] = e.target.value; setAnswers(a); }}
                rows={7}
                placeholder="Write your answer here…"
                className="input-field resize-none"
              />
            )}
          </motion.div>
        </AnimatePresence>

        <div className="flex gap-3">
          <Button variant="secondary" onClick={() => setCurrent((c) => Math.max(0, c - 1))} disabled={current === 0}>
            <ArrowLeft size={16} /> Back
          </Button>
          {isLast ? (
            <Button onClick={submit} disabled={!answered} className="flex-1">Submit quiz</Button>
          ) : (
            <Button onClick={() => setCurrent((c) => c + 1)} disabled={!answered} className="flex-1">
              Next <ArrowRight size={16} />
            </Button>
          )}
        </div>
      </PageContainer>
    );
  }

  // ---------- RESULTS ----------
  return (
    <PageContainer className="max-w-2xl">
      <motion.div initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} className="card mb-6 p-8 text-center">
        <div className="mb-2 text-5xl font-bold text-brand-600">{results.score}%</div>
        <p className="text-sm text-ink-muted">+{results.xp_earned} XP · 🔥 {results.streak} day streak</p>
      </motion.div>

      <div className="mb-6 space-y-4">
        {results.results.map((r: any, i: number) => (
          <div key={i} className="card p-5">
            <div className="mb-3 whitespace-pre-line font-medium text-ink">{r.question}</div>
            {mode === "quiz" ? (
              <div className="space-y-1.5 text-sm">
                <div className={r.is_correct ? "font-medium text-emerald-600" : "text-red-600"}>Your answer: {r.your_answer || "—"}</div>
                {!r.is_correct && <div className="text-emerald-600">Correct: {r.correct_answer}</div>}
                {r.explanation && <div className="mt-2 text-ink-muted">{r.explanation}</div>}
              </div>
            ) : (
              <div className="space-y-2 text-sm">
                <div className="font-semibold text-brand-600">{r.marks_awarded} / {r.marks} marks</div>
                <div className="text-ink-muted"><span className="font-medium text-ink">Feedback:</span> {r.feedback}</div>
                {r.model_answer && (
                  <div className="rounded-lg bg-slate-50 p-3 text-ink-muted">
                    <span className="font-medium text-ink">Model answer:</span> {r.model_answer}
                  </div>
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="flex gap-3">
        <Button variant="secondary" className="flex-1" onClick={() => { setStage("setup"); setResults(null); setTopic(""); }}>
          <RefreshCw size={16} /> New quiz
        </Button>
        <Button className="flex-1" onClick={() => router.push("/dashboard")}>Dashboard</Button>
      </div>
    </PageContainer>
  );
}
