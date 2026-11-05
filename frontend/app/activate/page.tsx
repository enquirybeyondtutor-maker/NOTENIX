"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ShieldCheck, ArrowRight, AlertCircle, CheckCircle2 } from "lucide-react";
import { authAPI, saveAuth, getUser, logout } from "@/lib/api";
import { Logo } from "@/components/ui/Logo";
import { Button } from "@/components/ui/Button";
import { Input, Field } from "@/components/ui/Input";

/**
 * Parent activation for a Beyond Tutors-issued student account.
 * Step 1: parent's email + mobile → a 6-digit code is emailed to the parent.
 * Step 2: code + new password → account active, dashboard opens.
 */
export default function ActivatePage() {
  const router = useRouter();
  const [student, setStudent] = useState<any | null>(null);
  const [step, setStep] = useState<"details" | "code">("details");
  const [parentEmail, setParentEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [agreed, setAgreed] = useState(false);
  const [showTerms, setShowTerms] = useState(false);
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [cooldown, setCooldown] = useState(0);

  useEffect(() => {
    if (!localStorage.getItem("notenix_token")) {
      router.replace("/login");
      return;
    }
    setStudent(getUser());
    authAPI
      .me()
      .then(({ data }) => {
        if (!data.needs_activation) {
          router.replace(data.role === "teacher" || data.role === "admin" ? "/teacher" : "/dashboard");
          return;
        }
        setStudent(data);
      })
      .catch(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (cooldown <= 0) return;
    const t = setTimeout(() => setCooldown((c) => c - 1), 1000);
    return () => clearTimeout(t);
  }, [cooldown]);

  const sendCode = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!agreed) return setError("Please tick the box to agree to the Terms and Conditions.");
    setLoading(true);
    setError("");
    try {
      const { data } = await authAPI.activationSendCode(parentEmail.trim(), phone.trim(), agreed);
      setStep("code");
      setNotice(`We emailed a 6-digit code to ${data.email}.` + (data.dev_otp ? ` (dev code: ${data.dev_otp})` : ""));
      setCooldown(60);
    } catch (err: any) {
      setError(err.response?.data?.detail?.toString() || "Couldn't send the code. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const activate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (code.trim().length !== 6) return setError("Enter the 6-digit code from your email.");
    if (password.length < 8) return setError("Your new password must be at least 8 characters.");
    if (password !== confirm) return setError("The two passwords don't match.");
    setLoading(true);
    setError("");
    try {
      const res = await authAPI.activationVerify(code.trim(), password);
      saveAuth(res.data.access_token, res.data.user);
      router.replace("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail?.toString() || "Activation failed. Please try again.");
      setLoading(false);
    }
  };

  const signOut = () => {
    logout();
  };

  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      <aside className="relative hidden overflow-hidden bg-brand-600 lg:block">
        <div className="dotted-grid absolute inset-0 opacity-20" />
        <div className="relative flex h-full flex-col justify-between p-12">
          <Logo href="/" light />
          <div>
            <h2 className="text-3xl font-bold leading-tight text-white">
              One last step <br /> before the first class.
            </h2>
            <p className="mt-4 max-w-sm text-brand-100">
              We confirm a parent&apos;s email and mobile number for every Beyond Tutors student, so we can
              reach you about classes, homework and progress.
            </p>
          </div>
          <p className="text-sm text-brand-200">© {new Date().getFullYear()} Notenix · A unit of Beyond Groups</p>
        </div>
      </aside>

      <main className="flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-sm">
          <div className="mb-8 lg:hidden">
            <Logo href="/" />
          </div>
          <span className="inline-flex items-center gap-1.5 rounded-full bg-amber-50 px-3 py-1 text-xs font-semibold text-amber-700">
            Pending activation
          </span>
          <h1 className="mt-3 text-2xl font-bold text-ink">Activate the account</h1>
          <p className="mt-1.5 text-sm text-ink-muted">
            {student ? (
              <>
                For <span className="font-medium text-ink">{student.full_name}</span> ·{" "}
                <span className="font-mono text-xs">{student.email}</span>
              </>
            ) : (
              "Confirm the parent's details to continue."
            )}
          </p>

          {notice && step === "code" && (
            <div className="mt-5 flex items-start gap-2 rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
              <CheckCircle2 size={16} className="mt-0.5 shrink-0" /> {notice}
            </div>
          )}
          {error && (
            <div className="mt-5 flex items-start gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
              <AlertCircle size={16} className="mt-0.5 shrink-0" /> {error}
            </div>
          )}

          {step === "details" ? (
            <form onSubmit={sendCode} className="mt-6 space-y-4">
              <Field label="Parent's email address">
                <Input type="email" required value={parentEmail}
                  onChange={(e) => setParentEmail(e.target.value)} placeholder="you@example.com" autoComplete="email" />
              </Field>
              <Field label="Parent's mobile number (with country code)">
                <Input type="tel" required value={phone}
                  onChange={(e) => setPhone(e.target.value)} placeholder="+44 7700 900123" autoComplete="tel" />
              </Field>
              <label className="flex items-start gap-2.5 text-sm text-ink">
                <input type="checkbox" checked={agreed} onChange={(e) => setAgreed(e.target.checked)}
                  className="mt-0.5 h-4 w-4 shrink-0 cursor-pointer accent-brand-600" />
                <span>
                  I am the parent or guardian and I agree to the{" "}
                  <button type="button" onClick={() => setShowTerms(true)}
                    className="font-semibold text-brand-600 underline-offset-2 hover:underline">
                    Terms and Conditions
                  </button>
                </span>
              </label>
              <Button type="submit" loading={loading} disabled={!agreed} size="lg" className="w-full">
                {loading ? "Sending…" : <>Send code to my email <ArrowRight size={16} /></>}
              </Button>
            </form>
          ) : (
            <form onSubmit={activate} className="mt-6 space-y-4">
              <Field label="6-digit code">
                <input
                  inputMode="numeric"
                  autoComplete="one-time-code"
                  maxLength={6}
                  value={code}
                  onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))}
                  placeholder="••••••"
                  className="w-full rounded-lg border border-line bg-white px-3.5 py-3 text-center text-2xl font-semibold tracking-[0.5em] text-ink outline-none transition-all placeholder:text-ink-subtle placeholder:tracking-[0.5em] focus:border-brand-500 focus:ring-4 focus:ring-brand-600/10"
                />
              </Field>
              <Field label="New password (replaces the one we sent)">
                <Input type="password" required value={password}
                  onChange={(e) => setPassword(e.target.value)} placeholder="At least 8 characters" autoComplete="new-password" />
              </Field>
              <Field label="Confirm new password">
                <Input type="password" required value={confirm}
                  onChange={(e) => setConfirm(e.target.value)} placeholder="Type it again" autoComplete="new-password" />
              </Field>
              <Button type="submit" loading={loading} size="lg" className="w-full">
                {loading ? "Activating…" : <><ShieldCheck size={16} /> Activate account</>}
              </Button>
              <div className="flex items-center justify-between text-sm">
                <button type="button" onClick={() => { setStep("details"); setError(""); }}
                  className="text-ink-muted hover:text-ink">
                  Change email or number
                </button>
                <button type="button" onClick={() => sendCode()} disabled={cooldown > 0 || loading}
                  className="font-semibold text-brand-600 hover:text-brand-700 disabled:cursor-not-allowed disabled:text-ink-subtle">
                  {cooldown > 0 ? `Resend in ${cooldown}s` : "Resend code"}
                </button>
              </div>
            </form>
          )}

          <p className="mt-8 text-center text-xs text-ink-subtle">
            Not you?{" "}
            <button onClick={signOut} className="font-medium text-ink-muted hover:text-ink">Sign out</button>
          </p>
        </div>
      </main>
      {showTerms && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 px-4"
          onClick={() => setShowTerms(false)}>
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl" onClick={(e) => e.stopPropagation()}
            role="dialog" aria-modal="true" aria-labelledby="terms-title">
            <h2 id="terms-title" className="text-lg font-bold text-ink">Terms and Conditions</h2>
            <ul className="mt-3 list-disc space-y-2 pl-5 text-sm leading-relaxed text-ink-muted">
              <li>This Notenix subscription is purchased through <b className="text-ink">Beyond Tutors</b>. Beyond Tutors
                provides Notenix to its students as part of its tuition.</li>
              <li>The subscription costs <b className="text-ink">£49 per year</b>. This payment is made to Beyond Tutors,
                not to Notenix.</li>
              <li>The £49 will be included in the <b className="text-ink">next invoice issued by Beyond Tutors</b>. No card
                details are taken here.</li>
            </ul>
            <p className="mt-3 text-xs text-ink-subtle">
              See also the full{" "}
              <a href="/terms" target="_blank" className="font-medium text-brand-600 hover:underline">Terms</a> and{" "}
              <a href="/privacy" target="_blank" className="font-medium text-brand-600 hover:underline">Privacy policy</a>.
            </p>
            <div className="mt-5 flex justify-end gap-2">
              <Button variant="secondary" size="sm" onClick={() => setShowTerms(false)}>Close</Button>
              <Button size="sm" onClick={() => { setAgreed(true); setShowTerms(false); }}>I agree</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
