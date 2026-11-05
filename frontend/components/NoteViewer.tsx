"use client";
import { useEffect, useState } from "react";
import { Download, FileText, ChevronDown, ChevronUp, Camera, X, CheckCircle2 } from "lucide-react";
import { notesAPI } from "@/lib/api";
import { MathText } from "@/components/MathText";
import { formatDate } from "@/lib/utils";
import { compressImage } from "@/lib/images";

const MAX_PHOTOS = 10;
const noSave = {
  onContextMenu: (e: React.MouseEvent) => e.preventDefault(),
  onDragStart: (e: React.DragEvent) => e.preventDefault(),
};

/** One note / homework card. Tutors see the original file; students see watermarked
 *  page images only (no download), and can hand in photos of homework. */
export default function NoteViewer({ note, footer }: { note: any; footer?: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const [detail, setDetail] = useState<any>(null);
  const [pages, setPages] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => () => pages.forEach((u) => URL.revokeObjectURL(u)), [pages]);

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      const d = (await notesAPI.get(note.id)).data;
      setDetail(d);
      if (!d.file_data && d.pages) {
        const token = localStorage.getItem("notenix_token");
        const urls: string[] = [];
        for (let n = 1; n <= d.pages; n++) {
          const res = await fetch(`/api/notes/${note.id}/pages/${n}`, { headers: { Authorization: `Bearer ${token}` } });
          if (!res.ok) throw new Error();
          urls.push(URL.createObjectURL(await res.blob()));
          setPages([...urls]);
        }
      }
    } catch {
      setError("Couldn't load this file. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const toggle = () => {
    const next = !open;
    setOpen(next);
    if (next && !detail) load();
  };

  const file: string | undefined = detail?.file_data;
  const isPdf = file?.startsWith("data:application/pdf");
  const isHomework = note.kind === "homework";
  const sub = detail?.submission ?? note.submission;
  const status = sub?.marked_at ? `Marked${sub.mark ? `: ${sub.mark}` : ""}` : sub ? "Handed in" : null;

  return (
    <div className="card p-5">
      <button onClick={toggle} className="flex w-full items-start justify-between gap-3 text-left">
        <div>
          <div className="font-semibold text-ink">
            {isHomework && <span className="mr-2 rounded-full bg-amber-100 px-2 py-0.5 text-xs font-semibold text-amber-800">Homework</span>}
            {note.title}
            {status && <span className="ml-2 rounded-full bg-emerald-100 px-2 py-0.5 text-xs font-semibold text-emerald-800">{status}</span>}
          </div>
          <div className="mt-0.5 text-xs text-ink-subtle">
            {[note.subject, formatDate(note.created_at), note.due_at ? `due ${formatDate(note.due_at)}` : null, note.file_name].filter(Boolean).join(" · ")}
          </div>
        </div>
        {open ? <ChevronUp size={18} className="text-ink-subtle" /> : <ChevronDown size={18} className="text-ink-subtle" />}
      </button>
      {open && (
        <div className="mt-4 space-y-4">
          {note.body && (
            <div className="whitespace-pre-line text-sm text-ink">
              <MathText text={note.body} />
            </div>
          )}
          {loading && <p className="text-sm text-ink-muted">Loading{pages.length ? ` page ${pages.length + 1}…` : "…"}</p>}
          {error && <p className="text-sm text-red-600">{error}</p>}
          {file && (
            <>
              {isPdf ? (
                <iframe src={file} title={note.title} className="h-[70vh] w-full rounded-lg border border-line" />
              ) : (
                // eslint-disable-next-line @next/next/no-img-element
                <img src={file} alt={note.title} className="max-w-full rounded-lg border border-line" />
              )}
              <a href={file} download={note.file_name || "notes"} className="inline-flex items-center gap-1.5 text-sm font-medium text-brand-600 hover:text-brand-700">
                <Download size={14} /> Download {note.file_name || "file"}
              </a>
            </>
          )}
          {pages.length > 0 && (
            <div className="select-none space-y-3" {...noSave}>
              {pages.map((u, i) => (
                // eslint-disable-next-line @next/next/no-img-element
                <img key={u} src={u} alt={`Page ${i + 1}`} draggable={false} {...noSave}
                  className="pointer-events-auto w-full rounded-lg border border-line" />
              ))}
            </div>
          )}
          {!note.body && !note.has_file && <p className="flex items-center gap-1 text-sm text-ink-muted"><FileText size={14} /> Empty note</p>}
          {isHomework && detail && !file && <HandIn noteId={note.id} sub={sub} onDone={(s) => setDetail({ ...detail, submission: s })} />}
          {footer}
        </div>
      )}
    </div>
  );
}

function HandIn({ noteId, sub, onDone }: { noteId: number; sub: any; onDone: (s: any) => void }) {
  const [photos, setPhotos] = useState<string[]>([]);
  const [comment, setComment] = useState("");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const [editing, setEditing] = useState(!sub);

  const add = async (files: FileList | null) => {
    if (!files) return;
    setMsg("");
    const room = MAX_PHOTOS - photos.length;
    const picked = Array.from(files).slice(0, room);
    try {
      const out = await Promise.all(picked.map((f) => compressImage(f)));
      setPhotos((p) => [...p, ...out]);
    } catch {
      setMsg("One of those files isn't a photo we can read.");
    }
  };

  const send = async () => {
    if (!photos.length) return setMsg("Add at least one photo of your work.");
    setBusy(true);
    setMsg("");
    try {
      const { data } = await notesAPI.submit(noteId, { images: photos, comment });
      onDone({ ...data, images: photos });
      setEditing(false);
      setPhotos([]);
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || "Couldn't hand in. Please try again.");
    } finally {
      setBusy(false);
    }
  };

  if (sub?.marked_at) {
    return (
      <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-4 text-sm">
        <div className="flex items-center gap-2 font-semibold text-emerald-900"><CheckCircle2 size={16} /> Marked{sub.mark ? `: ${sub.mark}` : ""}</div>
        {sub.feedback && <p className="mt-2 whitespace-pre-line text-emerald-900">{sub.feedback}</p>}
      </div>
    );
  }
  if (sub && !editing) {
    return (
      <div className="rounded-lg border border-line bg-canvas p-4 text-sm">
        <div className="flex items-center gap-2 font-semibold text-ink"><CheckCircle2 size={16} className="text-emerald-600" /> Handed in {formatDate(sub.submitted_at)} · {sub.photos} photo{sub.photos === 1 ? "" : "s"}</div>
        <p className="mt-1 text-ink-muted">Your tutor will mark it soon.</p>
        <button onClick={() => setEditing(true)} className="mt-2 text-sm font-medium text-brand-600 hover:text-brand-700">Replace my hand-in</button>
      </div>
    );
  }
  return (
    <div className="rounded-lg border border-line p-4">
      <div className="font-semibold text-ink">Hand in your homework</div>
      <p className="mt-1 text-sm text-ink-muted">Take clear photos of your working (up to {MAX_PHOTOS}).</p>
      <div className="mt-3 flex flex-wrap gap-2">
        {photos.map((p, i) => (
          <div key={i} className="relative">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={p} alt={`Photo ${i + 1}`} className="h-24 w-24 rounded-md border border-line object-cover" />
            <button onClick={() => setPhotos(photos.filter((_, j) => j !== i))} aria-label="Remove photo"
              className="absolute -right-2 -top-2 rounded-full bg-surface p-0.5 shadow"><X size={14} /></button>
          </div>
        ))}
        {photos.length < MAX_PHOTOS && (
          <label className="flex h-24 w-24 cursor-pointer flex-col items-center justify-center gap-1 rounded-md border border-dashed border-line text-xs text-ink-muted hover:border-brand-400">
            <Camera size={18} /> Add photo
            <input type="file" accept="image/*" multiple capture="environment" className="hidden" onChange={(e) => { add(e.target.files); e.target.value = ""; }} />
          </label>
        )}
      </div>
      <textarea value={comment} onChange={(e) => setComment(e.target.value)} placeholder="Anything to tell your tutor? (optional)"
        className="mt-3 w-full rounded-lg border border-line p-2 text-sm" rows={2} />
      {msg && <p className="mt-2 text-sm text-red-600">{msg}</p>}
      <div className="mt-3 flex gap-2">
        <button onClick={send} disabled={busy} className="btn-primary rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-60">
          {busy ? "Handing in…" : "Hand in"}
        </button>
        {sub && <button onClick={() => setEditing(false)} className="px-3 text-sm text-ink-muted">Cancel</button>}
      </div>
    </div>
  );
}
