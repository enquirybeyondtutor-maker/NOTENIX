"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { CheckCircle2, Landmark, Lock, ShieldCheck } from "lucide-react";
import { seriesAPI } from "@/lib/api";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Input, Select, Field } from "@/components/ui/Input";
import PayLink from "@/components/PayLink";
import { type Account, useCountry, useRates, pickAccounts, priceFor, countryName } from "@/lib/country";
import { SERIES } from "@/lib/tmuaSeries";
import PayerDetailsFields from "@/components/PayerDetailsFields";
import NotenixIdPreview from "@/components/NotenixIdPreview";

// Enrol & pay for the TMUA Mock Series. The account is created locked; an admin confirms the
// payment in /admin/requests, which opens the series (Baseline Mock first, then each mock on its date).

type Info = { accounts: Account[]; pay_link: string; price: { amount: number; currency: string; early: boolean; full: number } };

export default function TmuaEnrol() {
  const [info, setInfo] = useState<Info | null>(null);
  const [loadError, setLoadError] = useState("");
  const [form, setForm] = useState({ full_name: "", email: "", password: "", paid_via: "", payer_name: "", payer_note: "", payer_dob: "", payer_country: "" });
  const [agree, setAgree] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState<{ reference: string; login_id: string; email: string } | null>(null);
  const country = useCountry();
  const rates = useRates();

  useEffect(() => {
    seriesAPI.tmua().then((r) => setInfo(r.data)).catch(() => setLoadError("Couldn't load the checkout. Please refresh the page."));
  }, []);
  useEffect(() => {
    if (!info) return;
    const { shown } = pickAccounts(info.accounts, country);
    if (shown[0]) setForm((f) => ({ ...f, paid_via: f.paid_via || shown[0].label }));
  }, [info, country]);

  const set = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) =>
    setForm((f) => ({ ...f, [k]: e.target.value }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!agree) { setError("Please confirm you've read the terms."); return; }
    setBusy(true); setError("");
    try {
      const { data } = await seriesAPI.tmuaEnrol(form);
      setDone({ reference: data.reference, login_id: data.login_id, email: data.email });
      window.scrollTo({ top: 0 });
    } catch (err: any) {
      setError(err.response?.data?.detail || "Couldn't send that. Please try again.");
    } finally {
      setBusy(false);
    }
  };

  if (loadError) return <PageContainer className="max-w-xl"><p className="rounded-lg bg-red-50 p-4 text-sm text-red-700">{loadError}</p></PageContainer>;
  if (!info) return <Spinner label="Loading checkout…" />;

  const gbp = `£${info.price.amount}`;
  const { shown, local } = pickAccounts(info.accounts, country);
  const price = local ? priceFor(info.price.amount, shown[0], rates) : gbp;

  if (done) {
    return (
      <PageContainer className="max-w-xl">
        <div className="card p-8 text-center">
          <span className="mx-auto grid h-14 w-14 place-items-center rounded-full bg-emerald-50 text-emerald-600"><CheckCircle2 size={28} /></span>
          <h1 className="mt-4 text-2xl font-bold text-ink">You&apos;re enrolled: payment being checked</h1>
          <p className="mt-2 text-sm text-ink-muted">
            Reference <b className="font-mono text-ink">{done.reference}</b>. We match your payment, usually within a few hours,
            then email <b className="text-ink">{done.email}</b>. Your account opens as soon as it&apos;s confirmed, with the Baseline Mock waiting in Tests.
          </p>
          <div className="mx-auto mt-5 max-w-sm rounded-xl border border-brand-200 bg-brand-50/60 p-4 text-left text-sm">
            <p className="font-semibold text-ink">Your Notenix login</p>
            <p className="mt-2 text-ink-muted">User ID</p>
            <p className="font-mono text-base font-semibold text-ink">{done.login_id}</p>
            <p className="mt-2 text-ink-muted">Password: the one you just chose.</p>
            <p className="mt-2 text-xs text-ink-muted">Save this user ID: you sign in with it, not your email.</p>
          </div>
          <Button href="/tmua-mocks#schedule" variant="secondary" className="mt-6">See the mock schedule</Button>
        </div>
      </PageContainer>
    );
  }

  return (
    <PageContainer className="max-w-3xl">
      <p className="text-sm font-semibold text-brand-600"><Link href="/tmua-mocks" className="hover:underline">TMUA Mock Series · {SERIES.sitting}</Link></p>
      <h1 className="mt-1 text-2xl font-bold tracking-tight text-ink sm:text-3xl">Enrol: {gbp} for the full series</h1>
      <p className="mt-1 text-sm text-ink-muted">
        {info.price.early
          ? <>Early-bird price until {SERIES.earlyLabel} (then £{info.price.full}). </>
          : null}
        Baseline Mock, 10 full mocks, rankings, worked solutions and topic sets on request. Your account opens once your payment is confirmed.
      </p>

      <form onSubmit={submit} className="mt-6 space-y-6">
        <div className="card space-y-4 p-6">
          <h2 className="font-semibold text-ink">1. Your Notenix account</h2>
          <Field label="Student's full name"><Input required value={form.full_name} onChange={set("full_name")} placeholder="e.g. Priya Patel" /></Field>
          <Field label="Email" hint="We send your confirmation and updates here. Your Notenix user ID is made from your name, e.g. priya@notenix.com.">
            <Input required type="email" value={form.email} onChange={set("email")} placeholder="you@example.com" /></Field>
          <NotenixIdPreview name={form.full_name} />
          <Field label="Choose a password" hint="At least 8 characters. Already have a Notenix account? Use its email and password.">
            <Input required type="password" minLength={8} value={form.password} onChange={set("password")} />
          </Field>
        </div>

        <div className="card space-y-4 p-6">
          <h2 className="flex items-center gap-2 font-semibold text-ink"><Landmark size={16} /> 2. Pay {price}</h2>
          {info.pay_link && <PayLink href={info.pay_link} label={`Pay ${local ? "by card" : `${gbp} now`}`}
            hint={local ? `Card or Apple/Google Pay through Wise. Charged as ${gbp}; your bank converts it.` : undefined} />}
          {info.pay_link && shown.length > 0 && <p className="text-xs font-medium uppercase tracking-wide text-ink-subtle">Or pay by bank transfer</p>}
          {shown.length === 0 && !info.pay_link && (
            <p className="rounded-lg bg-slate-50 p-4 text-sm text-ink-muted">Bank details aren&apos;t set up yet. Email support@notenix.com and we&apos;ll send them.</p>
          )}
          {shown.map((a) => (
            <div key={a.label} className={`space-y-3 rounded-lg border p-4 ${local ? "border-brand-300 bg-brand-50/40" : "border-line"}`}>
              <div className="flex flex-wrap items-center justify-between gap-2">
                <p className="text-sm font-semibold text-ink">{a.label}</p>
                {local && <span className="rounded-full bg-brand-600 px-2.5 py-0.5 text-[11px] font-semibold text-white">For {countryName(country)}</span>}
              </div>
              {local && <p className="text-sm text-ink">Send <b>{priceFor(info.price.amount, a, rates)}</b></p>}
              <dl className="mt-2 grid grid-cols-[auto,1fr] gap-x-4 gap-y-1 text-sm">
                {Object.entries(a.details).map(([k, v]) => (
                  <div key={k} className="contents"><dt className="text-ink-muted">{k}</dt><dd className="font-mono text-ink">{v}</dd></div>
                ))}
              </dl>
              {a.note && <p className="text-xs text-ink-subtle">{a.note}</p>}
            </div>
          ))}
          <p className="text-xs text-ink-muted">Pay exactly {price}, then fill in the details below so we can match your payment.</p>
          <div className="grid gap-4 sm:grid-cols-2">
            {shown.length > 1 && (
              <Field label="Account you paid into">
                <Select value={form.paid_via} onChange={set("paid_via")}>{shown.map((a) => <option key={a.label}>{a.label}</option>)}</Select>
              </Field>
            )}
            <Field label="Name of the person who paid"><Input required value={form.payer_name} onChange={set("payer_name")} placeholder="e.g. R Patel" /></Field>
            <PayerDetailsFields country={form.payer_country} dob={form.payer_dob}
              onCountry={(v) => setForm((f) => ({ ...f, payer_country: v }))} onDob={(v) => setForm((f) => ({ ...f, payer_dob: v }))} />
            <Field label="Wise or bank reference" hint="Optional: helps us find it faster.">
              <Input value={form.payer_note} onChange={set("payer_note")} placeholder="e.g. HDFC, ref 48213" />
            </Field>
          </div>
        </div>

        <label className="flex items-start gap-2 text-sm text-ink-muted">
          <input type="checkbox" checked={agree} onChange={(e) => setAgree(e.target.checked)} className="mt-1" />
          <span>I&apos;ve read the <Link href="/tmua-mocks#terms" className="font-medium text-brand-600 hover:underline">series terms</Link>: access opens after payment is confirmed, one account per student, refunds only before Mock 1 or within 48 hours if no mock has been started.</span>
        </label>
        {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
        <Button type="submit" loading={busy} className="w-full"><Lock size={15} /> I&apos;ve paid {price} · enrol me</Button>
        <p className="flex items-center justify-center gap-1.5 text-xs text-ink-muted">
          <ShieldCheck size={13} /> We never ask for card numbers or bank passwords.
        </p>
      </form>
    </PageContainer>
  );
}
