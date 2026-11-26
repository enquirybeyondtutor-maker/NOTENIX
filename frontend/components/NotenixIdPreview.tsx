"use client";
import { useEffect, useState } from "react";
import { BadgeCheck } from "lucide-react";
import { paymentsAPI } from "@/lib/api";

/** Shows the @notenix.com user ID a new student gets from their name (aryan@notenix.com, or
 *  aryan.s@… if that's taken), updating as they type. The ID is reserved when the form is sent. */
export default function NotenixIdPreview({ name }: { name: string }) {
  const [loginId, setLoginId] = useState<string | null>(null);

  useEffect(() => {
    const clean = name.trim();
    if (clean.length < 2) { setLoginId(null); return; }
    const t = setTimeout(() => {
      paymentsAPI.userIdPreview(clean).then((r) => setLoginId(r.data.login_id)).catch(() => setLoginId(null));
    }, 400);
    return () => clearTimeout(t);
  }, [name]);

  if (!loginId) return null;
  return (
    <div className="flex items-start gap-2.5 rounded-lg border border-brand-200 bg-brand-50/60 p-3 text-sm">
      <BadgeCheck size={16} className="mt-0.5 shrink-0 text-brand-600" />
      <div>
        <p className="text-ink-muted">Your Notenix user ID will be</p>
        <p className="font-mono font-semibold text-ink">{loginId}</p>
        <p className="mt-1 text-xs text-ink-muted">
          You sign in with this ID, not your email. We also email it to you once your payment is confirmed.
          Already have a Notenix account? You keep your existing user ID.
        </p>
      </div>
    </div>
  );
}
