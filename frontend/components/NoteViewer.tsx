"use client";
import { useState } from "react";
import { Download, FileText, ChevronDown, ChevronUp } from "lucide-react";
import { notesAPI } from "@/lib/api";
import { MathText } from "@/components/MathText";
import { formatDate } from "@/lib/utils";

/** One note card: text inline, attached file loaded on demand (it can be several MB). */
export default function NoteViewer({ note, footer }: { note: any; footer?: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const [file, setFile] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const toggle = async () => {
    const next = !open;
    setOpen(next);
    if (next && note.has_file && !file) {
      setLoading(true);
      try {
        setFile((await notesAPI.get(note.id)).data.file_data);
      } finally {
        setLoading(false);
      }
    }
  };

  const isPdf = file?.startsWith("data:application/pdf");
  return (
    <div className="card p-5">
      <button onClick={toggle} className="flex w-full items-start justify-between gap-3 text-left">
        <div>
          <div className="font-semibold text-ink">{note.title}</div>
          <div className="mt-0.5 text-xs text-ink-subtle">
            {[note.subject, formatDate(note.created_at), note.file_name].filter(Boolean).join(" · ")}
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
          {note.has_file && loading && <p className="text-sm text-ink-muted">Loading file…</p>}
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
          {!note.body && !note.has_file && <p className="flex items-center gap-1 text-sm text-ink-muted"><FileText size={14} /> Empty note</p>}
          {footer}
        </div>
      )}
    </div>
  );
}
