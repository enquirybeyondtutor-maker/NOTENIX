"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Mail, Lock, User, ArrowRight, AlertCircle, GraduationCap, PenSquare, Check } from "lucide-react";
import { authAPI, saveAuth } from "@/lib/api";
import { Logo } from "@/components/ui/Logo";
import { Button } from "@/components/ui/Button";
import { Input, Field } from "@/components/ui/Input";
import { cn, safeReturnTo } from "@/lib/utils";
import ReturnNote from "@/components/ReturnNote";

type Role = "student" | "teacher";

const ROLES: { id: Role; title: string; desc: string; icon: typeof GraduationCap }[] = [
  { id: "student", title: "Student", desc: "Practise for your exams & track progress", icon: GraduationCap },
  { id: "teacher", title: "Teacher", desc: "Create, assign & mark assessments", icon: PenSquare },
];

// Accounts are issued by Beyond Tutors; set NEXT_PUBLIC_OPEN_SIGNUP=true (and OPEN_SIGNUP on the
// backend) to bring the self-signup form back.
const OPEN_SIGNUP = process.env.NEXT_PUBLIC_OPEN_SIGNUP === "true";

export default function RegisterPage() {
  return OPEN_SIGNUP ? <RegisterForm /> : <IssuedAccountsNotice />;
}

function IssuedAccountsNotice() {
  return (
    <main className="flex min-h-screen items-center justify-center px-4 py-12">
      <div className="w-full max-w-sm text-center">
        <div className="mb-8 flex justify-center"><Logo href="/" /></div>
        <h1 className="text-2xl font-bold text-ink">Accounts come from Beyond Tutors</h1>
        <p className="mt-3 text-sm text-ink-muted">
          Every Beyond Tutors student gets a Notenix login (like name@thebeyondtutors.com) with
          homework, tests and class notes. Book a free trial class and we&apos;ll set yours up.
        </p>
        <div className="mt-6 flex flex-col gap-2">
          <Button href="https://www.thebeyondtutors.com/book" size="lg">Book a free trial class</Button>
          <Button href="/login" variant="secondary" size="lg">I already have a login</Button>
        </div>
      </div>
    </main>
  );
}

function RegisterForm() {
  const router = useRouter();
  const [role, setRole] = useState<Role>("student");
  const [form, setForm] = useState({ full_name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [returnTo, setReturnTo] = useState<string | null>(null);

  useEffect(() => {
    setReturnTo(safeReturnTo(new URLSearchParams(window.location.search).get("returnTo")));
  }, []);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (form.password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }
    setLoading(true);
    setError("");
    try {
      await authAPI.register({ ...form, role });
      // Account created but unverified — a code was emailed. Go enter it.
      const qs = new URLSearchParams({ email: form.email.toLowerCase(), sent: "1" });
      if (returnTo) qs.set("returnTo", returnTo);
      router.push(`/verify-email?${qs.toString()}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const perks =
    role === "teacher"
      ? ["AI-generated, board-aligned questions", "Assign to whole classes in a click", "Automatic marking & cohort analytics", "No credit card required"]
      : ["Free practice questions for your exam", "Instant marks and worked solutions", "Tests from your tutor or teacher in one place", "No card needed to start"];

  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      {/* Brand / value panel */}
      <aside className="relative hidden overflow-hidden bg-brand-600 lg:block">
        <div className="dotted-grid absolute inset-0 opacity-20" />
        <div className="relative flex h-full flex-col justify-between p-12">
          <Logo href="/" light />
          <div>
            <h2 className="text-3xl font-bold leading-tight text-white">
              Practise smarter <br /> for your exams.
            </h2>
            <p className="mt-4 max-w-sm text-brand-100">
              Timed practice, instant marking and tutor-marked mocks for students anywhere in the world.
            </p>
            <ul className="mt-8 space-y-3">
              {perks.map((p) => (
                <li key={p} className="flex items-center gap-3 text-sm text-white">
                  <span className="grid h-5 w-5 place-items-center rounded-full bg-white/20">
                    <Check size={12} />
                  </span>
                  {p}
                </li>
              ))}
            </ul>
          </div>
          <p className="text-sm text-brand-200">© {new Date().getFullYear()} Notenix · A unit of Beyond Groups</p>
        </div>
      </aside>

      {/* Form panel */}
      <main className="flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-sm">
          <div className="mb-8 lg:hidden">
            <Logo href="/" />
          </div>
          <h1 className="text-2xl font-bold text-ink">Create your account</h1>
          <p className="mt-1.5 text-sm text-ink-muted">Free to start — no card required. We&apos;ll email you a code to confirm your address.</p>
          <ReturnNote returnTo={returnTo} />

          {/* Role picker */}
          <div className="mt-6">
            <label className="mb-2 block text-sm font-medium text-ink">I am a…</label>
            <div className="grid grid-cols-2 gap-3">
              {ROLES.map((r) => {
                const active = role === r.id;
                return (
                  <button
                    key={r.id}
                    type="button"
                    onClick={() => setRole(r.id)}
                    className={cn(
                      "rounded-xl border p-3 text-left transition-all",
                      active ? "border-brand-500 bg-brand-50/60 ring-2 ring-brand-600/15" : "border-line bg-white hover:border-brand-300"
                    )}
                  >
                    <span className={cn("grid h-8 w-8 place-items-center rounded-lg", active ? "bg-brand-600 text-white" : "bg-slate-100 text-ink-muted")}>
                      <r.icon size={16} />
                    </span>
                    <div className="mt-2 text-sm font-semibold text-ink">{r.title}</div>
                    <div className="text-xs leading-snug text-ink-subtle">{r.desc}</div>
                  </button>
                );
              })}
            </div>
          </div>

          {error && (
            <div className="mt-5 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
              <AlertCircle size={16} /> {error}
            </div>
          )}

          <form onSubmit={handleRegister} className="mt-5 space-y-4">
            <Field label="Full name">
              <div className="relative">
                <User size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-ink-subtle" />
                <Input value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} required placeholder="Alex Johnson" className="pl-9" />
              </div>
            </Field>
            <Field label="Email">
              <div className="relative">
                <Mail size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-ink-subtle" />
                <Input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required placeholder="alex@example.com" className="pl-9" />
              </div>
            </Field>
            <Field label="Password" hint="At least 8 characters">
              <div className="relative">
                <Lock size={16} className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-ink-subtle" />
                <Input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required placeholder="••••••••" className="pl-9" />
              </div>
            </Field>
            <Button type="submit" loading={loading} size="lg" className="w-full">
              {loading ? "Creating account…" : <>Create free account <ArrowRight size={16} /></>}
            </Button>
            <p className="text-center text-xs text-ink-subtle">
              By creating an account you agree to our{" "}
              <Link href="/terms" className="underline hover:text-ink">terms</Link> and{" "}
              <Link href="/privacy" className="underline hover:text-ink">privacy policy</Link>.
            </p>
          </form>

          <p className="mt-6 text-center text-sm text-ink-muted">
            Already have an account?{" "}
            <Link href={returnTo ? `/login?returnTo=${encodeURIComponent(returnTo)}` : "/login"} className="font-semibold text-brand-600 hover:text-brand-700">
              Sign in
            </Link>
          </p>
        </div>
      </main>
    </div>
  );
}
