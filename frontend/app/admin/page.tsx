"use client";
import { useEffect, useState } from "react";
import { doubtAPI, SG_LEVELS } from "@/lib/doubtApi";
import { useRouter } from "next/navigation";
import { Shield, Users, GraduationCap, PenSquare, Ban, CheckCircle2, UserX, PenLine, UserPlus, KeyRound, Copy } from "lucide-react";
import { adminAPI, getUser, authAPI } from "@/lib/api";
import { coursesAPI, type Course, type Enrolment } from "@/lib/coursesApi";
import CoursePicker from "@/components/CoursePicker";
import CourseMigration from "./CourseMigration";
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
  needs_activation: boolean;
  parent_email: string | null;
  parent_phone: string | null;
  activated_at: string | null;
  terms_accepted_at: string | null;
  terms_price?: string | null;
  billing_currency?: string;
  ks3_year?: number | null;
  notify_email?: string | null;
  help_plan?: string | null;
  help_until?: string | null;
  sg_level?: string | null;
  subscription_label?: string;
  courses?: Enrolment[];
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
function IssueAccount({ onIssued, catalogue }: { onIssued: (i: Issued) => void; catalogue: Course[] }) {
  const [name, setName] = useState("");
  const [courses, setCourses] = useState<string[]>([]);
  const [email, setEmail] = useState("");
  const [touched, setTouched] = useState(false);
  const [role, setRole] = useState<"student" | "teacher">("student");
  const [access, setAccess] = useState<"trial" | "year">("trial");
  const [currency, setCurrency] = useState("GBP");
  const [prices, setPrices] = useState<{ currency: string; label: string; region: string }[]>([]);
  const [saving, setSaving] = useState(false);

  useEffect(() => { adminAPI.prices().then((r) => setPrices(r.data)).catch(() => {}); }, []);
  const priceLabel = prices.find((p) => p.currency === currency)?.label || "£49";
  const [error, setError] = useState("");

  // Suggest musa@beyondtutors.com from the name until the ID is edited by hand.
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
      const { data } = await coursesAPI.createUser({ full_name: name, email, role, access, currency, courses: role === "student" ? courses : [] });
      onIssued({ name: data.user.full_name, email: data.user.email, password: data.password, role });
      setName("");
      setEmail("");
      setTouched(false);
      setCourses([]);
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
      <p className="mt-1 text-sm text-ink-muted">Send the parent the ID and temporary password shown after you create the account. On first sign-in they enter their email and mobile, confirm an emailed code and set their own password.</p>
      <div className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
        <input className={field} value={name} onChange={(e) => setName(e.target.value)} placeholder="Full name (e.g. Musa Khan)" required />
        <input className={field} value={email} onChange={(e) => { setEmail(e.target.value); setTouched(true); }} placeholder="musa@beyondtutors.com" />
        <select className={field} value={role} onChange={(e) => setRole(e.target.value as any)}>
          <option value="student">Student</option>
          <option value="teacher">Tutor</option>
        </select>
        <select className={field} value={access} onChange={(e) => setAccess(e.target.value as any)} disabled={role !== "student"}>
          <option value="trial">Free trial access</option>
          <option value="year">Paid: 1 year ({priceLabel})</option>
        </select>
        <select className={field} value={currency} onChange={(e) => setCurrency(e.target.value)} disabled={role !== "student"}
          title="Currency Beyond Tutors bills this student in; shown in the parent's terms">
          {(prices.length ? prices : [{ currency: "GBP", label: "£49", region: "UK" }]).map((p) => (
            <option key={p.currency} value={p.currency}>{p.region}: {p.label} / year</option>
          ))}
        </select>
      </div>
      {role === "student" && (
        <div className="mt-3 flex flex-wrap items-center gap-2">
          <span className="text-sm font-medium text-ink">Courses:</span>
          {courses.map((c) => (
            <span key={c} className="inline-flex items-center gap-1 rounded-full bg-brand-50 px-2.5 py-1 text-xs font-semibold text-brand-700">
              {catalogue.find((x) => x.key === c)?.name || c}
              <button type="button" onClick={() => setCourses(courses.filter((x) => x !== c))} aria-label="Remove course" className="text-brand-400 hover:text-brand-700">×</button>
            </span>
          ))}
          <CoursePicker catalogue={catalogue} value="" exclude={courses} onChange={(k) => k && setCourses([...courses, k])}
            placeholder={courses.length ? "Add another course…" : "Choose the course they're paying for…"} className={field} />
          {courses.length === 0 && <span className="text-xs text-amber-700">No course: the student can open every course.</span>}
        </div>
      )}
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
    `When you first sign in, you'll be asked for a parent's email and mobile number. We'll email a 6-digit code to confirm it, and you'll choose your own password.

` +
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
  const [catalogue, setCatalogue] = useState<Course[]>([]);

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
        coursesAPI.catalogue().then((r) => setCatalogue(r.data)).catch(() => {});
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

  const [priceList, setPriceList] = useState<{ currency: string; label: string; region: string }[]>([]);
  useEffect(() => { adminAPI.prices().then((r) => setPriceList(r.data)).catch(() => {}); }, []);
  const changeCurrency = async (row: Row, currency: string) => {
    setBusy(row.id);
    try {
      await adminAPI.setCurrency(row.id, currency);
      load();
    } catch (e: any) {
      alert(e.response?.data?.detail || "Couldn't change the currency");
    } finally {
      setBusy(null);
    }
  };

  const changeDoubt = async (row: Row, plan: string, level?: string) => {
    setBusy(row.id);
    try {
      await doubtAPI.adminSet(row.id, { plan: plan || null, level: level || row.sg_level || "Sec 1" });
      load();
    } catch (e: any) {
      alert(e.response?.data?.detail || "Couldn't change Doubt Help");
    } finally {
      setBusy(null);
    }
  };

  const changeKs3 = async (row: Row, value: string) => {
    setBusy(row.id);
    try {
      const { data } = await adminAPI.setKs3(row.id, value ? Number(value) : null);
      if (value && data.tests_assigned) alert(`${row.full_name} is on KS3 Year ${value}: ${data.tests_assigned} test(s) and the notes were added.`);
      load();
    } catch (e: any) {
      alert(e.response?.data?.detail || "Couldn't change KS3");
    } finally {
      setBusy(null);
    }
  };

  const requireActivation = async (row: Row) => {
    if (!confirm(`Send ${row.full_name} back to "Pending activation"? They get a new temporary password, the saved parent email and phone are cleared, and the parent activates again on next sign-in.`)) return;
    setBusy(row.id);
    try {
      const { data } = await adminAPI.requireActivation(row.id);
      setIssued({ name: row.full_name, email: data.email, password: data.password, role: row.role });
      load();
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

  const addCourse = async (row: Row, course: string, access: "trial" | "year" | "none") => {
    if (!course) return;
    setBusy(row.id);
    try {
      await coursesAPI.add(row.id, course, access);
      load();
    } catch (e: any) {
      alert(e.response?.data?.detail || "Couldn't add the course.");
    } finally {
      setBusy(null);
    }
  };

  const removeCourse = async (row: Row, c: Enrolment) => {
    if (!confirm(`Remove ${c.name} from ${row.full_name}? They will lose access to it.`)) return;
    setBusy(row.id);
    try {
      await coursesAPI.remove(row.id, c.course);
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
      <IssueAccount catalogue={catalogue} onIssued={(i) => { setIssued(i); load(); }} />
      <CourseMigration catalogue={catalogue} onDone={load} />

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
                  <th className="px-4 py-3 font-medium">Parent activation</th>
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
                          {u.role === "student" && !u.is_admin && (
                            u.notify_email ? (
                              <div className="mt-0.5 text-xs text-emerald-700" title="Homework and class-notes emails go here">
                                ✉ Updates: {u.notify_email}
                              </div>
                            ) : (
                              <div className="mt-0.5 text-xs text-ink-subtle">✉ No update email yet</div>
                            )
                          )}
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
                      {u.role !== "student" || u.is_admin ? (
                        <span className="text-xs text-ink-subtle">—</span>
                      ) : u.needs_activation ? (
                        <div>
                          <span className="inline-flex rounded-full bg-amber-50 px-2 py-0.5 text-xs font-medium text-amber-700">Pending</span>
                          {u.parent_email && <div className="mt-1 text-xs text-ink-subtle">Code sent to {u.parent_email}</div>}
                        </div>
                      ) : u.activated_at ? (
                        <div className="text-xs">
                          <span className="inline-flex rounded-full bg-emerald-50 px-2 py-0.5 font-medium text-emerald-700">Activated {formatDate(u.activated_at)}</span>
                          <div className="mt-1 text-ink">{u.parent_email}</div>
                          <div className="text-ink-subtle">{u.parent_phone}</div>
                          {u.terms_accepted_at && (
                            <div className="text-ink-subtle">Agreed to {u.terms_price || "£49 per year"} terms {formatDate(u.terms_accepted_at)}</div>
                          )}
                        </div>
                      ) : (
                        <span className="text-xs text-ink-subtle">Not activated by a parent</span>
                      )}
                      {u.role === "student" && !u.is_admin && priceList.length > 0 && (
                        <select value={u.billing_currency || "GBP"} disabled={busy === u.id}
                          onChange={(e) => changeCurrency(u, e.target.value)} title="Billing currency shown in the parent's terms"
                          className="mt-1 block rounded-md border border-line bg-white px-1.5 py-0.5 text-xs text-ink outline-none focus:border-brand-500">
                          {priceList.map((p) => <option key={p.currency} value={p.currency}>{p.label}/yr ({p.region})</option>)}
                        </select>
                      )}
                      {u.role === "student" && !u.is_admin && (
                        <select value={u.ks3_year ? String(u.ks3_year) : ""} disabled={busy === u.id}
                          onChange={(e) => changeKs3(u, e.target.value)} title="Notenix KS3: tests, notes, homework help, monthly parent report"
                          className="mt-1 block rounded-md border border-line bg-white px-1.5 py-0.5 text-xs text-ink outline-none focus:border-brand-500">
                          <option value="">KS3: off</option>
                          <option value="7">KS3: Year 7</option>
                          <option value="8">KS3: Year 8</option>
                          <option value="9">KS3: Year 9</option>
                        </select>
                      )}
                      {u.role === "student" && !u.is_admin && (
                        <div className="mt-1 flex items-center gap-1">
                          <select value={u.help_plan && u.help_until && new Date(u.help_until + "Z") > new Date() ? u.help_plan : ""} disabled={busy === u.id}
                            onChange={(e) => changeDoubt(u, e.target.value)} title="Ask a Tutor: picking a plan adds its time (1 year, 30 days, or a 7-day trial)"
                            className="rounded-md border border-line bg-white px-1.5 py-0.5 text-xs text-ink outline-none focus:border-brand-500">
                            <option value="">Doubt Help: off</option>
                            <option value="trial">Doubt: trial (5 Qs)</option>
                            <option value="annual">Ask a Tutor 1 year (+365 days)</option>
                            <option value="doubt">Doubt Help (+30 days)</option>
                            <option value="plus">Doubt Plus (+30 days)</option>
                          </select>
                          <select value={u.sg_level || ""} disabled={busy === u.id} onChange={(e) => changeDoubt(u, u.help_plan || "", e.target.value)}
                            title="Singapore level (sets the subjects)" className="rounded-md border border-line bg-white px-1 py-0.5 text-xs text-ink">
                            <option value="">Level</option>
                            {SG_LEVELS.map((l) => <option key={l}>{l}</option>)}
                          </select>
                        </div>
                      )}
                      {u.role === "student" && !u.is_admin && u.help_plan && u.help_until && (
                        <div className="text-[11px] text-ink-subtle">Doubt Help until {formatDate(u.help_until)}</div>
                      )}
                      {u.role === "student" && !u.is_admin && !u.needs_activation && (
                        <button onClick={() => requireActivation(u)} disabled={busy === u.id}
                          className="mt-1 block text-xs font-medium text-brand-600 hover:underline disabled:opacity-50">
                          Ask parent to activate
                        </button>
                      )}
                    </td>
                    <td className="px-4 py-3">
                      <div>{accessLabel(u)}</div>
                      {u.role === "student" && !u.is_admin && !u.ks3_year && (
                        <CourseCell row={u} catalogue={catalogue} busy={busy === u.id} onAdd={addCourse} onRemove={removeCourse} />
                      )}
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

/** A student's courses: chips (× removes) and an add-course control. No courses = every course. */
function CourseCell({ row, catalogue, busy, onAdd, onRemove }: {
  row: Row; catalogue: Course[]; busy: boolean;
  onAdd: (row: Row, course: string, access: "trial" | "year" | "none") => void;
  onRemove: (row: Row, c: Enrolment) => void;
}) {
  const [access, setAccess] = useState<"trial" | "year" | "none">(row.access_kind === "trial" ? "trial" : "year");
  const list = row.courses ?? [];
  return (
    <div className="mt-2 max-w-[220px] space-y-1">
      {list.length === 0 ? (
        <div className="text-[11px] font-medium text-amber-700">All courses (none set)</div>
      ) : (
        <div className="flex flex-wrap gap-1">
          {list.map((c) => (
            <span key={c.course} title={c.until ? `${c.kind === "trial" ? "Trial" : "Paid"} until ${formatDate(c.until)}` : "No end date"}
              className={cn("inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-[11px] font-semibold",
                !c.live ? "bg-red-50 text-red-700 line-through" : c.kind === "trial" ? "bg-amber-50 text-amber-800" : "bg-brand-50 text-brand-700")}>
              {c.name}
              <button onClick={() => onRemove(row, c)} disabled={busy} aria-label={`Remove ${c.name}`} className="opacity-60 hover:opacity-100">×</button>
            </span>
          ))}
        </div>
      )}
      <div className="flex gap-1">
        <CoursePicker catalogue={catalogue} value="" disabled={busy} exclude={[]} onChange={(k) => onAdd(row, k, access)}
          placeholder="+ Course…" className="w-[120px] rounded-md border border-line bg-white px-1.5 py-0.5 text-xs text-ink-muted outline-none" />
        <select value={access} onChange={(e) => setAccess(e.target.value as any)} disabled={busy} title="Trial, a paid year (adds to a live course), or no end date"
          className="rounded-md border border-line bg-white px-1 py-0.5 text-xs text-ink-muted outline-none">
          <option value="year">1 year</option>
          <option value="trial">Trial</option>
          <option value="none">No end</option>
        </select>
      </div>
    </div>
  );
}
