"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Send, LogIn } from "lucide-react";
import { requestsAPI, getUser } from "@/lib/api";
import { REQUEST_EXAMS } from "@/lib/requestExams";
import { Button } from "./ui/Button";
import { Input, Select, Field } from "./ui/Input";

const DRAFT_KEY = "notenix_request_draft";

// The request form works signed-out too: the draft is kept while the student signs up,
// then restored when they come back to /request.
export default function RequestForm() {
  const router = useRouter();
  const [signedIn, setSignedIn] = useState(false);
  const [price, setPrice] = useState<{ price: number; currency: string } | null>(null);
  const [exam, setExam] = useState("");  // blank = "Choose your exam", never a silent default
  const [subject, setSubject] = useState("");
  const [details, setDetails] = useState("");
  const [date, setDate] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setSignedIn(!!getUser());
    const qs = new URLSearchParams(window.location.search);
    const qsExam = qs.get("exam");
    const qsSubject = qs.get("subject");
    let d: any = null;
    try {
      d = JSON.parse(sessionStorage.getItem(DRAFT_KEY) || "null");
      if (d) { setExam(d.exam); setSubject(d.subject); setDetails(d.details); setDate(d.date); }
    } catch {}
    // A course link's exam/subject wins over a draft written for a different exam.
    if (qsExam && REQUEST_EXAMS.includes(qsExam) && d?.exam !== qsExam) {
      setExam(qsExam);
      setSubject((qsSubject || "").slice(0, 120));
    }
    requestsAPI.config().then((r) => setPrice({ price: r.data.price, currency: r.data.currency })).catch(() => {});
  }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (!signedIn) {
      try { sessionStorage.setItem(DRAFT_KEY, JSON.stringify({ exam, subject, details, date })); } catch {}
      router.push(`/register?returnTo=${encodeURIComponent(window.location.pathname + window.location.search)}`);
      return;
    }
    setBusy(true);
    try {
      await requestsAPI.create({ exam, subject, details, preferred_date: date ? new Date(date).toISOString() : null });
      try { sessionStorage.removeItem(DRAFT_KEY); } catch {}
      router.push("/requests?new=1");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Couldn't send your request. Please try again.");
      setBusy(false);
    }
  };

  return (
    <form onSubmit={submit} className="card space-y-5 p-6 sm:p-8">
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Exam">
          <Select value={exam} onChange={(e) => setExam(e.target.value)} required>
            <option value="" disabled>Choose your exam</option>
            {REQUEST_EXAMS.map((x) => <option key={x}>{x}</option>)}
          </Select>
        </Field>
        <Field label="Subject or paper" hint="e.g. Math, Physics, Paper 2, Biology">
          <Input value={subject} onChange={(e) => setSubject(e.target.value)} maxLength={120} />
        </Field>
      </div>
      <Field label="Anything we should know?" hint="Topics, tier/class, target score, exam date…">
        <textarea
          value={details}
          onChange={(e) => setDetails(e.target.value)}
          rows={4}
          maxLength={2000}
          className="w-full rounded-lg border border-line bg-white px-3.5 py-2.5 text-sm text-ink outline-none transition-all placeholder:text-ink-subtle focus:border-brand-500 focus:ring-4 focus:ring-brand-600/10"
        />
      </Field>
      <Field label="When would you like to sit it? (optional)">
        <Input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
      </Field>

      {price && (
        <p className="text-sm text-ink-muted">
          {price.price > 0
            ? <>Price: <b className="text-ink">{price.currency} {price.price.toFixed(2)}</b> per test, paid by bank transfer from any country.</>
            : <>Free right now: we assign the mock, you sit it online, and a tutor marks your written answers with
                feedback. No payment and no Pro needed. You can have up to 5 open requests at a time.</>}
        </p>
      )}
      {error && <p className="text-sm text-red-600">{error}</p>}
      <Button type="submit" size="lg" loading={busy} className="w-full sm:w-auto">
        {signedIn ? <><Send size={16} /> Send request</> : <><LogIn size={16} /> Create a free account to send</>}
      </Button>
      {!signedIn && (
        <p className="text-xs text-ink-subtle">
          Already have an account?{" "}
          <button type="button" onClick={() => {
            try { sessionStorage.setItem(DRAFT_KEY, JSON.stringify({ exam, subject, details, date })); } catch {}
            router.push(`/login?returnTo=${encodeURIComponent(window.location.pathname + window.location.search)}`);
          }} className="font-semibold text-brand-600 hover:underline">Sign in</button>{" "}
          · By sending a request you agree to our <a href="/terms" className="underline">terms</a> and{" "}
          <a href="/privacy" className="underline">privacy policy</a>.
        </p>
      )}
    </form>
  );
}
