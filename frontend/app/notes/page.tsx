"use client";
import { useEffect, useState } from "react";
import { NotebookText } from "lucide-react";
import { notesAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, Spinner, EmptyState } from "@/components/ui/Page";
import NoteViewer from "@/components/NoteViewer";

export default function NotesPage() {
  const { ready } = useAuthGuard("student");
  const [notes, setNotes] = useState<any[] | null>(null);

  useEffect(() => {
    if (ready) notesAPI.mine().then((r) => setNotes(r.data)).catch(() => setNotes([]));
  }, [ready]);

  if (!ready || notes === null) return <Spinner label="Loading notes…" />;
  return (
    <PageContainer>
      <PageHeader icon={NotebookText} title="Class notes" subtitle="Notes your tutor has shared with you." />
      {notes.length === 0 ? (
        <EmptyState icon={NotebookText} title="No notes yet" desc="When your tutor shares class notes, they will appear here." />
      ) : (
        <div className="space-y-3">{notes.map((n) => <NoteViewer key={n.id} note={n} />)}</div>
      )}
    </PageContainer>
  );
}
