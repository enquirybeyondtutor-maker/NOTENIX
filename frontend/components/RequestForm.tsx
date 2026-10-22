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
  const [exam, setExam] = useState("SAT");
  const [subject, setSubject] = useState("");
  const [details, setDetails] = useState("");
  const [date, setDate] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    setSignedIn(!!getUser());
    const qsExam = new URLSearchParams(window.location.search).get("exam");
    try {
      const d = JSON.parse(sessionStorage.getItem(DRAFT_KEY) || "null");
      if (d) { setExam(d.exam); setSubject(d.subject); setDetails(d.details); setDate(d.date); }
    } catch {}
    if (qsExam && REQUEST_EXAMS.includes(qsExam)) setExam(qsExam);
    requestsAPI.config().then((r) => setPrice({ price: r.data.price, currency: r.data.currency })).catch(() => {});
  }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (!signedIn) {
      try { sessionStorage.setItem(DRAFT_KEY, JSON.stringify({ exam, subject, details, date })); } catch {}
      router.push("/register?returnTo=/request");
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
          <Select value={exam} onChange={(e) => setExam(e.target.value)}>
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
            : <>Requests are <b className="text-emerald-600">free</b> right now.</>}
        </p>
      )}
      {error && <p className="text-sm text-red-600">{error}</p>}
      <Button type="submit" size="lg" loading={busy} className="w-full sm:w-auto">
        {signedIn ? <><Send size={16} /> Send request</> : <><LogIn size={16} /> Create a free account to send</>}
      </Button>
    </form>
  );
}
