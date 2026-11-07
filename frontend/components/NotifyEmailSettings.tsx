"use client";
import { useState } from "react";
import { Mail, CheckCircle2, AlertCircle } from "lucide-react";
import { authAPI, saveAuth } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { Input, Field } from "@/components/ui/Input";

/** Settings card: the student's own email for homework and class-notes updates. */
export default function NotifyEmailSettings({ user }: { user: any }) {
  const [email, setEmail] = useState<string>(user?.notify_email || "");
  const [saved, setSaved] = useState<string>(user?.notify_email || "");
  const [busy, setBusy] = useState(false);
  const [ok, setOk] = useState("");
  const [error, setError] = useState("");

  const submit = async (value: string) => {
    setBusy(true);
    setOk("");
    setError("");
    try {
      const { data } = await authAPI.setNotifyEmail(value);
      const token = localStorage.getItem("notenix_token");
      if (token) saveAuth(token, data);
      setSaved(data.notify_email || "");
      setEmail(data.notify_email || "");
      setOk(value ? `Updates will go to ${value}. We've sent a confirmation there.` : "Homework emails are turned off.");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Couldn't save that.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <form onSubmit={(e) => { e.preventDefault(); submit(email.trim()); }} className="card p-6">
      <h2 className="flex items-center gap-2 text-base font-semibold text-ink"><Mail size={16} /> Homework updates by email</h2>
      <p className="mt-1 text-sm text-ink-muted">
        We&apos;ll email you whenever homework or class notes are added, so you don&apos;t need to keep checking Notenix.
      </p>
      {ok && <div className="mt-4 flex items-center gap-2 rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700"><CheckCircle2 size={16} /> {ok}</div>}
      {error && <div className="mt-4 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600"><AlertCircle size={16} /> {error}</div>}
      <div className="mt-4">
        <Field label="Your email" hint="Your own inbox (Gmail, Outlook, school email), not your Notenix user ID.">
          <Input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="you@gmail.com" autoComplete="email" />
        </Field>
      </div>
      <div className="mt-5 flex items-center justify-end gap-3">
        {saved && <button type="button" onClick={() => submit("")} disabled={busy} className="text-sm text-ink-muted hover:text-ink">Turn off</button>}
        <Button type="submit" loading={busy} disabled={!email.trim() || email.trim() === saved}>{saved ? "Update email" : "Send me updates"}</Button>
      </div>
    </form>
  );
}
