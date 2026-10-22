import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowRight, CheckCircle2, ClipboardCheck, Send, PenLine, UserCheck } from "lucide-react";
import { EXAMS, EXAM_BY_SLUG } from "@/lib/exams";
import { SITE } from "@/lib/site";
import SampleQuiz from "@/components/SampleQuiz";
import { Button } from "@/components/ui/Button";

// Only the exams in lib/exams.ts exist; anything else 404s (static routes like /pricing win anyway).
export const dynamicParams = false;

export function generateStaticParams() {
  return EXAMS.map((e) => ({ exam: e.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ exam: string }> }): Promise<Metadata> {
  const exam = EXAM_BY_SLUG[(await params).exam];
  if (!exam) return {};
  const url = `${SITE}/${exam.slug}`;
  return {
    title: exam.title,
    description: exam.description,
    keywords: exam.keywords,
    alternates: { canonical: url },
    openGraph: { type: "website", url, siteName: "Notenix", title: exam.title, description: exam.description },
    twitter: { card: "summary_large_image", title: exam.title, description: exam.description },
  };
}

const STEPS = [
  { icon: Send, title: "Request a test", desc: "Tell us your exam and when you want to sit it." },
  { icon: ClipboardCheck, title: "We send it", desc: "Our team assigns a full mock to your Notenix account." },
  { icon: PenLine, title: "Sit it online", desc: "Timed, exam-style, on any device." },
  { icon: UserCheck, title: "Tutor marks it", desc: "Get your score, written feedback and next steps." },
];

export default async function ExamPage({ params }: { params: Promise<{ exam: string }> }) {
  const exam = EXAM_BY_SLUG[(await params).exam];
  if (!exam) notFound();
  const url = `${SITE}/${exam.slug}`;

  const jsonLd = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "Notenix", item: SITE },
          { "@type": "ListItem", position: 2, name: `${exam.name} practice`, item: url },
        ],
      },
      {
        "@type": "Course",
        name: `${exam.fullName} practice tests`,
        description: exam.description,
        url,
        provider: { "@type": "Organization", name: "Notenix", url: SITE },
        isAccessibleForFree: true,
        educationalLevel: exam.name,
        hasCourseInstance: { "@type": "CourseInstance", courseMode: "online", courseWorkload: "PT2H" },
        offers: { "@type": "Offer", price: "0", priceCurrency: "GBP", category: "Free" },
      },
      {
        "@type": "FAQPage",
        mainEntity: exam.faqs.map((f) => ({
          "@type": "Question",
          name: f.q,
          acceptedAnswer: { "@type": "Answer", text: f.a },
        })),
      },
    ],
  };

  const others = EXAMS.filter((e) => e.slug !== exam.slug);

  return (
    <div>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />

      {/* Hero */}
      <section className="relative overflow-hidden border-b border-line">
        <div className="dotted-grid absolute inset-0 opacity-70" />
        <div className="relative mx-auto max-w-5xl px-4 py-16 sm:px-6 lg:py-20">
          <nav aria-label="Breadcrumb" className="text-xs text-ink-subtle">
            <Link href="/" className="hover:text-ink">Notenix</Link> <span className="mx-1">/</span> {exam.name} practice
          </nav>
          <h1 className="mt-4 text-3xl font-bold tracking-tight text-ink sm:text-5xl">
            {exam.name} practice tests, <span className="text-brand-600">marked by tutors</span>
          </h1>
          <p className="mt-5 max-w-2xl text-lg text-ink-muted">{exam.tagline}</p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Button href="#try" size="lg">Try free questions <ArrowRight size={18} /></Button>
            <Button href={`/request?exam=${encodeURIComponent(exam.name)}`} variant="secondary" size="lg">
              Request a marked mock
            </Button>
          </div>
          <dl className="mt-10 grid grid-cols-2 gap-3 sm:grid-cols-4">
            {exam.facts.map((f) => (
              <div key={f.label} className="rounded-xl border border-line bg-white px-4 py-3">
                <dt className="text-xs font-medium text-ink-subtle">{f.label}</dt>
                <dd className="mt-1 text-sm font-semibold text-ink">{f.value}</dd>
              </div>
            ))}
          </dl>
        </div>
      </section>

      {/* About + format */}
      <section className="mx-auto grid max-w-5xl gap-10 px-4 py-16 sm:px-6 lg:grid-cols-2">
        <div>
          <h2 className="text-2xl font-bold text-ink">What is the {exam.fullName}?</h2>
          <p className="mt-4 leading-relaxed text-ink-muted">{exam.intro}</p>
          <h3 className="mt-8 text-lg font-semibold text-ink">{exam.name} format</h3>
          <ul className="mt-3 space-y-2">
            {exam.format.map((x) => (
              <li key={x} className="flex gap-2 text-sm leading-relaxed text-ink-muted">
                <CheckCircle2 size={16} className="mt-0.5 shrink-0 text-brand-600" /> {x}
              </li>
            ))}
          </ul>
        </div>
        <div className="card p-6 sm:p-8">
          <h2 className="text-xl font-bold text-ink">How Notenix helps you prepare</h2>
          <ul className="mt-5 space-y-3">
            {exam.howWeHelp.map((x) => (
              <li key={x} className="flex gap-2 text-sm leading-relaxed text-ink-muted">
                <CheckCircle2 size={16} className="mt-0.5 shrink-0 text-emerald-600" /> {x}
              </li>
            ))}
          </ul>
          <Button href="/register?returnTo=/request" className="mt-6 w-full">Create a free account</Button>
        </div>
      </section>

      {/* Free sample */}
      <section id="try" className="scroll-mt-20 border-y border-line bg-white">
        <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6">
          <span className="eyebrow">Free, no sign-up</span>
          <h2 className="mt-2 text-2xl font-bold text-ink">Free {exam.name} practice questions</h2>
          <p className="mt-2 text-ink-muted">Answer each question and check it instantly. Worked solutions included.</p>
          <div className="mt-8">
            <SampleQuiz examName={exam.name} questions={exam.samples} />
          </div>
        </div>
      </section>

      {/* Request flow */}
      <section className="mx-auto max-w-5xl px-4 py-16 sm:px-6">
        <h2 className="text-2xl font-bold text-ink">Get a full {exam.name} mock marked by our team</h2>
        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {STEPS.map((s, i) => (
            <div key={s.title}>
              <span className="grid h-10 w-10 place-items-center rounded-lg bg-brand-600 text-white"><s.icon size={18} /></span>
              <div className="mt-3 text-xs font-bold text-ink-subtle">0{i + 1}</div>
              <h3 className="mt-1 font-semibold text-ink">{s.title}</h3>
              <p className="mt-1 text-sm text-ink-muted">{s.desc}</p>
            </div>
          ))}
        </div>
        <Button href={`/request?exam=${encodeURIComponent(exam.name)}`} className="mt-8">
          Request a {exam.name} test <ArrowRight size={16} />
        </Button>
      </section>

      {/* FAQ */}
      <section className="border-t border-line bg-white">
        <div className="mx-auto max-w-3xl px-4 py-16 sm:px-6">
          <h2 className="text-2xl font-bold text-ink">{exam.name} practice: frequently asked questions</h2>
          <div className="mt-6 divide-y divide-line">
            {exam.faqs.map((f) => (
              <details key={f.q} className="group py-4">
                <summary className="cursor-pointer list-none font-medium text-ink marker:hidden">
                  <span className="flex items-center justify-between gap-4">
                    {f.q}
                    <span className="text-ink-subtle transition-transform group-open:rotate-45">+</span>
                  </span>
                </summary>
                <p className="mt-2 text-sm leading-relaxed text-ink-muted">{f.a}</p>
              </details>
            ))}
          </div>
          <div className="mt-10 text-sm text-ink-muted">
            Also practise:{" "}
            {others.map((e, i) => (
              <span key={e.slug}>
                <Link href={`/${e.slug}`} className="font-medium text-brand-600 hover:underline">{e.name}</Link>
                {i < others.length - 1 ? " · " : ""}
              </span>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}
