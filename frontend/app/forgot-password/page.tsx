"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { Zap, Mail, ArrowRight, CheckCircle } from "lucide-react";
import { api } from "@/lib/api";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await api.post("/auth/forgot-password", { email });
      setSent(true);
    } catch {
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen grid-bg flex items-center justify-center px-4 relative overflow-hidden">
      <div className="orb w-96 h-96 bg-purple-600/20 top-[-100px] left-[-100px]" />
      <div className="orb w-80 h-80 bg-cyan-600/15 bottom-[-50px] right-[-50px]" />

      <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md relative z-10">
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-2 mb-6">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center">
              <Zap size={20} className="text-white" />
            </div>
            <span className="font-orbitron text-xl font-bold gradient-text tracking-wider">NOTENIX</span>
          </Link>
          <h1 className="text-2xl font-orbitron font-bold text-white">Reset Password</h1>
          <p className="text-slate-400 mt-2 text-sm">We'll send a reset link to your email</p>
        </div>

        <div className="glass-card p-8">
          {sent ? (
            <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="text-center py-4">
              <CheckCircle size={48} className="text-green-400 mx-auto mb-4" />
              <h3 className="font-semibold text-white mb-2">Check your inbox</h3>
              <p className="text-slate-400 text-sm mb-6">
                If <span className="text-white">{email}</span> has an account, you'll receive a reset link shortly.
              </p>
              <Link href="/login" className="text-purple-400 hover:text-purple-300 text-sm font-medium">
                Back to login →
              </Link>
            </motion.div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-5">
              {error && (
                <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-3 text-red-400 text-sm">{error}</div>
              )}
              <div>
                <label className="text-xs text-slate-400 font-medium mb-2 block uppercase tracking-wider">Email Address</label>
                <div className="relative">
                  <Mail size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                  <input
                    type="email" value={email} onChange={(e) => setEmail(e.target.value)} required
                    placeholder="your@email.com"
                    className="w-full bg-white/5 border border-white/10 rounded-lg pl-10 pr-4 py-3 text-white placeholder-slate-600 focus:outline-none focus:border-purple-500/50 transition-all text-sm"
                  />
                </div>
              </div>
              <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} type="submit" disabled={loading}
                className="btn-neon relative w-full py-3 rounded-lg text-white font-semibold flex items-center justify-center gap-2 disabled:opacity-50 z-10">
                <span className="relative z-10 flex items-center gap-2">
                  {loading ? "Sending..." : <><span>Send Reset Link</span><ArrowRight size={16} /></>}
                </span>
              </motion.button>
              <p className="text-center text-sm text-slate-500">
                <Link href="/login" className="text-purple-400 hover:text-purple-300">Back to login</Link>
              </p>
            </form>
          )}
        </div>
      </motion.div>
    </div>
  );
}
