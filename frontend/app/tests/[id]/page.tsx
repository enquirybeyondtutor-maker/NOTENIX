"use client";
import { useEffect, useMemo, useRef, useState, useCallback } from "react";
import { useRouter, useParams } from "next/navigation";
import { Clock, ChevronLeft, ChevronRight, Flag, AlertCircle, CheckCircle2, Loader2, ImagePlus, X } from "lucide-react";
import { testsAPI, getUser } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Logo } from "@/components/ui/Logo";
import { cn, humanize } from "@/lib/utils";

interface Question {
  question: string;
  options?: string[];
  marks?: number;
  image?: string | null;
}
interface TestData {
  assignment_id: number;
  title: string;
  subject: string;
  topic: string;
  level: string;
  exam_board: string;
  mode?: "mcq" | "written";
  kind?: "test" | "homework";
  duration_minutes: number | null;
  started_at?: string | null;
  server_now?: string | null;
  draft_answers?: (string | null)[] | null;
  questions: Question[];
}

function fmtTime(s: number) {
  const m = Math.floor(s / 60);
  const sec = s % 60;
  return `${m}:${sec.toString().padStart(2, "0")}`;
}

const MAX_PHOTOS_PER_Q = 4;

// Downscale + JPEG-compress a photo in the browser so multi-MB camera shots become
// ~150–400 KB before upload. Retries at lower quality if still large.
function compressImage(file: File, maxSide = 1400): Promise<string> {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => {
      URL.revokeObjectURL(url);
      const scale = Math.min(1, maxSide / Math.max(img.width, img.height));
      const w = Math.max(1, Math.round(img.width * scale));
      const h = Math.max(1, Math.round(img.height * scale));
      const canvas = document.createElement("canvas");
      canvas.width = w;
      canvas.height = h;
      const ctx = canvas.getContext("2d");
      if (!ctx) return reject(new Error("Canvas not supported"));
      ctx.drawImage(img, 0, 0, w, h);
      let out = canvas.toDataURL("image/jpeg", 0.8);
      if (out.length > 1_400_000) out = canvas.toDataURL("image/jpeg", 0.6);
      resolve(out);
    };
    img.onerror = () => { URL.revokeObjectURL(url); reject(new Error("Could not read image")); };
    img.src = url;
  });
}

export default function AttemptTestPage() {
  const router = useRouter();
  const params = useParams();
  const id = params?.id as string;
  const { ready } = useAuthGuard("student");

  const [test, setTest] = useState<TestData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [current, setCurrent] = useState(0);
  const [answers, setAnswers] = useState<Record<number, string>>({});
  const [photos, setPhotos] = useState<Record<number, string[]>>({});
  const [photoBusy, setPhotoBusy] = useState(false);
  const [remaining, setRemaining] = useState<number | null>(null);
  const [startedAt] = useState(() => Date.now());
  const [submitting, setSubmitting] = useState(false);
  const [reviewOpen, setReviewOpen] = useState(false);

  // Server-anchored deadline (local-clock ms). Set once the test loads.
  const deadlineRef = useRef<number | null>(null);
  // Integrity signals gathered during the sitting.
  const focusLost = useRef(0);
  const timeAwayMs = useRef(0);
  const pasteAttempts = useRef(0);
  const awayStart = useRef<number | null>(null);

  const markAway = useCallback(() => {
    if (awayStart.current == null) {
      awayStart.current = Date.now();
      focusLost.current += 1;
    }
  }, []);
  const markBack = useCallback(() => {
    if (awayStart.current != null) {
      timeAwayMs.current += Date.now() - awayStart.current;
      awayStart.current = null;
    }
  }, []);

  useEffect(() => {
    if (!ready) return;
    testsAPI
      .get(id)
      .then(({ data }) => {
        setTest(data);
        // restore any autosaved draft
        if (Array.isArray(data.draft_answers)) {
          const restored: Record<number, string> = {};
          data.draft_answers.forEach((a: string | null, i: number) => { if (a) restored[i] = a; });
          if (Object.keys(restored).length) setAnswers(restored);
        }
        // server-anchored countdown: deadline = started_at + duration, in the local clock
        if (data.duration_minutes && data.started_at && data.server_now) {
          const skew = Date.now() - Date.parse(data.server_now); // localNow - serverNow
          const deadline = Date.parse(data.started_at) + skew + data.duration_minutes * 60000;
          deadlineRef.current = deadline;
          setRemaining(Math.max(0, Math.round((deadline - Date.now()) / 1000)));
        }
      })
      .catch((e) => setError(e.response?.data?.detail || "Could not load this test."))
      .finally(() => setLoading(false));
  }, [ready, id]);

  const handleSubmit = useCallback(async () => {
    if (!test || submitting) return;
    setSubmitting(true);
    markBack(); // flush any in-progress away time
    const ordered = test.questions.map((_, i) => answers[i] ?? "");
    const orderedImages = test.questions.map((_, i) => photos[i] ?? []);
    const hasAnyPhotos = orderedImages.some((imgs) => imgs.length > 0);
    try {
      await testsAPI.submit(id, {
        answers: ordered,
        answer_images: hasAnyPhotos ? orderedImages : undefined,
        time_taken_seconds: Math.round((Date.now() - startedAt) / 1000),
        focus_lost_count: focusLost.current,
        time_away_seconds: Math.round(timeAwayMs.current / 1000),
        paste_attempts: pasteAttempts.current,
      });
      router.replace(`/tests/${id}/result`);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Submission failed. Please try again.");
      setSubmitting(false);
    }
  }, [test, submitting, answers, photos, id, startedAt, router, markBack]);

  async function addPhotos(files: FileList | null) {
    if (!files || files.length === 0) return;
    setError("");
    setPhotoBusy(true);
    try {
      const existing = photos[current] ?? [];
      const room = MAX_PHOTOS_PER_Q - existing.length;
      if (room <= 0) {
        setError(`You can attach up to ${MAX_PHOTOS_PER_Q} photos per question.`);
        return;
      }
      const picked = Array.from(files).slice(0, room);
      const encoded = await Promise.all(picked.map((f) => compressImage(f)));
      setPhotos((p) => ({ ...p, [current]: [...(p[current] ?? []), ...encoded] }));
    } catch {
      setError("Couldn't process that image. Please try another photo.");
    } finally {
      setPhotoBusy(false);
    }
  }

  function removePhoto(qi: number, idx: number) {
    setPhotos((p) => ({ ...p, [qi]: (p[qi] ?? []).filter((_, j) => j !== idx) }));
  }

  // Countdown driven by the server-anchored deadline — resilient to refresh/reopen.
  useEffect(() => {
    if (deadlineRef.current == null) return;
    const tick = () => {
      const left = Math.max(0, Math.round((deadlineRef.current! - Date.now()) / 1000));
      setRemaining(left);
      if (left <= 0) handleSubmit();
    };
    tick();
    const t = setInterval(tick, 1000);
    return () => clearInterval(t);
  }, [test, handleSubmit]);

  // Integrity: count tab/window switches and time spent away from the exam.
  useEffect(() => {
    if (!test || test.kind === "homework") return;  // homework isn't proctored
    const onVis = () => (document.hidden ? markAway() : markBack());
    document.addEventListener("visibilitychange", onVis);
    window.addEventListener("blur", markAway);
    window.addEventListener("focus", markBack);
    return () => {
      document.removeEventListener("visibilitychange", onVis);
      window.removeEventListener("blur", markAway);
      window.removeEventListener("focus", markBack);
    };
  }, [test, markAway, markBack]);

  // Autosave draft answers (text) every couple of seconds while working.
  useEffect(() => {
    if (!test || submitting) return;
    const t = setTimeout(() => {
      const ordered = test.questions.map((_, i) => answers[i] ?? "");
      if (ordered.some((a) => a)) testsAPI.saveDraft(id, ordered).catch(() => {});
    }, 1500);
    return () => clearTimeout(t);
  }, [answers, test, id, submitting]);

  const blockPaste = (e: React.ClipboardEvent) => { e.preventDefault(); pasteAttempts.current += 1; };

  const saveExit = async () => {
    if (test) {
      const ordered = test.questions.map((_, i) => answers[i] ?? "");
      try { await testsAPI.saveDraft(id, ordered); } catch {}
    }
    router.push("/homework");
  };

  const isAnswered = useCallback(
    (i: number) => Boolean((answers[i] ?? "").trim()) || (photos[i]?.length ?? 0) > 0,
    [answers, photos]
  );
  const answeredCount = useMemo(
    () => (test ? test.questions.filter((_, i) => isAnswered(i)).length : 0),
    [test, isAnswered]
  );
  const anyPhotos = useMemo(() => Object.values(photos).some((p) => p.length > 0), [photos]);

  const isWritten = test?.mode === "written";
  const isHomework = test?.kind === "homework";
  const aiMarking = !!getUser()?.ai_marking;

  if (!ready || loading) return <Spinner label="Preparing your test…" />;

  if (error && !test) {
    return (
      <div className="mx-auto max-w-md px-4 py-24 text-center">
        <span className="mx-auto grid h-12 w-12 place-items-center rounded-xl bg-red-50 text-red-600">
          <AlertCircle size={22} />
        </span>
        <h1 className="mt-4 text-lg font-semibold text-ink">Can't open this test</h1>
        <p className="mt-1.5 text-sm text-ink-muted">{error}</p>
        <Button href="/tests" variant="secondary" className="mt-6">Back to my tests</Button>
      </div>
    );
  }
  if (!test) return null;

  const q = test.questions[current];
  const total = test.questions.length;
  const lowTime = remaining !== null && remaining <= 60;

  return (
    <div
      className="fixed inset-0 z-[60] flex flex-col bg-canvas"
      onCopy={isHomework ? undefined : (e) => e.preventDefault()}
      onContextMenu={isHomework ? undefined : (e) => e.preventDefault()}
    >
      {/* Exam top bar */}
      <header className="flex items-center justify-between border-b border-line bg-white px-4 py-3 sm:px-6">
        <div className="flex items-center gap-3">
          <Logo href={null} />
          <div className="hidden border-l border-line pl-3 sm:block">
            <div className="text-sm font-semibold text-ink">{test.title}</div>
            <div className="text-xs text-ink-subtle">
              {humanize(test.subject)}{test.exam_board ? ` · ${test.exam_board}` : ""}
              {isWritten ? " · Written" : ""}{isHomework ? " · Homework" : ""}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          {remaining !== null && (
            <div className={cn("flex items-center gap-1.5 rounded-lg border px-3 py-1.5 text-sm font-semibold tabular-nums",
              lowTime ? "border-red-200 bg-red-50 text-red-600" : "border-line text-ink")}>
              <Clock size={15} /> {fmtTime(remaining)}
            </div>
          )}
          {isHomework && (
            <Button size="sm" variant="secondary" onClick={saveExit}>
              Save &amp; exit
            </Button>
          )}
          <Button size="sm" onClick={() => setReviewOpen(true)}>
            <Flag size={14} /> {isHomework ? "Submit" : "Finish"}
          </Button>
        </div>
      </header>

      {/* Progress */}
      <div className="h-1 w-full bg-slate-100">
        <div className="h-full bg-brand-600 transition-all" style={{ width: `${((current + 1) / total) * 100}%` }} />
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Question navigator */}
        <aside className="hidden w-52 shrink-0 overflow-y-auto border-r border-line bg-white p-4 lg:block">
          <div className="mb-3 text-xs font-semibold uppercase tracking-wide text-ink-subtle">
            Questions
          </div>
          <div className="grid grid-cols-5 gap-2">
            {test.questions.map((_, i) => (
              <button
                key={i}
                onClick={() => setCurrent(i)}
                className={cn(
                  "grid h-9 place-items-center rounded-lg border text-sm font-medium transition-colors",
                  i === current
                    ? "border-brand-600 bg-brand-600 text-white"
                    : isAnswered(i)
                    ? "border-brand-200 bg-brand-50 text-brand-700"
                    : "border-line text-ink-muted hover:bg-slate-50"
                )}
              >
                {i + 1}
              </button>
            ))}
          </div>
          <div className="mt-4 text-xs text-ink-subtle">{answeredCount} of {total} answered</div>
        </aside>

        {/* Question */}
        <main className="flex-1 overflow-y-auto">
          <div className="mx-auto max-w-2xl px-4 py-8 sm:px-6">
            <div className="flex items-center justify-between">
              <div className="text-sm font-medium text-ink-subtle">Question {current + 1} of {total}</div>
              {isWritten && q.marks != null && (
                <span className="rounded-full bg-brand-50 px-2.5 py-0.5 text-xs font-semibold text-brand-700">
                  {q.marks} {q.marks === 1 ? "mark" : "marks"}
                </span>
              )}
            </div>
            {q.question && (
              <h2 className="mt-2 whitespace-pre-line text-lg font-semibold leading-relaxed text-ink sm:text-xl">{q.question}</h2>
            )}

            {q.image && (
              <img src={q.image} alt="Question figure" className="mt-4 max-h-96 w-auto max-w-full rounded-lg border border-line" />
            )}

            {isWritten ? (
              <div className="mt-6">
                <textarea
                  value={answers[current] ?? ""}
                  onChange={(e) => setAnswers((a) => ({ ...a, [current]: e.target.value }))}
                  onPaste={isHomework ? undefined : blockPaste}
                  placeholder="Write your answer here…"
                  rows={12}
                  className="w-full resize-y rounded-xl border border-line bg-white p-4 text-sm leading-relaxed text-ink shadow-sm outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100"
                />
                <div className="mt-2 text-right text-xs text-ink-subtle">
                  {(answers[current] ?? "").trim().split(/\s+/).filter(Boolean).length} words
                </div>

                {/* Photo answers — for handwritten working, diagrams, etc. */}
                <div className="mt-5 rounded-xl border border-dashed border-line-strong bg-slate-50/60 p-4">
                  <div className="flex items-center justify-between">
                    <div className="text-sm font-medium text-ink">Or upload a photo of your working</div>
                    <span className="text-xs text-ink-subtle">{(photos[current]?.length ?? 0)}/{MAX_PHOTOS_PER_Q}</span>
                  </div>
                  <p className="mt-0.5 text-xs text-ink-subtle">Handwritten answers, diagrams or maths working. Marked by your teacher.</p>

                  {(photos[current]?.length ?? 0) > 0 && (
                    <div className="mt-3 flex flex-wrap gap-3">
                      {photos[current].map((src, idx) => (
                        <div key={idx} className="relative">
                          <img src={src} alt={`Answer photo ${idx + 1}`} className="h-24 w-24 rounded-lg border border-line object-cover" />
                          <button type="button" onClick={() => removePhoto(current, idx)}
                            className="absolute -right-2 -top-2 grid h-6 w-6 place-items-center rounded-full bg-white text-ink-muted shadow ring-1 ring-line hover:text-red-600"
                            title="Remove photo">
                            <X size={13} />
                          </button>
                        </div>
                      ))}
                    </div>
                  )}

                  {(photos[current]?.length ?? 0) < MAX_PHOTOS_PER_Q && (
                    <label className="mt-3 inline-flex cursor-pointer items-center gap-2 rounded-lg border border-line bg-white px-3 py-2 text-sm font-medium text-ink shadow-xs hover:bg-slate-50">
                      {photoBusy ? <Loader2 size={15} className="animate-spin" /> : <ImagePlus size={15} />}
                      {photoBusy ? "Processing…" : "Add photo"}
                      <input type="file" accept="image/*" capture="environment" multiple className="hidden"
                        disabled={photoBusy}
                        onChange={(e) => { addPhotos(e.target.files); e.target.value = ""; }} />
                    </label>
                  )}
                </div>
              </div>
            ) : (
              <div className="mt-6 space-y-3">
                {(q.options ?? []).map((opt) => {
                  const selected = answers[current] === opt;
                  return (
                    <button
                      key={opt}
                      onClick={() => setAnswers((a) => ({ ...a, [current]: opt }))}
                      className={cn("option-btn flex items-center gap-3", selected && "selected")}
                    >
                      <span className={cn("grid h-5 w-5 shrink-0 place-items-center rounded-full border",
                        selected ? "border-brand-600 bg-brand-600 text-white" : "border-line-strong")}>
                        {selected && <CheckCircle2 size={14} />}
                      </span>
                      <span>{opt}</span>
                    </button>
                  );
                })}
              </div>
            )}

            <div className="mt-8 flex items-center justify-between">
              <Button variant="secondary" size="sm" disabled={current === 0} onClick={() => setCurrent((c) => Math.max(0, c - 1))}>
                <ChevronLeft size={16} /> Previous
              </Button>
              {current < total - 1 ? (
                <Button size="sm" onClick={() => setCurrent((c) => Math.min(total - 1, c + 1))}>
                  Next <ChevronRight size={16} />
                </Button>
              ) : (
                <Button size="sm" onClick={() => setReviewOpen(true)}>
                  Review &amp; submit <Flag size={14} />
                </Button>
              )}
            </div>
          </div>
        </main>
      </div>

      {/* Review / submit modal */}
      {reviewOpen && (
        <div className="fixed inset-0 z-[70] flex items-center justify-center bg-ink/30 p-4" onClick={() => !submitting && setReviewOpen(false)}>
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-lg font-semibold text-ink">Submit your {isWritten ? "answers" : "test"}?</h3>
            <p className="mt-1.5 text-sm text-ink-muted">
              You've answered <span className="font-semibold text-ink">{answeredCount}</span> of {total} questions.
              {answeredCount < total && (isWritten ? " Unanswered questions will score zero." : " Unanswered questions will be marked as incorrect.")}
            </p>
            {isWritten && (
              <p className="mt-2 text-sm text-ink-muted">
                {aiMarking && !anyPhotos
                  ? "Your answers will be marked instantly by AI with feedback and a model answer."
                  : anyPhotos
                  ? "Because you've attached photos, your answers will be sent to your teacher for marking — you'll see feedback once they're marked."
                  : "Your answers will be sent to your teacher for marking — you'll see feedback once they're marked."}
              </p>
            )}
            {error && (
              <div className="mt-4 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
                <AlertCircle size={16} /> {error}
              </div>
            )}
            <div className="mt-6 flex justify-end gap-2">
              <Button variant="secondary" onClick={() => setReviewOpen(false)} disabled={submitting}>
                Keep working
              </Button>
              <Button onClick={handleSubmit} loading={submitting}>
                {submitting
                  ? (isWritten && aiMarking && !anyPhotos ? "Marking your answers…" : "Submitting…")
                  : (isWritten ? "Submit answers" : "Submit test")}
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
