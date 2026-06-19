"use client";
import { useEffect, useState, Suspense } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import { Zap, CheckCircle, XCircle, Loader2 } from "lucide-react";
import { api } from "@/lib/api";

function VerifyContent() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");

  useEffect(() => {
    if (!token) { setStatus("error"); return; }
    api.get(`/auth/verify-email?token=${encodeURIComponent(token)}`)
      .then(() => setStatus("success"))
      .catch(() => setStatus("error"));
  }, [token]);

  return (
    <div className="text-center py-4">
      {status === "loading" && (
        <><Loader2 size={48} className="text-purple-400 animate-spin mx-auto mb-4" />
        <p className="text-slate-400 text-sm">Verifying your email...</p></>
      )}
      {status === "success" && (
        <motion.div initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}>
          <CheckCircle size={56} className="text-green-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">Email Verified!</h3>
          <p className="text-slate-400 text-sm mb-6">Your account is now fully activated.</p>
          <Link href="/dashboard">
            <motion.button whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}
              className="btn-neon relative px-8 py-3 rounded-xl text-white font-semibold z-10">
              <span className="relative z-10">Go to Dashboard →</span>
            </motion.button>
          </Link>
        </motion.div>
      )}
      {status === "error" && (
        <motion.div initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}>
          <XCircle size={56} className="text-red-400 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-white mb-2">Link Expired</h3>
          <p className="text-slate-400 text-sm mb-6">This verification link is invalid or has expired.</p>
          <Link href="/dashboard" className="text-purple-400 hover:text-purple-300 text-sm font-medium block mb-3">
            Go to dashboard to resend →
          </Link>
          <Link href="/login" className="text-slate-500 hover:text-slate-400 text-sm">Back to login</Link>
        </motion.div>
      )}
    </div>
  );
}

export default function VerifyEmailPage() {
  return (
    <div className="min-h-screen grid-bg flex items-center justify-center px-4 relative overflow-hidden">
      <div className="orb w-96 h-96 bg-green-600/15 top-[-100px] left-[-100px]" />
      <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md relative z-10">
        <div className="text-center mb-8">
          <Link href="/" className="inline-flex items-center gap-2 mb-6">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center">
              <Zap size={20} className="text-white" />
            </div>
            <span className="font-orbitron text-xl font-bold gradient-text tracking-wider">NOTENIX</span>
          </Link>
        </div>
        <div className="glass-card p-8">
          <Suspense fallback={<div className="text-center py-8"><Loader2 size={32} className="text-purple-400 animate-spin mx-auto" /></div>}>
            <VerifyContent />
          </Suspense>
        </div>
      </motion.div>
    </div>
  );
}
