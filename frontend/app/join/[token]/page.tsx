"use client";
import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Link2, AlertCircle, Loader2 } from "lucide-react";
import { testsAPI, getUser } from "@/lib/api";
import { Logo } from "@/components/ui/Logo";
import { Button } from "@/components/ui/Button";

export default function JoinTestPage() {
  const router = useRouter();
  const params = useParams();
  const token = params?.token as string;
  const [state, setState] = useState<"checking" | "guest" | "joining" | "error">("checking");
  const [error, setError] = useState("");

  useEffect(() => {
    const hasToken = typeof window !== "undefined" && !!localStorage.getItem("notenix_token");
    if (!hasToken || !getUser()) {
      setState("guest");
      return;
    }
    setState("joining");
    testsAPI
      .join(token)
      .then(({ data }) => {
        router.replace(data.already_completed ? `/tests/${data.assignment_id}/result` : `/tests/${data.assignment_id}`);
      })
      .catch((e) => {
        setError(e.response?.data?.detail || "This test link is invalid or has been disabled.");
        setState("error");
      });
  }, [token, router]);

  const returnTo = `/join/${token}`;

  return (
    <div className="mx-auto flex min-h-[70vh] max-w-md flex-col items-center justify-center px-4 text-center">
      <Logo href="/" />

      {state === "checking" || state === "joining" ? (
        <div className="mt-8 flex items-center gap-2 text-ink-muted">
          <Loader2 className="animate-spin" size={18} /> Opening your test…
        </div>
      ) : state === "error" ? (
        <div className="mt-8">
          <span className="mx-auto grid h-12 w-12 place-items-center rounded-xl bg-red-50 text-red-600">
            <AlertCircle size={22} />
          </span>
          <h1 className="mt-4 text-lg font-semibold text-ink">Can't open this test</h1>
          <p className="mt-1.5 text-sm text-ink-muted">{error}</p>
          <Button href="/tests" variant="secondary" className="mt-6">Go to my tests</Button>
        </div>
      ) : (
        // guest
        <div className="mt-8 w-full">
          <span className="mx-auto grid h-12 w-12 place-items-center rounded-xl bg-brand-50 text-brand-600">
            <Link2 size={22} />
          </span>
          <h1 className="mt-4 text-xl font-bold text-ink">You've been invited to a test</h1>
          <p className="mt-2 text-sm text-ink-muted">Sign in or create a free student account to open it.</p>
          <div className="mt-6 flex flex-col gap-2">
            <Button href={`/register?returnTo=${encodeURIComponent(returnTo)}`} size="lg">Create free account</Button>
            <Button href={`/login?returnTo=${encodeURIComponent(returnTo)}`} variant="secondary" size="lg">Sign in</Button>
          </div>
        </div>
      )}
    </div>
  );
}
