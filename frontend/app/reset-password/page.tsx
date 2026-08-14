"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { KeyRound, Lock, ArrowRight, AlertCircle, CheckCircle2 } from "lucide-react";
import { authAPI, saveAuth } from "@/lib/api";
import { Logo } from "@/components/ui/Logo";
import { Button } from "@/components/ui/Button";
import { Input, Field } from "@/components/ui/Input";

export default function ResetPasswordPage() {
  const router = useRouter();
  const [step, setStep] = useState<"email" | "reset">("email");
  const [email, setEmail] = useState("");
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [cooldown, setCooldown] = useState(0);

  // Prefill email if passed from the login page.
  useEffect(() => {
    const e = (new URLSearchParams(window.location.search).get("email") || "").toLowerCase();
    if (e) setEmail(e);
  }, []);

  useEffect(() => {
    if (cooldown <= 0) return;
    const t = setTimeout(() => setCooldown((c) => c - 1), 1000);
    return () => clearTimeout(t);
  }, [cooldown]);

  const sendCode = async (ev: React.FormEvent) => {
    ev.preventDefault();
    if (!email.trim()) { setError("Enter your account email."); return; }
    setLoading(true);
    setError("");
    try {
      await authAPI.forgotPassword(email.trim().toLowerCase());
      setStep("reset");
      setNotice(`If an account exists for ${email.toLowerCase()}, we've sent a 6-digit reset code. Enter it below.`);
      setCooldown(60);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Couldn't send a reset code. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const resend = async () => {
    if (cooldown > 0 || !email) return;
    setError("");
    try {
      await authAPI.forgotPassword(email.trim().toLowerCase());
      setNotice(`A new code is on its way to ${email.toLowerCase()}.`);
      setCooldown(60);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Please wait before requesting another code.");
    }
  };

  const reset = async (ev: React.FormEvent) => {
    ev.preventDefault();
    if (code.trim().length !== 6) { setError("Enter the 6-digit code from your email."); return; }
    if (password.length < 8) { setError("Your new password must be at least 8 characters."); return; }
    setLoading(true);
    setError("");
    try {
      const res = await authAPI.resetPassword(email.trim().toLowerCase(), code.trim(), password);
      saveAuth(res.data.access_token, res.data.user);
      const role = res.data.user?.role;
      router.push(role === "teacher" || role === "admin" ? "/teacher" : "/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Couldn't reset your password. Please try again.");
      setLoading(false);
    }
  };

  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      {/* Brand panel */}
      <aside className="relative hidden overflow-hidden bg-brand-600 lg:block">
        <div className="dotted-grid absolute inset-0 opacity-20" />
        <div className="relative flex h-full flex-col justify-between p-12">
          <Logo href="/" light />
          <div>
            <h2 className="text-3xl font-bold leading-tight text-white">
              Locked out? <br /> Let's get you back in.
            </h2>
            <p className="mt-4 max-w-sm text-brand-100">
              We'll email you a one-time code so you can set a new password securely.
            </p>
          </div>
          <p className="text-sm text-brand-200">© {new Date().getFullYear()} Notenix · Beyond Imagination</p>
        </div>
      </aside>

      {/* Form panel */}
      <main className="flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-sm">
          <div className="mb-8 lg:hidden">
            <Logo href="/" />
          </div>
          <span className="grid h-11 w-11 place-items-center rounded-xl bg-brand-50 text-brand-600">
            <KeyRound size={22} />
          </span>
          <h1 className="mt-4 text-2xl font-bold text-ink">Reset your password</h1>
          <p className="mt-1.5 text-sm text-ink-muted">
            {step === "email"
              ? "Enter your account email and we'll send you a reset code."
              : "Enter the code we emailed you and choose a new password."}
          </p>

          {notice && (
            <div className="mt-5 flex items-start gap-2 rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
              <CheckCircle2 size={16} className="mt-0.5 shrink-0" /> {notice}
            </div>
          )}
          {error && (
            <div className="mt-5 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
              <AlertCircle size={16} /> {error}
            </div>
          )}

          {step === "email" ? (
            <form onSubmit={sendCode} className="mt-6 space-y-4">
              <Field label="Email">
                <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required placeholder="you@school.co.uk" />
              </Field>
              <Button type="submit" loading={loading} size="lg" className="w-full">
                {loading ? "Sending…" : <>Send reset code <ArrowRight size={16} /></>}
              </Button>
            </form>
          ) : (
            <form onSubmit={reset} className="mt-6 space-y-4">
              <Field label="Reset code">
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
              <Field label="New password" hint="At least 8 characters.">
                <div className="relative">
                  <Lock size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-ink-subtle" />
                  <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required placeholder="••••••••" className="pl-9" />
                </div>
              </Field>
              <Button type="submit" loading={loading} size="lg" className="w-full">
                {loading ? "Resetting…" : <>Reset password <ArrowRight size={16} /></>}
              </Button>
              <div className="text-center text-sm text-ink-muted">
                Didn&apos;t get it?{" "}
                <button
                  type="button"
                  onClick={resend}
                  disabled={cooldown > 0}
                  className="font-semibold text-brand-600 hover:text-brand-700 disabled:cursor-not-allowed disabled:text-ink-subtle"
                >
                  {cooldown > 0 ? `Resend in ${cooldown}s` : "Resend code"}
                </button>
              </div>
            </form>
          )}

          <p className="mt-6 text-center text-sm text-ink-muted">
            Remembered it?{" "}
            <Link href="/login" className="font-semibold text-brand-600 hover:text-brand-700">
              Back to sign in
            </Link>
          </p>
        </div>
      </main>
    </div>
  );
}
