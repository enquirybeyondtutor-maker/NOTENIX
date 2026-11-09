"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { Lock, BadgeCheck, LogIn, ArrowRight } from "lucide-react";
import { api, papersAPI } from "@/lib/api";
import { PageContainer, Spinner } from "@/components/ui/Page";
import { Button } from "@/components/ui/Button";

// Revision paper: page 1 is free, the rest load only for a signed-in student
// whose access is live (the backend checks it on every page request).
type State = "loading" | "visitor" | "member" | "ended" | "error";

export default function PaperPage() {
  const { slug } = useParams<{ slug: string }>();
  const [meta, setMeta] = useState<any | null>(null);
  const [state, setState] = useState<State>("loading");
  const [pages, setPages] = useState<string[]>([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    let urls: string[] = [];
    (async () => {
      try {
        const { data } = await papersAPI.info(slug);
        setMeta(data);
        if (!localStorage.getItem("notenix_token")) return setState("visitor");
        // Plain fetch so a 401 shows the sign-in prompt instead of bouncing to /login.
        const token = localStorage.getItem("notenix_token");
        const blobs: string[] = [];
        for (let n = 2; n <= data.pages; n++) {
          const res = await fetch(`/api/papers/${slug}/pages/${n}`, { headers: { Authorization: `Bearer ${token}` } });
          if (res.status === 401) return setState("visitor");
          if (res.status === 403) {
            setMessage((await res.json().catch(() => ({})))?.detail || "Your Notenix access has ended.");
            return setState("ended");
          }
          if (!res.ok) throw new Error(String(res.status));
          blobs.push(URL.createObjectURL(await res.blob()));
        }
        urls = blobs;
        setPages(blobs);
        setState("member");
      } catch {
        setState("error");
      }
    })();
    return () => urls.forEach((u) => URL.revokeObjectURL(u));
  }, [slug]);

  if (!meta && state === "loading") return <Spinner label="Loading paper…" />;
  if (!meta) return <PageContainer><p className="text-ink-muted">This paper could not be found.</p></PageContainer>;

  const returnTo = `/papers/${slug}`;
  return (
    <PageContainer className="max-w-3xl">
      <p className="text-sm font-semibold text-brand-600">Revision · {meta.subject}</p>
      <div className="mt-1 flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-2xl font-bold tracking-tight text-ink sm:text-3xl">{meta.title}</h1>
        <span className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-bold ${state === "member" ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-ink"}`}>
          {state === "member" ? <><BadgeCheck size={14} /> Notenix member</> : "Free preview"}
        </span>
      </div>
      <p className="mt-1 text-sm text-ink-muted">{meta.board} · {meta.pages} pages</p>

      <div className="mt-6 space-y-4">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={`${api.defaults.baseURL}/papers/${slug}/preview`} alt="Page 1" className="w-full rounded-xl border border-slate-200 bg-white" />
        {pages.map((src, i) => (
          // eslint-disable-next-line @next/next/no-img-element
          <img key={src} src={src} alt={`Page ${i + 2}`} className="w-full rounded-xl border border-slate-200 bg-white" />
        ))}
      </div>

      {state === "loading" && <Spinner label="Checking your access…" />}

      {(state === "visitor" || state === "ended") && (
        <div className="card mt-4 p-8 text-center">
          <span className="mx-auto grid h-12 w-12 place-items-center rounded-full bg-brand-50 text-brand-600"><Lock size={22} /></span>
          <p className="mt-3 text-lg font-semibold text-ink">
            {state === "ended" && /your courses/.test(message) ? "This paper is for another course" : state === "ended" ? "Renew to keep reading" : "The rest is waiting for you"}
          </p>
          <p className="mt-1 text-sm text-ink-muted">
            {state === "ended" ? message : `Unlock page 2 and the full paper (${meta.pages - 1} more pages) with Notenix.`}
          </p>
          <div className="mt-5 flex flex-col items-center gap-3">
            {state === "ended" && meta.course && /your courses/.test(message) ? (
              <Button href={`/courses?add=${meta.course}`}>Add {meta.course_name} <ArrowRight size={16} /></Button>
            ) : (
              <Button href="/pricing">Get Notenix access <ArrowRight size={16} /></Button>
            )}
            {state === "visitor" && (
              <a href={`/login?returnTo=${encodeURIComponent(returnTo)}`} className="inline-flex items-center gap-1.5 text-sm font-semibold text-brand-600">
                <LogIn size={15} /> Already a subscriber? Sign in
              </a>
            )}
          </div>
        </div>
      )}

      {state === "error" && (
        <div className="card mt-4 p-6 text-center text-sm text-ink-muted">
          We couldn&apos;t load the rest of this paper. Please refresh to try again.
        </div>
      )}
    </PageContainer>
  );
}
