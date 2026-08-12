"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { PenLine, FileUp, Lock, Sparkles, ArrowRight, BookOpen, CheckCircle2, Hourglass, Wand2, X } from "lucide-react";
import { practiceAPI, getUser } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, EmptyState, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import { Input, Select, Field } from "@/components/ui/Input";
import { humanize } from "@/lib/utils";

const SUBJECTS = ["maths", "biology", "chemistry", "physics", "computer_science", "economics", "english_literature", "geography", "history", "psychology", "business"];
const LEVELS = ["GCSE", "A-Level"];

interface LibItem {
  test_id: number;
  title: string;
  subject: string;
  topic: string;
  level: string;
  exam_board: string;
  num_questions: number;
  total_marks: number;
  attempted: boolean;
  marking_status: "graded" | "awaiting_marking" | null;
}

export default function PracticePage() {
  const router = useRouter();
  const { ready } = useAuthGuard("student");
  const user = getUser();
  const canWrite = !!user?.can_write_practice;
  const aiMarking = !!user?.ai_marking;

  const [library, setLibrary] = useState<LibItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // upload form
  const [files, setFiles] = useState<File[]>([]);
  const [subject, setSubject] = useState("chemistry");
  const [level, setLevel] = useState("GCSE");
  const [uploading, setUploading] = useState(false);
  const [starting, setStarting] = useState<number | null>(null);

  useEffect(() => {
    if (!ready || !canWrite) { setLoading(false); return; }
    practiceAPI
      .library()
      .then(({ data }) => setLibrary(data))
      .catch(() => setLibrary([]))
      .finally(() => setLoading(false));
  }, [ready, canWrite]);

  async function upload(e: React.FormEvent) {
    e.preventDefault();
    if (files.length === 0) { setError("Choose a PDF or image to upload."); return; }
    setError("");
    setUploading(true);
    try {
      const fd = new FormData();
      files.forEach((f) => fd.append("files", f));
      fd.append("subject", subject);
      fd.append("level", level);
      const { data } = await practiceAPI.uploadPaper(fd);
      router.push(`/tests/${data.assignment_id}`);
    } catch (e: any) {
      setError(e.response?.data?.detail || "Couldn't read that paper. Try a clearer file.");
      setUploading(false);
    }
  }

  async function startLibrary(item: LibItem) {
    if (item.attempted) { router.push(`/tests`); return; }
    setStarting(item.test_id);
    try {
      const { data } = await practiceAPI.startLibrary(item.test_id);
      router.push(`/tests/${data.assignment_id}`);
    } catch {
      setStarting(null);
    }
  }

  if (!ready || loading) return <Spinner label="Loading practice…" />;

  if (!canWrite) {
    return (
      <PageContainer>
        <PageHeader icon={PenLine} title="Written practice" subtitle="Practise extended-response exam questions and get examiner feedback." />
        <EmptyState
          icon={Lock}
          title="Written practice is a Pro feature"
          desc="Upgrade to Pro to practise writing full exam answers and get instant AI marking with feedback and model answers — or ask your teacher to enable access for you."
          action={<Button href="/pricing"><Sparkles size={16} /> See Pro plans</Button>}
        />
      </PageContainer>
    );
  }

  if (uploading) {
    return (
      <div className="mx-auto flex max-w-md flex-col items-center px-4 py-24 text-center">
        <span className="grid h-14 w-14 place-items-center rounded-2xl bg-brand-50 text-brand-600">
          <Wand2 size={26} className="animate-pulse" />
        </span>
        <h1 className="mt-5 text-lg font-semibold text-ink">Reading your paper & pulling out the questions…</h1>
        <p className="mt-1.5 text-sm text-ink-muted">This takes a few seconds.</p>
      </div>
    );
  }

  return (
    <PageContainer>
      <PageHeader
        icon={PenLine}
        title="Written practice"
        subtitle="Answer real past-paper questions in full — then get marked feedback."
      />

      <div className={`mb-6 rounded-xl border p-4 text-sm ${aiMarking ? "border-brand-100 bg-brand-50/60 text-ink-muted" : "border-amber-200 bg-amber-50 text-amber-800"}`}>
        {aiMarking ? (
          <span className="inline-flex items-center gap-1.5"><Sparkles size={14} className="text-brand-600" /> Your answers are marked instantly by AI with feedback and a model answer.</span>
        ) : (
          <span className="inline-flex items-center gap-1.5"><Hourglass size={14} /> Your answers are sent to your teacher for marking — you'll see feedback here once they're marked.</span>
        )}
      </div>

      {error && (
        <div className="mb-5 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">{error}</div>
      )}

      {/* Upload your own paper */}
      <form onSubmit={upload} className="card space-y-5 p-6">
        <div className="flex items-start gap-3">
          <span className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-brand-50 text-brand-600"><FileUp size={17} /></span>
          <div>
            <h2 className="text-base font-semibold text-ink">Upload a past paper</h2>
            <p className="text-sm text-ink-muted">We'll pull out the written questions so you can answer them.</p>
          </div>
        </div>
        <label className="flex cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed border-line-strong bg-slate-50 px-4 py-8 text-center transition-colors hover:border-brand-400 hover:bg-brand-50/40">
          <FileUp size={22} className="text-ink-subtle" />
          <span className="mt-2 text-sm font-medium text-ink">{files.length ? "Add more files" : "Choose a PDF or images"}</span>
          <span className="mt-0.5 text-xs text-ink-subtle">PDF, PNG or JPG · up to 10 files · 15 MB each</span>
          <input type="file" accept="application/pdf,.pdf,image/*" multiple className="hidden"
            onChange={(e) => {
              const picked = Array.from(e.target.files || []);
              setFiles((prev) => [...prev, ...picked].slice(0, 10));
              e.target.value = "";
            }} />
        </label>
        {files.length > 0 && (
          <ul className="space-y-2">
            {files.map((f, i) => (
              <li key={i} className="flex items-center justify-between gap-3 rounded-lg border border-line bg-white px-3 py-2 text-sm">
                <span className="truncate text-ink">{i + 1}. {f.name}</span>
                <button type="button" onClick={() => setFiles((prev) => prev.filter((_, j) => j !== i))}
                  className="shrink-0 text-ink-subtle hover:text-red-600" title="Remove">
                  <X size={15} />
                </button>
              </li>
            ))}
          </ul>
        )}
        <div className="grid gap-5 sm:grid-cols-2">
          <Field label="Subject">
            <Select value={subject} onChange={(e) => setSubject(e.target.value)}>
              {SUBJECTS.map((s) => <option key={s} value={s}>{humanize(s)}</option>)}
            </Select>
          </Field>
          <Field label="Level">
            <Select value={level} onChange={(e) => setLevel(e.target.value)}>{LEVELS.map((l) => <option key={l}>{l}</option>)}</Select>
          </Field>
        </div>
        <div className="flex justify-end border-t border-line pt-5">
          <Button type="submit" disabled={files.length === 0}><FileUp size={16} /> Start practice</Button>
        </div>
      </form>

      {/* Shared library */}
      <div className="mt-10">
        <h2 className="mb-3 flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-ink-subtle">
          <BookOpen size={15} /> Practice library
        </h2>
        {library.length === 0 ? (
          <div className="card p-6 text-sm text-ink-muted">No library papers yet — upload your own above to get started.</div>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2">
            {library.map((item) => (
              <div key={item.test_id} className="card card-hover flex flex-col p-5">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="badge-brand">{humanize(item.subject)}</span>
                  <span className="badge-neutral">{item.level}</span>
                  {item.exam_board && <span className="badge-neutral">{item.exam_board}</span>}
                </div>
                <h3 className="mt-3 font-semibold text-ink">{item.title}</h3>
                <div className="mt-1 text-xs text-ink-subtle">{item.num_questions} questions · {item.total_marks} marks</div>
                <div className="mt-4 flex items-center justify-between border-t border-line pt-4">
                  {item.attempted ? (
                    <span className="inline-flex items-center gap-1.5 text-xs font-medium text-emerald-600">
                      {item.marking_status === "awaiting_marking"
                        ? <><Hourglass size={13} className="text-amber-600" /> <span className="text-amber-600">Awaiting marking</span></>
                        : <><CheckCircle2 size={13} /> Completed</>}
                    </span>
                  ) : <span className="text-xs text-ink-subtle">Not started</span>}
                  <Button size="sm" onClick={() => startLibrary(item)} loading={starting === item.test_id}
                    variant={item.attempted ? "secondary" : "primary"}>
                    {item.attempted ? "View" : "Start"} <ArrowRight size={14} />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </PageContainer>
  );
}
