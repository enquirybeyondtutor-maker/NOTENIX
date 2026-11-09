"use client";
import { useEffect, useState } from "react";
import { Sparkles, Check } from "lucide-react";
import { satAPI, satCurrency, type Price } from "@/lib/satApi";
import { saveAuth } from "@/lib/api";
import { useCountry } from "@/lib/country";
import { Button } from "@/components/ui/Button";
import { Input, Field } from "@/components/ui/Input";

/** Free 7-day Notenix SAT trial: student's email → code → password → signed in.
 *  A diagnostic taken before signing up is passed in and saved to the new account. */
export default function TrialSignup({ diagnosticAnswers, onDone }: { diagnosticAnswers?: Record<string, string>; onDone?: () => void }) {
  const country = useCountry();
  const [price, setPrice] = useState<Price | null>(null);
  const [step, setStep] = useState<"details" | "code" | "password">("details");
  const [f, setF] = useState({ full_name: "", email: "", parent_email: "", test_date: "", target: "", agree: false });
  const [code, setCode] = useState("");
  const [token, setToken] = useState("");
  const [pw, setPw] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => { if (country) satAPI.price(satCurrency(country)).then((r) => setPrice(r.data)).catch(() => {}); }, [country]);
  const set = (k: keyof typeof f) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setF((x) => ({ ...x, [k]: e.target.type === "checkbox" ? e.target.checked : e.target.value }));

  const run = async (fn: () => Promise<void>) => {
    setBusy(true); setError("");
    try { await fn(); } catch (e: any) { setError(e.response?.data?.detail || "Something went wrong. Please try again."); } finally { setBusy(false); }
  };
  const start = (e: React.FormEvent) => { e.preventDefault(); run(async () => {
    const { data } = await satAPI.trialStart({
      full_name: f.full_name, email: f.email, parent_email: f.parent_email || undefined,
      test_date: f.test_date || undefined, target: f.target ? Number(f.target) : undefined,
      currency: satCurrency(country), agree_terms: f.agree,
    });
    if (data.dev_otp) setCode(data.dev_otp);
    setStep("code");
  }); };
  const verify = (e: React.FormEvent) => { e.preventDefault(); run(async () => {
    const { data } = await satAPI.trialVerify(f.email, code);
    setToken(data.setup_token);
    setStep("password");
  }); };
  const complete = (e: React.FormEvent) => { e.preventDefault(); run(async () => {
    const { data } = await satAPI.trialComplete({ email: f.email, setup_token: token, password: pw, diagnostic_answers: diagnosticAnswers });
    saveAuth(data.access_token, data.user);
    onDone?.();
    window.location.href = "/sat/practice";
  }); };

  return (
    <div className="card p-6">
      <div className="flex items-center gap-2 text-sm font-semibold text-brand-700"><Sparkles size={16} /> Free for 7 days</div>
      <h2 className="mt-1 text-xl font-bold text-ink">Start your free SAT week</h2>
      <ul className="mt-3 space-y-1.5 text-sm text-ink-muted">
        {["Full-length adaptive practice tests with Desmos", "Score out of 1600 with a skill-by-skill report",
          "Worked explanations for every question", diagnosticAnswers ? "Keeps this diagnostic in your account" : "Track your score up to test day"]
          .map((x) => <li key={x} className="flex gap-2"><Check size={15} className="mt-0.5 shrink-0 text-emerald-600" /> {x}</li>)}
      </ul>

      {step === "details" && (
        <form onSubmit={start} className="mt-5 space-y-3">
          <Field label="Your name"><Input required value={f.full_name} onChange={set("full_name")} placeholder="e.g. Aisha Khan" /></Field>
          <Field label="Your email" hint="You'll sign in with this."><Input required type="email" value={f.email} onChange={set("email")} placeholder="you@example.com" /></Field>
          <Field label="Parent's email (optional)" hint="For a weekly progress update."><Input type="email" value={f.parent_email} onChange={set("parent_email")} /></Field>
          <div className="grid grid-cols-2 gap-3">
            <Field label="SAT date (optional)"><Input type="date" value={f.test_date} onChange={set("test_date")} /></Field>
            <Field label="Target score"><Input type="number" min={400} max={1600} step={10} value={f.target} onChange={set("target")} placeholder="1400" /></Field>
          </div>
          <label className="flex items-start gap-2 text-xs text-ink-muted">
            <input type="checkbox" checked={f.agree} onChange={set("agree")} className="mt-0.5" />
            <span>I agree to the <a href="/terms" className="underline">Terms</a> and <a href="/privacy" className="underline">Privacy policy</a>.</span>
          </label>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <Button type="submit" loading={busy} className="w-full">Email me a code</Button>
          {price && <p className="text-center text-xs text-ink-subtle">No card needed. After your free week, a full year is {price.label}.</p>}
        </form>
      )}
      {step === "code" && (
        <form onSubmit={verify} className="mt-5 space-y-3">
          <p className="text-sm text-ink">We&apos;ve emailed a 6-digit code to <b>{f.email}</b>.</p>
          <Field label="Code"><Input required inputMode="numeric" value={code} onChange={(e) => setCode(e.target.value)} placeholder="123456" /></Field>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <Button type="submit" loading={busy} className="w-full">Confirm</Button>
        </form>
      )}
      {step === "password" && (
        <form onSubmit={complete} className="mt-5 space-y-3">
          <p className="text-sm text-ink">Email confirmed. Choose a password: you&apos;ll sign in with <b>{f.email}</b>.</p>
          <Field label="Password" hint="At least 8 characters."><Input required type="password" minLength={8} value={pw} onChange={(e) => setPw(e.target.value)} /></Field>
          {error && <p className="text-sm text-red-600">{error}</p>}
          <Button type="submit" loading={busy} className="w-full">Start my free week</Button>
        </form>
      )}
    </div>
  );
}
