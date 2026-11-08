"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { NotebookText, BookOpen, ArrowRight } from "lucide-react";
import { notesAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, Spinner, EmptyState } from "@/components/ui/Page";
import NoteViewer from "@/components/NoteViewer";

// Class notes only. Homework files live on /homework (students couldn't find them here).
export default function NotesPage() {
  const { ready } = useAuthGuard("student");
  const [notes, setNotes] = useState<any[] | null>(null);
  const [hash, setHash] = useState("");
  useEffect(() => setHash(window.location.hash), []);

  useEffect(() => {
    if (ready) notesAPI.mine().then((r) => setNotes(r.data)).catch(() => setNotes([]));
  }, [ready]);

  if (!ready || notes === null) return <Spinner label="Loading notes…" />;
  const classNotes = notes.filter((n) => n.kind !== "homework");
  const homeworkTodo = notes.filter((n) => n.kind === "homework" && !n.submission).length;
  return (
    <PageContainer>
      <PageHeader icon={NotebookText} title="Class notes" subtitle="Notes from your lessons, newest first." />
      {homeworkTodo > 0 && (
        <Link href="/homework" className="card mb-4 flex items-center justify-between gap-3 border-amber-200 bg-amber-50/60 p-4 hover:bg-amber-50">
          <span className="flex items-center gap-3 text-sm text-ink">
            <BookOpen size={18} className="shrink-0 text-amber-600" />
            You have {homeworkTodo} homework {homeworkTodo === 1 ? "worksheet" : "worksheets"} to hand in. Homework is now on the Homework page.
          </span>
          <ArrowRight size={16} className="shrink-0 text-amber-700" />
        </Link>
      )}
      {classNotes.length === 0 ? (
        <EmptyState icon={NotebookText} title="No notes yet" desc="When your tutor shares class notes, they will appear here." />
      ) : (
        <div className="space-y-3">{classNotes.map((n) => <NoteViewer key={n.id} note={n} defaultOpen={hash === `#note-${n.id}`} />)}</div>
      )}
    </PageContainer>
  );
}
