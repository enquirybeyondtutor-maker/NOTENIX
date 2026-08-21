"use client";
import { useEffect, useState, useCallback } from "react";
import { CheckSquare, ArrowLeft, User as UserIcon, ClipboardList, Send, AlertCircle, ShieldAlert, Bot, Eye, Clock } from "lucide-react";
import { markingAPI, teacherAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, EmptyState, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Field } from "@/components/ui/Input";
import { humanize } from "@/lib/utils";

interface QueueItem {
  attempt_id: number;
  student: string;
  test_title: string;
  subject: string;
  level: string;
  num_questions: number;
  submitted_at: string | null;
}
interface MarkQ {
  question: string;
  marks: number;
  mark_scheme: string | null;
  image?: string | null;
  answer_images?: string[] | null;
  your_answer: string;
  time_seconds?: number | null;
}
interface Integrity {
  focus_lost: number;
  time_away_seconds: number;
  paste_attempts: number;
  copy_attempts: number;
  fullscreen_exits: number;
  burst_flags: number;
  auto_submitted: boolean;
  ai_flag: string | null;
  ai_notes: string | null;
}
interface Detail {
  attempt_id: number;
  student: string;
  test_title: string;
  subject: string;
  level: string;
  time_taken_seconds?: number | null;
  questions: MarkQ[];
  integrity?: Integrity;
}
interface Entry { marks_awarded: number; feedback: string; model_answer: string }

function fmtAway(s: number) {
  if (s < 60) return `${s}s`;
  return `${Math.floor(s / 60)}m ${s % 60}s`;
}

export default function MarkingPage() {
  const { ready } = useAuthGuard("teacher");
  const [queue, setQueue] = useState<QueueItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [detail, setDetail] = useState<Detail | null>(null);
  const [entries, setEntries] = useState<Entry[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [aiCheck, setAiCheck] = useState<{ verdict: string; notes: string } | null>(null);
  const [aiBusy, setAiBusy] = useState(false);

  const loadQueue = useCallback(() => {
    setLoading(true);
    markingAPI.queue()
      .then(({ data }) => setQueue(data))
      .catch(() => setQueue([]))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => { if (ready) loadQueue(); }, [ready, loadQueue]);

  async function open(id: number) {
    setError("");
    setAiCheck(null);
    try {
      const { data } = await markingAPI.get(id);
      setDetail(data);
      setEntries(data.questions.map(() => ({ marks_awarded: 0, feedback: "", model_answer: "" })));
      if (data.integrity?.ai_flag) setAiCheck({ verdict: data.integrity.ai_flag, notes: data.integrity.ai_notes || "" });
    } catch (e: any) {
      setError(e.response?.data?.detail || "Could not open this attempt.");
    }
  }

  async function runAiCheck() {
    if (!detail) return;
    setAiBusy(true);
    setError("");
    try {
      const { data } = await teacherAPI.aiCheck(detail.attempt_id);
      setAiCheck({ verdict: data.verdict, notes: data.notes });
    } catch (e: any) {
      setError(e.response?.data?.detail || "AI check failed.");
    } finally {
      setAiBusy(false);
    }
  }

  function setEntry(i: number, patch: Partial<Entry>) {
    setEntries((es) => es.map((e, idx) => (idx === i ? { ...e, ...patch } : e)));
  }

  async function submit() {
    if (!detail) return;
    setBusy(true);
    setError("");
    try {
      await markingAPI.submit(detail.attempt_id, entries.map((e) => ({
        marks_awarded: e.marks_awarded,
        feedback: e.feedback.trim() || undefined,
        model_answer: e.model_answer.trim() || undefined,
      })));
      setDetail(null);
      setEntries([]);
      loadQueue();
    } catch (e: any) {
      setError(e.response?.data?.detail || "Could not save marks.");
      setBusy(false);
    }
  }

  if (!ready || loading) return <Spinner label="Loading marking queue…" />;

  // ── Marking a single attempt ──
  if (detail) {
    const totalMarks = detail.questions.reduce((s, q) => s + (q.marks || 0), 0);
    const awarded = entries.reduce((s, e) => s + (Number(e.marks_awarded) || 0), 0);
    return (
      <PageContainer>
        <button onClick={() => { setDetail(null); setError(""); }} className="mb-4 inline-flex items-center gap-1.5 text-sm text-ink-muted hover:text-ink">
          <ArrowLeft size={15} /> Back to queue
        </button>

        <div className="card mb-6 flex flex-wrap items-center justify-between gap-3 p-5">
          <div>
            <div className="badge-brand mb-1">{humanize(detail.subject)} · {detail.level}</div>
            <h1 className="text-lg font-bold text-ink">{detail.test_title}</h1>
            <p className="mt-0.5 inline-flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-ink-muted">
              <span className="inline-flex items-center gap-1.5"><UserIcon size={13} /> {detail.student}</span>
              {detail.time_taken_seconds != null && (
                <span className="inline-flex items-center gap-1.5"><Clock size={13} /> {fmtAway(detail.time_taken_seconds)} total</span>
              )}
            </p>
          </div>
          <div className="text-right">
            <div className="text-xs uppercase tracking-wide text-ink-subtle">Total awarded</div>
            <div className="text-2xl font-bold text-ink">{awarded}<span className="text-base text-ink-subtle">/{totalMarks}</span></div>
          </div>
        </div>

        {/* Integrity panel */}
        {detail.integrity && (
          <div className="card mb-6 p-5">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div className="flex items-center gap-2 text-sm font-semibold text-ink">
                <ShieldAlert size={16} className="text-ink-subtle" /> Integrity
              </div>
              <Button size="sm" variant="secondary" onClick={runAiCheck} loading={aiBusy}>
                <Bot size={14} /> {aiBusy ? "Checking…" : "Check for AI"}
              </Button>
            </div>
            <div className="mt-3 flex flex-wrap gap-2 text-xs">
              <span className={`rounded-lg px-2.5 py-1 font-medium ${detail.integrity.focus_lost >= 3 ? "bg-amber-50 text-amber-700" : "bg-slate-100 text-ink-muted"}`}>
                <Eye size={11} className="mr-1 inline" /> Left tab {detail.integrity.focus_lost}× · away {fmtAway(detail.integrity.time_away_seconds)}
              </span>
              <span className={`rounded-lg px-2.5 py-1 font-medium ${detail.integrity.paste_attempts > 0 ? "bg-amber-50 text-amber-700" : "bg-slate-100 text-ink-muted"}`}>
                {detail.integrity.paste_attempts} paste attempt{detail.integrity.paste_attempts === 1 ? "" : "s"}
              </span>
              <span className={`rounded-lg px-2.5 py-1 font-medium ${detail.integrity.copy_attempts > 0 ? "bg-amber-50 text-amber-700" : "bg-slate-100 text-ink-muted"}`}>
                {detail.integrity.copy_attempts} copy attempt{detail.integrity.copy_attempts === 1 ? "" : "s"}
              </span>
              {detail.integrity.fullscreen_exits > 0 && (
                <span className="rounded-lg bg-amber-50 px-2.5 py-1 font-medium text-amber-700">
                  Left fullscreen {detail.integrity.fullscreen_exits}×
                </span>
              )}
              {detail.integrity.burst_flags > 0 && (
                <span className="rounded-lg bg-red-50 px-2.5 py-1 font-medium text-red-700">
                  Paste-like burst after returning
                </span>
              )}
              {detail.integrity.auto_submitted && (
                <span className="rounded-lg bg-slate-100 px-2.5 py-1 font-medium text-ink-muted">Auto-submitted (time ran out)</span>
              )}
            </div>
            {aiCheck && (
              <div className={`mt-3 rounded-lg border p-3 text-sm ${
                aiCheck.verdict === "likely_ai" ? "border-red-200 bg-red-50 text-red-700"
                : aiCheck.verdict === "likely_human" ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                : "border-line bg-slate-50 text-ink-muted"}`}>
                <span className="font-semibold">
                  AI check: {aiCheck.verdict === "likely_ai" ? "Likely AI-written" : aiCheck.verdict === "likely_human" ? "Likely the student" : "Uncertain"}
                </span>
                {aiCheck.notes && <span> — {aiCheck.notes}</span>}
                <span className="mt-1 block text-xs opacity-70">A soft signal, not proof. Use your judgement.</span>
              </div>
            )}
          </div>
        )}

        {error && (
          <div className="mb-5 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
            <AlertCircle size={16} /> {error}
          </div>
        )}

        <div className="space-y-4">
          {detail.questions.map((q, i) => (
            <div key={i} className="card p-5">
              <div className="flex items-center justify-between">
                <span className="text-sm font-semibold text-ink">Question {i + 1}</span>
                <div className="flex items-center gap-2">
                  {q.time_seconds != null && (
                    <span className="inline-flex items-center gap-1 rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-ink-muted">
                      <Clock size={11} /> {fmtAway(q.time_seconds)}
                    </span>
                  )}
                  <span className="rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-semibold text-ink-muted">{q.marks} marks</span>
                </div>
              </div>
              {q.question && <p className="mt-1 whitespace-pre-line font-medium text-ink">{q.question}</p>}
              {q.image && <img src={q.image} alt="Question" className="mt-3 max-h-96 w-auto max-w-full rounded-lg border border-line" />}

              {q.mark_scheme && (
                <div className="mt-3 whitespace-pre-line rounded-lg border border-brand-100 bg-brand-50/50 p-3 text-sm text-ink-muted">
                  <span className="font-medium text-ink">Mark scheme: </span>{q.mark_scheme}
                </div>
              )}

              <div className="mt-3 whitespace-pre-line rounded-lg bg-slate-50 p-3 text-sm text-ink-muted">
                <span className="mb-1 block font-medium text-ink">Student answer</span>
                {q.your_answer || (q.answer_images?.length ? "(uploaded photo below)" : "— (not answered)")}
                {(q.answer_images?.length ?? 0) > 0 && (
                  <div className="mt-2 flex flex-wrap gap-3">
                    {q.answer_images!.map((src, j) => (
                      <a key={j} href={src} target="_blank" rel="noopener noreferrer">
                        <img src={src} alt={`Student answer photo ${j + 1}`} className="max-h-96 w-auto max-w-full rounded-lg border border-line hover:opacity-90" />
                      </a>
                    ))}
                  </div>
                )}
              </div>

              <div className="mt-4 grid gap-4 sm:grid-cols-[140px_1fr]">
                <Field label="Marks awarded">
                  <input type="number" min={0} max={q.marks} value={entries[i]?.marks_awarded ?? 0}
                    onChange={(e) => setEntry(i, { marks_awarded: Math.max(0, Math.min(q.marks, Number(e.target.value) || 0)) })}
                    className="w-full rounded-lg border border-line bg-white px-3.5 py-2.5 text-sm text-ink outline-none focus:border-brand-500 focus:ring-4 focus:ring-brand-600/10" />
                </Field>
                <Field label="Feedback">
                  <textarea rows={2} value={entries[i]?.feedback ?? ""}
                    onChange={(e) => setEntry(i, { feedback: e.target.value })}
                    placeholder="What earned marks, what was missing…"
                    className="w-full resize-y rounded-lg border border-line bg-white px-3.5 py-2.5 text-sm text-ink outline-none focus:border-brand-500 focus:ring-4 focus:ring-brand-600/10" />
                </Field>
              </div>
              <Field label="Model answer (optional)">
                <textarea rows={2} value={entries[i]?.model_answer ?? ""}
                  onChange={(e) => setEntry(i, { model_answer: e.target.value })}
                  placeholder="A concise answer that would score full marks"
                  className="w-full resize-y rounded-lg border border-line bg-white px-3.5 py-2.5 text-sm text-ink outline-none focus:border-brand-500 focus:ring-4 focus:ring-brand-600/10" />
              </Field>
            </div>
          ))}
        </div>

        <div className="mt-6 flex justify-end">
          <Button onClick={submit} loading={busy} size="lg"><Send size={16} /> Submit marks</Button>
        </div>
      </PageContainer>
    );
  }

  // ── Queue ──
  return (
    <PageContainer>
      <PageHeader icon={CheckSquare} title="Marking" subtitle="Written answers waiting for you to mark." />
      {queue.length === 0 ? (
        <EmptyState icon={CheckSquare} title="Nothing to mark" desc="When a student submits written answers that need marking, they'll appear here." />
      ) : (
        <div className="card divide-y divide-line">
          {queue.map((q) => (
            <button key={q.attempt_id} onClick={() => open(q.attempt_id)}
              className="flex w-full items-center justify-between gap-3 p-4 text-left transition-colors hover:bg-slate-50">
              <div className="flex items-center gap-3">
                <span className="grid h-9 w-9 place-items-center rounded-lg bg-amber-50 text-amber-600"><ClipboardList size={16} /></span>
                <div>
                  <div className="text-sm font-medium text-ink">{q.test_title}</div>
                  <div className="text-xs text-ink-subtle">
                    {q.student} · {humanize(q.subject)} · {q.num_questions} questions
                  </div>
                </div>
              </div>
              <span className="rounded-lg bg-brand-600 px-3 py-1.5 text-xs font-semibold text-white">Mark</span>
            </button>
          ))}
        </div>
      )}
    </PageContainer>
  );
}
