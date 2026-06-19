"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import { Check, Zap, Star, Crown, ArrowRight, Sparkles } from "lucide-react";
import { paymentsAPI } from "@/lib/api";
import { useRouter } from "next/navigation";

const plans = [
  {
    id: "free",
    name: "Free",
    icon: Zap,
    price: "£0",
    period: "forever",
    color: "border-white/10",
    iconColor: "text-slate-400",
    badge: null,
    features: ["3 quiz attempts", "All subjects & boards", "AI question generation", "Basic results", "—", "—", "—", "—"],
    cta: "Get Started",
    ctaStyle: "border border-white/15 text-slate-300 hover:border-white/25 hover:text-white",
    disabled: false,
  },
  {
    id: "monthly",
    name: "Monthly",
    icon: Star,
    price: "£100",
    period: "per month",
    color: "border-purple-500/40 bg-purple-500/5",
    iconColor: "text-purple-400",
    badge: "Most Popular",
    features: [
      "Unlimited quizzes",
      "All 11 subjects",
      "All 4 exam boards",
      "AI-powered analysis",
      "Spaced Repetition (SRS)",
      "Progress tracking",
      "XP & badges",
      "Quiz history",
    ],
    cta: "Start Monthly",
    ctaStyle: "btn-neon text-white",
    disabled: false,
  },
  {
    id: "yearly",
    name: "Yearly",
    icon: Crown,
    price: "£1100",
    period: "per year",
    saving: "Save £100",
    color: "border-cyan-500/40 bg-cyan-500/5",
    iconColor: "text-cyan-400",
    badge: "Best Value",
    features: [
      "Everything in Monthly",
      "Mock exam mode",
      "AI study planner",
      "Parent/teacher dashboard",
      "PDF export reports",
      "Priority support",
      "Early access features",
      "Dedicated exam coaching",
    ],
    cta: "Start Yearly",
    ctaStyle: "border border-cyan-500/50 text-cyan-300 hover:bg-cyan-500/10",
    disabled: false,
  },
];

const faqItems = [
  { q: "Can I cancel anytime?", a: "Yes. Subscriptions can be cancelled at any time through your account. You keep access until the end of your billing period." },
  { q: "What exam boards are covered?", a: "AQA, Edexcel, OCR, and Cambridge — all major UK exam boards across GCSE and A-Level." },
  { q: "How does the free tier work?", a: "You get 3 quiz attempts for free with no credit card required. After that, subscribe to continue." },
  { q: "Is there a student discount?", a: "We offer group rates for schools. Contact us for institutional pricing." },
];

export default function PricingPage() {
  const router = useRouter();
  const [loading, setLoading] = useState<string | null>(null);
  const [openFaq, setOpenFaq] = useState<number | null>(null);

  const handleSubscribe = async (planId: string) => {
    if (planId === "free") { router.push("/register"); return; }
    const token = localStorage.getItem("notenix_token");
    if (!token) { router.push("/register"); return; }
    setLoading(planId);
    try {
      const res = await paymentsAPI.createCheckout(planId);
      window.location.href = res.data.checkout_url;
    } catch {
      setLoading(null);
    }
  };

  return (
    <div className="min-h-screen grid-bg px-4 sm:px-6 py-12 max-w-6xl mx-auto">
      <div className="orb w-96 h-96 bg-purple-600/15 top-0 left-1/4" />

      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="text-center mb-12 relative z-10">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-purple-500/30 bg-purple-500/10 text-purple-300 text-sm mb-6">
          <Sparkles size={14} /> Simple, transparent pricing
        </div>
        <h1 className="text-4xl font-orbitron font-bold text-white mb-4">Invest in Your Grades</h1>
        <p className="text-slate-400 max-w-xl mx-auto">Start free, upgrade when you need unlimited access. Cancel anytime.</p>
      </motion.div>

      {/* Plans */}
      <div className="grid md:grid-cols-3 gap-6 mb-16 relative z-10">
        {plans.map((plan, i) => (
          <motion.div key={plan.id} initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.12 }} className="relative">
            {plan.badge && (
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 z-10">
                <span className={`text-xs font-bold px-4 py-1 rounded-full ${plan.id === "monthly" ? "bg-purple-500 text-white" : "bg-cyan-500 text-white"}`}>
                  {plan.badge}
                </span>
              </div>
            )}
            <div className={`glass-card p-7 h-full flex flex-col ${plan.color}`}>
              <div className="mb-6">
                <plan.icon size={28} className={`${plan.iconColor} mb-3`} />
                <div className="flex items-baseline gap-2">
                  <span className="text-3xl font-orbitron font-bold text-white">{plan.price}</span>
                  <span className="text-sm text-slate-500">{plan.period}</span>
                </div>
                {plan.saving && (
                  <span className="inline-block text-xs bg-green-500/15 border border-green-500/30 text-green-400 rounded-full px-3 py-0.5 mt-2">{plan.saving}</span>
                )}
                <h3 className="text-lg font-semibold text-white mt-2">{plan.name}</h3>
              </div>

              <ul className="space-y-3 flex-1 mb-7">
                {plan.features.map((f, fi) => (
                  <li key={fi} className={`flex items-center gap-3 text-sm ${f === "—" ? "text-slate-700" : "text-slate-300"}`}>
                    {f === "—" ? (
                      <span className="w-4 h-4 flex items-center justify-center text-slate-700">—</span>
                    ) : (
                      <Check size={15} className={plan.id === "yearly" ? "text-cyan-400" : plan.id === "monthly" ? "text-purple-400" : "text-slate-500"} />
                    )}
                    {f}
                  </li>
                ))}
              </ul>

              <motion.button whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}
                onClick={() => handleSubscribe(plan.id)} disabled={loading === plan.id}
                className={`w-full py-3 rounded-xl font-semibold text-sm flex items-center justify-center gap-2 transition-all disabled:opacity-50 ${plan.ctaStyle} ${plan.ctaStyle.includes("btn-neon") ? "relative z-10" : ""}`}>
                {loading === plan.id ? "Redirecting..." : <>{plan.cta} <ArrowRight size={15} /></>}
              </motion.button>
            </div>
          </motion.div>
        ))}
      </div>

      {/* FAQ */}
      <motion.div initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }} className="max-w-2xl mx-auto relative z-10">
        <h2 className="text-2xl font-orbitron font-bold text-white text-center mb-8">Frequently Asked Questions</h2>
        <div className="space-y-3">
          {faqItems.map((item, i) => (
            <div key={i} className="glass-card overflow-hidden">
              <button className="w-full px-6 py-4 flex items-center justify-between text-left" onClick={() => setOpenFaq(openFaq === i ? null : i)}>
                <span className="font-medium text-white text-sm">{item.q}</span>
                <span className="text-slate-400 text-lg">{openFaq === i ? "−" : "+"}</span>
              </button>
              {openFaq === i && (
                <motion.div initial={{ height: 0 }} animate={{ height: "auto" }} className="px-6 pb-4">
                  <p className="text-sm text-slate-400 leading-relaxed">{item.a}</p>
                </motion.div>
              )}
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}
