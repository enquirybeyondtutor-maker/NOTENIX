"use client";
import { useEffect, useState } from "react";
import { Inbox, X, Mail, Download } from "lucide-react";
import { notesAPI } from "@/lib/api";
import { formatDate } from "@/lib/utils";

/** Teacher view: worksheet homework handed in by students, with marking.
 *  "Email PDF" sends the hand-in to the tutor as one PDF (photos inside a white border, Notenix
 *  header and footer on each page) for proper marking; "Download PDF" saves the same file. */
const EMAIL_KEY = "nx-handin-email";
export default function HomeworkHandins() {
  const [rows, setRows] = useState<any[] | null>(null);
  const [open, setOpen] = useState<any>(null);
  const [mark, setMark] = useState("");
  const [feedback, setFeedback] = useState("");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const [emailTo, setEmailTo] = useState("");
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState("");
  const [downloading, setDownloading] = useState(false);

  const load = () => notesAPI.submissions().then((r) => setRows(r.data)).catch(() => setRows([]));
  useEffect(() => { load(); }, []);

  const view = async (id: number) => {
    setMsg("");
    setSent("");
    const { data } = await notesAPI.submission(id);
    setOpen(data);
    setEmailTo((typeof window !== "undefined" && localStorage.getItem(EMAIL_KEY)) || data.email_to || "");
    setMark(data.mark || "");
    setFeedback(data.feedback || "");
  };

  const save = async () => {
    setBusy(true);
    setMsg("");
    try {
      await notesAPI.markSubmission(open.id, { mark, feedback });
      setOpen(null);
      load();
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || "Couldn't save the mark.");
    } finally {
      setBusy(false);
    }
  };

  const emailPdf = async () => {
    setSending(true);
    setMsg("");
    setSent("");
    try {
      const { data } = await notesAPI.emailSubmission(open.id, emailTo.trim());
      if (emailTo.trim()) localStorage.setItem(EMAIL_KEY, emailTo.trim());
      setSent(`Sent to ${data.sent_to}`);
    } catch (e: any) {
      setMsg(e?.response?.data?.detail || "Couldn't send the email.");
    } finally {
      setSending(false);
    }
  };

  const downloadPdf = async () => {
    setDownloading(true);
    setMsg("");
    try {
      const { data } = await notesAPI.submissionPdf(open.id);
      const url = URL.createObjectURL(data as Blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${open.student.full_name} - ${open.title}.pdf`.replace(/[^\w\s().-]/g, "");
      a.click();
      setTimeout(() => URL.revokeObjectURL(url), 5000);
    } catch {
      setMsg("Couldn't make the PDF.");
    } finally {
      setDownloading(false);
    }
  };

  if (rows === null || rows.length === 0) return null;
  const waiting = rows.filter((r) => !r.marked_at).length;

  return (
    <div className="card mb-6 p-5">
      <div className="flex items-center gap-2 font-semibold text-ink">
        <Inbox size={18} /> Worksheet hand-ins
        {waiting > 0 && <span className="rounded-full bg-amber-100 px-2 py-0.5 text-xs font-semibold text-amber-800">{waiting} to mark</span>}
      </div>
      <div className="mt-3 divide-y divide-line">
        {rows.map((r) => (
          <button key={r.id} onClick={() => view(r.id)} className="flex w-full items-center justify-between gap-3 py-2.5 text-left hover:bg-canvas">
            <div>
              <div className="text-sm font-medium text-ink">{r.student.full_name} · {r.title}</div>
              <div className="text-xs text-ink-subtle">
                Handed in {formatDate(r.submitted_at)} · {r.photos} photo{r.photos === 1 ? "" : "s"}
                {r.due_at && r.submitted_at > r.due_at ? " · late" : ""}
              </div>
            </div>
            <span className={`rounded-full px-2 py-0.5 text-xs font-semibold ${r.marked_at ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-800"}`}>
              {r.marked_at ? (r.mark || "Marked") : "To mark"}
            </span>
          </button>
        ))}
      </div>

      {open && (
        <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/40 p-4" onClick={() => setOpen(null)}>
          <div className="my-8 w-full max-w-3xl rounded-xl bg-surface p-5" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-start justify-between gap-3">
              <div>
                <div className="font-semibold text-ink">{open.student.full_name} · {open.title}</div>
                <div className="text-xs text-ink-subtle">{open.student.email} · handed in {formatDate(open.submitted_at)}</div>
              </div>
              <button onClick={() => setOpen(null)} aria-label="Close"><X size={18} /></button>
            </div>
            <div className="mt-4 rounded-lg border border-brand-200 bg-brand-50/50 p-3">
              <div className="text-xs font-semibold text-ink">Mark it on paper or in a PDF app</div>
              <div className="mt-2 flex flex-wrap items-center gap-2">
                <input type="email" value={emailTo} onChange={(e) => setEmailTo(e.target.value)} placeholder="your@email.com"
                  className="min-w-[200px] flex-1 rounded-lg border border-line bg-surface p-2 text-sm" />
                <button onClick={emailPdf} disabled={sending}
                  className="inline-flex items-center gap-1.5 rounded-lg bg-brand-600 px-3 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-60">
                  <Mail size={15} /> {sending ? "Sending…" : "Email PDF"}
                </button>
                <button onClick={downloadPdf} disabled={downloading}
                  className="inline-flex items-center gap-1.5 rounded-lg border border-line bg-surface px-3 py-2 text-sm font-medium text-ink hover:bg-canvas disabled:opacity-60">
                  <Download size={15} /> {downloading ? "Preparing…" : "Download PDF"}
                </button>
              </div>
              <p className="mt-1.5 text-xs text-ink-subtle">All {open.images.length} photo{open.images.length === 1 ? "" : "s"} in one PDF with a cover page and mark box, nothing cropped.</p>
              {sent && <p className="mt-1.5 text-xs font-semibold text-emerald-700">✓ {sent}</p>}
            </div>
            {open.comment && <p className="mt-3 rounded-lg bg-canvas p-3 text-sm text-ink">&ldquo;{open.comment}&rdquo;</p>}
            <div className="mt-4 space-y-3">
              {open.images.map((src: string, i: number) => (
                // eslint-disable-next-line @next/next/no-img-element
                <img key={i} src={src} alt={`Photo ${i + 1}`} className="w-full rounded-lg border border-line" />
              ))}
            </div>
            <div className="mt-4 grid gap-3 sm:grid-cols-[160px_1fr]">
              <input value={mark} onChange={(e) => setMark(e.target.value)} placeholder="Mark, e.g. 7/10"
                className="rounded-lg border border-line p-2 text-sm" />
              <textarea value={feedback} onChange={(e) => setFeedback(e.target.value)} placeholder="Feedback for the student"
                className="rounded-lg border border-line p-2 text-sm" rows={3} />
            </div>
            {msg && <p className="mt-2 text-sm text-red-600">{msg}</p>}
            <div className="mt-3 flex justify-end gap-2">
              <button onClick={() => setOpen(null)} className="px-3 text-sm text-ink-muted">Cancel</button>
              <button onClick={save} disabled={busy} className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-60">
                {busy ? "Saving…" : open.marked_at ? "Update mark" : "Save mark"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
