"use client";
import { useEffect, useState } from "react";
import { BookOpen } from "lucide-react";
import { useAuthGuard } from "@/lib/guard";
import { useInbox, boardKind } from "@/lib/inbox";
import { PageContainer, PageHeader, Spinner, EmptyState } from "@/components/ui/Page";
import NoteViewer from "@/components/NoteViewer";
import AssignmentBoard from "@/components/AssignmentBoard";

// Every piece of homework in one place: worksheets/files from the tutor (hand in photos)
// and homework set as an online test. Files used to sit under Notes, where students missed them.
export default function HomeworkPage() {
  const { ready } = useAuthGuard("student");
  const inbox = useInbox(ready);
  const [hash, setHash] = useState("");
  useEffect(() => setHash(window.location.hash), []);

  if (!ready || !inbox) return <Spinner label="Loading your homework…" />;

  const files = inbox.notes.filter((n) => n.kind === "homework");
  const todo = files.filter((n) => !n.submission);
  const handedIn = files.filter((n) => n.submission);
  const hwTests = inbox.tests.filter((t) => boardKind(t) === "homework");

  return (
    <PageContainer>
      <PageHeader icon={BookOpen} title="My homework" subtitle="Everything your tutor has set you. Open a worksheet, do it on paper, then hand in photos or a PDF scan." />

      {files.length === 0 && hwTests.length === 0 ? (
        <EmptyState icon={BookOpen} title="No homework yet" desc="When your tutor sets homework, it'll appear here and on your dashboard." />
      ) : (
        <div className="space-y-8">
          {files.length > 0 && (
            <section className="space-y-3">
              <h2 className="text-sm font-semibold uppercase tracking-wide text-ink-subtle">To hand in · {todo.length}</h2>
              {todo.length === 0 ? (
                <div className="card p-6 text-sm text-ink-muted">You&apos;ve handed in all your worksheet homework.</div>
              ) : (
                todo.map((n) => <NoteViewer key={n.id} note={n} defaultOpen={hash === `#note-${n.id}`} />)
              )}
              {handedIn.length > 0 && (
                <>
                  <h2 className="pt-4 text-sm font-semibold uppercase tracking-wide text-ink-subtle">Handed in · {handedIn.length}</h2>
                  {handedIn.map((n) => <NoteViewer key={n.id} note={n} defaultOpen={hash === `#note-${n.id}`} />)}
                </>
              )}
            </section>
          )}
          <AssignmentBoard kind="homework" embedded />
        </div>
      )}
    </PageContainer>
  );
}
