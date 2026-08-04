"use client";
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Mail, Lock, ArrowRight, AlertCircle } from "lucide-react";
import { authAPI, saveAuth } from "@/lib/api";
import { Logo } from "@/components/ui/Logo";
import { Button } from "@/components/ui/Button";
import { Input, Field } from "@/components/ui/Input";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await authAPI.login(email, password);
      saveAuth(res.data.access_token, res.data.user);
      const role = res.data.user?.role;
      const returnTo = new URLSearchParams(window.location.search).get("returnTo");
      router.push(returnTo || (role === "teacher" || role === "admin" ? "/teacher" : "/dashboard"));
    } catch (err: any) {
      const status = err.response?.status;
      const detail: string = err.response?.data?.detail || "";
      // Unverified account — send them to the verification screen (auto-resends a code).
      if (status === 403 && detail.toLowerCase().includes("verify")) {
        router.push(`/verify-email?email=${encodeURIComponent(email.toLowerCase())}&resend=1`);
        return;
      }
      setError(detail || "Login failed. Check your credentials.");
    } finally {
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
              Set, sit and score — <br /> all in one portal.
            </h2>
            <p className="mt-4 max-w-sm text-brand-100">
              Notenix brings assessment creation, assignment, sitting and AI marking into a single
              workflow for UK schools.
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
          <h1 className="text-2xl font-bold text-ink">Welcome back</h1>
          <p className="mt-1.5 text-sm text-ink-muted">Sign in to your Notenix account.</p>

          {error && (
            <div className="mt-6 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
              <AlertCircle size={16} /> {error}
            </div>
          )}

          <form onSubmit={handleLogin} className="mt-6 space-y-4">
            <Field label="Email">
              <div className="relative">
                <Mail size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-ink-subtle" />
                <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required placeholder="you@school.co.uk" className="pl-9" />
              </div>
            </Field>
            <Field label="Password">
              <div className="relative">
                <Lock size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-ink-subtle" />
                <Input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required placeholder="••••••••" className="pl-9" />
              </div>
            </Field>
            <Button type="submit" loading={loading} size="lg" className="w-full">
              {loading ? "Signing in…" : <>Sign in <ArrowRight size={16} /></>}
            </Button>
          </form>

          <p className="mt-6 text-center text-sm text-ink-muted">
            Don&apos;t have an account?{" "}
            <Link href="/register" className="font-semibold text-brand-600 hover:text-brand-700">
              Create one free
            </Link>
          </p>
        </div>
      </main>
    </div>
  );
}
