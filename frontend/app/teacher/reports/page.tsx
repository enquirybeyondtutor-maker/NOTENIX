"use client";
import { useEffect, useMemo, useState } from "react";
import { FileBarChart, Download, RefreshCw, Sparkles } from "lucide-react";
import { reportsAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, EmptyState, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Input, Select, Field } from "@/components/ui/Input";
import ReportView from "@/components/report/ReportView";

interface Attempt { attempt_id: number; title: string; score: number; date: string | null }
interface Candidate { id: number; full_name: string; email: string; exams: { exam: string; attempts: Attempt[] }[] }

export default function ReportsPage() {
  const { ready } = useAuthGuard("teacher");
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [loading, setLoading] = useState(true);
  const [studentId, setStudentId] = useState<number | null>(null);
  const [exam, setExam] = useState("");
  const [picked, setPicked] = useState<number[]>([]);
  const [target, setTarget] = useState("");
  const [pronouns, setPronouns] = useState("");
  const [adminCopy, setAdminCopy] = useState(false);
  const [building, setBuilding] = useState(false);
  const [error, setError] = useState("");
  const [report, setReport] = useState<any | null>(null);

  useEffect(() => {
    if (!ready) return;
    reportsAPI.candidates()
      .then(({ data }) => setCandidates(data))
      .catch(() => setCandidates([]))
      .finally(() => setLoading(false));
  }, [ready]);

  const student = candidates.find((c) => c.id === studentId);
  const attempts = useMemo(() => student?.exams.find((e) => e.exam === exam)?.attempts || [], [student, exam]);

  const chooseStudent = (id: number) => {
    const s = candidates.find((c) => c.id === id);
    const ex = s?.exams[0]?.exam || "";
    setStudentId(id);
    setExam(ex);
    setPicked((s?.exams[0]?.attempts || []).map((a) => a.attempt_id));
    setReport(null);
  };
  const chooseExam = (ex: string) => {
    setExam(ex);
    setPicked((student?.exams.find((e) => e.exam === ex)?.attempts || []).map((a) => a.attempt_id));
    setReport(null);
  };

  const build = async () => {
    if (!studentId || !exam || !picked.length) return;
    setBuilding(true);
    setError("");
    try {
      const { data: started } = await reportsAPI.startBuild({ student_id: studentId, exam, attempt_ids: picked, target, pronouns });
      const deadline = Date.now() + 4 * 60 * 1000;
      while (Date.now() < deadline) {
        await new Promise((r) => setTimeout(r, 2500));
        const { data } = await reportsAPI.job(started.job_id);
        if (data.status === "done") { setReport(data.report); return; }
        if (data.status === "error") { setError(data.error || "Could not build the report."); return; }
      }
      setError("This is taking longer than expected. Please try again.");
    } catch (e: any) {
      setError(e?.response?.data?.detail || "Could not build the report. Please try again.");
    } finally {
      setBuilding(false);
    }
  };

  const download = () => {
    if (!report) return;
    const prev = document.title;
    // Browsers use the page title as the suggested PDF filename.
    document.title = `${report.student.name} - ${report.exam} Performance Analysis - ${new Date().toISOString().slice(0, 10)}`;
    window.print();
    setTimeout(() => { document.title = prev; }, 500);
  };

  if (!ready || loading) return <Spinner label="Loading students…" />;

  return (
    <div>
      <div className="print:hidden">
        <PageContainer className="pb-4">
          <PageHeader icon={FileBarChart} title="Performance reports"
            subtitle="Branded ESAT / TMUA analysis for one student, ready to download as PDF and send to their parents." />

          {candidates.length === 0 ? (
            <EmptyState icon={FileBarChart} title="No graded mocks yet"
              desc="Once students complete multiple-choice tests, you can build their performance report here." />
          ) : (
            <div className="card grid gap-5 p-5 lg:grid-cols-[1fr_1fr]">
              <div className="space-y-4">
                <Field label="Student">
                  <Select value={studentId ?? ""} onChange={(e) => chooseStudent(Number(e.target.value))}>
                    <option value="" disabled>Choose a student…</option>
                    {candidates.map((c) => (
                      <option key={c.id} value={c.id}>{c.full_name} — {c.exams.map((e) => `${e.exam} (${e.attempts.length})`).join(", ")}</option>
                    ))}
                  </Select>
                </Field>
                {student && (
                  <Field label="Exam">
                    <Select value={exam} onChange={(e) => chooseExam(e.target.value)}>
                      {student.exams.map((e) => <option key={e.exam} value={e.exam}>{e.exam}</option>)}
                    </Select>
                  </Field>
                )}
                <Field label="Target universities / course (optional)" hint="Used to frame where they stand, e.g. “Cambridge Engineering, Imperial EEE”.">
                  <Input value={target} onChange={(e) => setTarget(e.target.value)} placeholder="e.g. Warwick Maths, LSE Economics" />
                </Field>
                <Field label="Refer to the student as" hint="The report uses their first name; pick pronouns only if you know them.">
                  <Select value={pronouns} onChange={(e) => setPronouns(e.target.value)}>
                    <option value="">First name only</option>
                    <option value="he">he / him</option>
                    <option value="she">she / her</option>
                    <option value="they">they / them</option>
                  </Select>
                </Field>
              </div>

              <div className="space-y-4">
                <Field label="Mocks to include">
                  <div className="max-h-56 space-y-1 overflow-y-auto rounded-lg border border-line p-2">
                    {!student && <p className="px-1 py-2 text-sm text-ink-subtle">Choose a student first.</p>}
                    {attempts.map((a) => (
                      <label key={a.attempt_id} className="flex cursor-pointer items-center gap-2.5 rounded-md px-2 py-1.5 text-sm hover:bg-slate-50">
                        <input type="checkbox" className="h-4 w-4 accent-indigo-600" checked={picked.includes(a.attempt_id)}
                          onChange={(e) => setPicked((p) => e.target.checked ? [...p, a.attempt_id] : p.filter((x) => x !== a.attempt_id))} />
                        <span className="flex-1 truncate text-ink">{a.title}</span>
                        <span className="text-xs text-ink-subtle">{a.date ? new Date(a.date).toLocaleDateString("en-GB", { day: "numeric", month: "short" }) : ""}</span>
                        <span className="w-12 text-right font-semibold text-brand-600">{Math.round(a.score)}%</span>
                      </label>
                    ))}
                  </div>
                </Field>
                <label className="flex items-center gap-2 text-sm text-ink">
                  <input type="checkbox" className="h-4 w-4 accent-indigo-600" checked={adminCopy} onChange={(e) => setAdminCopy(e.target.checked)} />
                  Include integrity signals (admin copy — don’t send to parents)
                </label>
                <div className="flex flex-wrap gap-2">
                  <Button onClick={build} disabled={!studentId || !picked.length || building}>
                    {building ? <><RefreshCw size={16} className="animate-spin" /> Analysing…</> : report ? <><RefreshCw size={16} /> Rebuild</> : <><Sparkles size={16} /> Build report</>}
                  </Button>
                  {report && <Button variant="secondary" onClick={download}><Download size={16} /> Download PDF</Button>}
                </div>
                {building && <p className="text-xs text-ink-subtle">Tagging topics and writing the commentary — this takes about 20–40 seconds.</p>}
                {error && <p className="text-sm text-red-600">{error}</p>}
                {report && <p className="text-xs text-ink-subtle">In the print dialog choose <b>Save as PDF</b>, paper A4, and keep “Background graphics” on.</p>}
              </div>
            </div>
          )}
        </PageContainer>
      </div>

      {report && (
        <div className="bg-slate-100 py-8 print:bg-white print:py-0">
          <ReportView report={report} adminCopy={adminCopy} />
        </div>
      )}
    </div>
  );
}
