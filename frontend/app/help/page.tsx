"use client";
import { useEffect, useState } from "react";
import { Camera, LifeBuoy, X, CheckCircle2, Clock } from "lucide-react";
import { helpAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, Spinner, EmptyState } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { MathText } from "@/components/MathText";
import { formatDate } from "@/lib/utils";
import { compressImage } from "@/lib/images";

const SUBJECTS = ["Maths", "Science", "English", "Other"];

export default function HomeworkHelpPage() {
  const { ready } = useAuthGuard("student");
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState("");
  const [subject, setSubject] = useState("Maths");
  const [question, setQuestion] = useState("");
  const [photos, setPhotos] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");

  const load = () => helpAPI.mine().then((r) => { setData(r.data); if (r.data.subjects?.length) setSubject((cur) => r.data.subjects.includes(cur) ? cur : r.data.subjects[0]); }).catch((e) => setError(e?.response?.data?.detail || "Couldn't load."));
  useEffect(() => { if (ready) load(); }, [ready]);

  const addPhotos = async (files: FileList | null) => {
    if (!files) return;
    try {
      const out = await Promise.all(Array.from(files).slice(0, 4 - photos.length).map((f) => compressImage(f)));
      setPhotos((p) => [...p, ...out]);
    } catch {
      setMsg("One of those files isn't a photo we can read.");
    }
  };

  const send = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!photos.length && !question.trim()) return setMsg("Add a photo of the question or type it out.");
    setBusy(true);
    setMsg("");
    try {
      await helpAPI.ask({ subject, question, images: photos });
      setQuestion("");
      setPhotos([]);
      setMsg("Sent! A tutor will reply here, usually within a day.");
      load();
    } catch (err: any) {
      setMsg(err?.response?.data?.detail || "Couldn't send. Please try again.");
    } finally {
      setBusy(false);
    }
  };

  if (!ready || (!data && !error)) return <Spinner label="Loading homework help…" />;
  if (error) return <PageContainer><EmptyState icon={LifeBuoy} title="Homework help" desc={error} /></PageContainer>;
  const a = data.allowance;

  return (
    <PageContainer>
      <PageHeader icon={LifeBuoy} title={a.plan ? "Ask a tutor" : "Homework help"}
        subtitle={a.plan ? `Stuck on a question${data.level ? ` (${data.level})` : ""}? Send a photo and a Beyond Tutors tutor explains it.` : "Stuck on school homework? Send it to a Beyond Tutors tutor."} />

      <form onSubmit={send} className="card p-5">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="font-semibold text-ink">Ask about a homework question</div>
          <span className={`rounded-full px-2.5 py-0.5 text-xs font-semibold ${a.left ? "bg-brand-50 text-brand-700" : "bg-red-50 text-red-700"}`}>
            {a.left} of {a.cap} questions left {a.period === "trial" ? (a.plan ? "in your free trial" : "in your free week") : a.plan ? `until ${new Date(a.until).toLocaleDateString("en-GB", { day: "numeric", month: "short" })}` : "this month"}
          </span>
        </div>
        <div className="mt-4 flex flex-wrap gap-2">
          {(data.subjects || SUBJECTS).map((s: string) => (
            <button type="button" key={s} onClick={() => setSubject(s)}
              className={`rounded-full border px-3 py-1 text-sm ${subject === s ? "border-brand-600 bg-brand-600 text-white" : "border-line text-ink-muted hover:border-brand-400"}`}>
              {s}
            </button>
          ))}
        </div>
        <div className="mt-4 flex flex-wrap gap-2">
          {photos.map((p, i) => (
            <div key={i} className="relative">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={p} alt={`Photo ${i + 1}`} className="h-24 w-24 rounded-md border border-line object-cover" />
              <button type="button" onClick={() => setPhotos(photos.filter((_, j) => j !== i))} aria-label="Remove photo"
                className="absolute -right-2 -top-2 rounded-full bg-surface p-0.5 shadow"><X size={14} /></button>
            </div>
          ))}
          {photos.length < 4 && (
            <label className="flex h-24 w-24 cursor-pointer flex-col items-center justify-center gap-1 rounded-md border border-dashed border-line text-xs text-ink-muted hover:border-brand-400">
              <Camera size={18} /> Photo
              <input type="file" accept="image/*" multiple capture="environment" className="hidden"
                onChange={(e) => { addPhotos(e.target.files); e.target.value = ""; }} />
            </label>
          )}
        </div>
        <textarea value={question} onChange={(e) => setQuestion(e.target.value)} rows={3}
          placeholder="Which question, and what's confusing you? e.g. 'Q4: I don't get how to find the missing angle.'"
          className="mt-3 w-full rounded-lg border border-line bg-surface p-2.5 text-sm text-ink" />
        {msg && <p className="mt-2 text-sm text-ink-muted">{msg}</p>}
        <Button type="submit" loading={busy} disabled={!a.left} className="mt-3">Send to a tutor</Button>
        <p className="mt-2 text-xs text-ink-subtle">Tutors explain how to do it, so you can finish it yourself; they won&apos;t just give the answer.</p>
      </form>

      <h2 className="mt-8 mb-3 font-semibold text-ink">Your questions</h2>
      {data.requests.length === 0 ? (
        <p className="text-sm text-ink-muted">Nothing asked yet.</p>
      ) : (
        <div className="space-y-3">
          {data.requests.map((h: any) => (
            <div key={h.id} className="card p-5">
              <div className="flex items-center justify-between gap-2">
                <div className="text-sm font-semibold text-ink">{h.subject} · {formatDate(h.created_at)}</div>
                {h.status === "answered" ? (
                  <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-2 py-0.5 text-xs font-semibold text-emerald-700"><CheckCircle2 size={12} /> Answered</span>
                ) : (
                  <span className="inline-flex items-center gap-1 rounded-full bg-amber-50 px-2 py-0.5 text-xs font-semibold text-amber-700"><Clock size={12} /> Waiting for a tutor</span>
                )}
              </div>
              {h.question && <p className="mt-2 whitespace-pre-line text-sm text-ink-muted">{h.question}</p>}
              {h.images?.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-2">
                  {h.images.map((src: string, i: number) => (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img key={i} src={src} alt="" className="h-20 w-20 rounded-md border border-line object-cover" />
                  ))}
                </div>
              )}
              {h.reply && (
                <div className="mt-4 rounded-lg border border-emerald-200 bg-emerald-50/60 p-4">
                  <div className="text-xs font-semibold text-emerald-800">Tutor&apos;s reply</div>
                  <div className="mt-1 whitespace-pre-line text-sm text-ink"><MathText text={h.reply} /></div>
                  {h.reply_images?.map((src: string, i: number) => (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img key={i} src={src} alt="" className="mt-2 max-w-full rounded-md border border-line" />
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </PageContainer>
  );
}
