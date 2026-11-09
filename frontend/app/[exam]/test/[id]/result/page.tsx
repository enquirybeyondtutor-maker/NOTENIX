"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import { useAuthGuard } from "@/lib/guard";
import { examAPI, type ExamInfo } from "@/lib/examApi";
import { PageContainer, Spinner } from "@/components/ui/Page";
import ExamReport from "@/components/exam/ExamReport";
import { formatDate } from "@/lib/utils";

export default function ExamResultPage() {
  const { ready } = useAuthGuard("student");
  const { exam, id } = useParams<{ exam: string; id: string }>();
  const [r, setR] = useState<any>(null);
  const [info, setInfo] = useState<ExamInfo | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!ready) return;
    examAPI.result(id).then((x) => { setR(x.data); return examAPI.info(x.data.exam); }).then((i) => setInfo(i.data))
      .catch((e) => setError(e.response?.data?.detail || "Couldn't load your score."));
  }, [ready, id]);

  if (error) return <div className="mx-auto max-w-lg p-10 text-center text-sm text-red-600">{error}</div>;
  if (!ready || !r || !info) return <Spinner label="Working out your score…" />;
  const diag = r.kind === "diagnostic";
  return (
    <PageContainer>
      <a href={`/${r.exam || exam}/practice`} className="mb-4 inline-flex items-center gap-1 text-sm font-medium text-brand-600 hover:text-brand-700"><ArrowLeft size={15} /> {info.name} practice</a>
      <h1 className="text-2xl font-bold text-ink">{r.title}</h1>
      <p className="mt-1 text-sm text-ink-muted">Finished {formatDate(r.attempt.completed_at)}</p>
      <div className="mt-6">
        <ExamReport info={info} r={r} target={r.target}
          note={diag ? `A short diagnostic gives a band, not an exact score. ${info.about_score}` : undefined} />
      </div>
    </PageContainer>
  );
}
