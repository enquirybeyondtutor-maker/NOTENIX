"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Shield, Users, GraduationCap, PenSquare, Ban, CheckCircle2, UserX, PenLine, UserPlus, KeyRound, Copy } from "lucide-react";
import { adminAPI, getUser, authAPI } from "@/lib/api";
import { PageContainer, PageHeader, StatCard, Spinner, EmptyState } from "@/components/ui/Page";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { formatDate, relativeTime, cn } from "@/lib/utils";

interface Row {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  is_admin: boolean;
  can_write: boolean;
  plan: string;
  access_until: string | null;
  access_kind: string | null;
  created_at: string;
  last_active: string | null;
}

interface Issued {
  name: string;
  email: string;
  password: string;
  role: string;
}

function accessLabel(u: Row) {
  if (u.role !== "student" || u.is_admin) return <span className="text-xs text-ink-subtle">Staff</span>;
  if (!u.access_until) return <span className="text-xs text-ink-subtle">No expiry</span>;
  const ended = new Date(u.access_until + "Z") < new Date();
  return (
    <span className={cn("text-xs font-medium", ended ? "text-red-600" : u.access_kind === "trial" ? "text-amber-600" : "text-emerald-600")}>
      {u.access_kind === "trial" ? "Trial" : "Paid"} {ended ? "ended" : "until"} {formatDate(u.access_until)}
    </span>
  );
}

/** Form to issue a Beyond Tutors account; the generated password is shown once. */
function IssueAccount({ onIssued }: { onIssued: (i: Issued) => void }) {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [touched, setTouched] = useState(false);
  const [role, setRole] = useState<"student" | "teacher">("student");
  const [access, setAccess] = useState<"trial" | "year">("trial");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  // Suggest musa@thebeyondtutors.com from the name until the ID is edited by hand.
  useEffect(() => {
    if (touched || name.trim().length < 2) return;
    const t = setTimeout(() => adminAPI.suggestId(name).then((r) => setEmail(r.data.email)).catch(() => {}), 300);
    return () => clearTimeout(t);
  }, [name, touched]);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    try {
      const { data } = await adminAPI.createUser({ full_name: name, email, role, access });
      onIssued({ name: data.user.full_name, email: data.user.email, password: data.password, role });
      setName("");
      setEmail("");
      setTouched(false);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Couldn't create the account.");
    } finally {
      setSaving(false);
    }
  };

  const field = "rounded-lg border border-line bg-white px-3 py-2 text-sm text-ink outline-none focus:border-brand-500";
  return (
    <form onSubmit={submit} className="card mt-8 p-6">
      <h2 className="flex items-center gap-2 font-semibold text-ink"><UserPlus size={18} /> Issue a Notenix account</h2>
      <p className="mt-1 text-sm text-ink-muted">Students can't sign up or change their password. Give them the ID and password shown after you create the account.</p>
      <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <input className={field} value={name} onChange={(e) => setName(e.target.value)} placeholder="Full name (e.g. Musa Khan)" required />
        <input className={field} value={email} onChange={(e) => { setEmail(e.target.value); setTouched(true); }} placeholder="musa@thebeyondtutors.com" />
        <select className={field} value={role} onChange={(e) => setRole(e.target.value as any)}>
          <option value="student">Student</option>
          <option value="teacher">Tutor</option>
        </select>
        <select className={field} value={access} onChange={(e) => setAccess(e.target.value as any)} disabled={role !== "student"}>
          <option value="trial">Free trial access</option>
          <option value="year">Paid: 1 year (£49)</option>
        </select>
      </div>
      <div className="mt-4 flex items-center gap-3">
        <Button type="submit" loading={saving}>Create account</Button>
        {error && <span className="text-sm text-red-600">{error}</span>}
      </div>
    </form>
  );
}

function IssuedCard({ issued, onClose }: { issued: Issued; onClose: () => void }) {
  const [copied, setCopied] = useState(false);
  const message =
    `Hi ${issued.name.split(" ")[0]}, your Notenix account from Beyond Tutors is ready.\n\n` +
    `Sign in: https://www.notenix.com/login\nUser ID: ${issued.email}\nPassword: ${issued.password}\n\n` +
    `Your homework, tests and class notes will all be there. Please keep these details private.`;
  return (
    <div className="mt-6 rounded-xl border border-emerald-200 bg-emerald-50 p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="font-semibold text-emerald-900">Login details for {issued.name}</div>
          <div className="mt-2 font-mono text-sm text-emerald-900">User ID: {issued.email}<br />Password: {issued.password}</div>
          <p className="mt-2 text-xs text-emerald-800">This password is shown only once. Copy it now; you can always reset it later.</p>
        </div>
        <button onClick={onClose} className="text-xs text-emerald-800 hover:underline">Close</button>
      </div>
      <Button size="sm" variant="secondary" className="mt-3"
        onClick={() => navigator.clipboard.writeText(message).then(() => setCopied(true))}>
        <Copy size={14} /> {copied ? "Copied" : "Copy welcome message"}
      </Button>
    </div>
  );
}

export default function AdminPage() {
  const router = useRouter();
  const [ready, setReady] = useState(false);
  const [overview, setOverview] = useState<any>(null);
  const [users, setUsers] = useState<Row[]>([]);
  const [busy, setBusy] = useState<number | null>(null);
  const [issued, setIssued] = useState<Issued | null>(null);

  useEffect(() => {
    const token = typeof window !== "undefined" ? localStorage.getItem("notenix_token") : null;
    if (!token) {
      router.replace("/login");
      return;
    }
    authAPI
      .me()
      .then(({ data }) => {
        if (!data.is_admin) {
          router.replace(data.role === "teacher" ? "/teacher" : "/dashboard");
          return;
        }
        setReady(true);
        load();
      })
      .catch(() => router.replace("/login"));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const load = () => {
    Promise.all([
      adminAPI.overview().then((r) => r.data).catch(() => null),
      adminAPI.users().then((r) => r.data).catch(() => []),
    ]).then(([o, u]) => {
      setOverview(o);
      setUsers(u);
    });
  };

  const toggleBan = async (row: Row) => {
    setBusy(row.id);
    try {
      if (row.is_active) await adminAPI.ban(row.id);
      else await adminAPI.unban(row.id);
      load();
    } catch (e: any) {
      alert(e.response?.data?.detail || "Action failed");
    } finally {
      setBusy(null);
    }
  };

  const changeRole = async (row: Row, role: string) => {
    setBusy(row.id);
    try {
      await adminAPI.setRole(row.id, role);
      load();
    } finally {
      setBusy(null);
    }
  };

  const toggleWrite = async (row: Row) => {
    setBusy(row.id);
    try {
      await adminAPI.setWriteAccess(row.id, !row.can_write);
      load();
    } catch (e: any) {
      alert(e.response?.data?.detail || "Action failed");
    } finally {
      setBusy(null);
    }
  };

  const resetPw = async (row: Row) => {
    if (!confirm(`Give ${row.full_name} a new password? They'll be signed out everywhere.`)) return;
    setBusy(row.id);
    try {
      const { data } = await adminAPI.resetPassword(row.id);
      setIssued({ name: row.full_name, email: data.email, password: data.password, role: row.role });
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (e: any) {
      alert(e.response?.data?.detail || "Action failed");
    } finally {
      setBusy(null);
    }
  };

  const changeAccess = async (row: Row, access: string) => {
    if (!access) return;
    setBusy(row.id);
    try {
      await adminAPI.setAccess(row.id, access as "trial" | "year" | "none");
      load();
    } finally {
      setBusy(null);
    }
  };

  if (!ready) return <Spinner label="Loading admin…" />;

  return (
    <PageContainer>
      <PageHeader icon={Shield} title="Admin" subtitle="Manage users, roles and access."
        actions={<Button href="/admin/requests" size="sm">Test requests &amp; payments</Button>} />

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard label="Total users" value={overview?.users ?? 0} icon={Users} />
        <StatCard label="Teachers" value={overview?.teachers ?? 0} icon={PenSquare} />
        <StatCard label="Students" value={overview?.students ?? 0} icon={GraduationCap} />
        <StatCard label="Suspended" value={overview?.suspended ?? 0} icon={UserX} />
      </div>

      {issued && <IssuedCard issued={issued} onClose={() => setIssued(null)} />}
      <IssueAccount onIssued={(i) => { setIssued(i); load(); }} />

      <h2 className="mb-3 mt-8 text-sm font-semibold uppercase tracking-wide text-ink-subtle">
        All users · {users.length}
      </h2>

      {users.length === 0 ? (
        <EmptyState icon={Users} title="No users yet" />
      ) : (
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-line text-left text-xs uppercase tracking-wide text-ink-subtle">
                  <th className="px-4 py-3 font-medium">User</th>
                  <th className="px-4 py-3 font-medium">Role</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                  <th className="px-4 py-3 font-medium">Access</th>
                  <th className="px-4 py-3 font-medium">Written</th>
                  <th className="px-4 py-3 font-medium">Joined</th>
                  <th className="px-4 py-3 font-medium text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-line">
                {users.map((u) => (
                  <tr key={u.id} className={cn(!u.is_active && "bg-red-50/40")}>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-3">
                        <span className="grid h-8 w-8 place-items-center rounded-lg bg-brand-50 text-xs font-semibold text-brand-700">
                          {(u.full_name?.[0] || "U").toUpperCase()}
                        </span>
                        <div>
                          <div className="font-medium text-ink">
                            {u.full_name} {u.is_admin && <Badge tone="brand" className="ml-1">admin</Badge>}
                          </div>
                          <div className="text-xs text-ink-subtle">{u.email}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <select
                        value={u.role}
                        disabled={u.is_admin || busy === u.id}
                        onChange={(e) => changeRole(u, e.target.value)}
                        className="rounded-md border border-line bg-white px-2 py-1 text-xs text-ink outline-none focus:border-brand-500 disabled:opacity-60"
                      >
                        <option value="student">student</option>
                        <option value="teacher">teacher</option>
                        <option value="admin">admin</option>
                      </select>
                    </td>
                    <td className="px-4 py-3">
                      {u.is_active ? (
                        <span className="badge-success"><CheckCircle2 size={12} /> Active</span>
                      ) : (
                        <span className="badge-danger"><Ban size={12} /> Suspended</span>
                      )}
                    </td>
                    <td className="px-4 py-3">
                      <div>{accessLabel(u)}</div>
                      {u.role === "student" && !u.is_admin && (
                        <select value="" disabled={busy === u.id} onChange={(e) => changeAccess(u, e.target.value)}
                          className="mt-1 rounded-md border border-line bg-white px-1.5 py-0.5 text-xs text-ink-muted outline-none">
                          <option value="">Change…</option>
                          <option value="year">Add 1 paid year</option>
                          <option value="trial">Restart free trial</option>
                          <option value="none">Remove expiry</option>
                        </select>
                      )}
                    </td>
                    <td className="px-4 py-3">
                      {u.plan === "pro" ? (
                        <span className="inline-flex items-center gap-1 text-xs font-medium text-brand-700">
                          <PenLine size={12} /> Pro
                        </span>
                      ) : (
                        <button
                          onClick={() => toggleWrite(u)}
                          disabled={busy === u.id}
                          className={cn(
                            "inline-flex items-center gap-1 rounded-lg px-2.5 py-1 text-xs font-medium transition-colors disabled:opacity-50",
                            u.can_write ? "bg-brand-50 text-brand-700 hover:bg-brand-100" : "text-ink-subtle hover:bg-slate-100"
                          )}
                          title={u.can_write ? "Revoke written practice access" : "Grant written practice access"}
                        >
                          <PenLine size={12} /> {u.can_write ? "On" : "Off"}
                        </button>
                      )}
                    </td>
                    <td className="px-4 py-3 text-xs text-ink-subtle">{formatDate(u.created_at)}</td>
                    <td className="px-4 py-3 text-right">
                      {!u.is_admin && (
                        <button onClick={() => resetPw(u)} disabled={busy === u.id}
                          className="mr-1 rounded-lg px-3 py-1.5 text-xs font-medium text-brand-600 transition-colors hover:bg-brand-50 disabled:opacity-50">
                          <KeyRound size={12} className="mr-1 inline" />Reset password
                        </button>
                      )}
                      {u.is_admin ? (
                        <span className="text-xs text-ink-subtle">—</span>
                      ) : (
                        <button
                          onClick={() => toggleBan(u)}
                          disabled={busy === u.id}
                          className={cn(
                            "rounded-lg px-3 py-1.5 text-xs font-medium transition-colors disabled:opacity-50",
                            u.is_active ? "text-red-600 hover:bg-red-50" : "text-emerald-600 hover:bg-emerald-50"
                          )}
                        >
                          {u.is_active ? "Suspend" : "Reinstate"}
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </PageContainer>
  );
}
