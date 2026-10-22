"use client";
import { useEffect, useState } from "react";
import { Sparkles, CheckCircle2 } from "lucide-react";
import { paymentsAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, Spinner } from "@/components/ui/Page";
import PaymentBox from "@/components/PaymentBox";
import { formatDate } from "@/lib/utils";

// Upgrade to Pro by bank transfer. An admin confirms the payment, which turns Pro on for 30 days.
export default function PayPage() {
  const { ready } = useAuthGuard();
  const [info, setInfo] = useState<any>(null);
  const [pending, setPending] = useState(false);

  useEffect(() => {
    if (!ready) return;
    paymentsAPI.accounts().then((r) => setInfo(r.data)).catch(() => setInfo({}));
    paymentsAPI.mine()
      .then((r) => setPending(r.data.some((p: any) => p.purpose === "pro" && p.status === "claimed")))
      .catch(() => {});
  }, [ready]);

  if (!ready || !info) return <Spinner label="Loading…" />;

  return (
    <PageContainer className="max-w-3xl">
      <PageHeader title="Upgrade to Notenix Pro" subtitle="Pay by bank transfer from any country." icon={Sparkles} />

      {info.plan === "pro" && (
        <div className="mb-5 flex items-center gap-2 rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
          <CheckCircle2 size={16} /> You're on Pro{info.pro_until ? ` until ${formatDate(info.pro_until)}` : ""}. Paying again adds another 30 days.
        </div>
      )}

      {pending ? (
        <div className="card p-6 text-sm text-ink-muted">
          We've got your payment details and are checking our account. You'll get an email as soon as Pro is switched on.
        </div>
      ) : info.pro_price > 0 ? (
        <PaymentBox purpose="pro" amount={info.pro_price} currency={info.currency} reference={info.pro_reference}
          onClaimed={() => setPending(true)} />
      ) : (
        <div className="card p-6 text-sm text-ink-muted">Pro isn't on sale right now. Everything free stays free.</div>
      )}
    </PageContainer>
  );
}
