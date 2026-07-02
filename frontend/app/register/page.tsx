"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Zap, Mail, Lock, User, ArrowRight, AlertCircle, CheckCircle } from "lucide-react";
import { authAPI, saveAuth } from "@/lib/api";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ full_name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (form.password.length < 8) { setError("Password must be at least 8 characters"); return; }
    setLoading(true); setError("");
    try {
      const res = await authAPI.register(form);
      saveAuth(res.data.access_token, res.data.user);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Registration failed. Please try again.");
    } finally { setLoading(false); }
  };

  const perks = ["3 free quizzes to start", "Built on real past papers", "Instant examiner-style marking", "No credit card required"];

  return (
    <div className="min-h-screen grid-bg flex items-center justify-center px-4 relative overflow-hidden py-8">
      <div className="orb w-96 h-96 bg-purple-300/25 top-[-100px] right-[-100px]" />
      <div className="orb w-80 h-80 bg-pink-300/15 bottom-[-50px] left-[-50px]" />
      <div className="w-full max-w-4xl relative z-10 grid md:grid-cols-2 gap-10 items-center">
        <motion.div initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.7 }}>
          <Link href="/" className="inline-flex items-center gap-2.5 mb-8">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-600 to-pink-500 flex items-center justify-center shadow-purple">
              <Zap size={20} className="text-white" />
            </div>
            <span className="text-xl font-bold"><span className="text-purple-600">Note</span>nix</span>
          </Link>
          <h1 className="text-3xl font-bold mb-4">Start Your Journey</h1>
          <p className="text-gray-500 mb-8 leading-relaxed">Join UK students mastering GCSE and A-Level subjects with quizzes built on real exam papers.</p>
          <div className="space-y-3">
            {perks.map((p) => (
              <div key={p} className="flex items-center gap-3 text-sm text-gray-600">
                <CheckCircle size={16} className="text-green-500 flex-shrink-0" /> {p}
              </div>
            ))}
          </div>
        </motion.div>
        <motion.div initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.7 }}>
          <div className="card p-8">
            <h2 className="text-xl font-bold mb-5">Create Free Account</h2>
            {error && (
              <div className="flex items-center gap-2 bg-red-50 border border-red-200 rounded-xl p-3 mb-4 text-red-600 text-sm">
                <AlertCircle size={16} /> {error}
              </div>
            )}
            <form onSubmit={handleRegister} className="space-y-4">
              {[
                { key: "full_name", label: "Full Name", type: "text", placeholder: "Alex Johnson", icon: User },
                { key: "email", label: "Email", type: "email", placeholder: "alex@school.co.uk", icon: Mail },
                { key: "password", label: "Password", type: "password", placeholder: "Min 8 characters", icon: Lock },
              ].map(({ key, label, type, placeholder, icon: Icon }) => (
                <div key={key}>
                  <label className="text-xs font-semibold text-gray-500 mb-2 block uppercase tracking-wider">{label}</label>
                  <div className="relative">
                    <Icon size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input type={type} value={form[key as keyof typeof form]} onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                      required placeholder={placeholder} className="input-field pl-10" />
                  </div>
                </div>
              ))}
              <button type="submit" disabled={loading} className="btn-primary w-full justify-center py-3 mt-2">
                {loading ? "Creating account..." : <><span>Create Free Account</span><ArrowRight size={16} /></>}
              </button>
            </form>
            <p className="text-center text-sm text-gray-500 mt-5">
              Already have an account? <Link href="/login" className="text-purple-600 font-semibold">Sign in</Link>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
