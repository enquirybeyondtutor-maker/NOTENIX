"use client";
import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { Inbox, Check, X, Send, Wallet, CheckSquare } from "lucide-react";
import { authAPI, requestsAPI, paymentsAPI } from "@/lib/api";
import { PageContainer, PageHeader, Spinner, EmptyState } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Input, Select, Field } from "@/components/ui/Input";
import { formatDate, relativeTime, cn } from "@/lib/utils";

const STATUS_LABEL: Record<string, string> = {
  awaiting_payment: "Awaiting payment", payment_claimed: "Payment to check", open: "Needs a test",
  assigned: "Assigned", submitted: "Needs marking", marked: "Marked", cancelled: "Cancelled",
};

function AssignBox({ req, tests, onDone }: { req: any; tests: any[]; onDone: () => void }) {
  // Suggest tests for the same exam first.
  const sorted = useMemo(() => {
    const exam = (req.exam || "").toLowerCase();
    const hit = (t: any) => `${t.level} ${t.title} ${t.subject}`.toLowerCase().includes(exam);
    return [...tests].sort((a, b) => Number(hit(b)) - Number(hit(a)));
  }, [tests, req.exam]);
  const [testId, setTestId] = useState<string>(sorted[0]?.id ? String(sorted[0].id) : "");
  const [due, setDue] = useState("");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const assign = async () => {
    if (!testId) return;
    setBusy(true); setError("");
    try {
      await requestsAPI.assign(req.id, { test_id: Number(testId), due_at: due ? new Date(due).toISOString() : null, note });
      onDone();
    } catch (err: any) {
      setError(err.response?.data?.detail || "Couldn't assign.");
      setBusy(false);
    }
  };

  return (
    <div className="mt-4 grid gap-3 rounded-lg border border-line bg-slate-50 p-4 sm:grid-cols-[2fr_1fr]">
      <Field label="Test to send">
        <Select value={testId} onChange={(e) => setTestId(e.target.value)}>
          {sorted.map((t) => (
            <option key={t.id} value={t.id}>
              #{t.id} {t.title} · {t.level} · {t.num_questions}Q{t.duration_minutes ? ` · ${t.duration_minutes}m` : ""}{t.mode === "written" ? " · written" : ""}
            </option>
          ))}
        </Select>
      </Field>
      <Field label="Due (optional)">
        <Input type="date" value={due} onChange={(e) => setDue(e.target.value)} />
      </Field>
      <div className="sm:col-span-2">
        <Field label="Note to student (optional)">
          <Input value={note} onChange={(e) => setNote(e.target.value)} placeholder="e.g. Sit this under timed conditions in one go." />
        </Field>
      </div>
      {error && <p className="text-sm text-red-600 sm:col-span-2">{error}</p>}
      <div className="sm:col-span-2">
        <Button size="sm" onClick={assign} loading={busy} disabled={!testId}><Send size={14} /> Send test to student</Button>
        <span className="ml-3 text-xs text-ink-subtle">Need a new test? Create it in Teacher → Create, then come back.</span>
      </div>
    </div>
  );
}

export default function AdminRequestsPage() {
  const router = useRouter();
  const [ready, setReady] = useState(false);
  const [rows, setRows] = useState<any[] | null>(null);
  const [tests, setTests] = useState<any[]>([]);
  const [proPayments, setProPayments] = useState<any[]>([]);
  const [tab, setTab] = useState<"action" | "all">("action");
  const [busy, setBusy] = useState<string | null>(null);

  const load = () => {
    requestsAPI.adminList().then((r) => setRows(r.data)).catch(() => setRows([]));
    requestsAPI.adminTests().then((r) => setTests(r.data)).catch(() => {});
    paymentsAPI.adminList("claimed").then((r) => setProPayments(r.data.filter((p: any) => p.purpose === "pro"))).catch(() => {});
  };

  useEffect(() => {
    if (!localStorage.getItem("notenix_token")) { router.replace("/login"); return; }
    authAPI.me()
      .then(({ data }) => {
        if (!data.is_admin) { router.replace(data.role === "teacher" ? "/teacher" : "/dashboard"); return; }
        setReady(true);
        load();
      })
      .catch(() => router.replace("/login"));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const act = async (key: string, fn: () => Promise<any>) => {
    setBusy(key);
    try { await fn(); } catch (err: any) { alert(err.response?.data?.detail || "Something went wrong."); }
    setBusy(null);
    load();
  };

  if (!ready || rows === null) return <Spinner label="Loading requests…" />;

  const stage = (r: any) => (r.status === "assigned" && r.progress ? r.progress : r.status);
  const needsAction = (r: any) => ["payment_claimed", "open", "submitted"].includes(stage(r));
  const visible = tab === "action" ? rows.filter(needsAction) : rows;

  return (
    <PageContainer>
      <PageHeader
        title="Test requests"
        subtitle="Confirm payments, send tests, and mark finished attempts."
        icon={Inbox}
        actions={<Button href="/marking" size="sm" variant="secondary"><CheckSquare size={14} /> Marking queue</Button>}
      />

      {proPayments.length > 0 && (
        <div className="card mb-6 p-5">
          <h2 className="flex items-center gap-2 font-semibold text-ink"><Wallet size={16} /> Pro payments to check</h2>
          <div className="mt-3 divide-y divide-line">
            {proPayments.map((p) => (
              <div key={p.id} className="flex flex-wrap items-center justify-between gap-3 py-3 text-sm">
                <div>
                  <b>{p.user?.full_name}</b> <span className="text-ink-subtle">{p.user?.email}</span>
                  <div className="text-ink-muted">
                    {p.currency} {p.amount} · ref <span className="font-mono">{p.reference}</span> · via {p.paid_via || "?"} · payer {p.payer_name || "?"}
                    {p.payer_note ? ` · "${p.payer_note}"` : ""} · {relativeTime(p.created_at)}
                  </div>
                </div>
                <div className="flex gap-2">
                  <Button size="sm" loading={busy === `p${p.id}`} onClick={() => act(`p${p.id}`, () => paymentsAPI.review(p.id, true))}><Check size={14} /> Received</Button>
                  <Button size="sm" variant="ghost" onClick={() => act(`p${p.id}`, () => paymentsAPI.review(p.id, false))}><X size={14} /> Not found</Button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="mb-4 flex gap-2">
        {(["action", "all"] as const).map((t) => (
          <button key={t} onClick={() => setTab(t)}
            className={cn("rounded-lg px-3 py-1.5 text-sm font-medium", tab === t ? "bg-brand-600 text-white" : "bg-white text-ink-muted ring-1 ring-line")}>
            {t === "action" ? `Needs action (${rows.filter(needsAction).length})` : `All (${rows.length})`}
          </button>
        ))}
      </div>

      {!visible.length ? (
        <EmptyState icon={Inbox} title={tab === "action" ? "Nothing to do" : "No requests yet"} desc="New requests show up here and are emailed to ADMIN_EMAILS." />
      ) : (
        <div className="space-y-4">
          {visible.map((r) => {
            const s = stage(r);
            return (
              <div key={r.id} className="card p-5">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <h3 className="font-semibold text-ink">#{r.id} · {r.exam}{r.subject ? ` · ${r.subject}` : ""}</h3>
                      <span className={needsAction(r) ? "badge-warning" : "badge-neutral"}>{STATUS_LABEL[s] || s}</span>
                      {r.price > 0 && <span className="badge-neutral">{r.currency} {r.price}</span>}
                    </div>
                    <p className="mt-1 text-sm text-ink-muted">
                      {r.student?.full_name} · <a href={`mailto:${r.student?.email}`} className="text-brand-600">{r.student?.email}</a>
                      {" · "}{formatDate(r.created_at)}{r.preferred_date ? ` · wants it by ${formatDate(r.preferred_date)}` : ""}
                    </p>
                    {r.details && <p className="mt-2 text-sm text-ink">{r.details}</p>}
                    {r.test && <p className="mt-2 text-sm text-ink-muted">Sent: <b>{r.test.title}</b>{r.score != null ? ` · scored ${r.score}%${r.grade ? ` (${r.grade})` : ""}` : ""}</p>}
                    {r.payment && (
                      <p className="mt-2 text-sm text-ink-muted">
                        Payment {r.payment.status}: {r.payment.currency} {r.payment.amount} · ref <span className="font-mono">{r.reference}</span> · via {r.payment.paid_via || "?"} · payer {r.payment.payer_name || "?"}
                        {r.payment.payer_note ? ` · "${r.payment.payer_note}"` : ""}
                      </p>
                    )}
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {s === "payment_claimed" && r.payment && (
                      <>
                        <Button size="sm" loading={busy === `r${r.id}`} onClick={() => act(`r${r.id}`, () => paymentsAPI.review(r.payment.id, true))}><Check size={14} /> Payment received</Button>
                        <Button size="sm" variant="ghost" onClick={() => act(`r${r.id}`, () => paymentsAPI.review(r.payment.id, false))}><X size={14} /> Not found</Button>
                      </>
                    )}
                    {s === "awaiting_payment" && (
                      <Button size="sm" variant="secondary" onClick={() => act(`r${r.id}`, () => requestsAPI.update(r.id, { status: "open" }))}>Make free</Button>
                    )}
                    {s === "submitted" && <Button size="sm" href="/marking">Mark it</Button>}
                    {["awaiting_payment", "payment_claimed", "open"].includes(s) && (
                      <Button size="sm" variant="ghost" onClick={() => { if (confirm("Cancel this request? The student is emailed.")) act(`r${r.id}`, () => requestsAPI.update(r.id, { status: "cancelled" })); }}>Cancel</Button>
                    )}
                  </div>
                </div>
                {s === "open" && (tests.length ? <AssignBox req={r} tests={tests} onDone={load} /> : <p className="mt-3 text-sm text-ink-muted">No tests yet. Create one first.</p>)}
              </div>
            );
          })}
        </div>
      )}
    </PageContainer>
  );
}
