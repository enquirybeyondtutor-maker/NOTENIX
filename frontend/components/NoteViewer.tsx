"use client";
import { useEffect, useRef, useState } from "react";
import { Download, FileText, ChevronDown, ChevronUp, Camera, X, CheckCircle2, Lock, Unlock } from "lucide-react";
import { api, notesAPI } from "@/lib/api";
import { invalidateInbox } from "@/lib/inbox";
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
export default function NoteViewer({ note, footer, defaultOpen = false }: { note: any; footer?: React.ReactNode; defaultOpen?: boolean }) {
  const [open, setOpen] = useState(false);
  // Students' cards carry `seen`; a new one shows a "New" badge until it is first opened.
  const [isNew, setIsNew] = useState(note.seen === false);
  const [detail, setDetail] = useState<any>(null);
  // One slot per page: blob URL when loaded, "" while loading, "x" if it failed.
  const [pages, setPages] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const urls = useRef<string[]>([]);

  useEffect(() => () => urls.current.forEach((u) => URL.revokeObjectURL(u)), []);

  const fetchPage = async (n: number): Promise<string> => {
    const token = localStorage.getItem("notenix_token");
    for (let attempt = 0; attempt < 6; attempt++) {
      try {
        const res = await fetch(`/api/notes/${note.id}/pages/${n}`, { headers: { Authorization: `Bearer ${token}` } });
        if (res.status === 200) {
          const u = URL.createObjectURL(await res.blob());
          urls.current.push(u);
          return u;
        }
        if (res.status === 404 || res.status === 401 || res.status === 403) break;
      } catch { /* network hiccup: retry */ }
      await new Promise((r) => setTimeout(r, 1500 * (attempt + 1)));
    }
    return "x";
  };

  const loadPages = async (count: number, only?: number[]) => {
    const todo = only ?? Array.from({ length: count }, (_, i) => i + 1);
    setPages((p) => {
      const next = p.length === count ? [...p] : Array(count).fill("");
      todo.forEach((n) => (next[n - 1] = ""));
      return next;
    });
    let i = 0;
    const worker = async () => {
      while (i < todo.length) {
        const n = todo[i++];
        const u = await fetchPage(n);
        setPages((p) => { const next = [...p]; next[n - 1] = u; return next; });
      }
    };
    await Promise.all([worker(), worker(), worker()]);
  };

  const load = async () => {
    setLoading(true);
    setError("");
    try {
      let d = (await notesAPI.get(note.id)).data;
      setDetail(d);
      // A new upload is turned into pages in the background: wait for it (up to ~3 min).
      for (let t = 0; d.rendering && t < 60; t++) {
        await new Promise((r) => setTimeout(r, 3000));
        d = (await notesAPI.get(note.id)).data;
        setDetail(d);
      }
      if (d.rendering) setError("This file is still being prepared. Please try again in a minute.");
      else if (!d.file_data && d.pages) await loadPages(d.pages);
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
    if (next && isNew) {
      setIsNew(false);
      // Refresh the menu badges once the server has recorded it (not before, or they'd still say New).
      api.post(`/notes/${note.id}/seen`).catch(() => {}).finally(() => window.dispatchEvent(new Event("notenix:seen")));
    }
  };

  // Opened from a dashboard link (/homework#note-12): expand it straight away.
  useEffect(() => {
    if (!defaultOpen) return;
    toggle();
    setTimeout(() => document.getElementById(`note-${note.id}`)?.scrollIntoView({ behavior: "smooth", block: "start" }), 100);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const file: string | undefined = detail?.file_data;
  const isPdf = file?.startsWith("data:application/pdf");
  const isHomework = note.kind === "homework";
  const sub = detail?.submission ?? note.submission;
  const status = sub?.marked_at ? `Marked${sub.mark ? `: ${sub.mark}` : ""}` : sub ? "Handed in" : null;

  return (
    <div id={`note-${note.id}`} className={`card scroll-mt-24 p-5 ${isNew ? "ring-2 ring-brand-200" : ""}`}>
      <button onClick={toggle} className="flex w-full items-start justify-between gap-3 text-left">
        <div>
          <div className="font-semibold text-ink">
            {isNew && <span className="mr-2 rounded-full bg-brand-600 px-2 py-0.5 text-xs font-semibold text-white">New</span>}
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
          {loading && detail?.rendering && <p className="text-sm text-ink-muted">Preparing pages… this takes a moment the first time.</p>}
          {loading && !detail?.rendering && !pages.length && <p className="text-sm text-ink-muted">Loading…</p>}
          {pages.length > 0 && pages.some((u) => !u) && <p className="text-sm text-ink-muted">Loading pages ({pages.filter((u) => u && u !== "x").length}/{pages.length})…</p>}
          {error && (
            <p className="text-sm text-red-600">
              {error} <button onClick={load} className="font-medium underline">Try again</button>
            </p>
          )}
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
              {pages.map((u, i) =>
                u === "x" ? (
                  <div key={i} className="rounded-lg border border-line p-6 text-center text-sm text-ink-muted">
                    Page {i + 1} didn&apos;t load.{" "}
                    <button onClick={() => loadPages(pages.length, [i + 1])} className="font-medium text-brand-600 underline">Retry</button>
                  </div>
                ) : u ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img key={i} src={u} alt={`Page ${i + 1}`} draggable={false} {...noSave}
                    className="pointer-events-auto w-full rounded-lg border border-line" />
                ) : (
                  <div key={i} className="flex aspect-[1/1.41] w-full items-center justify-center rounded-lg border border-line text-sm text-ink-subtle">
                    Page {i + 1}…
                  </div>
                ),
              )}
            </div>
          )}
          {!note.body && !note.has_file && <p className="flex items-center gap-1 text-sm text-ink-muted"><FileText size={14} /> Empty note</p>}
          {isHomework && detail && !file && (
            <HandIn noteId={note.id} sub={sub} onDone={(s) => {
              setDetail({ ...detail, submission: s });
              // Handing in unlocks the solutions: fetch the note again so the panel opens up.
              if (detail.solution) notesAPI.get(note.id).then((r) => setDetail(r.data)).catch(() => {});
            }} />
          )}
          {isHomework && detail?.solution && <Solutions noteId={note.id} info={detail.solution} />}
          {isHomework && detail?.solution_data && (
            <a href={detail.solution_data} download={note.solution_name || "solutions"}
              className="inline-flex items-center gap-1.5 text-sm font-medium text-brand-600 hover:text-brand-700">
              <Lock size={14} /> Solutions: {note.solution_name || "file"} (students see these after handing in)
            </a>
          )}
          {footer}
        </div>
      )}
    </div>
  );
}

/** Homework solutions: locked until the student hands in, then shown as watermarked page images. */
function Solutions({ noteId, info }: { noteId: number; info: { locked: boolean; pages?: number | null } }) {
  const [pages, setPages] = useState<string[] | null>(null);
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const urls = useRef<string[]>([]);
  useEffect(() => () => urls.current.forEach((u) => URL.revokeObjectURL(u)), []);

  if (info.locked) {
    return (
      <div className="flex items-start gap-3 rounded-lg border border-dashed border-line bg-canvas p-4 text-sm">
        <Lock size={18} className="mt-0.5 shrink-0 text-ink-subtle" />
        <div>
          <div className="font-semibold text-ink">Solutions are locked</div>
          <p className="mt-0.5 text-ink-muted">Hand in your work above and the worked solutions open straight away, so you can check your answers.</p>
        </div>
      </div>
    );
  }

  const show = async () => {
    setBusy(true);
    setMsg("");
    const token = localStorage.getItem("notenix_token");
    try {
      let count = info.pages ?? null;
      // Solutions are turned into pages in the background; wait briefly if they're not ready yet.
      for (let t = 0; !count && t < 20; t++) {
        await new Promise((r) => setTimeout(r, 3000));
        count = (await notesAPI.get(noteId)).data.solution?.pages ?? null;
      }
      if (!count) return setMsg("The solutions are still being prepared. Please try again in a minute.");
      const out: string[] = [];
      for (let n = 1; n <= count; n++) {
        const res = await fetch(`/api/notes/${noteId}/solution/pages/${n}`, { headers: { Authorization: `Bearer ${token}` } });
        if (res.status !== 200) throw new Error(String(res.status));
        const u = URL.createObjectURL(await res.blob());
        urls.current.push(u);
        out.push(u);
      }
      setPages(out);
    } catch {
      setMsg("Couldn't load the solutions. Please try again.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="rounded-lg border border-emerald-200 bg-emerald-50/50 p-4">
      <div className="flex flex-wrap items-center gap-3">
        <div className="flex items-center gap-2 font-semibold text-emerald-900"><Unlock size={16} /> Solutions unlocked</div>
        {!pages && (
          <button onClick={show} disabled={busy} className="ml-auto rounded-lg bg-emerald-600 px-3 py-1.5 text-sm font-semibold text-white hover:bg-emerald-700 disabled:opacity-60">
            {busy ? "Loading…" : "Show solutions"}
          </button>
        )}
      </div>
      {msg && <p className="mt-2 text-sm text-red-600">{msg}</p>}
      {pages && (
        <div className="mt-3 select-none space-y-3" {...noSave}>
          {pages.map((u, i) => (
            // eslint-disable-next-line @next/next/no-img-element
            <img key={i} src={u} alt={`Solutions page ${i + 1}`} draggable={false} {...noSave} className="w-full rounded-lg border border-line bg-white" />
          ))}
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

  // A PDF scan of the worksheet: the server turns each page into a hand-in photo.
  const addPdf = async (files: FileList | null) => {
    const file = files?.[0];
    if (!file) return;
    setMsg("");
    const room = MAX_PHOTOS - photos.length;
    if (room <= 0) return setMsg(`You can hand in up to ${MAX_PHOTOS} pages.`);
    if (file.size > 15 * 1024 * 1024) return setMsg("That PDF is too large (max 15 MB). Try a smaller scan, or add photos instead.");
    setBusy(true);
    try {
      const dataUri: string = await new Promise((resolve, reject) => {
        const r = new FileReader();
        r.onload = () => resolve(String(r.result));
        r.onerror = () => reject(new Error("read"));
        r.readAsDataURL(file);
      });
      const { data } = await api.post(`/notes/${noteId}/pdf-pages`, { file: dataUri, max_pages: room });
      setPhotos((p) => [...p, ...data.pages]);
      if (data.truncated) setMsg(`Only the first ${data.pages.length} of ${data.total_pages} PDF pages were added: you can hand in up to ${MAX_PHOTOS} pages.`);
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || "Couldn't read that PDF. Please try again, or add photos instead.");
    } finally {
      setBusy(false);
    }
  };

  const send = async () => {
    if (!photos.length) return setMsg("Add at least one photo of your work.");
    setBusy(true);
    setMsg("");
    try {
      const { data } = await notesAPI.submit(noteId, { images: photos, comment });
      onDone({ ...data, images: photos });
      invalidateInbox();  // homework count in the menu and dashboard
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
      <p className="mt-1 text-sm text-ink-muted">Take clear photos of your working, or attach a PDF scan (up to {MAX_PHOTOS} pages).</p>
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
        {photos.length < MAX_PHOTOS && (
          <label className={`flex h-24 w-24 cursor-pointer flex-col items-center justify-center gap-1 rounded-md border border-dashed border-line text-xs text-ink-muted hover:border-brand-400 ${busy ? "pointer-events-none opacity-60" : ""}`}>
            <FileText size={18} /> {busy ? "Reading…" : "Attach PDF"}
            <input type="file" accept="application/pdf,.pdf" className="hidden" disabled={busy} onChange={(e) => { addPdf(e.target.files); e.target.value = ""; }} />
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
