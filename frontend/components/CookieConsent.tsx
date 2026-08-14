"use client";
import { useEffect, useState } from "react";
import { Cookie } from "lucide-react";

declare global {
  interface Window {
    gtag?: (...args: any[]) => void;
  }
}

const KEY = "notenix_consent";

export default function CookieConsent() {
  const [show, setShow] = useState(false);

  useEffect(() => {
    try {
      if (!localStorage.getItem(KEY)) setShow(true);
    } catch {
      /* storage blocked — don't show */
    }
  }, []);

  const choose = (granted: boolean) => {
    try {
      localStorage.setItem(KEY, granted ? "granted" : "denied");
    } catch {
      /* ignore */
    }
    if (granted && typeof window.gtag === "function") {
      window.gtag("consent", "update", { analytics_storage: "granted" });
    }
    setShow(false);
  };

  if (!show) return null;

  return (
    <div className="fixed inset-x-0 bottom-0 z-[80] p-4 sm:p-5">
      <div className="mx-auto flex max-w-3xl flex-col gap-4 rounded-2xl border border-line bg-white p-5 shadow-xl sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-start gap-3">
          <span className="mt-0.5 grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-brand-50 text-brand-600">
            <Cookie size={18} />
          </span>
          <p className="text-sm text-ink-muted">
            We use a cookie to understand how Notenix is used and improve it. Analytics stays off
            until you accept. Essential cookies (needed to sign in) are always on.
          </p>
        </div>
        <div className="flex shrink-0 gap-2">
          <button
            onClick={() => choose(false)}
            className="rounded-lg border border-line bg-white px-4 py-2 text-sm font-medium text-ink transition-colors hover:bg-slate-50"
          >
            Decline
          </button>
          <button
            onClick={() => choose(true)}
            className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-brand-700"
          >
            Accept
          </button>
        </div>
      </div>
    </div>
  );
}
