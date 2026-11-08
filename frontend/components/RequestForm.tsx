"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Send, Lock, FileText } from "lucide-react";
import { requestsAPI, getUser, saveAuth } from "@/lib/api";
import { REQUEST_EXAMS } from "@/lib/requestExams";
import { Button } from "./ui/Button";
import { Input, Select, Field } from "./ui/Input";

const DRAFT_KEY = "notenix_request_draft";

// "Get this paper marked" links from the Beyond Tutors past-papers pages carry the paper:
// /request?exam=GCSE&paper=Paper%201H&code=8300/1H&series=June%202024&course=AQA%20GCSE%20Maths&qp=…&ms=…
type Paper = { name: string; code?: string; series?: string; course?: string; qp?: string; ms?: string };

function paperFromUrl(qs: URLSearchParams): Paper | null {
  const name = (qs.get("paper") || "").trim().slice(0, 120);
  if (!name) return null;
  const get = (k: string) => (qs.get(k) || "").trim().slice(0, 500) || undefined;
  return { name, code: get("code"), series: get("series"), course: get("course"), qp: get("qp"), ms: get("ms") };
}

export const paperLabel = (p: Paper) =>
  [p.course, p.series, p.name + (p.code ? ` (${p.code})` : "")].filter(Boolean).join(" · ");

// Signed-out visitors get one free test: they leave the student's name, email, WhatsApp and a
// password, which creates a free account they use to sit the test. After that, more tests need
// a subscription (the backend answers 402).
export default function RequestForm() {
  const router = useRouter();
  const [signedIn, setSignedIn] = useState(false);
  const [price, setPrice] = useState<{ price: number; currency: string } | null>(null);
  const [exam, setExam] = useState("");  // blank = "Choose your exam", never a silent default
  const [subject, setSubject] = useState("");
  const [details, setDetails] = useState("");
  const [date, setDate] = useState("");
  const [guest, setGuest] = useState({ full_name: "", email: "", whatsapp: "", password: "" });
  const [needsSub, setNeedsSub] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [paper, setPaper] = useState<Paper | null>(null);

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
    const p = paperFromUrl(qs);
    if (p) {
      setPaper(p);
      if (qsExam && REQUEST_EXAMS.includes(qsExam)) setExam(qsExam);
      setSubject((qsSubject || p.course || "").slice(0, 120));
    }
    requestsAPI.config().then((r) => setPrice({ price: r.data.price, currency: r.data.currency })).catch(() => {});
  }, []);

  const setG = (k: keyof typeof guest) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setGuest((g) => ({ ...g, [k]: e.target.value }));

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setBusy(true);
    const preferred_date = date ? new Date(date).toISOString() : null;
    try {
      const extra = (paper ? { paper } : {}) as {};
      let assignmentId: number | null = null;
      if (signedIn) {
        const { data } = await requestsAPI.create({ exam, subject, details, preferred_date, ...extra });
        assignmentId = data.assignment_id;
      } else {
        const { data } = await requestsAPI.guest({ ...guest, exam, subject, details, preferred_date, ...extra });
        saveAuth(data.access_token, data.user);
        assignmentId = data.request?.assignment_id;
      }
      try { sessionStorage.removeItem(DRAFT_KEY); } catch {}
      // A marked past paper opens its upload page at once; other requests wait for the team.
      // Full load either way, so the header shows the new sign-in.
      window.location.href = paper && assignmentId ? `/tests/${assignmentId}` : "/requests?new=1";
    } catch (err: any) {
      if (err.response?.status === 402) setNeedsSub(true);
      setError(err.response?.data?.detail || "Couldn't send your request. Please try again.");
      setBusy(false);
    }
  };

  return (
    <form onSubmit={submit} className="card space-y-5 p-6 sm:p-8">
      {paper && (
        <div className="rounded-xl border border-brand-200 bg-brand-50 p-4">
          <div className="flex items-start gap-3">
            <FileText size={18} className="mt-0.5 shrink-0 text-brand-600" />
            <div>
              <div className="text-xs font-bold uppercase tracking-wide text-brand-700">Paper to be marked</div>
              <div className="mt-0.5 font-semibold text-ink">{paperLabel(paper)}</div>
              <p className="mt-1 text-sm text-ink-muted">
                Sit it at home, then upload photos of your answers. A tutor marks it against the official
                mark scheme and sends you your mark and feedback.
              </p>
            </div>
          </div>
        </div>
      )}
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
      <Field label={paper ? "Anything the tutor should know? (optional)" : "Anything we should know?"}
        hint={paper ? "Tier, target grade, exam date…" : "Topics, tier/class, target score, exam date…"}>
        <textarea
          value={details}
          onChange={(e) => setDetails(e.target.value)}
          rows={4}
          maxLength={2000}
          className="w-full rounded-lg border border-line bg-white px-3.5 py-2.5 text-sm text-ink outline-none transition-all placeholder:text-ink-subtle focus:border-brand-500 focus:ring-4 focus:ring-brand-600/10"
        />
      </Field>
      {!paper && (
        <Field label="When would you like to sit it? (optional)">
          <Input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
        </Field>
      )}

      {!signedIn && (
        <div className="space-y-4 border-t border-line pt-5">
          <div>
            <h3 className="font-semibold text-ink">Where should we send it?</h3>
            <p className="mt-1 text-sm text-ink-muted">
              {paper ? "We'll message you on WhatsApp and email when your paper is marked."
                : "Our team will message you on WhatsApp and email when your test is ready."}
            </p>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            <Field label="Student's full name">
              <Input required value={guest.full_name} onChange={setG("full_name")} maxLength={120} placeholder="e.g. Priya Patel" />
            </Field>
            <Field label="Email">
              <Input required type="email" value={guest.email} onChange={setG("email")} placeholder="you@example.com" />
            </Field>
            <Field label="WhatsApp number" hint="With country code, e.g. +61 412 345 678">
              <Input required type="tel" value={guest.whatsapp} onChange={setG("whatsapp")} placeholder="+44 7700 900123" />
            </Field>
            <Field label="Choose a password" hint="At least 8 characters. You'll sign in with it to sit your test.">
              <Input required type="password" minLength={8} value={guest.password} onChange={setG("password")} />
            </Field>
          </div>
        </div>
      )}

      {price && (
        <p className="text-sm text-ink-muted">
          {price.price > 0
            ? <>Price: <b className="text-ink">{price.currency} {price.price.toFixed(2)}</b> per test, paid by bank transfer from any country.</>
            : paper
              ? <>Your first marked paper is <b className="text-ink">free</b>. Your upload page opens straight away. For
                  more marked papers, subscribe to Notenix or join Beyond Tutors.</>
              : <>Your first test is <b className="text-ink">free</b>: we send the mock, you sit it online, and a tutor marks
                your written answers with feedback. For more tests, subscribe to Notenix or join Beyond Tutors.</>}
        </p>
      )}
      {needsSub ? (
        <div className="rounded-xl border border-brand-200 bg-brand-50 p-4 text-sm">
          <p className="font-semibold text-ink">You&apos;ve used your free test</p>
          <p className="mt-1 text-ink-muted">Subscribe to keep requesting tests, or join Beyond Tutors, where Notenix is included.</p>
          <div className="mt-3 flex flex-wrap gap-2">
            <Button href="/revision/checkout" size="sm">Subscribe: £149 / year</Button>
            <Button href="/pricing" variant="secondary" size="sm">See plans</Button>
          </div>
        </div>
      ) : error && <p className="text-sm text-red-600">{error}</p>}
      <Button type="submit" size="lg" loading={busy} className="w-full sm:w-auto">
        {paper
          ? <><Send size={16} /> {signedIn ? "Get my paper marked" : "Get my paper marked free"}</>
          : signedIn ? <><Send size={16} /> Send request</> : <><Lock size={16} /> Request my free test</>}
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
