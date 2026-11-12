"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { PenLine, Lock, ArrowRight, BookOpen, CheckCircle2, Hourglass } from "lucide-react";
import { practiceAPI, getUser } from "@/lib/api";
import { useAuthGuard } from "@/lib/guard";
import { PageContainer, PageHeader, EmptyState, Spinner } from "@/components/ui/Page";
import { coursesAPI } from "@/lib/coursesApi";
import { Button } from "@/components/ui/Button";
import { humanize } from "@/lib/utils";

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

  const [library, setLibrary] = useState<LibItem[]>([]);
  // Names of the student's live courses (null = no course limit), for the library hint.
  const [myCourses, setMyCourses] = useState<string[] | null>(null);
  useEffect(() => {
    coursesAPI.mine().then((r) => setMyCourses(r.data.restricted ? r.data.courses.filter((c) => c.live).map((c) => c.name) : null)).catch(() => {});
  }, []);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [starting, setStarting] = useState<number | null>(null);

  useEffect(() => {
    if (!ready || !canWrite) { setLoading(false); return; }
    practiceAPI
      .library()
      .then(({ data }) => setLibrary(data))
      .catch(() => setLibrary([]))
      .finally(() => setLoading(false));
  }, [ready, canWrite]);

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
        <PageHeader icon={PenLine} title="Written practice" subtitle="Practise extended-response exam questions and get feedback from a tutor." />
        <EmptyState
          icon={Lock}
          title="Written practice isn't switched on for you yet"
          desc="Ask your tutor to enable written practice, and you'll be able to answer full exam questions here and get them marked."
          action={<Button href="/courses">Open my courses</Button>}
        />
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <PageHeader
        icon={PenLine}
        title="Written practice"
        subtitle="Answer real past-paper questions in full — then get marked feedback."
      />

      <div className="mb-6 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800">
        <span className="inline-flex items-center gap-1.5"><Hourglass size={14} /> Your answers are sent to your tutor for marking. You'll see feedback here once they're marked.</span>
      </div>

      {error && (
        <div className="mb-5 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">{error}</div>
      )}

      {/* Shared library */}
      <div>
        <h2 className="mb-3 flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-ink-subtle">
          <BookOpen size={15} /> Practice library
        </h2>
        {myCourses && myCourses.length > 0 && (
          <p className="mb-3 text-sm text-ink-muted">
            Papers for your courses: {myCourses.join(", ")}.{" "}
            <a href="/courses" className="font-medium text-brand-600 hover:text-brand-700">Add a course</a>
          </p>
        )}
        {library.length === 0 ? (
          <div className="card p-6 text-sm text-ink-muted">No library papers yet. Your tutor will add papers here; you can also send a past paper to be marked from Request a test.</div>
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
