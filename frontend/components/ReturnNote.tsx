"use client";
import { useEffect, useState } from "react";
import { Sparkles, Send } from "lucide-react";
import { paymentsAPI } from "@/lib/api";

const SYM: Record<string, string> = { GBP: "£", USD: "$", EUR: "€", INR: "₹", THB: "฿" };

// Reminds people on the auth screens what they were in the middle of, so signing in or up
// mid-purchase doesn't feel like starting over.
export default function ReturnNote({ returnTo }: { returnTo: string | null }) {
  const [pro, setPro] = useState<{ price: number; currency: string; days: number } | null>(null);
  const isPay = !!returnTo && returnTo.startsWith("/pay");
  const isRequest = !!returnTo && returnTo.startsWith("/request");

  useEffect(() => {
    if (!isPay) return;
    paymentsAPI.plans()
      .then((r) => setPro({ price: r.data.pro.price, currency: r.data.currency, days: r.data.pro.days }))
      .catch(() => {});
  }, [isPay]);

  if (isPay) {
    return (
      <div className="mt-6 flex gap-3 rounded-xl border border-brand-200 bg-brand-50 p-4 text-sm">
        <Sparkles size={16} className="mt-0.5 shrink-0 text-brand-600" />
        <div>
          <div className="font-semibold text-ink">
            Upgrading to Pro{pro ? `: ${SYM[pro.currency] ?? `${pro.currency} `}${pro.price.toFixed(2)}` : ""}
          </div>
          <p className="mt-0.5 text-ink-muted">
            A one-off {pro?.days ?? 30}-day pass paid by bank transfer. It doesn&apos;t renew automatically. You&apos;ll see the
            payment details next.
          </p>
        </div>
      </div>
    );
  }
  if (isRequest) {
    const exam = new URLSearchParams(returnTo!.split("?")[1] || "").get("exam");
    return (
      <div className="mt-6 flex gap-3 rounded-xl border border-brand-200 bg-brand-50 p-4 text-sm">
        <Send size={16} className="mt-0.5 shrink-0 text-brand-600" />
        <p className="text-ink-muted">
          <span className="font-semibold text-ink">Requesting a mock test{exam ? ` for ${exam}` : ""}.</span> We&apos;ll take you
          back to your request after this step.
        </p>
      </div>
    );
  }
  return null;
}
