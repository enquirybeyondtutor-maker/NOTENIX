"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Shield, Users, GraduationCap, PenSquare, Ban, CheckCircle2, UserX } from "lucide-react";
import { adminAPI, getUser, authAPI } from "@/lib/api";
import { PageContainer, PageHeader, StatCard, Spinner, EmptyState } from "@/components/ui/Page";
import { Badge } from "@/components/ui/Badge";
import { formatDate, relativeTime, cn } from "@/lib/utils";

interface Row {
  id: number;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
  is_admin: boolean;
  plan: string;
  created_at: string;
  last_active: string | null;
}

export default function AdminPage() {
  const router = useRouter();
  const [ready, setReady] = useState(false);
  const [overview, setOverview] = useState<any>(null);
  const [users, setUsers] = useState<Row[]>([]);
  const [busy, setBusy] = useState<number | null>(null);

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

  if (!ready) return <Spinner label="Loading admin…" />;

  return (
    <PageContainer>
      <PageHeader icon={Shield} title="Admin" subtitle="Manage users, roles and access." />

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard label="Total users" value={overview?.users ?? 0} icon={Users} />
        <StatCard label="Teachers" value={overview?.teachers ?? 0} icon={PenSquare} />
        <StatCard label="Students" value={overview?.students ?? 0} icon={GraduationCap} />
        <StatCard label="Suspended" value={overview?.suspended ?? 0} icon={UserX} />
      </div>

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
                    <td className="px-4 py-3 text-xs text-ink-subtle">{formatDate(u.created_at)}</td>
                    <td className="px-4 py-3 text-right">
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
