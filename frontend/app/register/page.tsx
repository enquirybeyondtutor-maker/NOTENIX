"use client";
import { useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Zap, Mail, Lock, User, ArrowRight, AlertCircle, CheckCircle, MailCheck } from "lucide-react";
import { authAPI } from "@/lib/api";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ full_name: "", email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [registered, setRegistered] = useState(false);

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    if (form.password.length < 8) { setError("Password must be at least 8 characters"); return; }
    setLoading(true);
    setError("");
    try {
      const res = await authAPI.register(form);
      localStorage.setItem("notenix_token", res.data.access_token);
      localStorage.setItem("notenix_user", JSON.stringify(res.data.user));
      setRegistered(true);
      setTimeout(() => router.push("/dashboard"), 2500);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const perks = ["3 free quizzes to start", "All subjects & exam boards", "AI-powered analysis", "No credit card required"];

  if (registered) {
    return (
      <div className="min-h-screen grid-bg flex items-center justify-center px-4">
        <motion.div initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }} className="text-center max-w-md">
          <MailCheck size={64} className="text-green-400 mx-auto mb-4" />
          <h2 className="text-2xl font-orbitron font-bold text-white mb-2">Account Created!</h2>
          <div className="glass-card p-5 border-blue-500/20 bg-blue-500/5 mt-4">
            <p className="text-slate-300 text-sm">A verification email has been sent to <span className="text-white font-medium">{form.email}</span>. Check your inbox to activate your account.</p>
            <p className="text-slate-500 text-xs mt-2">Redirecting to dashboard...</p>
          </div>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen grid-bg flex items-center justify-center px-4 relative overflow-hidden py-8">
      <div className="orb w-96 h-96 bg-purple-600/20 top-[-100px] right-[-100px]" />
      <div className="orb w-80 h-80 bg-cyan-600/15 bottom-[-50px] left-[-50px]" />

      <div className="w-full max-w-4xl relative z-10 grid md:grid-cols-2 gap-8 items-center">
        {/* Left side */}
        <motion.div initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.7 }}>
          <Link href="/" className="inline-flex items-center gap-2 mb-8">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center">
              <Zap size={20} className="text-white" />
            </div>
            <span className="font-orbitron text-xl font-bold gradient-text tracking-wider">NOTENIX</span>
          </Link>
          <h1 className="text-3xl font-orbitron font-bold text-white mb-4">Start Your Journey</h1>
          <p className="text-slate-400 mb-8 leading-relaxed">Join thousands of UK students mastering GCSE and A-Level subjects with AI.</p>
          <div className="space-y-3">
            {perks.map((perk) => (
              <div key={perk} className="flex items-center gap-3 text-sm text-slate-300">
                <CheckCircle size={16} className="text-green-400 flex-shrink-0" />
                {perk}
              </div>
            ))}
          </div>
        </motion.div>

        {/* Right side - form */}
        <motion.div initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.7 }}>
          <div className="glass-card p-8">
            <h2 className="text-xl font-semibold text-white mb-5">Create Free Account</h2>

            {error && (
              <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/30 rounded-lg p-3 mb-4 text-red-400 text-sm">
                <AlertCircle size={16} /> {error}
              </div>
            )}

            {/* Google OAuth */}
            <a href={`${API_BASE}/auth/google/login`}>
              <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} type="button"
                className="w-full py-3 rounded-lg border border-white/15 text-white font-medium text-sm flex items-center justify-center gap-3 hover:bg-white/5 transition-all mb-4">
                <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
                  <path d="M17.64 9.2c0-.637-.057-1.251-.164-1.84H9v3.481h4.844c-.209 1.125-.843 2.078-1.796 2.717v2.258h2.908c1.702-1.567 2.684-3.875 2.684-6.615z" fill="#4285F4"/>
                  <path d="M9 18c2.43 0 4.467-.806 5.956-2.184l-2.908-2.258c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711H.957v2.332C2.438 15.983 5.482 18 9 18z" fill="#34A853"/>
                  <path d="M3.964 10.707c-.18-.54-.282-1.117-.282-1.707s.102-1.167.282-1.707V4.961H.957C.347 6.175 0 7.55 0 9s.348 2.825.957 4.039l3.007-2.332z" fill="#FBBC05"/>
                  <path d="M9 3.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C13.463.891 11.426 0 9 0 5.482 0 2.438 2.017.957 4.961L3.964 6.293C4.672 4.166 6.656 3.58 9 3.58z" fill="#EA4335"/>
                </svg>
                Continue with Google
              </motion.button>
            </a>

            <div className="flex items-center gap-3 mb-4">
              <div className="flex-1 h-px bg-white/8" />
              <span className="text-xs text-slate-600">or</span>
              <div className="flex-1 h-px bg-white/8" />
            </div>

            <form onSubmit={handleRegister} className="space-y-4">
              {[
                { key: "full_name", label: "Full Name", type: "text", placeholder: "Alex Johnson", icon: User },
                { key: "email", label: "Email", type: "email", placeholder: "alex@school.co.uk", icon: Mail },
                { key: "password", label: "Password", type: "password", placeholder: "Min 8 characters", icon: Lock },
              ].map(({ key, label, type, placeholder, icon: Icon }) => (
                <div key={key}>
                  <label className="text-xs text-slate-400 font-medium mb-2 block uppercase tracking-wider">{label}</label>
                  <div className="relative">
                    <Icon size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                    <input type={type} value={form[key as keyof typeof form]} onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                      required placeholder={placeholder}
                      className="w-full bg-white/5 border border-white/10 rounded-lg pl-10 pr-4 py-3 text-white placeholder-slate-600 focus:outline-none focus:border-purple-500/50 focus:bg-purple-500/5 transition-all text-sm" />
                  </div>
                </div>
              ))}

              <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }} type="submit" disabled={loading}
                className="btn-neon relative w-full py-3 rounded-lg text-white font-semibold flex items-center justify-center gap-2 disabled:opacity-50 mt-2 z-10">
                <span className="relative z-10 flex items-center gap-2">
                  {loading ? "Creating account..." : <><span>Create Free Account</span><ArrowRight size={16} /></>}
                </span>
              </motion.button>
            </form>

            <p className="text-center text-sm text-slate-500 mt-5">
              Already have an account?{" "}
              <Link href="/login" className="text-purple-400 hover:text-purple-300 font-medium">Sign in</Link>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
