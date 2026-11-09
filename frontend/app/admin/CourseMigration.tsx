"use client";
import { useEffect, useState } from "react";
import { Layers } from "lucide-react";
import { coursesAPI, type Course } from "@/lib/coursesApi";
import CoursePicker from "@/components/CoursePicker";
import { Button } from "@/components/ui/Button";
import { formatDate } from "@/lib/utils";

type Suggestion = {
  user_id: number; full_name: string; email: string;
  access_kind: string | null; access_until: string | null;
  suggested: { course: string; name: string; tests: number }[];
};

/** Students who still open every course. Courses suggested from their tutors' tests are
 *  pre-ticked; the admin adjusts and applies. Each student keeps their current end date. */
export default function CourseMigration({ catalogue, onDone }: { catalogue: Course[]; onDone: () => void }) {
  const [rows, setRows] = useState<Suggestion[] | null>(null);
  const [picked, setPicked] = useState<Record<number, string[]>>({});
  const [open, setOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState("");

  const load = () =>
    coursesAPI.suggestions().then((r) => {
      setRows(r.data);
      setPicked(Object.fromEntries(r.data.map((s: Suggestion) => [s.user_id, s.suggested.map((x) => x.course)])));
    }).catch(() => setRows([]));
  useEffect(() => { load(); }, []);

  if (!rows || rows.length === 0) return null;
  const name = (k: string) => catalogue.find((c) => c.key === k)?.name || k;
  const toggle = (uid: number, k: string) =>
    setPicked((p) => ({ ...p, [uid]: p[uid]?.includes(k) ? p[uid].filter((x) => x !== k) : [...(p[uid] ?? []), k] }));
  const ready = rows.filter((r) => (picked[r.user_id] ?? []).length > 0);

  const apply = async () => {
    setSaving(true);
    setMsg("");
    try {
      const { data } = await coursesAPI.apply(ready.map((r) => ({ user_id: r.user_id, courses: picked[r.user_id] })));
      setMsg(`Done: ${data.added} course${data.added === 1 ? "" : "s"} added to ${ready.length} student${ready.length === 1 ? "" : "s"}.`);
      await load();
      onDone();
    } catch (e: any) {
      setMsg(e.response?.data?.detail || "Couldn't apply the courses.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="card mt-6 border-amber-200 p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="flex items-center gap-2 font-semibold text-ink"><Layers size={18} /> Move students onto courses</h2>
          <p className="mt-1 text-sm text-ink-muted">
            {rows.length} student{rows.length === 1 ? " can" : "s can"} still open every course. Pick each student&apos;s courses
            (ticked ones are suggested from the tests their tutors set). They keep their current end date.
          </p>
        </div>
        <Button size="sm" variant="secondary" onClick={() => setOpen(!open)}>{open ? "Hide" : "Review students"}</Button>
      </div>
      {open && (
        <>
          <div className="mt-4 divide-y divide-line rounded-lg border border-line">
            {rows.map((r) => {
              const mine = picked[r.user_id] ?? [];
              const options = [...new Set([...r.suggested.map((s) => s.course), ...mine])];
              return (
                <div key={r.user_id} className="flex flex-col gap-2 p-3 sm:flex-row sm:items-center sm:justify-between">
                  <div className="min-w-0">
                    <div className="text-sm font-medium text-ink">{r.full_name}</div>
                    <div className="text-xs text-ink-subtle">
                      {r.email} · {r.access_until ? `${r.access_kind === "trial" ? "Trial" : "Paid"} until ${formatDate(r.access_until)}` : "No end date"}
                    </div>
                  </div>
                  <div className="flex flex-wrap items-center gap-1.5">
                    {options.map((k) => {
                      const s = r.suggested.find((x) => x.course === k);
                      return (
                        <label key={k} className={`inline-flex cursor-pointer items-center gap-1 rounded-full border px-2.5 py-1 text-xs font-medium ${mine.includes(k) ? "border-brand-300 bg-brand-50 text-brand-700" : "border-line text-ink-muted"}`}>
                          <input type="checkbox" className="h-3 w-3" checked={mine.includes(k)} onChange={() => toggle(r.user_id, k)} />
                          {name(k)}{s ? ` (${s.tests} test${s.tests === 1 ? "" : "s"})` : ""}
                        </label>
                      );
                    })}
                    <CoursePicker catalogue={catalogue} value="" exclude={options} onChange={(k) => k && toggle(r.user_id, k)}
                      placeholder="+ Course…" className="rounded-md border border-line bg-white px-1.5 py-1 text-xs text-ink-muted" />
                  </div>
                </div>
              );
            })}
          </div>
          <div className="mt-4 flex flex-wrap items-center gap-3">
            <Button onClick={apply} loading={saving} disabled={ready.length === 0}>
              Apply courses to {ready.length} student{ready.length === 1 ? "" : "s"}
            </Button>
            <span className="text-xs text-ink-subtle">Students left with no course ticked keep access to everything.</span>
            {msg && <span className="text-sm text-ink">{msg}</span>}
          </div>
        </>
      )}
    </div>
  );
}
