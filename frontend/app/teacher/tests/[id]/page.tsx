"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useParams } from "next/navigation";
import { ArrowLeft, Users, Send, AlertCircle, CheckCircle2, Clock, UserPlus, Link2, Copy, Check } from "lucide-react";
import { teacherAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Input, Field } from "@/components/ui/Input";
import { cn, humanize, formatDate } from "@/lib/utils";

interface Assignment {
  assignment_id: number;
  student: string;
  email: string;
  class_label: string | null;
  due_at: string | null;
  status: string;
  score: number | null;
  grade: string | null;
  completed_at: string | null;
}
interface Detail {
  test: {
    id: number; title: string; subject: string; topic: string; level: string;
    exam_board: string; num_questions: number; duration_minutes: number | null;
    share_token: string | null;
    questions: { question: string; options: string[] }[];
  };
  assignments: Assignment[];
}

export default function TeacherTestDetailPage() {
  const params = useParams();
  const id = params?.id as string;
  const { ready } = useAuthGuard("teacher");
  const [data, setData] = useState<Detail | null>(null);
  const [loading, setLoading] = useState(true);

  // assign form
  const [emails, setEmails] = useState("");
  const [classLabel, setClassLabel] = useState("");
  const [dueAt, setDueAt] = useState("");
  const [assigning, setAssigning] = useState(false);
  const [msg, setMsg] = useState<{ tone: "ok" | "err"; text: string } | null>(null);

  // share link
  const [shareToken, setShareToken] = useState<string | null>(null);
  const [shareBusy, setShareBusy] = useState(false);
  const [copied, setCopied] = useState(false);
  const shareUrl = shareToken && typeof window !== "undefined" ? `${window.location.origin}/join/${shareToken}` : "";

  const toggleShare = async () => {
    setShareBusy(true);
    try {
      if (shareToken) {
        await teacherAPI.unshare(id);
        setShareToken(null);
      } else {
        const { data } = await teacherAPI.share(id);
        setShareToken(data.share_token);
      }
    } catch {
      /* ignore */
    } finally {
      setShareBusy(false);
    }
  };

  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(shareUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      /* ignore */
    }
  };

  const load = () => {
    teacherAPI
      .testDetail(id)
      .then(({ data }) => {
        setData(data);
        setShareToken(data.test?.share_token ?? null);
      })
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    if (!ready) return;
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ready, id]);

  const assign = async (e: React.FormEvent) => {
    e.preventDefault();
    const list = emails.split(/[\s,;]+/).map((s) => s.trim()).filter(Boolean);
    if (list.length === 0) {
      setMsg({ tone: "err", text: "Enter at least one student email." });
      return;
    }
    setAssigning(true);
    setMsg(null);
    try {
      const { data: res } = await teacherAPI.assign(id, {
        student_emails: list,
        class_label: classLabel.trim() || undefined,
        due_at: dueAt ? new Date(dueAt).toISOString() : null,
      });
      const parts = [`${res.assigned} assigned`];
      if (res.skipped_already_assigned) parts.push(`${res.skipped_already_assigned} already had it`);
      if (res.not_found?.length) parts.push(`${res.not_found.length} not found: ${res.not_found.join(", ")}`);
      setMsg({ tone: res.assigned > 0 ? "ok" : "err", text: parts.join(" · ") });
      setEmails("");
      load();
    } catch (e: any) {
      setMsg({ tone: "err", text: e.response?.data?.detail || "Could not assign." });
    } finally {
      setAssigning(false);
    }
  };

  if (!ready || loading) return <Spinner label="Loading test…" />;
  if (!data) {
    return (
      <PageContainer>
        <div className="card p-10 text-center text-ink-muted">Test not found.</div>
      </PageContainer>
    );
  }

  const { test, assignments } = data;
  const completed = assignments.filter((a) => a.status === "completed");

  return (
    <PageContainer>
      <Link href="/teacher/tests" className="mb-4 inline-flex items-center gap-1.5 text-sm text-ink-muted hover:text-ink">
        <ArrowLeft size={15} /> Back to tests
      </Link>

      <div className="mb-6 flex flex-wrap items-center gap-2">
        <span className="badge-brand">{humanize(test.subject)}</span>
        <span className="badge-neutral">{test.level}</span>
        <span className="badge-neutral">{test.exam_board}</span>
        {test.duration_minutes ? <span className="badge-neutral"><Clock size={12} /> {test.duration_minutes} min</span> : null}
      </div>
      <h1 className="text-2xl font-bold tracking-tight text-ink">{test.title}</h1>
      <p className="mt-1 text-sm text-ink-muted">{humanize(test.topic)} · {test.num_questions} questions</p>

      <div className="mt-8 grid gap-6 lg:grid-cols-[1fr_360px]">
        {/* Left: assignments + results */}
        <div className="order-2 lg:order-1">
          <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-ink-subtle">
            Assignments · {assignments.length}
          </h2>
          {assignments.length === 0 ? (
            <div className="card p-8 text-center text-sm text-ink-muted">
              Not assigned to anyone yet. Use the panel to assign it to students.
            </div>
          ) : (
            <div className="card overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-line text-left text-xs uppercase tracking-wide text-ink-subtle">
                      <th className="px-4 py-3 font-medium">Student</th>
                      <th className="px-4 py-3 font-medium">Status</th>
                      <th className="px-4 py-3 font-medium text-right">Score</th>
                      <th className="px-4 py-3 font-medium text-right">Grade</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-line">
                    {assignments.map((a) => (
                      <tr key={a.assignment_id}>
                        <td className="px-4 py-3">
                          <div className="font-medium text-ink">{a.student}</div>
                          <div className="text-xs text-ink-subtle">{a.email}</div>
                        </td>
                        <td className="px-4 py-3">
                          {a.status === "completed" ? (
                            <span className="badge-success"><CheckCircle2 size={12} /> Completed</span>
                          ) : (
                            <span className="badge-warning"><Clock size={12} /> Assigned</span>
                          )}
                        </td>
                        <td className="px-4 py-3 text-right font-semibold text-ink">
                          {a.score != null ? `${a.score}%` : "—"}
                        </td>
                        <td className="px-4 py-3 text-right">
                          {a.grade ? <span className="font-semibold text-brand-600">{a.grade}</span> : "—"}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Question preview */}
          <h2 className="mb-3 mt-8 text-sm font-semibold uppercase tracking-wide text-ink-subtle">
            Questions preview
          </h2>
          <div className="card divide-y divide-line">
            {test.questions.map((q, i) => (
              <div key={i} className="p-4">
                <div className="text-xs font-medium text-ink-subtle">Question {i + 1}</div>
                <p className="mt-1 text-sm font-medium text-ink">{q.question}</p>
                <ul className="mt-2 grid gap-1 sm:grid-cols-2">
                  {q.options?.map((o, j) => (
                    <li key={j} className="text-xs text-ink-muted">{o}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

        {/* Right: share + assign panels */}
        <div className="order-1 space-y-6 lg:order-2">
          {/* Share link */}
          <div className="card p-5">
            <div className="flex items-center gap-2">
              <span className="grid h-9 w-9 place-items-center rounded-lg bg-brand-50 text-brand-600">
                <Link2 size={17} />
              </span>
              <h2 className="font-semibold text-ink">Share link</h2>
            </div>
            <p className="mt-2 text-sm text-ink-muted">
              Anyone with the link can open this test after signing in — no need to add them by email.
            </p>
            {shareToken ? (
              <div className="mt-4 space-y-2">
                <div className="flex items-center gap-2">
                  <input readOnly value={shareUrl} onFocus={(e) => e.currentTarget.select()}
                    className="w-full rounded-lg border border-line bg-slate-50 px-3 py-2 text-xs text-ink outline-none" />
                  <Button size="sm" variant="secondary" onClick={copyLink} className="shrink-0">
                    {copied ? <><Check size={14} /> Copied</> : <><Copy size={14} /> Copy</>}
                  </Button>
                </div>
                <button onClick={toggleShare} disabled={shareBusy}
                  className="text-xs font-medium text-red-600 hover:underline disabled:opacity-50">
                  Disable link
                </button>
              </div>
            ) : (
              <Button onClick={toggleShare} loading={shareBusy} variant="secondary" className="mt-4 w-full">
                <Link2 size={15} /> Create share link
              </Button>
            )}
          </div>

          {/* Assign panel */}
          <div className="card p-5 lg:sticky lg:top-20">
            <div className="flex items-center gap-2">
              <span className="grid h-9 w-9 place-items-center rounded-lg bg-brand-50 text-brand-600">
                <UserPlus size={17} />
              </span>
              <h2 className="font-semibold text-ink">Assign to students</h2>
            </div>

            <form onSubmit={assign} className="mt-4 space-y-4">
              <Field label="Student emails" hint="Comma, space or newline separated.">
                <textarea
                  value={emails}
                  onChange={(e) => setEmails(e.target.value)}
                  rows={4}
                  placeholder={"alex@school.co.uk\nsam@school.co.uk"}
                  className="w-full resize-y rounded-lg border border-line bg-white px-3.5 py-2.5 text-sm text-ink outline-none transition-all placeholder:text-ink-subtle focus:border-brand-500 focus:ring-4 focus:ring-brand-600/10"
                />
              </Field>
              <Field label="Class label" hint="Optional — shown to students.">
                <Input value={classLabel} onChange={(e) => setClassLabel(e.target.value)} placeholder="e.g. Year 11 Chemistry" />
              </Field>
              <Field label="Due date" hint="Optional.">
                <Input type="datetime-local" value={dueAt} onChange={(e) => setDueAt(e.target.value)} />
              </Field>

              {msg && (
                <div className={cn("flex items-start gap-2 rounded-lg border p-3 text-xs",
                  msg.tone === "ok" ? "border-emerald-200 bg-emerald-50 text-emerald-700" : "border-red-200 bg-red-50 text-red-600")}>
                  {msg.tone === "ok" ? <CheckCircle2 size={14} className="mt-0.5 shrink-0" /> : <AlertCircle size={14} className="mt-0.5 shrink-0" />}
                  <span>{msg.text}</span>
                </div>
              )}

              <Button type="submit" className="w-full" loading={assigning}>
                <Send size={15} /> {assigning ? "Assigning…" : "Assign test"}
              </Button>
              <p className="text-center text-[11px] text-ink-subtle">
                Students must already have a Notenix account with that email.
              </p>
            </form>

            {completed.length > 0 && (
              <div className="mt-5 border-t border-line pt-4">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-ink-muted">Completed</span>
                  <span className="font-semibold text-ink">{completed.length}/{assignments.length}</span>
                </div>
                <div className="mt-2 flex items-center justify-between text-sm">
                  <span className="text-ink-muted">Class average</span>
                  <span className="font-semibold text-brand-600">
                    {Math.round(completed.reduce((s, a) => s + (a.score || 0), 0) / completed.length)}%
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </PageContainer>
  );
}
