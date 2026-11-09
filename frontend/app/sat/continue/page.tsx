"use client";
import { useEffect, useState } from "react";
import { Landmark, CheckCircle2, Lock, ShieldCheck } from "lucide-react";
import { getUser } from "@/lib/api";
import { satCheckoutAPI } from "@/lib/satApi";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Input, Select, Field } from "@/components/ui/Input";
import { type Account, useCountry, useRates, pickAccounts, priceFor, countryName } from "@/lib/country";

type Price = { currency: string; amount: number; label: string };

// Continue Notenix SAT after the free week: one payment for access until the SAT (12 months),
// local price for local accounts, paid by bank transfer, confirmed by an admin in /admin/requests.
export default function SatContinue() {
  const [info, setInfo] = useState<{ accounts: Account[]; prices: Record<string, Price>; usd: Price; pay_link?: string } | null>(null);
  const [form, setForm] = useState({ email: "", password: "", paid_via: "", payer_name: "", payer_note: "" });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState<{ reference: string } | null>(null);
  const country = useCountry();
  const rates = useRates();

  useEffect(() => {
    const u = getUser() as any;
    if (u?.email) setForm((f) => ({ ...f, email: u.email }));
    satCheckoutAPI.info().then((r) => setInfo(r.data))
      .catch(() => setInfo({ accounts: [], prices: {}, usd: { currency: "USD", amount: 129, label: "$129" } }));
  }, []);

  useEffect(() => {
    if (!info) return;
    const { shown } = pickAccounts(info.accounts, country);
    if (shown[0]) setForm((f) => ({ ...f, paid_via: shown[0].label }));
  }, [info, country]);

  const set = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) =>
    setForm((f) => ({ ...f, [k]: e.target.value }));

  if (!info) return <Spinner label="Loading…" />;
  const { shown, local } = pickAccounts(info.accounts, country);
  const priceOf = (a?: Account): Price => {
    const cur = (a?.currency || "USD").toUpperCase();
    return info.prices[cur] || { currency: "USD", amount: info.usd.amount, label: priceFor(info.usd.amount, a, rates) };
  };
  const chosen = shown.find((a) => a.label === form.paid_via) || shown[0];
  const price = local ? priceOf(chosen) : info.usd;

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const { data } = await satCheckoutAPI.pay({ ...form, currency: price.currency });
      setDone({ reference: data.reference });
    } catch (err: any) {
      setError(err.response?.data?.detail || "Couldn't send that. Please try again.");
    } finally {
      setBusy(false);
    }
  };

  if (done) {
    return (
      <PageContainer className="max-w-xl">
        <div className="card p-8 text-center">
          <span className="mx-auto grid h-14 w-14 place-items-center rounded-full bg-emerald-50 text-emerald-600"><CheckCircle2 size={28} /></span>
          <h1 className="mt-4 text-2xl font-bold text-ink">Thank you! We&apos;re checking your payment</h1>
          <p className="mt-2 text-sm text-ink-muted">
            Reference <b className="font-mono text-ink">{done.reference}</b>. We match it to our bank account, usually within a few hours,
            then email you. Notenix SAT then switches back on until your test (12 months), and all your scores are kept.
          </p>
          <Button href="/login" className="mt-6">Go to sign in</Button>
        </div>
      </PageContainer>
    );
  }

  return (
    <PageContainer className="max-w-3xl">
      <p className="text-sm font-semibold text-brand-600">Notenix SAT · Until your SAT date</p>
      <h1 className="mt-1 text-2xl font-bold tracking-tight text-ink sm:text-3xl">{price.label}, one payment</h1>
      <p className="mt-1 text-sm text-ink-muted">
        Full adaptive practice tests with a score out of 1600, skill drills, your study plan to test day and a weekly
        progress email. 12 months of access, enough for your test and a resit. Nothing renews by itself.
      </p>

      <form onSubmit={submit} className="mt-6 space-y-6">
        <div className="card space-y-4 p-6">
          <h2 className="font-semibold text-ink">1. The Notenix SAT login</h2>
          <p className="text-sm text-ink-muted">The email and password used for the free week.</p>
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Email"><Input required type="email" value={form.email} onChange={set("email")} placeholder="you@example.com" autoCapitalize="none" /></Field>
            <Field label="Password"><Input required type="password" value={form.password} onChange={set("password")} /></Field>
          </div>
          <p className="text-xs text-ink-subtle">No free week yet? <a href="/sat/diagnostic" className="font-medium text-brand-600 hover:underline">Take the free diagnostic</a> to start one.</p>
        </div>

        <div className="card space-y-4 p-6">
          <h2 className="flex items-center gap-2 font-semibold text-ink"><Landmark size={16} /> 2. Pay {price.label}</h2>
                    {shown.length === 0 ? (
            <p className="rounded-lg bg-slate-50 p-4 text-sm text-ink-muted">Bank details aren&apos;t set up yet. Reply to any Notenix email and we&apos;ll send them.</p>
          ) : (
            shown.map((a) => (
              <div key={a.label} className={`space-y-3 rounded-lg border p-4 ${local ? "border-brand-300 bg-brand-50/40" : "border-line"}`}>
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="text-sm font-semibold text-ink">{a.label}</p>
                  {local && <span className="rounded-full bg-brand-600 px-2.5 py-0.5 text-[11px] font-semibold text-white">For {countryName(country)}</span>}
                </div>
                <p className="text-sm text-ink">Send <b>{local ? priceOf(a).label : info.usd.label}</b> · reference: the student&apos;s name</p>
                <dl className="mt-2 grid grid-cols-[auto,1fr] gap-x-4 gap-y-1 text-sm">
                  {Object.entries(a.details).map(([k, v]) => (
                    <div key={k} className="contents"><dt className="text-ink-muted">{k}</dt><dd className="font-mono text-ink">{v}</dd></div>
                  ))}
                </dl>
                {a.note && <p className="text-xs text-ink-subtle">{a.note}</p>}
              </div>
            ))
          )}
          <div className="grid gap-4 sm:grid-cols-2">
            {shown.length > 1 && (
              <Field label="Account you paid into">
                <Select value={form.paid_via} onChange={set("paid_via")}>
                  {shown.map((a) => <option key={a.label}>{a.label}</option>)}
                </Select>
              </Field>
            )}
            <Field label="Name of the person who paid"><Input required value={form.payer_name} onChange={set("payer_name")} placeholder="e.g. R Patel" /></Field>
            <Field label="Bank or Wise reference" hint="Optional: helps us find it faster.">
              <Input value={form.payer_note} onChange={set("payer_note")} placeholder="e.g. Barclays, ref 48213" />
            </Field>
          </div>
        </div>

        {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
        <Button type="submit" loading={busy} className="w-full"><Lock size={15} /> I&apos;ve paid {price.label}</Button>
        <p className="flex items-center justify-center gap-1.5 text-xs text-ink-muted">
          <ShieldCheck size={13} /> We never ask for card numbers or bank passwords. Access switches on when we confirm your payment.
        </p>
      </form>
    </PageContainer>
  );
}
