"use client";
import { useEffect, useState } from "react";
import { Mail, X, CheckCircle2 } from "lucide-react";
import { authAPI, getUser, saveAuth } from "@/lib/api";
import { Button } from "@/components/ui/Button";

const SNOOZE_KEY = "notenix_notify_prompt_snoozed";
const SNOOZE_DAYS = 7;

/** Asks a student (once, then weekly if they say "Not now") for their own email so homework and
 *  class notes reach them by email. Only shown when they have no real inbox on file. */
export default function NotifyEmailPrompt() {
  const [show, setShow] = useState(false);
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [done, setDone] = useState(false);

  useEffect(() => {
    const u = getUser() as any;
    if (!u || u.role !== "student") return;
    try {
      const snoozed = Number(localStorage.getItem(SNOOZE_KEY) || 0);
      if (snoozed && Date.now() - snoozed < SNOOZE_DAYS * 864e5) return;
    } catch { /* storage blocked: just ask */ }
    authAPI.me().then(({ data }) => { if (data.ask_notify_email) setShow(true); }).catch(() => {});
  }, []);

  const snooze = () => {
    try { localStorage.setItem(SNOOZE_KEY, String(Date.now())); } catch { /* ignore */ }
    setShow(false);
  };

  const save = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      const { data } = await authAPI.setNotifyEmail(email);
      const token = localStorage.getItem("notenix_token");
      if (token) saveAuth(token, data);
      setDone(true);
      setTimeout(() => setShow(false), 2500);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Couldn't save that. Please try again.");
    } finally {
      setBusy(false);
    }
  };

  if (!show) return null;
  return (
    <div className="fixed inset-x-0 bottom-0 z-40 p-3 sm:bottom-4 sm:left-auto sm:right-4 sm:max-w-md" role="dialog" aria-labelledby="notify-title">
      <div className="card relative p-5 shadow-xl">
        {!done && (
          <button onClick={snooze} className="absolute right-3 top-3 text-ink-subtle hover:text-ink" aria-label="Not now"><X size={18} /></button>
        )}
        {done ? (
          <div className="flex items-start gap-3">
            <CheckCircle2 className="mt-0.5 shrink-0 text-emerald-600" size={20} />
            <div>
              <div className="font-semibold text-ink">You&apos;re all set</div>
              <p className="mt-1 text-sm text-ink-muted">We&apos;ve sent a confirmation to {email}. Homework and class notes will arrive there.</p>
            </div>
          </div>
        ) : (
          <form onSubmit={save}>
            <div className="flex items-center gap-2 pr-6">
              <span className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-brand-50 text-brand-600"><Mail size={18} /></span>
              <h2 id="notify-title" className="font-semibold text-ink">Get your homework by email</h2>
            </div>
            <p className="mt-3 text-sm text-ink-muted">
              Add your own email and we&apos;ll send you an update whenever homework or class notes are added, so you
              don&apos;t need to keep opening Notenix to check.
            </p>
            <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@gmail.com"
              autoComplete="email" className="mt-3 w-full rounded-lg border border-line bg-surface px-3.5 py-2.5 text-sm text-ink outline-none focus:border-brand-500" />
            {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
            <div className="mt-3 flex items-center gap-3">
              <Button type="submit" loading={busy} size="sm">Send me updates</Button>
              <button type="button" onClick={snooze} className="text-sm text-ink-muted hover:text-ink">Not now</button>
            </div>
            <p className="mt-2 text-xs text-ink-subtle">Only homework and notes updates. Change or turn off any time in Settings.</p>
          </form>
        )}
      </div>
    </div>
  );
}
