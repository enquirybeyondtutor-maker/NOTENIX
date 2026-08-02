"use client";
import { useEffect, useState } from "react";
import { Check, Sparkles, Building2, ArrowRight } from "lucide-react";
import { paymentsAPI, getUser } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

export default function Pricing() {
  const [plans, setPlans] = useState<any>(null);
  const [user, setUser] = useState<any>(null);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    setUser(getUser());
    paymentsAPI.plans().then((r) => setPlans(r.data)).catch(() => {});
  }, []);

  const upgrade = async () => {
    if (!getUser()) {
      window.location.href = "/register";
      return;
    }
    try {
      const res = await paymentsAPI.checkout();
      window.location.href = res.data.url;
    } catch (err: any) {
      setMsg(err.response?.data?.detail || "Payments aren't enabled yet — coming soon!");
    }
  };

  const freeFeatures: string[] = plans?.free?.features || [
    "3 AI quizzes to start",
    "Assigned tests from teachers",
    "Instant marking & grade estimates",
    "Progress tracking",
  ];
  const proFeatures: string[] = plans?.pro?.features || [
    "Unlimited AI quizzes",
    "Exam mode with written marking",
    "Full analytics & feedback",
    "Priority support",
  ];

  return (
    <div className="mx-auto max-w-5xl px-4 py-16 sm:px-6">
      <div className="mx-auto max-w-2xl text-center">
        <span className="eyebrow">Pricing</span>
        <h1 className="mt-3 text-3xl font-bold tracking-tight text-ink sm:text-4xl">
          Simple pricing for students and schools
        </h1>
        <p className="mt-4 text-lg text-ink-muted">
          Start free. Upgrade when you're ready. Schools get bulk pricing and admin tools.
        </p>
      </div>

      {msg && (
        <div className="mx-auto mt-6 max-w-md rounded-lg border border-brand-200 bg-brand-50 p-3 text-center text-sm text-brand-700">
          {msg}
        </div>
      )}

      <div className="mt-12 grid gap-6 md:grid-cols-2">
        {/* Free */}
        <div className="card flex flex-col p-8">
          <h3 className="text-lg font-semibold text-ink">Free</h3>
          <div className="mt-2 flex items-baseline gap-1">
            <span className="text-4xl font-bold text-ink">£0</span>
            <span className="text-sm text-ink-subtle">/ forever</span>
          </div>
          <p className="mt-1 text-sm text-ink-muted">For individual students getting started.</p>
          <ul className="mt-6 flex-1 space-y-3">
            {freeFeatures.map((f) => (
              <li key={f} className="flex items-center gap-2 text-sm text-ink-muted">
                <Check size={16} className="text-emerald-500" /> {f}
              </li>
            ))}
          </ul>
          <Button href="/register" variant="secondary" className="mt-8 w-full">Get started free</Button>
        </div>

        {/* Pro */}
        <div className="card relative flex flex-col border-brand-300 p-8 ring-1 ring-brand-200">
          <span className="badge-brand absolute -top-3 left-8">
            <Sparkles size={12} /> Most popular
          </span>
          <h3 className="text-lg font-semibold text-ink">Pro</h3>
          <div className="mt-2 flex items-baseline gap-1">
            <span className="text-4xl font-bold text-ink">£{plans?.pro?.price ?? "9.99"}</span>
            <span className="text-sm text-ink-subtle">/ month</span>
          </div>
          <p className="mt-1 text-sm text-ink-muted">Everything you need to excel.</p>
          <ul className="mt-6 flex-1 space-y-3">
            {proFeatures.map((f) => (
              <li key={f} className="flex items-center gap-2 text-sm text-ink-muted">
                <Check size={16} className="text-brand-600" /> {f}
              </li>
            ))}
          </ul>
          <Button onClick={upgrade} disabled={user?.plan === "pro"} className="mt-8 w-full">
            {user?.plan === "pro" ? "You're Pro ✓" : "Upgrade to Pro"}
          </Button>
        </div>
      </div>

      {/* Schools tier */}
      <div className="mt-6 flex flex-col items-center justify-between gap-4 rounded-2xl border border-line bg-white p-6 sm:flex-row sm:p-8">
        <div className="flex items-start gap-4">
          <span className="grid h-11 w-11 shrink-0 place-items-center rounded-lg bg-slate-100 text-ink-muted">
            <Building2 size={20} />
          </span>
          <div>
            <h3 className="font-semibold text-ink">Schools &amp; departments</h3>
            <p className="mt-1 text-sm text-ink-muted">
              Teacher accounts, class assignment, cohort analytics and admin controls. Bulk pricing per seat.
            </p>
          </div>
        </div>
        <Button href="mailto:hello@notenix.com" variant="secondary" className="shrink-0">
          Talk to us <ArrowRight size={15} />
        </Button>
      </div>
    </div>
  );
}
