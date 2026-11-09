"use client";
import { useEffect, useRef, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { GraduationCap, CalendarDays, Target, PlayCircle, RotateCcw, BarChart3 } from "lucide-react";
import { useAuthGuard } from "@/lib/guard";
import { examAPI, hasEngine, diagKey, fmt, type ExamInfo, type ExamPlan, type ExamSkill } from "@/lib/examApi";
import { StudyPlan } from "@/components/sat/StudyPlan";
import ExamSkillMap from "@/components/exam/ExamSkillMap";
import { PageContainer, PageHeader, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { formatDate } from "@/lib/utils";

// Practice home for an exam-engine exam (e.g. /tmua/practice): test date and target, the
// diagnostic, this week's plan, the practice tests and the skill map.
export default function ExamPractice() {
  const { exam } = useParams<{ exam: string }>();
  const { user, ready } = useAuthGuard("student");
  const router = useRouter();
  const [info, setInfo] = useState<ExamInfo | null>(null);
  const [h, setH] = useState<any>(null);
  const [error, setError] = useState("");
  const [goal, setGoal] = useState({ test_date: "", target: "" });
  const [busy, setBusy] = useState("");
  const [plan, setPlan] = useState<ExamPlan | null>(null);
  const [skills, setSkills] = useState<ExamSkill[]>([]);
  const savedDiag = useRef(false);

  const load = async () => {
    try {
      const [i, r] = await Promise.all([examAPI.info(exam), examAPI.home(exam)]);
      setInfo(i.data);
      // A diagnostic taken before signing in: keep it, once.
      if (!r.data.diagnostic && !savedDiag.current) {
        savedDiag.current = true;
        try {
          const saved = JSON.parse(localStorage.getItem(diagKey(exam)) || "null");
          if (saved?.result && saved.answers) {
            await examAPI.saveDiagnostic(exam, saved.answers);
            localStorage.removeItem(diagKey(exam));
            return load();
          }
        } catch { /* nothing saved */ }
      }
      setH(r.data);
      setGoal({ test_date: r.data.test_date || "", target: r.data.target ? String(r.data.target) : "" });
      examAPI.plan(exam).then((p) => setPlan(p.data)).catch(() => {});
      examAPI.skills(exam).then((s) => setSkills(s.data)).catch(() => {});
    } catch (e: any) {
      setError(e.response?.data?.detail || "Couldn't load practice.");
    }
  };
  useEffect(() => {
    if (!ready) return;
    if (!hasEngine(exam)) { setError("Practice tests aren't available for this exam yet."); return; }
    load();
  }, [ready, exam]); // eslint-disable-line react-hooks/exhaustive-deps

  if (error) {
    return (
      <PageContainer>
        <div className="card mx-auto max-w-lg p-8 text-center">
          <p className="text-sm text-ink">{error}</p>
          <Button href="/courses" className="mt-5">My courses</Button>
        </div>
      </PageContainer>
    );
  }
  if (!ready || !h || !info) return <Spinner label="Loading practice…" />;

  const start = async (slug: string) => {
    setBusy(slug);
    try {
      const { data } = await examAPI.start(exam, slug);
      router.push(`/${exam}/test/${data.attempt_id}`);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Couldn't start the test.");
      setBusy("");
    }
  };
  const saveGoal = async () => {
    await examAPI.setGoal(exam, { test_date: goal.test_date || null, target: goal.target ? Number(goal.target) : null });
    load();
  };
  const days = h.test_date ? Math.ceil((new Date(h.test_date).getTime() - Date.now()) / 86400000) : null;
  const changed = goal.test_date !== (h.test_date || "") || goal.target !== (h.target ? String(h.target) : "");

  return (
    <PageContainer>
      <PageHeader icon={GraduationCap} title={`${info.name} practice${user?.full_name ? `, ${user.full_name.split(" ")[0]}` : ""}`}
        subtitle={`Full ${info.name} practice tests with the real timings, a score estimate out of ${info.scale.max.toFixed(1)}, your skill map and a plan to test day.`} />

      <div className="grid gap-4 lg:grid-cols-3">
        <div className="card p-5">
          <div className="flex items-center gap-2 text-sm font-semibold text-ink"><CalendarDays size={16} className="text-brand-600" /> Your {info.name} date</div>
          <div className="mt-2 text-2xl font-bold text-ink">{days !== null ? (days > 0 ? `${days} days to go` : "Test day has passed") : "Not set"}</div>
          <input type="date" value={goal.test_date} onChange={(e) => setGoal({ ...goal, test_date: e.target.value })}
            className="mt-3 w-full rounded-lg border border-line px-3 py-2 text-sm" />
        </div>
        <div className="card p-5">
          <div className="flex items-center gap-2 text-sm font-semibold text-ink"><Target size={16} className="text-brand-600" /> Target score</div>
          <div className="mt-2 text-2xl font-bold text-ink">{h.target ? fmt(h.target, info) : "Not set"}</div>
          <input type="number" min={info.scale.min} max={info.scale.max} step={0.1} value={goal.target} onChange={(e) => setGoal({ ...goal, target: e.target.value })}
            placeholder="e.g. 6.5" className="mt-3 w-full rounded-lg border border-line px-3 py-2 text-sm" />
        </div>
        <div className="card flex flex-col p-5">
          <div className="flex items-center gap-2 text-sm font-semibold text-ink"><BarChart3 size={16} className="text-brand-600" /> Diagnostic</div>
          {h.diagnostic ? (
            <>
              <div className="mt-2 text-2xl font-bold text-ink">≈ {fmt(h.diagnostic.total_score, info)}</div>
              <div className="text-xs text-ink-subtle">From your diagnostic, {formatDate(h.diagnostic.completed_at)}</div>
              <Button href={`/${exam}/test/${h.diagnostic.id}/result`} size="sm" variant="secondary" className="mt-auto">See the report</Button>
            </>
          ) : h.has_diagnostic ? (
            <>
              <p className="mt-2 text-sm text-ink-muted">A short timed check across both papers. Start here.</p>
              <Button size="sm" variant="secondary" className="mt-auto" loading={busy === "diagnostic"} onClick={() => start("diagnostic")}>Take the diagnostic</Button>
            </>
          ) : <p className="mt-2 text-sm text-ink-muted">Coming soon.</p>}
        </div>
      </div>
      {changed && <Button size="sm" className="mt-3" onClick={saveGoal}>Save date and target</Button>}

      {plan && <div className="mt-8"><StudyPlan plan={plan as any} /></div>}

      <h2 id="tests" className="mb-3 mt-10 scroll-mt-24 text-sm font-semibold uppercase tracking-wide text-ink-subtle">Full-length practice tests</h2>
      {h.forms.length === 0 ? <p className="text-sm text-ink-muted">Practice tests are on their way.</p> : (
        <div className="grid gap-4 sm:grid-cols-2">
          {h.forms.map((f: any) => {
            const open = f.attempts.find((a: any) => a.status === "in_progress");
            const done = f.attempts.filter((a: any) => a.status === "done");
            const best = done.reduce((m: number, a: any) => Math.max(m, a.total_score || 0), 0);
            return (
              <div key={f.slug} className="card flex flex-col p-5">
                <h3 className="font-semibold text-ink">{f.title}</h3>
                <p className="mt-1 text-sm text-ink-muted">{f.summary || info.mock_detail}</p>
                {done.length > 0 && <p className="mt-2 text-sm text-ink">Best score: <b>{fmt(best, info)}</b> · taken {done.length}×</p>}
                <div className="mt-4 flex flex-wrap gap-2">
                  {open ? (
                    <Button size="sm" onClick={() => router.push(`/${exam}/test/${open.id}`)}><RotateCcw size={14} /> Resume</Button>
                  ) : (
                    <Button size="sm" loading={busy === f.slug} onClick={() => start(f.slug)}><PlayCircle size={14} /> {done.length ? "Take again" : "Start"}</Button>
                  )}
                  {done[0] && <Button size="sm" variant="secondary" href={`/${exam}/test/${done[0].id}/result`}>Latest score report</Button>}
                </div>
              </div>
            );
          })}
        </div>
      )}
      {skills.length > 0 && <div className="mt-10"><ExamSkillMap info={info} skills={skills} /></div>}
    </PageContainer>
  );
}
