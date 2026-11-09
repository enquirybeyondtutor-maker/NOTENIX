"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { GraduationCap, CalendarDays, Target, PlayCircle, RotateCcw, BarChart3, Sparkles } from "lucide-react";
import { useAuthGuard } from "@/lib/guard";
import { satAPI, type SkillStatus, type StudyPlan as Plan } from "@/lib/satApi";
import { StudyPlan, SkillMap } from "@/components/sat/StudyPlan";
import { PageContainer, PageHeader, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { formatDate } from "@/lib/utils";

// SAT home for a signed-in student: test date + target, the diagnostic, the practice tests.
export default function SatPractice() {
  const { user, ready } = useAuthGuard("student");
  const router = useRouter();
  const [h, setH] = useState<any>(null);
  const [error, setError] = useState("");
  const [goal, setGoal] = useState({ test_date: "", target: "" });
  const [busy, setBusy] = useState("");
  const [plan, setPlan] = useState<Plan | null>(null);
  const [skills, setSkills] = useState<SkillStatus[]>([]);

  const load = () => satAPI.home().then((r) => {
    setH(r.data);
    setGoal({ test_date: r.data.test_date || "", target: r.data.target ? String(r.data.target) : "" });
    satAPI.plan().then((p) => setPlan(p.data)).catch(() => {});
    satAPI.skills().then((s) => setSkills(s.data)).catch(() => {});
  }).catch((e) => setError(e.response?.data?.detail || "Couldn't load SAT practice."));
  useEffect(() => { if (ready) load(); }, [ready]);

  if (error) {
    return (
      <PageContainer>
        <div className="card mx-auto max-w-lg p-8 text-center">
          <p className="text-sm text-ink">{error}</p>
          <Button href="/courses?add=sat" className="mt-5">Add Notenix SAT</Button>
        </div>
      </PageContainer>
    );
  }
  if (!ready || !h) return <Spinner label="Loading SAT practice…" />;

  const start = async (slug: string) => {
    setBusy(slug);
    try {
      const { data } = await satAPI.start(slug);
      router.push(`/sat/test/${data.attempt_id}`);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Couldn't start the test.");
      setBusy("");
    }
  };
  const saveGoal = async () => {
    await satAPI.setGoal({ test_date: goal.test_date || null, target: goal.target ? Number(goal.target) : null });
    load();
  };
  const days = h.test_date ? Math.ceil((new Date(h.test_date).getTime() - Date.now()) / 86400000) : null;
  const trial = h.course?.kind === "trial";

  return (
    <PageContainer>
      <PageHeader icon={GraduationCap} title={`SAT practice${user?.full_name ? `, ${user.full_name.split(" ")[0]}` : ""}`}
        subtitle="Full Digital SAT practice tests with the real module timings, adaptive Module 2, Desmos and a score out of 1600." />

      {trial && (
        <div className="mb-6 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-brand-200 bg-brand-50 p-4 text-sm">
          <span className="flex items-center gap-2 text-ink"><Sparkles size={16} className="text-brand-600" />
            Free week{h.course.until ? ` until ${formatDate(h.course.until)}` : ""}. Keep going until your SAT for {h.price.label}.</span>
          <Button href="/courses?add=sat" size="sm">Keep going to test day</Button>
        </div>
      )}

      <div className="grid gap-4 lg:grid-cols-3">
        <div className="card p-5">
          <div className="flex items-center gap-2 text-sm font-semibold text-ink"><CalendarDays size={16} className="text-brand-600" /> Your SAT date</div>
          <div className="mt-2 text-2xl font-bold text-ink">{days !== null ? (days > 0 ? `${days} days to go` : "Test day has passed") : "Not set"}</div>
          <input type="date" value={goal.test_date} onChange={(e) => setGoal({ ...goal, test_date: e.target.value })}
            className="mt-3 w-full rounded-lg border border-line px-3 py-2 text-sm" />
        </div>
        <div className="card p-5">
          <div className="flex items-center gap-2 text-sm font-semibold text-ink"><Target size={16} className="text-brand-600" /> Target score</div>
          <div className="mt-2 text-2xl font-bold text-ink">{h.target ?? "Not set"}</div>
          <input type="number" min={400} max={1600} step={10} value={goal.target} onChange={(e) => setGoal({ ...goal, target: e.target.value })}
            placeholder="e.g. 1400" className="mt-3 w-full rounded-lg border border-line px-3 py-2 text-sm" />
        </div>
        <div className="card flex flex-col p-5">
          <div className="flex items-center gap-2 text-sm font-semibold text-ink"><BarChart3 size={16} className="text-brand-600" /> Diagnostic</div>
          {h.diagnostic ? (
            <>
              <div className="mt-2 text-2xl font-bold text-ink">≈ {h.diagnostic.total_score}</div>
              <div className="text-xs text-ink-subtle">From your free diagnostic, {formatDate(h.diagnostic.completed_at)}</div>
              <Button href={`/sat/test/${h.diagnostic.id}/result`} size="sm" variant="secondary" className="mt-auto">See the report</Button>
            </>
          ) : (
            <>
              <p className="mt-2 text-sm text-ink-muted">A 34-minute check across every skill area.</p>
              <Button href="/sat/diagnostic" size="sm" variant="secondary" className="mt-auto">Take the diagnostic</Button>
            </>
          )}
        </div>
      </div>
      {(goal.test_date !== (h.test_date || "") || goal.target !== (h.target ? String(h.target) : "")) && (
        <Button size="sm" className="mt-3" onClick={saveGoal}>Save date and target</Button>
      )}

      {plan && <div className="mt-8"><StudyPlan plan={plan} /></div>}

      <h2 id="tests" className="mb-3 mt-10 scroll-mt-24 text-sm font-semibold uppercase tracking-wide text-ink-subtle">Full-length practice tests</h2>
      <div className="grid gap-4 sm:grid-cols-2">
        {h.forms.map((f: any) => {
          const open = f.attempts.find((a: any) => a.status === "in_progress");
          const done = f.attempts.filter((a: any) => a.status === "done");
          const best = done.reduce((m: number, a: any) => Math.max(m, a.total_score || 0), 0);
          return (
            <div key={f.slug} className="card flex flex-col p-5">
              <h3 className="font-semibold text-ink">{f.title}</h3>
              <p className="mt-1 text-sm text-ink-muted">{f.summary || "98 questions · 2 h 14 min · adaptive Module 2"}</p>
              {done.length > 0 && <p className="mt-2 text-sm text-ink">Best score: <b>{best}</b> · taken {done.length}×</p>}
              <div className="mt-4 flex flex-wrap gap-2">
                {open ? (
                  <Button size="sm" onClick={() => router.push(`/sat/test/${open.id}`)}><RotateCcw size={14} /> Resume</Button>
                ) : (
                  <Button size="sm" loading={busy === f.slug} onClick={() => start(f.slug)}><PlayCircle size={14} /> {done.length ? "Take again" : "Start"}</Button>
                )}
                {done[0] && <Button size="sm" variant="secondary" href={`/sat/test/${done[0].id}/result`}>Latest score report</Button>}
              </div>
            </div>
          );
        })}
      </div>
      {skills.length > 0 && <div className="mt-10"><SkillMap skills={skills} /></div>}
    </PageContainer>
  );
}
