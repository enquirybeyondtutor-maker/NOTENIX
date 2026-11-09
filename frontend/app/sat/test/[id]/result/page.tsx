"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { ArrowLeft } from "lucide-react";
import { useAuthGuard } from "@/lib/guard";
import { satAPI } from "@/lib/satApi";
import { PageContainer, Spinner } from "@/components/ui/Page";
import Report from "@/components/sat/Report";
import { formatDate } from "@/lib/utils";

export default function SatResultPage() {
  const { ready } = useAuthGuard("student");
  const { id } = useParams<{ id: string }>();
  const [r, setR] = useState<any>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (ready) satAPI.result(id).then((x) => setR(x.data)).catch((e) => setError(e.response?.data?.detail || "Couldn't load your score."));
  }, [ready, id]);

  if (error) return <div className="mx-auto max-w-lg p-10 text-center text-sm text-red-600">{error}</div>;
  if (!ready || !r) return <Spinner label="Working out your score…" />;

  const a = r.attempt;
  const count = (sec: string) => {
    const qs = r.modules.filter((m: any) => m.section === sec).flatMap((m: any) => m.questions);
    return { right: qs.filter((q: any) => q.correct).length, total: qs.length };
  };
  const hard = (s: "rw" | "m") => r.route?.[s] === "h";
  return (
    <PageContainer>
      <a href="/sat/practice" className="mb-4 inline-flex items-center gap-1 text-sm font-medium text-brand-600 hover:text-brand-700"><ArrowLeft size={15} /> SAT practice</a>
      <h1 className="text-2xl font-bold text-ink">{r.title}</h1>
      <p className="mt-1 text-sm text-ink-muted">Finished {formatDate(a.completed_at)}</p>
      <div className="mt-6">
        <Report
          total={a.total_score}
          rw={{ score: a.rw_score, ...count("rw") }}
          math={{ score: a.math_score, ...count("math") }}
          target={r.target}
          skills={r.skills}
          weakest={r.weakest}
          modules={r.modules}
          note={r.kind === "mock" ? (
            <>Module 2: {hard("rw") ? "harder" : "easier"} in Reading and Writing, {hard("m") ? "harder" : "easier"} in Math.
              {" "}Scores are Notenix estimates on the official 400–1600 scale; the real SAT uses the College Board&apos;s own scoring.</>
          ) : "Diagnostic scores are bands: a short test can only narrow your score down so far."}
        />
      </div>
    </PageContainer>
  );
}
