"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ArrowRight, AlertCircle, CheckCircle2, ClipboardCheck, BookOpen, Camera, LineChart } from "lucide-react";
import { ks3API, saveAuth } from "@/lib/api";
import { Logo } from "@/components/ui/Logo";
import { Button } from "@/components/ui/Button";
import { Input, Field } from "@/components/ui/Input";

const PERKS = [
  { icon: ClipboardCheck, title: "Baseline tests", desc: "Maths, Science and English, about 30 minutes each." },
  { icon: Camera, title: "Homework help", desc: "Stuck on school homework? Send a photo, a tutor replies." },
  { icon: BookOpen, title: "KS3 notes", desc: "Short notes for every topic this year." },
  { icon: LineChart, title: "Progress report", desc: "Emailed to you on day 7: scores and what to fix first." },
];

/**
 * Free 1-week Notenix KS3 trial ("Beat the Year 7 dip").
 * Step 1: child + parent email → 6-digit code emailed to the parent.
 * Step 2: code verified → a @notenix.com user ID is issued.
 * Step 3: the parent chooses the password → the trial week starts.
 */
export default function Ks3TrialPage() {
  const router = useRouter();
  const [step, setStep] = useState<"details" | "code" | "password" | "done">("details");
  const [childName, setChildName] = useState("");
  const [year, setYear] = useState(7);
  const [parentEmail, setParentEmail] = useState("");
  const [agreed, setAgreed] = useState(false);
  const [code, setCode] = useState("");
  const [password, setPassword] = useState("");
  const [loginId, setLoginId] = useState("");
  const [setupToken, setSetupToken] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [cooldown, setCooldown] = useState(0);

  const [source, setSource] = useState<string | undefined>();
  useEffect(() => {  // ?year=6&src=kent-grammar from the Kent grammar page
    const q = new URLSearchParams(window.location.search);
    const y = Number(q.get("year"));
    if ([6, 7, 8, 9].includes(y)) setYear(y);
    const src = q.get("src");
    if (src) setSource(src.slice(0, 40));
  }, []);

  useEffect(() => {
    if (cooldown <= 0) return;
    const t = setTimeout(() => setCooldown((c) => c - 1), 1000);
    return () => clearTimeout(t);
  }, [cooldown]);

  const sendCode = async (e?: React.FormEvent) => {
    e?.preventDefault();
    setLoading(true);
    setError("");
    try {
      await ks3API.startTrial({ child_name: childName, year_group: year, parent_email: parentEmail, agree_terms: agreed, source });
      setStep("code");
      setCooldown(60);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Couldn't send the code. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const verify = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const { data } = await ks3API.verifyTrial({ parent_email: parentEmail, code });
      setLoginId(data.login_id);
      setSetupToken(data.setup_token);
      setStep("password");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Couldn't check the code. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const complete = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirm) return setError("The two passwords don't match.");
    setLoading(true);
    setError("");
    try {
      const { data } = await ks3API.completeTrial({ parent_email: parentEmail, setup_token: setupToken, password });
      saveAuth(data.access_token, data.user);
      setStep("done");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Couldn't start the trial. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      <aside className="hidden bg-gradient-to-br from-brand-700 via-brand-600 to-indigo-500 p-12 lg:flex">
        <div className="flex w-full flex-col justify-between">
          <Logo href="/" light />
          <div>
            <span className="rounded-full bg-white/15 px-3 py-1 text-xs font-semibold text-white">Free for 1 week · no card</span>
            <h2 className="mt-4 text-3xl font-bold leading-tight text-white">Beat the Year 7 dip.</h2>
            <p className="mt-4 max-w-sm text-brand-100">
              New subjects, more homework, a new school. The first year of secondary is where many children quietly
              slip. In one week you&apos;ll know exactly where your child stands.
            </p>
            <ul className="mt-8 space-y-4">
              {PERKS.map((p) => (
                <li key={p.title} className="flex gap-3 text-white">
                  <span className="mt-0.5 grid h-8 w-8 shrink-0 place-items-center rounded-lg bg-white/15"><p.icon size={16} /></span>
                  <span><b className="block text-sm">{p.title}</b><span className="text-sm text-brand-100">{p.desc}</span></span>
                </li>
              ))}
            </ul>
          </div>
          <p className="text-sm text-brand-200">© {new Date().getFullYear()} Notenix · KS3 with Beyond Tutors</p>
        </div>
      </aside>

      <main className="flex items-center justify-center px-4 py-12">
        <div className="w-full max-w-sm">
          <div className="mb-8 lg:hidden"><Logo href="/" /></div>

          {step === "done" ? (
            <div>
              <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
                <CheckCircle2 size={14} /> Trial started
              </span>
              <h1 className="mt-3 text-2xl font-bold text-ink">{childName.split(" ")[0]}&apos;s free week starts now</h1>
              <div className="mt-6 rounded-xl border border-line bg-brand-50 p-4">
                <div className="text-xs text-ink-muted">{childName.split(" ")[0]}&apos;s Notenix login</div>
                <div className="mt-1 font-mono text-base font-semibold text-ink">{loginId}</div>
                <div className="mt-1 text-xs text-ink-muted">Use it with the password you just chose. We&apos;ve emailed this user ID to you too.</div>
              </div>
              <p className="mt-4 text-sm text-ink-muted">Start with the baseline tests: they&apos;re what your day-7 report is built on.</p>
              <Button size="lg" className="mt-6 w-full" onClick={() => router.push("/tests")}>
                Start the baseline tests <ArrowRight size={16} />
              </Button>
            </div>
          ) : (
            <>
              <span className="inline-flex items-center gap-1.5 rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700 lg:hidden">
                Free for 1 week · no card
              </span>
              <h1 className="mt-3 text-2xl font-bold text-ink">Start a free KS3 trial</h1>
              <p className="mt-1.5 text-sm text-ink-muted">For Years 7, 8 and 9. Takes a minute; no payment details.</p>

              {error && (
                <div className="mt-5 flex items-start gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
                  <AlertCircle size={16} className="mt-0.5 shrink-0" /> {error}
                </div>
              )}
              {step === "code" && !error && (
                <div className="mt-5 flex items-start gap-2 rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
                  <CheckCircle2 size={16} className="mt-0.5 shrink-0" /> We&apos;ve emailed a 6-digit code to {parentEmail}.
                </div>
              )}

              {step === "details" ? (
                <form onSubmit={sendCode} className="mt-6 space-y-4">
                  <Field label="Your child's name">
                    <Input required value={childName} onChange={(e) => setChildName(e.target.value)} placeholder="e.g. Aisha Khan" />
                  </Field>
                  <Field label="School year">
                    <select value={year} onChange={(e) => setYear(Number(e.target.value))}
                      className="w-full rounded-lg border border-line bg-white px-3.5 py-2.5 text-sm text-ink outline-none focus:border-brand-500">
                      <option value={6}>Year 6 (starting Year 7 in September)</option>
                      <option value={7}>Year 7</option>
                      <option value={8}>Year 8</option>
                      <option value={9}>Year 9</option>
                    </select>
                  </Field>
                  <Field label="Your email (parent or guardian)">
                    <Input type="email" required value={parentEmail} onChange={(e) => setParentEmail(e.target.value)}
                      placeholder="you@example.com" autoComplete="email" />
                  </Field>
                  <label className="flex items-start gap-2.5 text-sm text-ink">
                    <input type="checkbox" checked={agreed} onChange={(e) => setAgreed(e.target.checked)}
                      className="mt-0.5 h-4 w-4 shrink-0 cursor-pointer accent-brand-600" />
                    <span>
                      I&apos;m the parent or guardian and agree to the{" "}
                      <a href="/terms" target="_blank" className="font-semibold text-brand-600 hover:underline">Terms</a> and{" "}
                      <a href="/privacy" target="_blank" className="font-semibold text-brand-600 hover:underline">Privacy policy</a>.
                      The trial is free and ends by itself after 7 days.
                    </span>
                  </label>
                  <Button type="submit" loading={loading} disabled={!agreed} size="lg" className="w-full">
                    {loading ? "Sending…" : <>Email me a code <ArrowRight size={16} /></>}
                  </Button>
                  <p className="text-center text-xs text-ink-subtle">
                    Already have an account? <a href="/login" className="font-medium text-brand-600 hover:underline">Sign in</a>
                  </p>
                </form>
              ) : step === "password" ? (
                <form onSubmit={complete} className="mt-6 space-y-4">
                  <div className="rounded-xl border border-line bg-brand-50 p-4">
                    <div className="text-xs text-ink-muted">Email confirmed. {childName.split(" ")[0]}&apos;s Notenix user ID is</div>
                    <div className="mt-1 font-mono text-base font-semibold text-ink">{loginId}</div>
                    <div className="mt-1 text-xs text-ink-muted">{childName.split(" ")[0]} signs in with this and the password you choose below.</div>
                  </div>
                  <Field label="Choose a password">
                    <Input type="password" required minLength={8} value={password} onChange={(e) => setPassword(e.target.value)}
                      placeholder="At least 8 characters" autoComplete="new-password" />
                  </Field>
                  <Field label="Type it again">
                    <Input type="password" required minLength={8} value={confirm} onChange={(e) => setConfirm(e.target.value)}
                      placeholder="Same password" autoComplete="new-password" />
                  </Field>
                  <Button type="submit" loading={loading} size="lg" className="w-full">
                    {loading ? "Starting…" : <>Start the free week <ArrowRight size={16} /></>}
                  </Button>
                </form>
              ) : (
                <form onSubmit={verify} className="mt-6 space-y-4">
                  <Field label="6-digit code">
                    <input inputMode="numeric" autoComplete="one-time-code" maxLength={6} value={code}
                      onChange={(e) => setCode(e.target.value.replace(/\D/g, ""))} placeholder="••••••"
                      className="w-full rounded-lg border border-line bg-white px-3.5 py-3 text-center text-2xl font-semibold tracking-[0.5em] text-ink outline-none focus:border-brand-500 focus:ring-4 focus:ring-brand-600/10" />
                  </Field>
                  <Button type="submit" loading={loading} disabled={code.length !== 6} size="lg" className="w-full">
                    {loading ? "Checking…" : <>Confirm my email <ArrowRight size={16} /></>}
                  </Button>
                  <div className="flex items-center justify-between text-sm">
                    <button type="button" onClick={() => { setStep("details"); setError(""); }} className="text-ink-muted hover:text-ink">
                      Change details
                    </button>
                    <button type="button" onClick={() => sendCode()} disabled={cooldown > 0 || loading}
                      className="font-semibold text-brand-600 hover:text-brand-700 disabled:cursor-not-allowed disabled:text-ink-subtle">
                      {cooldown > 0 ? `Resend in ${cooldown}s` : "Resend code"}
                    </button>
                  </div>
                </form>
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
}
