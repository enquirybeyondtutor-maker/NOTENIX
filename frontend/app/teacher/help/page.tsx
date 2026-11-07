"use client";
import { useEffect, useState } from "react";
import { LifeBuoy, X, Camera } from "lucide-react";
import { helpAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, Spinner, EmptyState } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { formatDate } from "@/lib/utils";
import { compressImage } from "@/lib/images";

/** Tutor queue for KS3 homework-help questions. */
export default function TeacherHelpPage() {
  const { ready } = useAuthGuard("teacher");
  const [rows, setRows] = useState<any[] | null>(null);
  const [open, setOpen] = useState<any>(null);
  const [reply, setReply] = useState("");
  const [photos, setPhotos] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");

  const load = () => helpAPI.queue().then((r) => setRows(r.data)).catch(() => setRows([]));
  useEffect(() => { if (ready) load(); }, [ready]);

  const view = async (id: number) => {
    const { data } = await helpAPI.detail(id);
    setOpen(data);
    setReply(data.reply || "");
    setPhotos(data.reply_images || []);
    setMsg("");
  };

  const send = async () => {
    setBusy(true);
    setMsg("");
    try {
      await helpAPI.reply(open.id, { reply, images: photos });
      setOpen(null);
      load();
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || "Couldn't send the reply.");
    } finally {
      setBusy(false);
    }
  };

  if (!ready || rows === null) return <Spinner label="Loading questions…" />;
  const waiting = rows.filter((r) => r.status === "open").length;

  return (
    <PageContainer>
      <PageHeader icon={LifeBuoy} title="Homework help"
        subtitle={waiting ? `${waiting} question${waiting === 1 ? "" : "s"} waiting for a reply` : "KS3 students' homework questions"} />
      {rows.length === 0 ? (
        <EmptyState icon={LifeBuoy} title="No questions yet" desc="When a KS3 student sends a homework question, it appears here." />
      ) : (
        <div className="card divide-y divide-line">
          {rows.map((r) => (
            <button key={r.id} onClick={() => view(r.id)} className="flex w-full items-center justify-between gap-3 px-5 py-3 text-left hover:bg-canvas">
              <div>
                <div className="text-sm font-medium text-ink">{r.student.full_name} · {r.student.level || `Year ${r.student.year}`} · {r.subject}</div>
                <div className="text-xs text-ink-subtle">{formatDate(r.created_at)} · {r.question ? r.question.slice(0, 80) : `${r.photos} photo${r.photos === 1 ? "" : "s"}`}</div>
              </div>
              <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${r.status === "open" ? "bg-amber-100 text-amber-800" : "bg-emerald-100 text-emerald-800"}`}>
                {r.status === "open" ? "To answer" : "Answered"}
              </span>
            </button>
          ))}
        </div>
      )}

      {open && (
        <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/40 p-4" onClick={() => setOpen(null)}>
          <div className="my-8 w-full max-w-3xl rounded-xl bg-surface p-5" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="font-semibold text-ink">{open.student.full_name} · {open.student.level || `Year ${open.student.year}`} · {open.subject}</div>
                <div className="text-xs text-ink-subtle">{open.student.email} · asked {formatDate(open.created_at)}</div>
              </div>
              <button onClick={() => setOpen(null)} aria-label="Close"><X size={18} /></button>
            </div>
            {open.question && <p className="mt-3 whitespace-pre-line rounded-lg bg-canvas p-3 text-sm text-ink">{open.question}</p>}
            <div className="mt-3 space-y-3">
              {open.images.map((src: string, i: number) => (
                // eslint-disable-next-line @next/next/no-img-element
                <img key={i} src={src} alt={`Photo ${i + 1}`} className="w-full rounded-lg border border-line" />
              ))}
            </div>
            <textarea value={reply} onChange={(e) => setReply(e.target.value)} rows={6}
              placeholder="Explain the method step by step (maths in $...$). Guide them; don't just give the answer."
              className="mt-4 w-full rounded-lg border border-line bg-surface p-2.5 text-sm text-ink" />
            <div className="mt-2 flex flex-wrap items-center gap-2">
              {photos.map((p, i) => (
                <div key={i} className="relative">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={p} alt="" className="h-16 w-16 rounded-md border border-line object-cover" />
                  <button onClick={() => setPhotos(photos.filter((_, j) => j !== i))} className="absolute -right-2 -top-2 rounded-full bg-surface p-0.5 shadow" aria-label="Remove"><X size={12} /></button>
                </div>
              ))}
              <label className="inline-flex cursor-pointer items-center gap-1 text-sm text-brand-600 hover:underline">
                <Camera size={14} /> Attach working
                <input type="file" accept="image/*" multiple className="hidden"
                  onChange={async (e) => { const f = e.target.files; if (f) { const out = await Promise.all(Array.from(f).slice(0, 4).map((x) => compressImage(x))); setPhotos((p) => [...p, ...out].slice(0, 4)); } e.target.value = ""; }} />
              </label>
            </div>
            {msg && <p className="mt-2 text-sm text-red-600">{msg}</p>}
            <div className="mt-4 flex justify-end gap-2">
              <Button variant="secondary" onClick={() => setOpen(null)}>Cancel</Button>
              <Button onClick={send} loading={busy} disabled={!reply.trim()}>{open.status === "answered" ? "Update reply" : "Send reply"}</Button>
            </div>
          </div>
        </div>
      )}
    </PageContainer>
  );
}
