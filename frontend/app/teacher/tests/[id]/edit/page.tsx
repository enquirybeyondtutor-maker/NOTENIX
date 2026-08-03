"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, Plus, Trash2, CheckCircle2, AlertCircle, AlertTriangle } from "lucide-react";
import { teacherAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Input, Field } from "@/components/ui/Input";
import { cn } from "@/lib/utils";

interface EditQ {
  question: string;
  options: string[];
  answerIndex: number;
  explanation: string;
}

function toEditQ(q: any): EditQ {
  const options: string[] = (q.options || ["", "", "", ""]).slice(0, 4);
  while (options.length < 4) options.push("");
  const answerIndex = Math.max(0, options.findIndex((o) => o === q.answer));
  return { question: q.question || "", options, answerIndex, explanation: q.explanation || "" };
}

export default function EditTestPage() {
  const params = useParams();
  const router = useRouter();
  const id = params?.id as string;
  const { ready } = useAuthGuard("teacher");

  const [loading, setLoading] = useState(true);
  const [title, setTitle] = useState("");
  const [duration, setDuration] = useState<number>(0);
  const [attempts, setAttempts] = useState(0);
  const [questions, setQuestions] = useState<EditQ[]>([]);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready) return;
    teacherAPI
      .testFull(id)
      .then(({ data }) => {
        setTitle(data.title || "");
        setDuration(data.duration_minutes || 0);
        setAttempts(data.attempt_count || 0);
        setQuestions((data.questions || []).map(toEditQ));
      })
      .catch(() => setError("Could not load this test."))
      .finally(() => setLoading(false));
  }, [ready, id]);

  const setQ = (i: number, patch: Partial<EditQ>) =>
    setQuestions((qs) => qs.map((q, idx) => (idx === i ? { ...q, ...patch } : q)));
  const setOpt = (qi: number, oi: number, val: string) =>
    setQuestions((qs) => qs.map((q, idx) => (idx === qi ? { ...q, options: q.options.map((o, j) => (j === oi ? val : o)) } : q)));
  const blankQ = (): EditQ => ({ question: "", options: ["", "", "", ""], answerIndex: 0, explanation: "" });

  const save = async () => {
    const cleaned = questions
      .map((q) => ({ ...q, question: q.question.trim(), options: q.options.map((o) => o.trim()) }))
      .filter((q) => q.question && q.options.every(Boolean));
    if (cleaned.length === 0) {
      setError("Add at least one complete question (text + all four options).");
      return;
    }
    setError("");
    setSaving(true);
    try {
      await teacherAPI.updateTest(id, {
        title: title.trim() || undefined,
        duration_minutes: duration || null,
        questions: cleaned.map((q) => ({
          question: q.question,
          options: q.options,
          answer: q.options[q.answerIndex],
          explanation: q.explanation.trim() || undefined,
        })),
      });
      router.replace(`/teacher/tests/${id}`);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Could not save changes.");
      setSaving(false);
    }
  };

  if (!ready || loading) return <Spinner label="Loading test…" />;

  return (
    <PageContainer className="max-w-3xl">
      <Link href={`/teacher/tests/${id}`} className="mb-4 inline-flex items-center gap-1.5 text-sm text-ink-muted hover:text-ink">
        <ArrowLeft size={15} /> Back to test
      </Link>
      <h1 className="text-2xl font-bold tracking-tight text-ink">Edit test</h1>
      <p className="mt-1 text-sm text-ink-muted">Change the title, timing or any question.</p>

      {attempts > 0 && (
        <div className="mt-5 flex items-start gap-2 rounded-lg border border-amber-200 bg-amber-50 p-3 text-sm text-amber-700">
          <AlertTriangle size={16} className="mt-0.5 shrink-0" />
          <span>{attempts} student{attempts > 1 ? "s have" : " has"} already completed this test. Editing changes it for anyone who hasn't submitted yet, but won't re-mark past attempts.</span>
        </div>
      )}
      {error && (
        <div className="mt-5 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
          <AlertCircle size={16} /> {error}
        </div>
      )}

      <div className="card mt-5 space-y-5 p-6">
        <div className="grid gap-5 sm:grid-cols-[2fr_1fr]">
          <Field label="Test title">
            <Input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Test title" />
          </Field>
          <Field label="Time limit (min)" hint="0 = untimed">
            <Input type="number" min={0} max={240} value={duration}
              onChange={(e) => setDuration(Math.max(0, Math.min(240, Number(e.target.value) || 0)))} />
          </Field>
        </div>
      </div>

      <div className="mt-4 space-y-4">
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
            <Field label="Explanation (optional)">
              <Input value={q.explanation} onChange={(e) => setQ(i, { explanation: e.target.value })} placeholder="Why the answer is correct" />
            </Field>
          </div>
        ))}
      </div>

      <div className="mt-4 flex items-center justify-between">
        <Button type="button" variant="secondary" onClick={() => setQuestions((qs) => [...qs, blankQ()])}>
          <Plus size={16} /> Add question
        </Button>
        <Button onClick={save} loading={saving} size="lg">Save changes ({questions.length})</Button>
      </div>
    </PageContainer>
  );
}
