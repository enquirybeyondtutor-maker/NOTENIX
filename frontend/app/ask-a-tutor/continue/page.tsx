"use client";
import { useEffect, useState } from "react";
import { Landmark, CheckCircle2, Lock, ShieldCheck, Check } from "lucide-react";
import { getUser } from "@/lib/api";
import { doubtAPI } from "@/lib/doubtApi";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Input, Select, Field } from "@/components/ui/Input";
import { type Account, useCountry, pickAccounts, countryName } from "@/lib/country";

type Info = { accounts: Account[]; prices: Record<string, Record<string, number>>;
  plans: Record<string, { name: string; cap: number; calls: number; days?: number }> };
const SYM: Record<string, string> = { SGD: "S$", GBP: "£", USD: "$", AUD: "A$", INR: "₹" };
const money = (cur: string, n: number) => (SYM[cur] ? `${SYM[cur]}${n.toLocaleString("en")}` : `${cur} ${n.toLocaleString("en")}`);

/** Ask a Tutor is priced in S$: show the visitor's own local account if we have one, otherwise the
 *  Singapore (SGD) account rather than the international GBP one. */
function accountsFor(accounts: Account[], country: string) {
  const r = pickAccounts(accounts, country);
  if (r.local) return { ...r, place: countryName(country) };
  const sg = accounts.filter((a) => (a.countries || []).includes("SG"));
  return sg.length ? { shown: sg, local: true, place: "Singapore" } : { ...r, place: "" };
}

// Ask a Tutor plans, paid by bank transfer and confirmed by an admin.
export default function DoubtContinue() {
  const [info, setInfo] = useState<Info | null>(null);
  const [plan, setPlan] = useState<"annual" | "doubt" | "plus">("annual");
  const [form, setForm] = useState({ login_id: "", password: "", paid_via: "", payer_name: "", payer_note: "" });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState<{ reference: string } | null>(null);
  const country = useCountry();

  useEffect(() => {
    const u = getUser() as any;
    if (u?.email) setForm((f) => ({ ...f, login_id: u.email }));
    doubtAPI.checkoutInfo().then((r) => setInfo(r.data)).catch(() => setInfo({ accounts: [], prices: { annual: { SGD: 249 }, doubt: { SGD: 39 }, plus: { SGD: 79 } }, plans: {} }));
  }, []);
  useEffect(() => {
    if (!info) return;
    const { shown } = accountsFor(info.accounts, country);
    if (shown[0]) setForm((f) => ({ ...f, paid_via: shown[0].label }));
  }, [info, country]);

  if (!info) return <Spinner label="Loading…" />;
  const { shown, local, place } = accountsFor(info.accounts, country);
  const chosen = shown.find((a) => a.label === form.paid_via) || shown[0];
  const currency = local && chosen?.currency && info.prices[plan][chosen.currency.toUpperCase()] ? chosen.currency.toUpperCase() : "SGD";
  const price = money(currency, info.prices[plan][currency]);
  const set = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => setForm((f) => ({ ...f, [k]: e.target.value }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const { data } = await doubtAPI.checkout({ ...form, plan, currency });
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
          <p className="mt-2 text-sm text-ink-muted">Reference <b className="font-mono text-ink">{done.reference}</b>. We match it to our account, usually within a few hours, then email you. The plan starts when it&apos;s confirmed, and all earlier questions are kept.</p>
          <Button href="/login" className="mt-6">Go to sign in</Button>
        </div>
      </PageContainer>
    );
  }

  return (
    <PageContainer className="max-w-3xl">
      <p className="text-sm font-semibold text-brand-600">Ask a Tutor</p>
      <h1 className="mt-1 text-2xl font-bold tracking-tight text-ink sm:text-3xl">Choose a plan</h1>
      <form onSubmit={submit} className="mt-6 space-y-6">
        <div className="grid gap-4 sm:grid-cols-3">
          {(["annual", "doubt", "plus"] as const).map((p) => {
            const meta = info.plans[p] || { name: { annual: "1 year", doubt: "Doubt Help", plus: "Doubt Help Plus" }[p], cap: p === "plus" ? 50 : 20, calls: p === "plus" ? 2 : 0, days: p === "annual" ? 365 : 30 };
            const yearly = (meta.days || 30) >= 365;
            return (
              <button type="button" key={p} onClick={() => setPlan(p)}
                className={`card p-5 text-left transition ${plan === p ? "border-brand-500 ring-2 ring-brand-600/20" : "hover:border-brand-300"}`}>
                <div className="flex items-center justify-between"><span className="font-semibold text-ink">{meta.name}</span>
                  {plan === p && <span className="rounded-full bg-brand-600 px-2 py-0.5 text-[11px] font-semibold text-white">Selected</span>}</div>
                <div className="mt-1 text-2xl font-bold text-ink">{money(currency, info.prices[p][currency])}<span className="text-sm font-normal text-ink-subtle"> / {yearly ? "year" : "30 days"}</span></div>
                {yearly && <div className="text-xs font-medium text-emerald-700">Best value</div>}
                <ul className="mt-3 space-y-1 text-sm text-ink-muted">
                  <li className="flex items-center gap-2"><Check size={14} className="text-brand-600" /> Up to {meta.cap} questions{yearly ? " every month" : ""}</li>
                  {meta.calls > 0 && <li className="flex items-center gap-2"><Check size={14} className="text-brand-600" /> {meta.calls} live 30-minute calls</li>}
                </ul>
              </button>
            );
          })}
        </div>

        <div className="card space-y-4 p-6">
          <h2 className="font-semibold text-ink">1. Your child&apos;s Notenix login</h2>
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Notenix user ID"><Input required value={form.login_id} onChange={set("login_id")} placeholder="name@notenix.com" autoCapitalize="none" /></Field>
            <Field label="Password"><Input required type="password" value={form.password} onChange={set("password")} /></Field>
          </div>
          <p className="text-xs text-ink-subtle">No trial yet? <a href="/ask-a-tutor#start" className="font-medium text-brand-600 hover:underline">Start one first</a>, it&apos;s free.</p>
        </div>

        <div className="card space-y-4 p-6">
          <h2 className="flex items-center gap-2 font-semibold text-ink"><Landmark size={16} /> 2. Pay {price}</h2>
          {shown.length === 0 ? (
            <p className="rounded-lg bg-slate-50 p-4 text-sm text-ink-muted">Reply to any Notenix email or message us on WhatsApp and we&apos;ll send the payment details.</p>
          ) : shown.map((a) => (
            <div key={a.label} className={`space-y-3 rounded-lg border p-4 ${local ? "border-brand-300 bg-brand-50/40" : "border-line"}`}>
              <div className="flex flex-wrap items-center justify-between gap-2">
                <p className="text-sm font-semibold text-ink">{a.label}</p>
                {local && place && <span className="rounded-full bg-brand-600 px-2.5 py-0.5 text-[11px] font-semibold text-white">{place === "Singapore" && countryName(country) !== "Singapore" ? "Singapore account (S$)" : `For ${place}`}</span>}
              </div>
              <p className="text-sm text-ink">Send <b>{price}</b> · reference: your child&apos;s name</p>
              <dl className="grid grid-cols-[auto,1fr] gap-x-4 gap-y-1 text-sm">
                {Object.entries(a.details).map(([k, v]) => <div key={k} className="contents"><dt className="text-ink-muted">{k}</dt><dd className="font-mono text-ink">{v}</dd></div>)}
              </dl>
            </div>
          ))}
          <div className="grid gap-4 sm:grid-cols-2">
            {shown.length > 1 && (
              <Field label="Account you paid into"><Select value={form.paid_via} onChange={set("paid_via")}>{shown.map((a) => <option key={a.label}>{a.label}</option>)}</Select></Field>
            )}
            <Field label="Name of the person who paid"><Input required value={form.payer_name} onChange={set("payer_name")} placeholder="e.g. Mr Tan" /></Field>
            <Field label="Bank or PayNow reference" hint="Optional: helps us find it faster."><Input value={form.payer_note} onChange={set("payer_note")} /></Field>
          </div>
        </div>

        {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
        <Button type="submit" loading={busy} className="w-full"><Lock size={15} /> I&apos;ve paid {price}</Button>
        <p className="flex items-center justify-center gap-1.5 text-xs text-ink-muted"><ShieldCheck size={13} /> We never ask for card numbers or bank passwords. Nothing renews by itself.</p>
      </form>
    </PageContainer>
  );
}
