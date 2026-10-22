"use client";
import { useCallback, useEffect, useState } from "react";
import { Inbox, Plus, ArrowRight, CheckCircle2 } from "lucide-react";
import { requestsAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, EmptyState, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import PaymentBox from "@/components/PaymentBox";
import { formatDate } from "@/lib/utils";

const STATUS: Record<string, { label: string; cls: string }> = {
  awaiting_payment: { label: "Awaiting payment", cls: "badge-warning" },
  payment_claimed: { label: "Checking payment", cls: "badge-warning" },
  open: { label: "Being prepared", cls: "badge-brand" },
  assigned: { label: "Ready to sit", cls: "badge-success" },
  submitted: { label: "Being marked", cls: "badge-brand" },
  marked: { label: "Marked", cls: "badge-success" },
  cancelled: { label: "Cancelled", cls: "badge-neutral" },
};

export default function MyRequestsPage() {
  const { ready } = useAuthGuard();
  const [rows, setRows] = useState<any[] | null>(null);
  const [isNew, setIsNew] = useState(false);
  const [payFor, setPayFor] = useState<number | null>(null);

  const load = useCallback(() => {
    requestsAPI.mine().then((r) => setRows(r.data)).catch(() => setRows([]));
  }, []);

  useEffect(() => {
    if (!ready) return;
    setIsNew(new URLSearchParams(window.location.search).get("new") === "1");
    load();
  }, [ready, load]);

  const cancel = async (id: number) => {
    if (!confirm("Cancel this request?")) return;
    await requestsAPI.cancel(id).catch(() => {});
    load();
  };

  if (!ready || rows === null) return <Spinner label="Loading your requests…" />;

  return (
    <PageContainer className="max-w-4xl">
      <PageHeader
        title="My test requests"
        subtitle="Tests you've asked our team for. Marked results appear here and in My Tests."
        icon={Inbox}
        actions={<Button href="/request" size="sm"><Plus size={15} /> New request</Button>}
      />

      {isNew && (
        <div className="mb-5 flex items-start gap-2 rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
          <CheckCircle2 size={16} className="mt-0.5 shrink-0" />
          Request sent! {rows[0]?.status === "awaiting_payment" ? "Complete the payment below so we can prepare your test." : "We'll email you when your test is ready."}
        </div>
      )}

      {!rows.length ? (
        <EmptyState icon={Inbox} title="No requests yet" desc="Ask for a full mock and our tutors will mark it."
          action={<Button href="/request">Request a test</Button>} />
      ) : (
        <div className="space-y-4">
          {rows.map((r) => {
            const key = r.status === "assigned" && r.progress ? r.progress : r.status;
            const st = STATUS[key] || STATUS.open;
            const showPay = r.status === "awaiting_payment" && (payFor === r.id || (isNew && rows[0]?.id === r.id));
            return (
              <div key={r.id} className="card p-5">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="font-semibold text-ink">{r.exam}{r.subject ? ` · ${r.subject}` : ""}</h3>
                      <span className={st.cls}>{st.label}</span>
                    </div>
                    <p className="mt-1 text-xs text-ink-subtle">
                      Request #{r.id} · {formatDate(r.created_at)}
                      {r.preferred_date ? ` · wanted for ${formatDate(r.preferred_date)}` : ""}
                    </p>
                    {r.details && <p className="mt-2 text-sm text-ink-muted">{r.details}</p>}
                    {r.admin_note && <p className="mt-2 rounded-lg bg-slate-50 px-3 py-2 text-sm text-ink-muted"><b>From the team:</b> {r.admin_note}</p>}
                  </div>
                  <div className="flex flex-wrap items-center gap-2">
                    {r.test && r.progress === "assigned" && (
                      <Button href={`/tests/${r.assignment_id}`} size="sm">Sit {r.test.title} <ArrowRight size={14} /></Button>
                    )}
                    {r.progress === "marked" && (
                      <Button href={`/tests/${r.assignment_id}/result`} size="sm" variant="secondary">
                        See result{r.grade ? ` · ${r.grade}` : r.score != null ? ` · ${r.score}%` : ""}
                      </Button>
                    )}
                    {r.status === "awaiting_payment" && !showPay && (
                      <Button size="sm" onClick={() => setPayFor(r.id)}>Pay {r.currency} {r.price.toFixed(2)}</Button>
                    )}
                    {(r.status === "awaiting_payment" || r.status === "open") && (
                      <Button size="sm" variant="ghost" onClick={() => cancel(r.id)}>Cancel</Button>
                    )}
                  </div>
                </div>
                {showPay && (
                  <div className="mt-5 border-t border-line pt-5">
                    <PaymentBox purpose="test_request" requestId={r.id} amount={r.price} currency={r.currency}
                      reference={r.reference} onClaimed={load} />
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </PageContainer>
  );
}
