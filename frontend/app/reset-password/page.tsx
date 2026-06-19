"use client";
import { useState, Suspense } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Zap, Lock, ArrowRight, CheckCircle, AlertCircle } from "lucide-react";
import { api } from "@/lib/api";

function ResetPasswordForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token") || "";
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (password !== confirm) { setError("Passwords do not match"); return; }
    if (password.length < 8) { setError("Password must be at least 8 characters"); return; }
    setLoading(true);
    setError("");
    try {
      await api.post("/auth/reset-password", { token, new_password: password });
      setDone(true);
      setTimeout(() => router.push("/login"), 2500);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Reset link is invalid or expired.");
    } finally {
      setLoading(false);
    }
  };

  if (!token) return (
    <div className="text-center py-8">
      <AlertCircle size={40} className="text-red-400 mx-auto mb-3" />
      <p className="text-white font-semibold mb-2">Invalid reset link</p>
      <Link href="/forgot-password" className="text-purple-400 hover:text-purple-300 text-sm">Request a new one →</Link>
    </div>
  );

  return done ? (
    <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="text-center py-4">
      <CheckCircle size={48} className="text-green-400 mx-auto mb-4" />
      <h3 className="font-semibold text-white mb-2">Password updated!</h3>
      <p className="text-slate-400 text-sm">Redirecting you to login...</p>
    </motion.div>
  ) : (
    <form onSubmit={handleSubmit} className="space-y-5">
      {error && <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3 text-red-400 text-sm flex items-center gap-2"><AlertCircle size={15} />{error}</div>}
      {[
        { label: "New Password", value: password, set: setPassword, placeholder: "Min 8 characters" },
        { label: "Confirm Password", value: confirm, set: setConfirm, placeholder: "Repeat password" },
      ].map(({ label, value, set, placeholder }) => (
        <div key={label}>
          <label className="text-xs text-slate-400 font-medium mb-2 block uppercase tracking-wider">{label}</label>
          <div className="relative">
            <Lock size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <input type="password" value={value} onChange={(e) => set(e.target.value)} required placeholder={placeholder}
              className="w-full bg-white/5 border border-white/10 rounded-lg pl-10 pr-4 py-3 text-white placeholder-slate-600 focus:outline-none focus:border-purple-500/50 transition-all text-sm" />
          </div>
        </div>
      ))}
      <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} type="submit" disabled={loading}
        className="btn-neon relative w-full py-3 rounded-lg text-white font-semibold flex items-center justify-center gap-2 disabled:opacity-50 z-10">
        <span className="relative z-10 flex items-center gap-2">
          {loading ? "Updating..." : <><span>Set New Password</span><ArrowRight size={16} /></>}
        </span>
      </motion.button>
    </form>
  );
}

export default function ResetPasswordPage() {
  return (
    <div className="min-h-screen grid-bg flex items-center justify-center px-4 relative overflow-hidden">
      <div className="orb w-96 h-96 bg-purple-600/20 top-[-100px] right-[-100px]" />
      <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md relative z-10">
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-2 mb-6">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center">
              <Zap size={20} className="text-white" />
            </div>
            <span className="font-orbitron text-xl font-bold gradient-text tracking-wider">NOTENIX</span>
          </Link>
          <h1 className="text-2xl font-orbitron font-bold text-white">Set New Password</h1>
          <p className="text-slate-400 mt-2 text-sm">Choose a strong password for your account</p>
        </div>
        <div className="glass-card p-8">
          <Suspense fallback={<div className="text-slate-400 text-sm text-center py-4">Loading...</div>}>
            <ResetPasswordForm />
          </Suspense>
        </div>
      </motion.div>
    </div>
  );
}
