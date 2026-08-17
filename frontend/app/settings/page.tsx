"use client";
import { useEffect, useState } from "react";
import { UserCog, Mail, Shield, Sparkles, AlertCircle, CheckCircle2, Lock } from "lucide-react";
import { authAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Input, Field } from "@/components/ui/Input";
import { humanize, formatDate } from "@/lib/utils";

export default function SettingsPage() {
  const { user, ready } = useAuthGuard();
  const [name, setName] = useState("");
  const [availableAt, setAvailableAt] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [ok, setOk] = useState("");

  useEffect(() => {
    if (user) {
      setName(user.full_name || "");
      setAvailableAt(user.name_change_available_at || null);
    }
  }, [user]);

  const locked = !!availableAt && new Date(availableAt).getTime() > Date.now();

  const save = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(""); setOk("");
    const trimmed = name.trim();
    if (trimmed.length < 2) { setError("Please enter a name with at least 2 characters."); return; }
    if (trimmed === (user?.full_name || "")) { setError("That's already your name."); return; }
    setSaving(true);
    try {
      const { data } = await authAPI.updateProfile(trimmed);
      try { localStorage.setItem("notenix_user", JSON.stringify(data)); } catch {}
      setAvailableAt(data.name_change_available_at || null);
      setOk("Your display name has been updated.");
    } catch (e: any) {
      setError(e.response?.data?.detail || "Couldn't update your name. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  if (!ready || !user) return <Spinner label="Loading your account…" />;

  return (
    <PageContainer className="max-w-2xl">
      <PageHeader icon={UserCog} title="Account settings" subtitle="Manage your Notenix profile." />

      {/* Read-only account details */}
      <div className="card mb-6 divide-y divide-line">
        <div className="flex items-center gap-3 p-4">
          <Mail size={16} className="text-ink-subtle" />
          <div className="min-w-0">
            <div className="text-xs text-ink-subtle">Email</div>
            <div className="truncate text-sm font-medium text-ink">{user.email}</div>
          </div>
        </div>
        <div className="flex items-center gap-3 p-4">
          <Shield size={16} className="text-ink-subtle" />
          <div>
            <div className="text-xs text-ink-subtle">Role</div>
            <div className="text-sm font-medium text-ink capitalize">{user.role || "student"}</div>
          </div>
        </div>
        <div className="flex items-center gap-3 p-4">
          <Sparkles size={16} className="text-ink-subtle" />
          <div>
            <div className="text-xs text-ink-subtle">Plan</div>
            <div className="text-sm font-medium text-ink capitalize">{humanize(user.plan || "free")}</div>
          </div>
        </div>
      </div>

      {/* Display name */}
      <form onSubmit={save} className="card p-6">
        <h2 className="text-base font-semibold text-ink">Display name</h2>
        <p className="mt-1 text-sm text-ink-muted">
          This is the name shown on your tests, results and leaderboards. You can change it once every 60 days.
        </p>

        {ok && (
          <div className="mt-4 flex items-center gap-2 rounded-lg border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700">
            <CheckCircle2 size={16} /> {ok}
          </div>
        )}
        {error && (
          <div className="mt-4 flex items-center gap-2 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
            <AlertCircle size={16} /> {error}
          </div>
        )}

        <div className="mt-4">
          <Field label="Name" hint={locked ? undefined : "Between 2 and 120 characters."}>
            <Input value={name} onChange={(e) => setName(e.target.value)} disabled={locked || saving} maxLength={120} placeholder="Your name" />
          </Field>
        </div>

        {locked && availableAt && (
          <div className="mt-3 flex items-center gap-2 rounded-lg bg-slate-50 p-3 text-sm text-ink-muted">
            <Lock size={15} /> You can change your name again on <span className="font-medium text-ink">{formatDate(availableAt)}</span>.
          </div>
        )}

        <div className="mt-5 flex justify-end">
          <Button type="submit" loading={saving} disabled={locked}>Save changes</Button>
        </div>
      </form>
    </PageContainer>
  );
}
