"use client";
import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { MailCheck, ArrowRight, AlertCircle, CheckCircle2 } from "lucide-react";
import { authAPI, saveAuth } from "@/lib/api";
import { Logo } from "@/components/ui/Logo";
import { Button } from "@/components/ui/Button";
import { Field } from "@/components/ui/Input";

export default function VerifyEmailPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [returnTo, setReturnTo] = useState<string | null>(null);
  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [cooldown, setCooldown] = useState(0);
  const didAutoResend = useRef(false);

  // Read query params on mount (avoids useSearchParams Suspense requirement).
  useEffect(() => {
    const qs = new URLSearchParams(window.location.search);
    const e = (qs.get("email") || "").toLowerCase();
    setEmail(e);
    setReturnTo(qs.get("returnTo"));
    if (!e) {
      setError("Missing email — please sign up again.");
      return;
    }
    if (qs.get("sent") === "1") {
      setNotice(`We emailed a 6-digit code to ${e}. Enter it below.`);
      setCooldown(60);
    }
    if (qs.get("resend") === "1" && !didAutoResend.current) {
      didAutoResend.current = true;
      authAPI
        .resendOtp(e)
        .then(() => {
          setNotice(`We emailed a fresh code to ${e}. Enter it below.`);
          setCooldown(60);
        })
        .catch((err) => setError(err.response?.data?.detail || "Couldn't send a code."));
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Countdown for the resend cooldown.
  useEffect(() => {
    if (cooldown <= 0) return;
    const t = setTimeout(() => setCooldown((c) => c - 1), 1000);
    return () => clearTimeout(t);
  }, [cooldown]);

  const verify = async (ev: React.FormEvent) => {
    ev.preventDefault();
    if (code.trim().length !== 6) {
      setError("Enter the 6-digit code from your email.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await authAPI.verifyOtp(email, code.trim());
      saveAuth(res.data.access_token, res.data.user);
      const role = res.data.user?.role;
      router.push(returnTo || (role === "teacher" || role === "admin" ? "/teacher" : "/dashboard"));
    } catch (err: any) {
      setError(err.response?.data?.detail || "Verification failed. Please try again.");
      setLoading(false);
    }
  };

  const resend = async () => {
    if (cooldown > 0 || !email) return;
    setError("");
    try {
      await authAPI.resendOtp(email);
      setNotice(`A new code is on its way to ${email}.`);
      setCooldown(60);
    } catch (err: any) {
      const wait = err.response?.data?.detail || "Please wait before requesting another code.";
      setError(wait);
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
              One quick step <br /> to secure your account.
            </h2>
            <p className="mt-4 max-w-sm text-brand-100">
              We verify every email so teachers and students can trust who's on the platform.
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
            <MailCheck size={22} />
          </span>
          <h1 className="mt-4 text-2xl font-bold text-ink">Verify your email</h1>
          <p className="mt-1.5 text-sm text-ink-muted">
            {email ? <>Enter the 6-digit code we sent to <span className="font-medium text-ink">{email}</span>.</> : "Enter your verification code."}
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

          <form onSubmit={verify} className="mt-6 space-y-4">
            <Field label="Verification code">
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
            <Button type="submit" loading={loading} size="lg" className="w-full">
              {loading ? "Verifying…" : <>Verify &amp; continue <ArrowRight size={16} /></>}
            </Button>
          </form>

          <div className="mt-6 text-center text-sm text-ink-muted">
            Didn&apos;t get it?{" "}
            <button
              onClick={resend}
              disabled={cooldown > 0}
              className="font-semibold text-brand-600 hover:text-brand-700 disabled:cursor-not-allowed disabled:text-ink-subtle"
            >
              {cooldown > 0 ? `Resend in ${cooldown}s` : "Resend code"}
            </button>
          </div>
          <p className="mt-4 text-center text-xs text-ink-subtle">
            Wrong email?{" "}
            <Link href="/register" className="font-medium text-ink-muted hover:text-ink">
              Sign up again
            </Link>
          </p>
        </div>
      </main>
    </div>
  );
}
