"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { Check, Sparkles } from "lucide-react";
import { paymentsAPI, getUser } from "@/lib/api";

export default function Pricing() {
  const [plans, setPlans] = useState<any>(null);
  const [user, setUser] = useState<any>(null);
  const [msg, setMsg] = useState("");

  useEffect(() => {
    setUser(getUser());
    paymentsAPI.plans().then((r) => setPlans(r.data)).catch(() => {});
  }, []);

  const upgrade = async () => {
    if (!getUser()) { window.location.href = "/register"; return; }
    try {
      const res = await paymentsAPI.checkout();
      window.location.href = res.data.url;
    } catch (err: any) {
      setMsg(err.response?.data?.detail || "Payments aren't enabled yet — coming soon!");
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-12">
      <div className="text-center mb-10">
        <div className="section-label mb-3">Pricing</div>
        <h1 className="text-3xl font-bold">Simple, student-friendly pricing</h1>
      </div>
      {msg && <div className="bg-purple-50 border border-purple-200 text-purple-700 rounded-xl p-3 mb-6 text-sm text-center">{msg}</div>}

      <div className="grid md:grid-cols-2 gap-6">
        <div className="card p-8">
          <h3 className="font-bold text-lg mb-1">Free</h3>
          <div className="text-4xl font-extrabold mb-1">£0</div>
          <p className="text-gray-400 text-sm mb-6">Get started</p>
          <ul className="space-y-3 mb-8">
            {plans?.free.features.map((f: string) => (
              <li key={f} className="flex items-center gap-2 text-sm text-gray-600"><Check size={16} className="text-green-500" /> {f}</li>
            ))}
          </ul>
          <Link href="/register"><button className="btn-secondary w-full justify-center">Get started</button></Link>
        </div>

        <div className="card p-8 border-2 border-purple-300 relative">
          <div className="badge-pill absolute -top-3 left-1/2 -translate-x-1/2 bg-gradient-to-r from-purple-600 to-pink-500 text-white border-0"><Sparkles size={12} /> Most popular</div>
          <h3 className="font-bold text-lg mb-1">Pro</h3>
          <div className="text-4xl font-extrabold mb-1">£{plans?.pro.price}<span className="text-base font-normal text-gray-400">/mo</span></div>
          <p className="text-gray-400 text-sm mb-6">Unlimited everything</p>
          <ul className="space-y-3 mb-8">
            {plans?.pro.features.map((f: string) => (
              <li key={f} className="flex items-center gap-2 text-sm text-gray-600"><Check size={16} className="text-purple-600" /> {f}</li>
            ))}
          </ul>
          <button onClick={upgrade} className="btn-primary w-full justify-center" disabled={user?.plan === "pro"}>
            {user?.plan === "pro" ? "You're Pro ✓" : "Upgrade to Pro"}
          </button>
        </div>
      </div>
    </div>
  );
}
