"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  FilePlus2, Sparkles, AlertCircle, ArrowLeft, Wand2, PenLine, FileUp,
  Plus, Trash2, CheckCircle2, Loader2,
} from "lucide-react";
import { teacherAPI, getUser } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Input, Select, Field } from "@/components/ui/Input";
import { cn } from "@/lib/utils";

const SUBJECTS = ["maths", "biology", "chemistry", "physics", "computer_science", "economics", "english_literature", "geography", "history", "psychology", "business"];
const BOARDS = ["AQA", "Edexcel", "OCR", "Cambridge", "WJEC", "CCEA"];
const LEVELS = ["GCSE", "A-Level"];
const DIFFICULTIES = ["easy", "medium", "hard"];

type Mode = "ai" | "manual" | "pdf";
interface ManualQ {
  question: string;
  options: string[];
  answerIndex: number;
  explanation: string;
}
const blankQ = (): ManualQ => ({ question: "", options: ["", "", "", ""], answerIndex: 0, explanation: "" });

export default function NewTestPage() {
  const router = useRouter();
  const { ready } = useAuthGuard("teacher");
  const [mode, setMode] = useState<Mode>("ai");
  const [meta, setMeta] = useState({
    title: "", subject: "chemistry", topic: "", level: "GCSE",
    exam_board: "AQA", difficulty: "medium", num_questions: 10, duration_minutes: 30,
  });
  const [questions, setQuestions] = useState<ManualQ[]>([blankQ()]);
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [faithful, setFaithful] = useState(true);
  const [pdfMode, setPdfMode] = useState<"mcq" | "written">("mcq");
  const [isLibrary, setIsLibrary] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const isAdmin = !!getUser()?.is_admin;

  const set = (k: string, v: any) => setMeta((m) => ({ ...m, [k]: v }));
  const setQ = (i: number, patch: Partial<ManualQ>) =>
    setQuestions((qs) => qs.map((q, idx) => (idx === i ? { ...q, ...patch } : q)));
  const setOpt = (qi: number, oi: number, val: string) =>
    setQuestions((qs) => qs.map((q, idx) => (idx === qi ? { ...q, options: q.options.map((o, j) => (j === oi ? val : o)) } : q)));

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    // ---- Manual ----
    if (mode === "manual") {
      const cleaned = questions
        .map((q) => ({ ...q, question: q.question.trim(), options: q.options.map((o) => o.trim()) }))
        .filter((q) => q.question && q.options.every(Boolean));
      if (cleaned.length === 0) {
        setError("Add at least one complete question (text + all four options).");
        return;
      }
      setBusy(true);
      try {
        const { data } = await teacherAPI.createTest({
          title: meta.title.trim() || `${meta.topic || meta.subject} test`,
          subject: meta.subject, topic: meta.topic.trim() || "Custom", level: meta.level,
          exam_board: meta.exam_board, difficulty: meta.difficulty,
          duration_minutes: meta.duration_minutes || null,
          generate: false,
          questions: cleaned.map((q) => ({
            question: q.question, options: q.options,
            answer: q.options[q.answerIndex], explanation: q.explanation.trim() || undefined,
          })),
        });
        router.replace(`/teacher/tests/${data.id}`);
        return;
      } catch (e: any) {
        setError(e.response?.data?.detail || "Could not create the test.");
        setBusy(false);
        return;
      }
    }

    // ---- PDF ----
    if (mode === "pdf") {
      if (!pdfFile) {
        setError("Choose a PDF to upload.");
        return;
      }
      setBusy(true);
      try {
        const fd = new FormData();
        fd.append("file", pdfFile);
        fd.append("title", meta.title.trim());
        fd.append("subject", meta.subject);
        fd.append("topic", meta.topic.trim());
        fd.append("level", meta.level);
        fd.append("exam_board", meta.exam_board);
        fd.append("num_questions", String(meta.num_questions));
        fd.append("faithful", String(faithful));
        fd.append("mode", pdfMode);
        if (isAdmin && isLibrary) fd.append("is_library", "true");
        if (meta.duration_minutes) fd.append("duration_minutes", String(meta.duration_minutes));
        const { data } = await teacherAPI.createFromPdf(fd);
        router.replace(`/teacher/tests/${data.id}`);
        return;
      } catch (e: any) {
        setError(e.response?.data?.detail || "Could not build a test from that PDF.");
        setBusy(false);
        return;
      }
    }

    // ---- AI ----
    if (!meta.topic.trim()) {
      setError("Please enter a topic.");
      return;
    }
    setBusy(true);
    try {
      const { data } = await teacherAPI.createTest({
        ...meta, title: meta.title.trim() || `${meta.topic} test`,
        generate: true, duration_minutes: meta.duration_minutes || null,
      });
      router.replace(`/teacher/tests/${data.id}`);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Could not create the test. Please try again.");
      setBusy(false);
    }
  }

  if (!ready) return <Spinner />;

  if (busy) {
    const label = mode === "manual" ? "Saving your test…" : mode === "pdf" ? "Reading your PDF & writing questions…" : `Generating ${meta.num_questions} questions on ${meta.topic}…`;
    return (
      <div className="mx-auto flex max-w-md flex-col items-center px-4 py-24 text-center">
        <span className="grid h-14 w-14 place-items-center rounded-2xl bg-brand-50 text-brand-600">
          {mode === "manual" ? <Loader2 size={26} className="animate-spin" /> : <Wand2 size={26} className="animate-pulse" />}
        </span>
        <h1 className="mt-5 text-lg font-semibold text-ink">{label}</h1>
        {mode !== "manual" && <p className="mt-1.5 text-sm text-ink-muted">This takes a few seconds.</p>}
      </div>
    );
  }

  const MODES: { id: Mode; label: string; icon: typeof Wand2; desc: string }[] = [
    { id: "ai", label: "AI generate", icon: Wand2, desc: "From a topic" },
    { id: "manual", label: "Write manually", icon: PenLine, desc: "Author each question" },
    { id: "pdf", label: "From PDF", icon: FileUp, desc: "Upload a past paper" },
  ];

  return (
    <PageContainer className="max-w-3xl">
      <Link href="/teacher/tests" className="mb-4 inline-flex items-center gap-1.5 text-sm text-ink-muted hover:text-ink">
        <ArrowLeft size={15} /> Back to tests
      </Link>

      <div className="mb-6 flex items-start gap-3">
        <span className="mt-0.5 grid h-10 w-10 place-items-center rounded-lg bg-brand-50 text-brand-600">
          <FilePlus2 size={20} />
        </span>
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-ink">Create a test</h1>
          <p className="mt-1 text-sm text-ink-muted">Generate with AI, write your own questions, or upload a PDF.</p>
        </div>
      </div>

      {/* Mode selector */}
      <div className="mb-6 grid gap-3 sm:grid-cols-3">
        {MODES.map((m) => (
          <button
            key={m.id}
            type="button"
            onClick={() => setMode(m.id)}
            className={cn(
              "rounded-xl border p-4 text-left transition-all",
              mode === m.id ? "border-brand-500 bg-brand-50/60 ring-2 ring-brand-600/15" : "border-line bg-white hover:border-brand-300"
            )}
          >
            <span className={cn("grid h-9 w-9 place-items-center rounded-lg", mode === m.id ? "bg-brand-600 text-white" : "bg-slate-100 text-ink-muted")}>
              <m.icon size={17} />
            </span>
            <div className="mt-2 text-sm font-semibold text-ink">{m.label}</div>
            <div className="text-xs text-ink-subtle">{m.desc}</div>
          </button>
        ))}
      </div>

      {error && (
        <div className="mb-5 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
          <AlertCircle size={16} /> {error}
        </div>
      )}

      <form onSubmit={submit} className="space-y-5">
        {/* Common meta */}
        <div className="card space-y-5 p-6">
          <Field label="Test title" hint="Leave blank to auto-name.">
            <Input value={meta.title} onChange={(e) => set("title", e.target.value)} placeholder="e.g. Quadratics — end of unit test" />
          </Field>
          <div className="grid gap-5 sm:grid-cols-2">
            <Field label="Subject">
              <Select value={meta.subject} onChange={(e) => set("subject", e.target.value)}>
                {SUBJECTS.map((s) => <option key={s} value={s}>{s.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())}</option>)}
              </Select>
            </Field>
            <Field label="Topic" hint={mode === "pdf" ? "Optional — inferred from the document." : undefined}>
              <Input value={meta.topic} onChange={(e) => set("topic", e.target.value)} placeholder="e.g. Bonding & structure" required={mode === "ai"} />
            </Field>
          </div>
          <div className="grid gap-5 sm:grid-cols-3">
            <Field label="Level">
              <Select value={meta.level} onChange={(e) => set("level", e.target.value)}>{LEVELS.map((l) => <option key={l}>{l}</option>)}</Select>
            </Field>
            <Field label="Exam board">
              <Select value={meta.exam_board} onChange={(e) => set("exam_board", e.target.value)}>{BOARDS.map((b) => <option key={b}>{b}</option>)}</Select>
            </Field>
            <Field label="Time limit (min)" hint="0 = untimed">
              <Input type="number" min={0} max={240} value={meta.duration_minutes}
                onChange={(e) => set("duration_minutes", Math.max(0, Math.min(240, Number(e.target.value) || 0)))} />
            </Field>
          </div>
        </div>

        {/* Mode-specific */}
        {mode === "ai" && (
          <div className="card space-y-5 p-6">
            <div className="grid gap-5 sm:grid-cols-2">
              <Field label="Difficulty">
                <Select value={meta.difficulty} onChange={(e) => set("difficulty", e.target.value)}>
                  {DIFFICULTIES.map((d) => <option key={d} value={d}>{d[0].toUpperCase() + d.slice(1)}</option>)}
                </Select>
              </Field>
              <Field label="Number of questions" hint="1–30">
                <Input type="number" min={1} max={30} value={meta.num_questions}
                  onChange={(e) => set("num_questions", Math.max(1, Math.min(30, Number(e.target.value) || 1)))} />
              </Field>
            </div>
            <div className="flex items-center justify-between border-t border-line pt-5">
              <span className="inline-flex items-center gap-1.5 text-xs text-ink-subtle"><Sparkles size={13} className="text-brand-600" /> Powered by Claude AI</span>
              <Button type="submit" size="lg"><Wand2 size={16} /> Generate test</Button>
            </div>
          </div>
        )}

        {mode === "pdf" && (
          <div className="card space-y-5 p-6">
            <Field label="Upload PDF" hint="Past paper, worksheet or notes. Text-based PDFs work best (not scans).">
              <label className="flex cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed border-line-strong bg-slate-50 px-4 py-8 text-center transition-colors hover:border-brand-400 hover:bg-brand-50/40">
                <FileUp size={22} className="text-ink-subtle" />
                <span className="mt-2 text-sm font-medium text-ink">{pdfFile ? pdfFile.name : "Choose a PDF file"}</span>
                <span className="mt-0.5 text-xs text-ink-subtle">Max 15 MB</span>
                <input type="file" accept="application/pdf,.pdf" className="hidden"
                  onChange={(e) => setPdfFile(e.target.files?.[0] || null)} />
              </label>
            </Field>
            <div>
              <label className="mb-2 block text-sm font-medium text-ink">Question format</label>
              <div className="grid gap-2 sm:grid-cols-2">
                <button type="button" onClick={() => setPdfMode("mcq")}
                  className={cn("rounded-xl border p-3 text-left transition-all", pdfMode === "mcq" ? "border-brand-500 bg-brand-50/60 ring-2 ring-brand-600/15" : "border-line bg-white hover:border-brand-300")}>
                  <div className="text-sm font-semibold text-ink">Multiple choice</div>
                  <div className="text-xs text-ink-subtle">Auto-marked. Options with one correct answer.</div>
                </button>
                <button type="button" onClick={() => setPdfMode("written")}
                  className={cn("rounded-xl border p-3 text-left transition-all", pdfMode === "written" ? "border-brand-500 bg-brand-50/60 ring-2 ring-brand-600/15" : "border-line bg-white hover:border-brand-300")}>
                  <div className="flex items-center gap-1.5 text-sm font-semibold text-ink"><PenLine size={13} /> Written answers</div>
                  <div className="text-xs text-ink-subtle">Extended-response questions. Pro students AI-marked; others marked by you.</div>
                </button>
              </div>
            </div>

            {pdfMode === "mcq" && (
              <div>
                <label className="mb-2 block text-sm font-medium text-ink">How should we handle the questions?</label>
                <div className="grid gap-2 sm:grid-cols-2">
                  <button type="button" onClick={() => setFaithful(true)}
                    className={cn("rounded-xl border p-3 text-left transition-all", faithful ? "border-brand-500 bg-brand-50/60 ring-2 ring-brand-600/15" : "border-line bg-white hover:border-brand-300")}>
                    <div className="text-sm font-semibold text-ink">Keep exactly as written</div>
                    <div className="text-xs text-ink-subtle">Reads the pages visually and transcribes the questions word-for-word.</div>
                  </button>
                  <button type="button" onClick={() => setFaithful(false)}
                    className={cn("rounded-xl border p-3 text-left transition-all", !faithful ? "border-brand-500 bg-brand-50/60 ring-2 ring-brand-600/15" : "border-line bg-white hover:border-brand-300")}>
                    <div className="text-sm font-semibold text-ink">Create new questions</div>
                    <div className="text-xs text-ink-subtle">AI writes fresh questions based on the document's content.</div>
                  </button>
                </div>
              </div>
            )}

            {pdfMode === "written" && isAdmin && (
              <label className="flex cursor-pointer items-start gap-3 rounded-xl border border-line bg-white p-3">
                <input type="checkbox" checked={isLibrary} onChange={(e) => setIsLibrary(e.target.checked)}
                  className="mt-0.5 h-4 w-4 rounded border-line-strong text-brand-600 focus:ring-brand-500" />
                <span>
                  <span className="block text-sm font-semibold text-ink">Add to shared practice library</span>
                  <span className="block text-xs text-ink-subtle">Any student with written-practice access can self-start this paper.</span>
                </span>
              </label>
            )}

            <Field label={pdfMode === "written" ? "Max questions to extract" : "Number of questions"} hint="1–30">
              <Input type="number" min={1} max={30} value={meta.num_questions}
                onChange={(e) => set("num_questions", Math.max(1, Math.min(30, Number(e.target.value) || 1)))} />
            </Field>
            <div className="flex items-center justify-between border-t border-line pt-5">
              <span className="inline-flex items-center gap-1.5 text-xs text-ink-subtle"><Sparkles size={13} className="text-brand-600" /> AI reads your document</span>
              <Button type="submit" size="lg" disabled={!pdfFile}><FileUp size={16} /> Build from PDF</Button>
            </div>
          </div>
        )}

        {mode === "manual" && (
          <div className="space-y-4">
            {questions.map((q, i) => (
              <div key={i} className="card p-5">
                <div className="mb-3 flex items-center justify-between">
                  <span className="text-sm font-semibold text-ink">Question {i + 1}</span>
                  {questions.length > 1 && (
                    <button type="button" onClick={() => setQuestions((qs) => qs.filter((_, idx) => idx !== i))}
                      className="text-ink-subtle hover:text-red-600" title="Remove">
                      <Trash2 size={15} />
                    </button>
                  )}
                </div>
                <Field label="Question">
                  <Input value={q.question} onChange={(e) => setQ(i, { question: e.target.value })} placeholder="Enter the question" />
                </Field>
                <div className="mt-3 space-y-2">
                  <div className="text-xs font-medium text-ink-muted">Options — select the correct one</div>
                  {q.options.map((opt, oi) => (
                    <div key={oi} className="flex items-center gap-2">
                      <button type="button" onClick={() => setQ(i, { answerIndex: oi })}
                        className={cn("grid h-6 w-6 shrink-0 place-items-center rounded-full border transition-colors",
                          q.answerIndex === oi ? "border-emerald-500 bg-emerald-500 text-white" : "border-line-strong text-transparent hover:border-brand-400")}
                        title="Mark correct">
                        <CheckCircle2 size={13} />
                      </button>
                      <Input value={opt} onChange={(e) => setOpt(i, oi, e.target.value)} placeholder={`Option ${String.fromCharCode(65 + oi)}`} />
                    </div>
                  ))}
                </div>
                <Field label="Explanation (optional)"><Input value={q.explanation} onChange={(e) => setQ(i, { explanation: e.target.value })} placeholder="Why the answer is correct" /></Field>
              </div>
            ))}
            <div className="flex items-center justify-between">
              <Button type="button" variant="secondary" onClick={() => setQuestions((qs) => [...qs, blankQ()])}>
                <Plus size={16} /> Add question
              </Button>
              <Button type="submit" size="lg">Save test ({questions.length})</Button>
            </div>
          </div>
        )}
      </form>
    </PageContainer>
  );
}
