"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  FilePlus2, Sparkles, AlertCircle, ArrowLeft, Wand2, PenLine, FileUp,
  Plus, Trash2, CheckCircle2, Loader2, Images, X,
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

type Mode = "ai" | "manual" | "pdf" | "photo";
interface ManualQ {
  question: string;
  options: string[];
  answerIndex: number;
  explanation: string;
}
const blankQ = (): ManualQ => ({ question: "", options: ["", "", "", ""], answerIndex: 0, explanation: "" });

const MAX_PHOTO_QS = 20;

// Downscale + JPEG-compress an image in the browser before upload.
function compressImage(file: File, maxSide = 1500): Promise<string> {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => {
      URL.revokeObjectURL(url);
      const scale = Math.min(1, maxSide / Math.max(img.width, img.height));
      const w = Math.max(1, Math.round(img.width * scale));
      const h = Math.max(1, Math.round(img.height * scale));
      const canvas = document.createElement("canvas");
      canvas.width = w; canvas.height = h;
      const ctx = canvas.getContext("2d");
      if (!ctx) return reject(new Error("Canvas not supported"));
      ctx.drawImage(img, 0, 0, w, h);
      let out = canvas.toDataURL("image/jpeg", 0.82);
      if (out.length > 1_500_000) out = canvas.toDataURL("image/jpeg", 0.6);
      resolve(out);
    };
    img.onerror = () => { URL.revokeObjectURL(url); reject(new Error("Could not read image")); };
    img.src = url;
  });
}

export default function NewTestPage() {
  const router = useRouter();
  const { ready } = useAuthGuard("teacher");
  const [mode, setMode] = useState<Mode>("ai");
  const [meta, setMeta] = useState({
    title: "", subject: "chemistry", topic: "", level: "GCSE",
    exam_board: "AQA", difficulty: "medium", num_questions: 10, duration_minutes: 30,
  });
  const [questions, setQuestions] = useState<ManualQ[]>([blankQ()]);
  const [pdfFiles, setPdfFiles] = useState<File[]>([]);
  const [faithful, setFaithful] = useState(true);
  const [pdfMode, setPdfMode] = useState<"mcq" | "written">("mcq");
  const [isLibrary, setIsLibrary] = useState(false);
  const [photoImgs, setPhotoImgs] = useState<string[]>([]);   // compressed data URIs
  const [photoMarks, setPhotoMarks] = useState(10);
  const [photoBusy, setPhotoBusy] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const isAdmin = !!getUser()?.is_admin;

  const set = (k: string, v: any) => setMeta((m) => ({ ...m, [k]: v }));
  const setQ = (i: number, patch: Partial<ManualQ>) =>
    setQuestions((qs) => qs.map((q, idx) => (idx === i ? { ...q, ...patch } : q)));
  const setOpt = (qi: number, oi: number, val: string) =>
    setQuestions((qs) => qs.map((q, idx) => (idx === qi ? { ...q, options: q.options.map((o, j) => (j === oi ? val : o)) } : q)));

  async function addPhotoImgs(files: FileList | null) {
    if (!files || files.length === 0) return;
    setError("");
    setPhotoBusy(true);
    try {
      const room = MAX_PHOTO_QS - photoImgs.length;
      if (room <= 0) { setError(`You can add up to ${MAX_PHOTO_QS} screenshots.`); return; }
      const picked = Array.from(files).filter((f) => f.type.startsWith("image/")).slice(0, room);
      const encoded = await Promise.all(picked.map((f) => compressImage(f)));
      setPhotoImgs((prev) => [...prev, ...encoded]);
    } catch {
      setError("Couldn't process one of those images. Please try another.");
    } finally {
      setPhotoBusy(false);
    }
  }

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    // ---- Photo questions (each screenshot is a question, no transcription) ----
    if (mode === "photo") {
      if (photoImgs.length === 0) { setError("Add at least one screenshot."); return; }
      setBusy(true);
      try {
        const { data } = await teacherAPI.createPhotoQuestions({
          title: meta.title.trim(),
          subject: meta.subject, topic: meta.topic.trim(), level: meta.level, exam_board: meta.exam_board,
          marks_per_question: photoMarks, images: photoImgs,
          is_library: isAdmin && isLibrary,
        });
        router.replace(`/teacher/tests/${data.id}`);
        return;
      } catch (e: any) {
        setError(e.response?.data?.detail || "Could not create the test.");
        setBusy(false);
        return;
      }
    }

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
      if (pdfFiles.length === 0) {
        setError("Choose a PDF or image to upload.");
        return;
      }
      setBusy(true);
      try {
        const fd = new FormData();
        pdfFiles.forEach((f) => fd.append("files", f));
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
    const label = mode === "manual" || mode === "photo" ? "Saving your test…" : mode === "pdf" ? "Reading your PDF & writing questions…" : `Generating ${meta.num_questions} questions on ${meta.topic}…`;
    return (
      <div className="mx-auto flex max-w-md flex-col items-center px-4 py-24 text-center">
        <span className="grid h-14 w-14 place-items-center rounded-2xl bg-brand-50 text-brand-600">
          {mode === "manual" || mode === "photo" ? <Loader2 size={26} className="animate-spin" /> : <Wand2 size={26} className="animate-pulse" />}
        </span>
        <h1 className="mt-5 text-lg font-semibold text-ink">{label}</h1>
        {mode !== "manual" && <p className="mt-1.5 text-sm text-ink-muted">This takes a few seconds.</p>}
      </div>
    );
  }

  const MODES: { id: Mode; label: string; icon: typeof Wand2; desc: string }[] = [
    { id: "ai", label: "AI generate", icon: Wand2, desc: "From a topic" },
    { id: "manual", label: "Write manually", icon: PenLine, desc: "Author each MCQ" },
    { id: "pdf", label: "From PDF or image", icon: FileUp, desc: "Past paper → MCQ or written" },
    { id: "photo", label: "Photo questions", icon: Images, desc: "Screenshots as questions" },
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
          <p className="mt-1 text-sm text-ink-muted">Generate with AI, write questions by hand, or upload a PDF or image — as multiple-choice or written-answer.</p>
        </div>
      </div>

      {/* Mode selector */}
      <div className="mb-6 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
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
            <Field label="Upload PDF or images" hint="Past paper, worksheet, or one or more screenshots / photos of the questions.">
              <label className="flex cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed border-line-strong bg-slate-50 px-4 py-8 text-center transition-colors hover:border-brand-400 hover:bg-brand-50/40">
                <FileUp size={22} className="text-ink-subtle" />
                <span className="mt-2 text-sm font-medium text-ink">{pdfFiles.length ? "Add more files" : "Choose a PDF or images"}</span>
                <span className="mt-0.5 text-xs text-ink-subtle">PDF, PNG or JPG · up to 10 files · 15 MB each</span>
                <input type="file" accept="application/pdf,.pdf,image/*" multiple className="hidden"
                  onChange={(e) => {
                    const picked = Array.from(e.target.files || []);
                    setPdfFiles((prev) => [...prev, ...picked].slice(0, 10));
                    e.target.value = "";
                  }} />
              </label>
              {pdfFiles.length > 0 && (
                <ul className="mt-3 space-y-2">
                  {pdfFiles.map((f, i) => (
                    <li key={i} className="flex items-center justify-between gap-3 rounded-lg border border-line bg-white px-3 py-2 text-sm">
                      <span className="truncate text-ink">{i + 1}. {f.name}</span>
                      <button type="button" onClick={() => setPdfFiles((prev) => prev.filter((_, j) => j !== i))}
                        className="shrink-0 text-ink-subtle hover:text-red-600" title="Remove">
                        <Trash2 size={14} />
                      </button>
                    </li>
                  ))}
                </ul>
              )}
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
              <Button type="submit" size="lg" disabled={pdfFiles.length === 0}><FileUp size={16} /> Build test</Button>
            </div>
          </div>
        )}

        {mode === "photo" && (
          <div className="card space-y-5 p-6">
            <div>
              <div className="flex items-center gap-2">
                <span className="grid h-9 w-9 place-items-center rounded-lg bg-brand-50 text-brand-600"><Images size={17} /></span>
                <div>
                  <h2 className="text-base font-semibold text-ink">Screenshots as questions</h2>
                  <p className="text-sm text-ink-muted">Each screenshot becomes one question, shown exactly as uploaded. Students answer (type or photo) and you mark it.</p>
                </div>
              </div>
            </div>

            <label className="flex cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed border-line-strong bg-slate-50 px-4 py-8 text-center transition-colors hover:border-brand-400 hover:bg-brand-50/40">
              {photoBusy ? <Loader2 size={22} className="animate-spin text-brand-600" /> : <Images size={22} className="text-ink-subtle" />}
              <span className="mt-2 text-sm font-medium text-ink">{photoImgs.length ? "Add more screenshots" : "Choose screenshots"}</span>
              <span className="mt-0.5 text-xs text-ink-subtle">PNG or JPG · up to {MAX_PHOTO_QS} · {photoImgs.length}/{MAX_PHOTO_QS} added</span>
              <input type="file" accept="image/*" multiple className="hidden" disabled={photoBusy}
                onChange={(e) => { addPhotoImgs(e.target.files); e.target.value = ""; }} />
            </label>

            {photoImgs.length > 0 && (
              <div className="grid grid-cols-3 gap-3 sm:grid-cols-4">
                {photoImgs.map((src, i) => (
                  <div key={i} className="relative">
                    <img src={src} alt={`Question ${i + 1}`} className="h-28 w-full rounded-lg border border-line object-cover" />
                    <span className="absolute left-1 top-1 rounded bg-ink/70 px-1.5 py-0.5 text-[10px] font-semibold text-white">Q{i + 1}</span>
                    <button type="button" onClick={() => setPhotoImgs((prev) => prev.filter((_, j) => j !== i))}
                      className="absolute -right-2 -top-2 grid h-6 w-6 place-items-center rounded-full bg-white text-ink-muted shadow ring-1 ring-line hover:text-red-600" title="Remove">
                      <X size={13} />
                    </button>
                  </div>
                ))}
              </div>
            )}

            <div className="grid gap-5 sm:grid-cols-2">
              <Field label="Marks per question" hint="Applied to every question.">
                <Input type="number" min={1} max={100} value={photoMarks}
                  onChange={(e) => setPhotoMarks(Math.max(1, Math.min(100, Number(e.target.value) || 1)))} />
              </Field>
            </div>

            {isAdmin && (
              <label className="flex cursor-pointer items-start gap-3 rounded-xl border border-line bg-white p-3">
                <input type="checkbox" checked={isLibrary} onChange={(e) => setIsLibrary(e.target.checked)}
                  className="mt-0.5 h-4 w-4 rounded border-line-strong text-brand-600 focus:ring-brand-500" />
                <span>
                  <span className="block text-sm font-semibold text-ink">Add to shared practice library</span>
                  <span className="block text-xs text-ink-subtle">Any student with written-practice access can self-start this.</span>
                </span>
              </label>
            )}

            <div className="flex items-center justify-between border-t border-line pt-5">
              <span className="text-xs text-ink-subtle">Marked by you — no AI transcription.</span>
              <Button type="submit" size="lg" disabled={photoImgs.length === 0 || photoBusy}>
                <Images size={16} /> Build test ({photoImgs.length})
              </Button>
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
