"use client";
import { useEffect, useState } from "react";
import { Layers, CheckCircle2, Clock, Plus, ArrowLeft } from "lucide-react";
import { useAuthGuard } from "@/lib/guard";
import { coursesAPI, type Course, type Enrolment, type Price } from "@/lib/coursesApi";
import { PageContainer, PageHeader, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";
import CoursePicker from "@/components/CoursePicker";
import PaymentBox from "@/components/PaymentBox";
import { formatDate } from "@/lib/utils";

// My courses: what this student can open on their own, and buying another course
// (bank transfer; the course unlocks for a year once the team confirms the payment).
export default function CoursesPage() {
  const { user, ready } = useAuthGuard("student");
  const [data, setData] = useState<{ restricted: boolean; courses: Enrolment[]; pending: string[]; price: Price; prices?: Record<string, Price> } | null>(null);
  const [catalogue, setCatalogue] = useState<Course[]>([]);
  const [buying, setBuying] = useState("");

  const load = () => coursesAPI.mine().then((r) => setData(r.data)).catch(() => setData(null));
  useEffect(() => {
    if (!ready) return;
    load();
    coursesAPI.catalogue().then((r) => setCatalogue(r.data)).catch(() => {});
    const want = new URLSearchParams(window.location.search).get("add");
    if (want) setBuying(want);
  }, [ready]);

  if (!ready || !data) return <Spinner label="Loading your courses…" />;
  const name = (k: string) => catalogue.find((c) => c.key === k)?.name || k;
  const priceOf = (k: string) => data.prices?.[k] ?? data.price;  // SAT has its own price
  const live = data.courses.filter((c) => c.live);
  const ended = data.courses.filter((c) => !c.live);

  if (buying) {
    return (
      <PageContainer>
        <button onClick={() => setBuying("")} className="mb-4 inline-flex items-center gap-1 text-sm font-medium text-brand-600 hover:text-brand-700">
          <ArrowLeft size={15} /> My courses
        </button>
        <PageHeader icon={Plus} title={`Add ${name(buying)}`}
          subtitle={buying === "sat"
            ? `${priceOf(buying).label} for a year: full adaptive SAT practice tests, score reports and worked explanations.`
            : `${priceOf(buying).label} for a year: practice papers, quizzes, revision resources and test requests for ${name(buying)}.`} />
        <PaymentBox purpose="course" course={buying} amount={priceOf(buying).amount} currency={priceOf(buying).currency}
          reference={`NX-C${user?.id ?? ""}`} onClaimed={load} />
      </PageContainer>
    );
  }

  return (
    <PageContainer>
      <PageHeader icon={Layers} title="My courses" subtitle="The courses you can practise and revise on Notenix. Work your tutor sends you always appears, whatever the course." />

      {!data.restricted ? (
        <div className="card p-6 text-sm text-ink">
          <div className="flex items-center gap-2 font-semibold"><CheckCircle2 size={17} className="text-emerald-600" /> You can open every course</div>
          <p className="mt-1 text-ink-muted">Your account was set up before courses, so nothing is limited. Your tutor may set your courses later.</p>
        </div>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {live.map((c) => (
            <div key={c.course} className="card p-5">
              <span className={c.kind === "trial" ? "badge-neutral" : "badge-brand"}>{c.kind === "trial" ? "Free trial" : "Active"}</span>
              <h3 className="mt-3 font-semibold text-ink">{c.name}</h3>
              <p className="mt-1 text-sm text-ink-muted">{c.until ? `Until ${formatDate(c.until)}` : "No end date"}</p>
              {c.kind === "trial" && (
                <Button size="sm" className="mt-4" onClick={() => setBuying(c.course)}>Keep it: {priceOf(c.course).label} / year</Button>
              )}
            </div>
          ))}
          {ended.map((c) => (
            <div key={c.course} className="card border-red-200 p-5">
              <span className="badge-danger">Ended</span>
              <h3 className="mt-3 font-semibold text-ink">{c.name}</h3>
              <p className="mt-1 text-sm text-ink-muted">Ended {c.until ? formatDate(c.until) : ""}</p>
              <Button size="sm" className="mt-4" onClick={() => setBuying(c.course)}>Renew: {priceOf(c.course).label} / year</Button>
            </div>
          ))}
        </div>
      )}

      {data.pending.length > 0 && (
        <div className="mt-6 flex items-start gap-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-ink">
          <Clock size={17} className="mt-0.5 shrink-0 text-amber-600" />
          <span>We&apos;re checking your payment for {data.pending.map(name).join(", ")}. It unlocks as soon as it&apos;s confirmed, usually within 24 hours.</span>
        </div>
      )}

      {data.restricted && (
        <div className="card mt-8 p-6">
          <h2 className="flex items-center gap-2 font-semibold text-ink"><Plus size={18} /> Add a course</h2>
          <p className="mt-1 text-sm text-ink-muted">
            Each course is {data.price.label} for a year and unlocks its practice papers, quizzes, revision resources and test requests.
          </p>
          <CoursePicker catalogue={catalogue} value="" exclude={live.map((c) => c.course).concat(data.pending)}
            onChange={(k) => k && setBuying(k)} placeholder="Choose a course…"
            className="mt-4 w-full max-w-sm rounded-lg border border-line bg-white px-3 py-2 text-sm text-ink outline-none focus:border-brand-500" />
        </div>
      )}
    </PageContainer>
  );
}
