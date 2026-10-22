"use client";
import { useEffect, useState } from "react";
import { Copy, Check, Landmark, Send } from "lucide-react";
import { paymentsAPI } from "@/lib/api";
import { Button } from "./ui/Button";
import { Input, Select, Field } from "./ui/Input";

type Account = { label: string; currency?: string; details: Record<string, string>; note?: string };

function CopyValue({ value }: { value: string }) {
  const [done, setDone] = useState(false);
  return (
    <button
      type="button"
      onClick={() => { navigator.clipboard?.writeText(value).then(() => { setDone(true); setTimeout(() => setDone(false), 1500); }); }}
      className="inline-flex items-center gap-1.5 font-mono text-sm font-medium text-ink hover:text-brand-600"
      title="Copy"
    >
      {value} {done ? <Check size={13} className="text-emerald-600" /> : <Copy size={13} className="text-ink-subtle" />}
    </button>
  );
}

// Bank-transfer instructions + "I've paid" form. Used for Pro and for paid test requests.
export default function PaymentBox({
  purpose, requestId, amount, currency, reference, onClaimed,
}: {
  purpose: "pro" | "test_request";
  requestId?: number;
  amount: number;
  currency: string;
  reference: string;
  onClaimed?: () => void;
}) {
  const [accounts, setAccounts] = useState<Account[] | null>(null);
  const [via, setVia] = useState("");
  const [payerName, setPayerName] = useState("");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [msg, setMsg] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    paymentsAPI.accounts()
      .then((r) => { setAccounts(r.data.accounts || []); setVia(r.data.accounts?.[0]?.label || ""); })
      .catch(() => setAccounts([]));
  }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true); setError("");
    try {
      await paymentsAPI.claim({ purpose, request_id: requestId, paid_via: via, payer_name: payerName, payer_note: note });
      setMsg("Thanks! We'll check our account and confirm by email, usually within 24 hours.");
      onClaimed?.();
    } catch (err: any) {
      setError(err.response?.data?.detail || "Couldn't send that. Please try again.");
    } finally {
      setBusy(false);
    }
  };

  if (accounts === null) return <div className="text-sm text-ink-muted">Loading payment details…</div>;

  if (!accounts.length) {
    return (
      <div className="rounded-lg border border-line bg-slate-50 p-4 text-sm text-ink-muted">
        Online payment details aren't set up yet. Email{" "}
        <a href={`mailto:hello@notenix.com?subject=${encodeURIComponent("Payment " + reference)}`} className="font-medium text-brand-600">hello@notenix.com</a>{" "}
        with reference <b>{reference}</b> and we'll send you the details.
      </div>
    );
  }

  return (
    <div className="space-y-5">
      <div className="rounded-xl border border-brand-200 bg-brand-50 p-4">
        <div className="text-sm text-ink-muted">Amount</div>
        <div className="text-2xl font-bold text-ink">{currency} {amount.toFixed(2)}</div>
        <div className="mt-2 text-sm text-ink-muted">
          Payment reference (add it to your transfer): <CopyValue value={reference} />
        </div>
        <p className="mt-2 text-xs text-ink-subtle">
          Paying in another currency? Send the equivalent amount; your bank or Wise shows the conversion.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        {accounts.map((a) => (
          <div key={a.label} className="card p-4">
            <div className="flex items-center gap-2 text-sm font-semibold text-ink">
              <Landmark size={15} className="text-brand-600" /> {a.label}
            </div>
            <dl className="mt-3 space-y-2">
              {Object.entries(a.details).map(([k, v]) => (
                <div key={k}>
                  <dt className="text-xs text-ink-subtle">{k}</dt>
                  <dd><CopyValue value={String(v)} /></dd>
                </div>
              ))}
            </dl>
            {a.note && <p className="mt-3 text-xs text-ink-subtle">{a.note}</p>}
          </div>
        ))}
      </div>

      {msg ? (
        <div className="rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">{msg}</div>
      ) : (
        <form onSubmit={submit} className="card space-y-4 p-5">
          <h3 className="font-semibold text-ink">Paid? Tell us so we can match it</h3>
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Paid to">
              <Select value={via} onChange={(e) => setVia(e.target.value)}>
                {accounts.map((a) => <option key={a.label}>{a.label}</option>)}
              </Select>
            </Field>
            <Field label="Name on the paying account">
              <Input value={payerName} onChange={(e) => setPayerName(e.target.value)} placeholder="e.g. parent's name" required />
            </Field>
          </div>
          <Field label="Transfer ID or note (optional)" hint="Amount and currency sent, Wise/UPI transaction ID, date…">
            <Input value={note} onChange={(e) => setNote(e.target.value)} />
          </Field>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <Button type="submit" loading={busy}><Send size={15} /> I've paid</Button>
        </form>
      )}
    </div>
  );
}
