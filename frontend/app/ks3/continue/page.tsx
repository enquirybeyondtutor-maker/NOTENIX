"use client";
import { useEffect, useState } from "react";
import { Landmark, CheckCircle2, Lock, ShieldCheck } from "lucide-react";
import { paymentsAPI, getUser } from "@/lib/api";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Input, Select, Field } from "@/components/ui/Input";
import PayLink from "@/components/PayLink";
import { type Account, useCountry, useRates, pickAccounts, priceFor, countryName } from "@/lib/country";

type Price = { currency: string; amount: number; label: string };

// Continue Notenix KS3 after the free week: £149/year (local price for local accounts),
// paid by bank transfer, confirmed by an admin in /admin/requests.
export default function Ks3Continue() {
  const [info, setInfo] = useState<{ accounts: Account[]; prices: Record<string, Price>; gbp: Price; pay_link?: string } | null>(null);
  const [form, setForm] = useState({ login_id: "", password: "", paid_via: "", payer_name: "", payer_note: "" });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState<{ reference: string } | null>(null);
  const country = useCountry();
  const rates = useRates();

  useEffect(() => {
    const u = getUser() as any;
    if (u?.email) setForm((f) => ({ ...f, login_id: u.email }));
    paymentsAPI.ks3Info().then((r) => setInfo(r.data))
      .catch(() => setInfo({ accounts: [], prices: {}, gbp: { currency: "GBP", amount: 149, label: "£149" } }));
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
    const cur = (a?.currency || "GBP").toUpperCase();
    return info.prices[cur] || { currency: "GBP", amount: info.gbp.amount, label: priceFor(info.gbp.amount, a, rates) };
  };
  const chosen = shown.find((a) => a.label === form.paid_via) || shown[0];
  const price = local ? priceOf(chosen) : info.gbp;

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const { data } = await paymentsAPI.ks3Checkout({ ...form, currency: price.currency });
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
            then email you. Notenix KS3 then switches on for a full year, and all results so far are kept.
          </p>
          <Button href="/login" className="mt-6">Go to sign in</Button>
        </div>
      </PageContainer>
    );
  }

  return (
    <PageContainer className="max-w-3xl">
      <p className="text-sm font-semibold text-brand-600">Notenix KS3 · Year 7 to GCSE</p>
      <h1 className="mt-1 text-2xl font-bold tracking-tight text-ink sm:text-3xl">{price.label} / year</h1>
      <p className="mt-1 text-sm text-ink-muted">
        A timed test every half-term in Maths, Science and English, homework help from Beyond Tutors tutors, KS3 notes,
        and a progress report in your inbox every month.
      </p>

      <form onSubmit={submit} className="mt-6 space-y-6">
        <div className="card space-y-4 p-6">
          <h2 className="font-semibold text-ink">1. Your child&apos;s Notenix login</h2>
          <p className="text-sm text-ink-muted">The user ID from the free week (e.g. name@notenix.com) and its password.</p>
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Notenix user ID"><Input required value={form.login_id} onChange={set("login_id")} placeholder="name@notenix.com" autoCapitalize="none" /></Field>
            <Field label="Password"><Input required type="password" value={form.password} onChange={set("password")} /></Field>
          </div>
          <p className="text-xs text-ink-subtle">No free week yet? <a href="/ks3/trial" className="font-medium text-brand-600 hover:underline">Start one first</a>, it&apos;s free.</p>
        </div>

        <div className="card space-y-4 p-6">
          <h2 className="flex items-center gap-2 font-semibold text-ink"><Landmark size={16} /> 2. Pay {price.label}</h2>
          {info.pay_link && !local && <PayLink href={info.pay_link} label={`Pay ${info.gbp.label} now`} />}
          {info.pay_link && !local && shown.length > 0 && (
            <p className="text-xs font-medium uppercase tracking-wide text-ink-subtle">Or pay by bank transfer</p>
          )}
          {shown.length === 0 && !info.pay_link ? (
            <p className="rounded-lg bg-slate-50 p-4 text-sm text-ink-muted">Bank details aren&apos;t set up yet. Reply to any Notenix email and we&apos;ll send them.</p>
          ) : (
            shown.map((a) => (
              <div key={a.label} className={`space-y-3 rounded-lg border p-4 ${local ? "border-brand-300 bg-brand-50/40" : "border-line"}`}>
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="text-sm font-semibold text-ink">{a.label}</p>
                  {local && <span className="rounded-full bg-brand-600 px-2.5 py-0.5 text-[11px] font-semibold text-white">For {countryName(country)}</span>}
                </div>
                <p className="text-sm text-ink">Send <b>{local ? priceOf(a).label : info.gbp.label}</b> · reference: your child&apos;s name</p>
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
          <ShieldCheck size={13} /> We never ask for card numbers or bank passwords. The year starts when we confirm your payment.
        </p>
      </form>
    </PageContainer>
  );
}
