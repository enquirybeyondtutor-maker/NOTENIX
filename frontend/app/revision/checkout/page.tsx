"use client";
import { useEffect, useState } from "react";
import { Landmark, CheckCircle2, Lock, ShieldCheck } from "lucide-react";
import { paymentsAPI } from "@/lib/api";
import { coursesAPI, type Course } from "@/lib/coursesApi";
import CoursePicker from "@/components/CoursePicker";
import { safeReturnTo } from "@/lib/utils";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Input, Select, Field } from "@/components/ui/Input";
import PayLink from "@/components/PayLink";
import { type Account, useCountry, useRates, pickAccounts, priceFor, countryName } from "@/lib/country";

// One course a year for students outside Beyond Tutors: GCSE £99 a subject, all four GCSEs £349
// (?course=gcse-bundle), SAT £99, anything else £149. The backend prices the chosen course.
// Payment is by card (Wise link, £149 courses only) or bank transfer: the student tells us here,
// and an admin confirms it in /admin/requests, which switches the course on for a year.

const BUNDLE = "gcse-bundle";
const BUNDLE_NAME = "GCSE Maths, Biology, Chemistry and Physics";

export default function RevisionCheckout() {
  const [info, setInfo] = useState<{ accounts: Account[]; price: number; currency: string; pay_link?: string; standard_price?: number } | null>(null);
  const [returnTo, setReturnTo] = useState<string | null>(null);
  const [form, setForm] = useState({ course: "", full_name: "", email: "", password: "", paid_via: "", payer_name: "", payer_note: "" });
  const [catalogue, setCatalogue] = useState<Course[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState<{ reference: string; login_id?: string } | null>(null);
  const country = useCountry();
  const rates = useRates();

  useEffect(() => {
    const qs = new URLSearchParams(window.location.search);
    setReturnTo(safeReturnTo(qs.get("returnTo")));
    coursesAPI.catalogue().then((r) => {
      setCatalogue(r.data);
      const want = qs.get("course");
      if (want && (want === BUNDLE || r.data.some((c) => c.key === want))) setForm((f) => ({ ...f, course: want }));
    }).catch(() => {});
  }, []);

  // The price depends on the course (GCSE and SAT £99, the GCSE bundle £349, others £149).
  useEffect(() => {
    paymentsAPI.revisionInfo(form.course || undefined)
      .then((r) => { setInfo(r.data); setForm((f) => ({ ...f, paid_via: f.paid_via || r.data.accounts?.[0]?.label || "" })); })
      .catch(() => setInfo((i) => i ?? { accounts: [], price: 149, currency: "GBP" }));
  }, [form.course]);
  const courseName = form.course === BUNDLE ? BUNDLE_NAME : catalogue.find((c) => c.key === form.course)?.name;

  const set = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) =>
    setForm((f) => ({ ...f, [k]: e.target.value }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.course) { setError("Please choose your course."); return; }
    setBusy(true); setError("");
    try {
      const { data } = await paymentsAPI.revisionCheckout(form);
      setDone({ reference: data.reference, login_id: data.login_id });
    } catch (err: any) {
      setError(err.response?.data?.detail || "Couldn't send that. Please try again.");
    } finally {
      setBusy(false);
    }
  };

  // Once the country is known, preselect its local account in "Account you paid into".
  useEffect(() => {
    if (!info) return;
    const { shown } = pickAccounts(info.accounts, country);
    if (shown[0]) setForm((f) => ({ ...f, paid_via: shown[0].label }));
  }, [info, country]);

  if (!info) return <Spinner label="Loading checkout…" />;
  const gbpPrice = `${info.currency === "GBP" ? "£" : info.currency + " "}${info.price}`;
  // Only the visitor's own country's account (else the GBP ones), priced in its currency.
  const { shown, local } = pickAccounts(info.accounts, country);
  const price = local ? priceFor(info.price, shown[0], rates) : gbpPrice;

  if (done) {
    return (
      <PageContainer className="max-w-xl">
        <div className="card p-8 text-center">
          <span className="mx-auto grid h-14 w-14 place-items-center rounded-full bg-emerald-50 text-emerald-600"><CheckCircle2 size={28} /></span>
          <h1 className="mt-4 text-2xl font-bold text-ink">Payment received for checking</h1>
          <p className="mt-2 text-sm text-ink-muted">
            Reference <b className="font-mono text-ink">{done.reference}</b>. We match it to our bank account, usually within a few hours,
            then email you. {courseName || "Your course"} {form.course === BUNDLE ? "switch" : "switches"} on for a year as soon as it&apos;s confirmed.
          </p>
          {done.login_id && (
            <div className="mx-auto mt-5 max-w-sm rounded-xl border border-brand-200 bg-brand-50/60 p-4 text-left text-sm">
              <p className="font-semibold text-ink">Your Notenix login</p>
              <p className="mt-2 text-ink-muted">User ID</p>
              <p className="font-mono text-base font-semibold text-ink">{done.login_id}</p>
              <p className="mt-2 text-ink-muted">Password: the one you just chose.</p>
              <p className="mt-2 text-xs text-ink-muted">Save this user ID: you sign in with it, not your email. It&apos;s also in the confirmation we email to {form.email} once your payment is checked.</p>
            </div>
          )}
          <Button href={`/login${returnTo ? `?returnTo=${encodeURIComponent(returnTo)}` : ""}`} className="mt-6">Go to sign in</Button>
        </div>
      </PageContainer>
    );
  }

  return (
    <PageContainer className="max-w-3xl">
      <p className="text-sm font-semibold text-brand-600">Notenix course access</p>
      <h1 className="mt-1 text-2xl font-bold tracking-tight text-ink sm:text-3xl">
        {form.course ? <>{courseName}: {price} / year</> : <>{price} / year per course</>}
      </h1>
      <p className="mt-1 text-sm text-ink-muted">
        {form.course === BUNDLE
          ? "All four GCSE sciences and maths for a year: diagnostics, topic drills, practice papers and tutor-marked test requests."
          : "Practice papers, revision resources and tutor-marked test requests for your course. GCSE and SAT £99, other courses £149. Add more courses any time."}
      </p>

      <form onSubmit={submit} className="mt-6 space-y-6">
        <div className="card space-y-4 p-6">
          <h2 className="font-semibold text-ink">1. Your course and Notenix account</h2>
          <Field label="Course" hint="e.g. GCSE Biology, IGCSE Chemistry, A-Level Maths, TMUA. Each course is a separate purchase; the price updates when you choose.">
            {form.course === BUNDLE ? (
              <div className="flex items-center justify-between gap-3 rounded-lg border border-brand-200 bg-brand-50/50 px-3.5 py-2.5 text-sm">
                <span className="font-medium text-ink">{BUNDLE_NAME} <span className="text-ink-muted">(all four GCSEs)</span></span>
                <button type="button" onClick={() => setForm((f) => ({ ...f, course: "" }))}
                  className="shrink-0 font-semibold text-brand-600 hover:text-brand-700">Change</button>
              </div>
            ) : (
              <CoursePicker catalogue={catalogue} value={form.course} onChange={(k) => setForm((f) => ({ ...f, course: k }))}
                placeholder="Choose your course…"
                className="w-full rounded-lg border border-line bg-white px-3.5 py-2.5 text-sm text-ink outline-none focus:border-brand-500" />
            )}
          </Field>
          <Field label="Student's full name"><Input required value={form.full_name} onChange={set("full_name")} placeholder="e.g. Priya Patel" /></Field>
          <Field label="Email" hint="We send your receipt and updates here. Your Notenix user ID is made from the student's name, e.g. priya@notenix.com.">
            <Input required type="email" value={form.email} onChange={set("email")} placeholder="you@example.com" /></Field>
          <Field label="Choose a password" hint="At least 8 characters. You'll sign in with your Notenix user ID and this password.">
            <Input required type="password" minLength={8} value={form.password} onChange={set("password")} />
          </Field>
        </div>

        <div className="card space-y-4 p-6">
          <h2 className="flex items-center gap-2 font-semibold text-ink"><Landmark size={16} /> 2. Pay {price}</h2>
          {info.pay_link && <PayLink href={info.pay_link} label={`Pay ${local ? "by card" : `${price} now`}`}
            hint={local ? `Card or Apple/Google Pay through Wise. Charged as ${gbpPrice}; your bank converts it.` : undefined} />}
          {info.pay_link && shown.length > 0 && (
            <p className="text-xs font-medium uppercase tracking-wide text-ink-subtle">Or pay by bank transfer</p>
          )}
          {info.accounts.length === 0 ? (info.pay_link ? null :
            <p className="rounded-lg bg-slate-50 p-4 text-sm text-ink-muted">Bank details aren&apos;t set up yet. Email support@notenix.com and we&apos;ll send them.</p>
          ) : (
            shown.map((a) => (
              <div key={a.label} className={`space-y-3 rounded-lg border p-4 ${local ? "border-brand-300 bg-brand-50/40" : "border-line"}`}>
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <p className="text-sm font-semibold text-ink">{a.label}</p>
                  {local && <span className="rounded-full bg-brand-600 px-2.5 py-0.5 text-[11px] font-semibold text-white">For {countryName(country)}</span>}
                </div>
                {local && <p className="text-sm text-ink">Send <b>{priceFor(info.price, a, rates)}</b></p>}
                {a.pay_link && <PayLink href={a.pay_link} label={`Pay ${priceFor(info.price, a, rates)} now`} />}
                <dl className="mt-2 grid grid-cols-[auto,1fr] gap-x-4 gap-y-1 text-sm">
                  {Object.entries(a.details).map(([k, v]) => (
                    <div key={k} className="contents"><dt className="text-ink-muted">{k}</dt><dd className="font-mono text-ink">{v}</dd></div>
                  ))}
                </dl>
                {a.note && <p className="text-xs text-ink-subtle">{a.note}</p>}
              </div>
            ))
          )}
          <p className="text-xs text-ink-muted">Pay exactly {price}, then fill in the details below so we can match your payment.</p>
          <div className="grid gap-4 sm:grid-cols-2">
            {shown.length > 1 && (
              <Field label="Account you paid into">
                <Select value={form.paid_via} onChange={set("paid_via")}>
                  {shown.map((a) => <option key={a.label}>{a.label}</option>)}
                </Select>
              </Field>
            )}
            <Field label="Name of the person who paid"><Input required value={form.payer_name} onChange={set("payer_name")} placeholder="e.g. R Patel" /></Field>
            <Field label="Wise or bank reference" hint="Optional: helps us find it faster.">
              <Input value={form.payer_note} onChange={set("payer_note")} placeholder="e.g. Barclays, ref 48213" />
            </Field>
          </div>
        </div>

        {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
        <Button type="submit" loading={busy} className="w-full"><Lock size={15} /> I&apos;ve paid {price} · create my account</Button>
        <p className="flex items-center justify-center gap-1.5 text-xs text-ink-muted">
          <ShieldCheck size={13} /> We never ask for card numbers or bank passwords. Access starts once we confirm your payment.
        </p>
      </form>
    </PageContainer>
  );
}
