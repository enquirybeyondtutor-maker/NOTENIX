"use client";
import { useEffect, useState } from "react";
import { Landmark, CheckCircle2, Lock, ShieldCheck, Clock } from "lucide-react";
import { paymentsAPI, getUser } from "@/lib/api";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Input, Select, Field } from "@/components/ui/Input";
import { type Account, useCountry, pickAccounts, countryName } from "@/lib/country";
import { type Ks3Info, type Ks3Price, KS3_FALLBACK, loadKs3Info, ks3Years, ks3Tier, useOfferCountdown } from "@/lib/ks3Pricing";
import PayerDetailsFields from "@/components/PayerDetailsFields";

type Price = Ks3Price;

// Continue Notenix KS3 after the free week, priced by year group (Year 7/8/9, or Grade 5/6/7 on a
// track; local price for local accounts), paid by bank transfer, confirmed by an admin in /admin/requests.
// The backend charges the account's own year, so the year picker only chooses the price shown.
// No Wise card link here: that link is a fixed GBP amount and KS3 prices now differ by year.
// US Middle School families pay in dollars: without a local account for their country they see
// the USD price (no Wise card link, which is fixed in GBP), not the GBP one.
const GRADE_TRACKS = {
  us: { product: "Notenix Middle School", currency: "USD", trial: "/middle-school/trial",
        blurb: "Math and English Language Arts tests, homework help from Beyond Tutors tutors, grade-level notes, and a progress report in your inbox every month." },
  on: { product: "Notenix Ontario", currency: "CAD", trial: "/ontario/trial",
        blurb: "Math and Language tests that follow the Ontario curriculum, homework help from Beyond Tutors tutors, grade-level notes, and a progress report in your inbox every month." },
};

export default function Ks3Continue({ track }: { track?: "us" | "on" }) {
  const G = track ? GRADE_TRACKS[track] : null;
  const [info, setInfo] = useState<Ks3Info | null>(null);
  const [tier, setTier] = useState(0);
  const [form, setForm] = useState({ login_id: "", password: "", paid_via: "", payer_name: "", payer_note: "", payer_dob: "", payer_country: "" });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState<{ reference: string } | null>(null);
  const country = useCountry();
  const countdown = useOfferCountdown(info?.offer ? info.offer_until : null);

  useEffect(() => {
    const u = getUser() as any;
    if (u?.email) setForm((f) => ({ ...f, login_id: u.email }));
    if (u?.ks3_year) setTier(ks3Tier(u.ks3_year, u.ks3_track || null));
    loadKs3Info().then(setInfo).catch(() => setInfo(KS3_FALLBACK));
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
  const pick = (row?: Price[]): Price | undefined => row?.[tier] ?? row?.[0];
  const gbpPrice = pick(info.gbp) || KS3_FALLBACK.gbp[tier];
  const priceOf = (a?: Account): Price => pick(info.prices[(a?.currency || "GBP").toUpperCase()]) || gbpPrice;
  const chosen = shown.find((a) => a.label === form.paid_via) || shown[0];
  const fallback = (G && pick(info.prices[G.currency])) || gbpPrice;
  const price = local ? priceOf(chosen) : fallback;
  const shownRow = local ? info.prices[(chosen?.currency || "GBP").toUpperCase()] : (G ? info.prices[G.currency] : info.gbp);
  const product = G ? G.product : "Notenix KS3";

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
            then email you. {product} then switches on for a full year, and all results so far are kept.
          </p>
          <Button href="/login" className="mt-6">Go to sign in</Button>
        </div>
      </PageContainer>
    );
  }

  return (
    <PageContainer className="max-w-3xl">
      <p className="text-sm font-semibold text-brand-600">{G ? `${G.product} · Grades 5–7` : "Notenix KS3 · Year 7 to GCSE"}</p>
      <h1 className="mt-1 flex flex-wrap items-baseline gap-x-3 text-2xl font-bold tracking-tight text-ink sm:text-3xl">
        {countdown && price.was_label && <s className="text-xl font-semibold text-ink-subtle">{price.was_label}</s>}
        <span>{price.label} / year</span>
        <span className="text-base font-medium text-ink-muted">for {ks3Years(track)[tier].label}</span>
      </h1>
      {countdown && price.was_label && (
        <p className="mt-2 inline-flex items-center gap-1.5 rounded-full bg-amber-100 px-3 py-1 text-xs font-semibold text-amber-800">
          <Clock size={13} /> Launch offer: {countdown.replace("Offer ends", "ends")}
        </p>
      )}
      <p className="mt-1 text-sm text-ink-muted">
        {G
          ? G.blurb
          : "A timed test every half-term in Maths, Science and English, homework help from Beyond Tutors tutors, KS3 notes, and a progress report in your inbox every month."}
      </p>

      <form onSubmit={submit} className="mt-6 space-y-6">
        <div className="card space-y-4 p-6">
          <h2 className="font-semibold text-ink">1. Your child&apos;s Notenix login</h2>
          <p className="text-sm text-ink-muted">The user ID from the free week (e.g. name@notenix.com) and its password.</p>
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Notenix user ID"><Input required value={form.login_id} onChange={set("login_id")} placeholder="name@notenix.com" autoCapitalize="none" /></Field>
            <Field label="Password"><Input required type="password" value={form.password} onChange={set("password")} /></Field>
          </div>
          <Field label={track ? "Your child's grade" : "Your child's year"} hint="The price depends on the year. We charge the year on your child's account.">
            <Select value={String(tier)} onChange={(e) => setTier(Number(e.target.value))}>
              {ks3Years(track).map((y, i) => (
                <option key={y.year} value={i}>{y.label}: {(shownRow?.[i] || info.gbp[i] || gbpPrice).label} a year</option>
              ))}
            </Select>
          </Field>
          <p className="text-xs text-ink-subtle">No free week yet? <a href={G ? G.trial : "/ks3/trial"} className="font-medium text-brand-600 hover:underline">Start one first</a>, it&apos;s free.</p>
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
                <p className="text-sm text-ink">Send <b>{local ? priceOf(a).label : fallback.label}</b> · reference: your child&apos;s name</p>
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
            <PayerDetailsFields country={form.payer_country} dob={form.payer_dob}
              onCountry={(v) => setForm((f) => ({ ...f, payer_country: v }))} onDob={(v) => setForm((f) => ({ ...f, payer_dob: v }))} />
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
