"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight, AlertCircle, CheckCircle2 } from "lucide-react";
import { saveAuth } from "@/lib/api";
import { doubtAPI, SG_LEVELS } from "@/lib/doubtApi";
import { Button } from "@/components/ui/Button";
import { Input, Field } from "@/components/ui/Input";

/** Free Ask a Tutor trial: child + level + parent email → code → @notenix.com ID → password. */
export default function SignUp() {
  const router = useRouter();
  const [step, setStep] = useState<"details" | "code" | "password" | "done">("details");
  const [childName, setChildName] = useState("");
  const [level, setLevel] = useState("Sec 1");
  const [parentEmail, setParentEmail] = useState("");
  const [agreed, setAgreed] = useState(false);
  const [code, setCode] = useState("");
  const [loginId, setLoginId] = useState("");
  const [token, setToken] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [cooldown, setCooldown] = useState(0);
  const first = childName.split(" ")[0] || "your child";

  useEffect(() => {
    if (cooldown <= 0) return;
    const t = setTimeout(() => setCooldown((c) => c - 1), 1000);
    return () => clearTimeout(t);
  }, [cooldown]);

  const run = async (fn: () => Promise<void>, fallback: string) => {
    setLoading(true);
    setError("");
    try { await fn(); } catch (err: any) { setError(err.response?.data?.detail || fallback); } finally { setLoading(false); }
  };

  const sendCode = (e?: React.FormEvent) => {
    e?.preventDefault();
    run(async () => {
      await doubtAPI.startTrial({ child_name: childName, level, parent_email: parentEmail, agree_terms: agreed });
      setStep("code");
      setCooldown(60);
    }, "Couldn't send the code. Please try again.");
  };
  const verify = (e: React.FormEvent) => {
    e.preventDefault();
    run(async () => {
      const { data } = await doubtAPI.verifyTrial({ parent_email: parentEmail, code });
      setLoginId(data.login_id);
      setToken(data.setup_token);
      setStep("password");
    }, "Couldn't check the code.");
  };
  const complete = (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirm) return setError("The two passwords don't match.");
    run(async () => {
      const { data } = await doubtAPI.completeTrial({ parent_email: parentEmail, setup_token: token, password });
      saveAuth(data.access_token, data.user);
      setStep("done");
    }, "Couldn't start the trial.");
  };

  const select = "w-full rounded-lg border border-line bg-white px-3.5 py-2.5 text-sm text-ink outline-none focus:border-brand-500";
  return (
    <div id="start" className="card scroll-mt-24 p-6 shadow-xl">
      {step === "done" ? (
        <div>
          <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700"><CheckCircle2 size={14} /> Trial started</span>
          <h2 className="mt-3 text-xl font-bold text-ink">{first}&apos;s free trial is on</h2>
          <div className="mt-4 rounded-xl border border-line bg-brand-50 p-4">
            <div className="text-xs text-ink-muted">{first}&apos;s Notenix user ID</div>
            <div className="mt-1 font-mono text-base font-semibold text-ink">{loginId}</div>
            <div className="mt-1 text-xs text-ink-muted">Use it with the password you just chose. We&apos;ve emailed it to you too.</div>
          </div>
          <Button size="lg" className="mt-5 w-full" onClick={() => router.push("/help")}>Ask the first question <ArrowRight size={16} /></Button>
        </div>
      ) : (
        <>
          <h2 className="text-xl font-bold text-ink">Try it free: 5 questions in 7 days</h2>
          <p className="mt-1 text-sm text-ink-muted">No card, no commitment. Takes a minute.</p>
          {error && <div className="mt-4 flex items-start gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600"><AlertCircle size={16} className="mt-0.5 shrink-0" /> {error}</div>}
          {step === "code" && !error && <div className="mt-4 flex items-start gap-2 rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700"><CheckCircle2 size={16} className="mt-0.5 shrink-0" /> We&apos;ve emailed a 6-digit code to {parentEmail}.</div>}

          {step === "details" && (
            <form onSubmit={sendCode} className="mt-5 space-y-4">
              <Field label="Your child's name"><Input required value={childName} onChange={(e) => setChildName(e.target.value)} placeholder="e.g. Mei Ling Tan" /></Field>
              <Field label="Level">
                <select value={level} onChange={(e) => setLevel(e.target.value)} className={select}>
                  {SG_LEVELS.map((l) => <option key={l}>{l}</option>)}
                </select>
              </Field>
              <Field label="Your email (parent or guardian)"><Input type="email" required value={parentEmail} onChange={(e) => setParentEmail(e.target.value)} placeholder="you@example.com" autoComplete="email" /></Field>
              <label className="flex items-start gap-2.5 text-sm text-ink">
                <input type="checkbox" checked={agreed} onChange={(e) => setAgreed(e.target.checked)} className="mt-0.5 h-4 w-4 shrink-0 accent-brand-600" />
                <span>I&apos;m the parent or guardian and agree to the <a href="/terms" target="_blank" className="font-semibold text-brand-600 hover:underline">Terms</a> and <a href="/privacy" target="_blank" className="font-semibold text-brand-600 hover:underline">Privacy policy</a>.</span>
              </label>
              <Button type="submit" loading={loading} disabled={!agreed} size="lg" className="w-full">{loading ? "Sending…" : <>Email me a code <ArrowRight size={16} /></>}</Button>
              <p className="text-center text-xs text-ink-subtle">Already have a login? <a href="/login" className="font-medium text-brand-600 hover:underline">Sign in</a></p>
            </form>
          )}
          {step === "code" && (
            <form onSubmit={verify} className="mt-5 space-y-4">
              <Field label="6-digit code">
                <input inputMode="numeric" autoComplete="one-time-code" maxLength={6} value={code} onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))} placeholder="••••••"
                  className="w-full rounded-lg border border-line bg-white px-3.5 py-3 text-center text-2xl font-semibold tracking-[0.5em] text-ink outline-none focus:border-brand-500" />
              </Field>
              <Button type="submit" loading={loading} disabled={code.length !== 6} size="lg" className="w-full">Confirm my email <ArrowRight size={16} /></Button>
              <div className="flex justify-between text-sm">
                <button type="button" onClick={() => { setStep("details"); setError(""); }} className="text-ink-muted hover:text-ink">Change details</button>
                <button type="button" onClick={() => sendCode()} disabled={cooldown > 0 || loading} className="font-semibold text-brand-600 disabled:text-ink-subtle">{cooldown > 0 ? `Resend in ${cooldown}s` : "Resend code"}</button>
              </div>
            </form>
          )}
          {step === "password" && (
            <form onSubmit={complete} className="mt-5 space-y-4">
              <div className="rounded-xl border border-line bg-brand-50 p-4">
                <div className="text-xs text-ink-muted">Email confirmed. {first}&apos;s Notenix user ID is</div>
                <div className="mt-1 font-mono text-base font-semibold text-ink">{loginId}</div>
              </div>
              <Field label="Choose a password"><Input type="password" required minLength={8} value={password} onChange={(e) => setPassword(e.target.value)} placeholder="At least 8 characters" autoComplete="new-password" /></Field>
              <Field label="Type it again"><Input type="password" required minLength={8} value={confirm} onChange={(e) => setConfirm(e.target.value)} autoComplete="new-password" /></Field>
              <Button type="submit" loading={loading} size="lg" className="w-full">Start the free trial <ArrowRight size={16} /></Button>
            </form>
          )}
        </>
      )}
    </div>
  );
}
