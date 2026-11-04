"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Lock, LogIn, Check, BadgeCheck, Clock } from "lucide-react";
import { PageContainer } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";

// Landing page for "Continue in Notenix" links from the Beyond Tutors revision
// library (thebeyondtutors.com/revision/<subject>/<course>/<topic>). The full
// notes / worksheets / topic questions are not written yet, so signed-in
// students with live access see "coming soon"; everyone else sees the plans.

const BT = "https://www.thebeyondtutors.com";
const KINDS: Record<string, string> = { notes: "Revision notes", worksheet: "Worksheet", questions: "Topic questions" };
const SUBJECTS: Record<string, string> = { "computer-science": "Computer Science" };
const LEVELS: Record<string, string> = { gcse: "GCSE", igcse: "IGCSE", "a-level": "A-Level" };
const BOARDS: Record<string, string> = { aqa: "AQA", edexcel: "Edexcel", ocr: "OCR", cie: "Cambridge" };

const title = (slug: string) => slug.split("-").map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join(" ");

function courseName(subject: string, course: string) {
  const [board, ...rest] = course.split("-").reverse();
  const level = rest.reverse().join("-");
  return `${BOARDS[board] ?? title(board)} ${LEVELS[level] ?? title(level)} ${SUBJECTS[subject] ?? title(subject)}`;
}

const PLAN_FEATURES = [
  "Notes, worksheets and topic questions for every topic",
  "GCSE and A-Level, all major boards",
  "Timed tests with instant marking",
];

export default function RevisionResourcePage() {
  const { subject, course, topic } = useParams<{ subject: string; course: string; topic: string }>();
  const [kind, setKind] = useState("notes");
  const [access, setAccess] = useState<"checking" | "none" | "live" | "ended">("checking");
  // Full resource pages, once written (backend/papers/<subject>-<course>-<topic>-<kind>).
  const [pages, setPages] = useState<string[] | null>(null);

  useEffect(() => {
    setKind(new URLSearchParams(window.location.search).get("type") ?? "notes");
    const token = localStorage.getItem("notenix_token");
    if (!token) return setAccess("none");
    // /auth/me runs the same access check as every protected page. Plain fetch, so an
    // old token shows the plans instead of bouncing to /login.
    const type = new URLSearchParams(window.location.search).get("type") ?? "notes";
    const auth = { headers: { Authorization: `Bearer ${token}` } };
    fetch("/api/auth/me", auth)
      .then(async (r) => {
        setAccess(r.ok ? "live" : r.status === 403 ? "ended" : "none");
        if (!r.ok) return;
        const slug = `${subject}-${course}-${topic}-${type}`;
        const meta = await fetch(`/api/papers/${slug}`);
        if (!meta.ok) return setPages([]);
        const { pages: n } = await meta.json();
        const urls: string[] = [];
        for (let i = 1; i <= n; i++) {
          const res = await fetch(`/api/papers/${slug}/pages/${i}`, auth);
          if (res.ok) urls.push(URL.createObjectURL(await res.blob()));
        }
        setPages(urls);
      })
      .catch(() => setAccess("none"));
  }, []);

  const label = KINDS[kind] ?? KINDS.notes;
  const name = title(topic);
  const here = `/revision/${subject}/${course}/${topic}?type=${kind}`;

  return (
    <PageContainer className="max-w-3xl">
      <p className="text-sm font-semibold text-brand-600">{courseName(subject, course)}</p>
      <h1 className="mt-1 text-2xl font-bold tracking-tight text-ink sm:text-3xl">{name}</h1>
      <div className="mt-3 flex flex-wrap gap-2">
        {Object.entries(KINDS).map(([k, l]) => (
          <a key={k} href={`/revision/${subject}/${course}/${topic}?type=${k}`}
            className={`rounded-full border px-3 py-1.5 text-sm font-semibold ${k === kind ? "border-brand-400 bg-brand-50 text-brand-700" : "border-slate-200 text-ink"}`}>
            {l}
          </a>
        ))}
      </div>

      {access === "live" && pages && pages.length > 0 ? (
        <div className="mt-6 space-y-4">
          <p className="inline-flex items-center gap-1.5 rounded-full bg-emerald-100 px-3 py-1 text-xs font-bold text-emerald-700"><BadgeCheck size={14} /> Full access</p>
          {pages.map((src, i) => (
            // eslint-disable-next-line @next/next/no-img-element
            <img key={src} src={src} alt={`${label}, page ${i + 1}`} className="w-full rounded-xl border border-slate-200 bg-white" />
          ))}
        </div>
      ) : access === "live" ? (
        <div className="card mt-6 p-8 text-center">
          <span className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-emerald-50 text-emerald-600"><Clock size={22} /></span>
          <p className="mt-3 text-lg font-semibold text-ink">{label} for {name} are on the way</p>
          <p className="mt-1 text-sm text-ink-muted">
            You have full access. This resource is being written and will appear here as soon as it&apos;s ready.
          </p>
        </div>
      ) : (
        <>
          <div className="card mt-6 p-8 text-center">
            <span className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-brand-50 text-brand-600"><Lock size={22} /></span>
            <p className="mt-3 text-lg font-semibold text-ink">
              {access === "ended" ? "Your access has ended" : `Unlock the full ${label.toLowerCase()}`}
            </p>
            <p className="mt-1 text-sm text-ink-muted">
              {access === "ended"
                ? "Renew to keep reading every topic."
                : `Page 2 onwards of ${name} ${label.toLowerCase()}, and every other topic, with Notenix.`}
            </p>
            {access !== "ended" && (
              <a href={`/login?returnTo=${encodeURIComponent(here)}`} className="mt-4 inline-flex items-center gap-1.5 text-sm font-semibold text-brand-600">
                <LogIn size={15} /> Already have Notenix? Sign in
              </a>
            )}
          </div>

          <div className="mt-6 grid gap-6 md:grid-cols-2">
            <div className="card flex flex-col p-7">
              <h2 className="text-lg font-semibold text-ink">Notenix full access</h2>
              <p className="mt-3"><span className="text-4xl font-bold text-ink">£149</span><span className="text-ink-muted"> / year</span></p>
              <ul className="mt-5 flex-1 space-y-2.5 text-sm text-ink">
                {PLAN_FEATURES.map((f) => <li key={f} className="flex gap-2"><Check size={16} className="mt-0.5 shrink-0 text-brand-600" />{f}</li>)}
              </ul>
              <Button href={`/revision/checkout?returnTo=${encodeURIComponent(here)}`} variant="secondary" className="mt-7 w-full">Pay £149</Button>
            </div>
            <div className="card relative flex flex-col p-7 ring-2 ring-brand-500">
              <span className="absolute -top-3 left-6 rounded-full bg-brand-600 px-3 py-1 text-xs font-bold text-white">Best value</span>
              <h2 className="text-lg font-semibold text-ink">Beyond Tutors students</h2>
              <p className="mt-3"><span className="text-4xl font-bold text-ink">£49</span><span className="text-ink-muted"> / year</span></p>
              <ul className="mt-5 flex-1 space-y-2.5 text-sm text-ink">
                {["Everything in full access", "Your own tutor sets homework and tests", "Free during your trial class"].map((f) => (
                  <li key={f} className="flex gap-2"><BadgeCheck size={16} className="mt-0.5 shrink-0 text-brand-600" />{f}</li>
                ))}
              </ul>
              <Button href={`/login?returnTo=${encodeURIComponent(here)}`} className="mt-7 w-full">I&apos;m a Beyond Tutors student · Sign in</Button>
              <a href={`${BT}/book`} className="mt-3 text-center text-sm font-semibold text-brand-600">Not a student yet? Join Beyond Tutors</a>
            </div>
          </div>
        </>
      )}
    </PageContainer>
  );
}
