"use client";
import { useEffect, useState } from "react";
import { Mail, Download } from "lucide-react";

// "Mark it on paper or in a PDF app": email the student's work to the marker as one PDF, or download it.
// Used on worksheet hand-ins (HomeworkHandins) and written attempts (Marking page).
// The address is remembered on this device; the backend's default (the marker's own inbox) fills it first time.
const EMAIL_KEY = "nx-handin-email";

export default function EmailPdfBox({ defaultTo, note, filename, send, download }: {
  defaultTo?: string | null;
  note: string;
  filename: string;
  send: (to: string) => Promise<{ data: { sent_to: string } }>;
  download: () => Promise<{ data: unknown }>;
}) {
  const [to, setTo] = useState("");
  const [sending, setSending] = useState(false);
  const [downloading, setDownloading] = useState(false);
  const [sent, setSent] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    setTo((typeof window !== "undefined" && localStorage.getItem(EMAIL_KEY)) || defaultTo || "");
    setSent("");
    setError("");
  }, [defaultTo, filename]);

  const emailPdf = async () => {
    setSending(true);
    setSent("");
    setError("");
    try {
      const { data } = await send(to.trim());
      if (to.trim()) localStorage.setItem(EMAIL_KEY, to.trim());
      setSent(`Sent to ${data.sent_to}`);
    } catch (e: any) {
      setError(e?.response?.data?.detail || "Couldn't send the email.");
    } finally {
      setSending(false);
    }
  };

  const downloadPdf = async () => {
    setDownloading(true);
    setError("");
    try {
      const { data } = await download();
      const url = URL.createObjectURL(data as Blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${filename}.pdf`.replace(/[^\w\s().-]/g, "");
      a.click();
      setTimeout(() => URL.revokeObjectURL(url), 5000);
    } catch {
      setError("Couldn't make the PDF.");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="rounded-lg border border-brand-200 bg-brand-50/50 p-3">
      <div className="text-xs font-semibold text-ink">Mark it on paper or in a PDF app</div>
      <div className="mt-2 flex flex-wrap items-center gap-2">
        <input type="email" value={to} onChange={(e) => setTo(e.target.value)} placeholder="your@email.com"
          className="min-w-[200px] flex-1 rounded-lg border border-line bg-surface p-2 text-sm" />
        <button type="button" onClick={emailPdf} disabled={sending}
          className="inline-flex items-center gap-1.5 rounded-lg bg-brand-600 px-3 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-60">
          <Mail size={15} /> {sending ? "Sending…" : "Email PDF"}
        </button>
        <button type="button" onClick={downloadPdf} disabled={downloading}
          className="inline-flex items-center gap-1.5 rounded-lg border border-line bg-surface px-3 py-2 text-sm font-medium text-ink hover:bg-canvas disabled:opacity-60">
          <Download size={15} /> {downloading ? "Preparing…" : "Download PDF"}
        </button>
      </div>
      <p className="mt-1.5 text-xs text-ink-subtle">{note}</p>
      {sent && <p className="mt-1.5 text-xs font-semibold text-emerald-700">✓ {sent}</p>}
      {error && <p className="mt-1.5 text-xs font-semibold text-red-600">{error}</p>}
    </div>
  );
}
