"use client";
import { useEffect, useState } from "react";
import { NotebookText, Paperclip, Trash2, X } from "lucide-react";
import { notesAPI, teacherAPI, adminAPI } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, Spinner, EmptyState } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Input, Field } from "@/components/ui/Input";
import NoteViewer from "@/components/NoteViewer";

const MAX_BYTES = 9 * 1024 * 1024;
const splitEmails = (s: string) => s.split(/[\s,;]+/).map((e) => e.trim().toLowerCase()).filter(Boolean);

export default function TeacherNotesPage() {
  const { user, ready } = useAuthGuard("teacher");
  const [notes, setNotes] = useState<any[] | null>(null);
  const [students, setStudents] = useState<{ email: string; full_name: string }[]>([]);
  const [form, setForm] = useState({ title: "", subject: "", body: "", emails: "" });
  const [file, setFile] = useState<{ name: string; data: string } | null>(null);
  const [saving, setSaving] = useState(false);
  const [msg, setMsg] = useState("");
  const [shareFor, setShareFor] = useState<Record<number, string>>({});

  const load = () => notesAPI.teacherList().then((r) => setNotes(r.data)).catch(() => setNotes([]));

  useEffect(() => {
    if (!ready) return;
    load();
    // Admins pick from every student; tutors from the students they teach.
    const src = user?.is_admin
      ? adminAPI.users().then((r) => r.data.filter((u: any) => u.role === "student"))
      : teacherAPI.students().then((r) => r.data);
    src.then(setStudents).catch(() => {});
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ready]);

  const pickFile = (f: File | undefined) => {
    if (!f) return setFile(null);
    if (f.size > MAX_BYTES) return setMsg("That file is over 9 MB. Please compress it first.");
    const r = new FileReader();
    r.onload = () => setFile({ name: f.name, data: String(r.result) });
    r.readAsDataURL(f);
  };

  const save = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setMsg("");
    try {
      const { data } = await notesAPI.create({
        title: form.title, subject: form.subject, body: form.body,
        file_name: file?.name, file_data: file?.data, student_emails: splitEmails(form.emails),
      });
      setMsg(data.not_found.length ? `Saved. No account found for: ${data.not_found.join(", ")}` : "Notes shared.");
      setForm({ title: "", subject: "", body: "", emails: "" });
      setFile(null);
      load();
    } catch (err: any) {
      setMsg(err.response?.data?.detail || "Couldn't save the notes.");
    } finally {
      setSaving(false);
    }
  };

  const share = async (id: number) => {
    const { data } = await notesAPI.share(id, splitEmails(shareFor[id] || ""));
    if (data.not_found.length) alert(`No account found for: ${data.not_found.join(", ")}`);
    setShareFor({ ...shareFor, [id]: "" });
    load();
  };

  if (!ready || notes === null) return <Spinner label="Loading notes…" />;
  return (
    <PageContainer>
      <PageHeader icon={NotebookText} title="Class notes" subtitle="Share notes (text, PDF or image) with your students." />

      <form onSubmit={save} className="card space-y-4 p-6">
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Title">
            <Input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required placeholder="TMUA: inequalities, class 3" />
          </Field>
          <Field label="Subject (optional)">
            <Input value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} placeholder="Maths" />
          </Field>
        </div>
        <Field label="Notes (optional; use $…$ for maths)">
          <textarea value={form.body} onChange={(e) => setForm({ ...form, body: e.target.value })} rows={5}
            className="w-full rounded-lg border border-line bg-white px-3 py-2 text-sm text-ink outline-none focus:border-brand-500" />
        </Field>
        <div className="flex flex-wrap items-center gap-3">
          <label className="inline-flex cursor-pointer items-center gap-1.5 rounded-lg border border-line px-3 py-2 text-sm text-ink-muted hover:bg-slate-50">
            <Paperclip size={14} /> {file ? file.name : "Attach PDF or image"}
            <input type="file" accept="application/pdf,image/*" className="hidden" onChange={(e) => pickFile(e.target.files?.[0])} />
          </label>
          {file && <button type="button" onClick={() => setFile(null)} className="text-ink-subtle hover:text-ink"><X size={16} /></button>}
        </div>
        <Field label="Share with (student IDs, separated by commas)">
          <Input value={form.emails} onChange={(e) => setForm({ ...form, emails: e.target.value })} list="note-students" placeholder="musa@thebeyondtutors.com" />
        </Field>
        <datalist id="note-students">
          {students.map((s) => <option key={s.email} value={s.email}>{s.full_name}</option>)}
        </datalist>
        <div className="flex items-center gap-3">
          <Button type="submit" loading={saving}>Save &amp; share</Button>
          {msg && <span className="text-sm text-ink-muted">{msg}</span>}
        </div>
      </form>

      <h2 className="mb-3 mt-8 text-sm font-semibold uppercase tracking-wide text-ink-subtle">Your notes · {notes.length}</h2>
      {notes.length === 0 ? (
        <EmptyState icon={NotebookText} title="No notes yet" />
      ) : (
        <div className="space-y-3">
          {notes.map((n) => (
            <NoteViewer key={n.id} note={n} footer={
              <div className="space-y-3 border-t border-line pt-4">
                <div className="flex flex-wrap gap-2">
                  {n.students.length === 0 && <span className="text-xs text-ink-subtle">Not shared with anyone yet.</span>}
                  {n.students.map((s: any) => (
                    <span key={s.id} className="inline-flex items-center gap-1 rounded-full bg-slate-100 px-2.5 py-1 text-xs text-ink">
                      {s.full_name}
                      <button onClick={() => notesAPI.unshare(n.id, s.id).then(load)} title="Stop sharing" className="text-ink-subtle hover:text-red-600"><X size={12} /></button>
                    </span>
                  ))}
                </div>
                <div className="flex flex-wrap items-center gap-2">
                  <Input value={shareFor[n.id] || ""} onChange={(e) => setShareFor({ ...shareFor, [n.id]: e.target.value })}
                    list="note-students" placeholder="Add student ID" className="max-w-xs" />
                  <Button size="sm" variant="secondary" onClick={() => share(n.id)}>Share</Button>
                  <button onClick={() => { if (confirm("Delete these notes for everyone?")) notesAPI.remove(n.id).then(load); }}
                    className="ml-auto inline-flex items-center gap-1 text-xs font-medium text-red-600 hover:text-red-700">
                    <Trash2 size={13} /> Delete
                  </button>
                </div>
              </div>
            } />
          ))}
        </div>
      )}
    </PageContainer>
  );
}
