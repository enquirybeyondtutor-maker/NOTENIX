import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowRight, ChevronRight, CheckCircle2 } from "lucide-react";
import { MathText } from "@/components/MathText";
import { Button } from "@/components/ui/Button";
import { SITE } from "@/lib/site";
import { TOPICS, blocks, findTopic, summary, topicPath, topicsFor, yearSlug, subjectSlug } from "@/lib/ks3Topics";

type Params = { year: string; subject: string; topic: string };
export const dynamicParams = false;

export function generateStaticParams(): Params[] {
  return TOPICS.map((t) => ({ year: yearSlug(t.year), subject: subjectSlug(t.subject), topic: t.slug }));
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const p = await params;
  const t = findTopic(p.year, p.subject, p.topic);
  if (!t) return {};
  const title = `Year ${t.year} ${t.subject}: ${t.title} (KS3 notes and practice questions)`;
  return {
    title,
    description: `${summary(t)} Free KS3 notes with ${t.questions.length} practice questions and worked answers.`,
    alternates: { canonical: `${SITE}${topicPath(t)}` },
    openGraph: { title, url: `${SITE}${topicPath(t)}`, type: "article" },
  };
}

export default async function TopicPage({ params }: { params: Promise<Params> }) {
  const p = await params;
  const t = findTopic(p.year, p.subject, p.topic);
  if (!t) notFound();
  const others = topicsFor(t.year).filter((o) => o.key !== t.key);
  const url = `${SITE}${topicPath(t)}`;
  const jsonLd = [
    {
      "@context": "https://schema.org", "@type": "LearningResource", name: `Year ${t.year} ${t.subject}: ${t.title}`,
      description: summary(t), url, inLanguage: "en-GB", isAccessibleForFree: true,
      educationalLevel: `Key Stage 3, Year ${t.year}`, learningResourceType: ["Notes", "Practice questions"],
      about: t.subject, audience: { "@type": "EducationalAudience", educationalRole: "student" },
      provider: { "@type": "Organization", name: "Notenix", url: SITE },
    },
    {
      "@context": "https://schema.org", "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "KS3", item: `${SITE}/ks3` },
        { "@type": "ListItem", position: 2, name: `Year ${t.year}`, item: `${SITE}/ks3/${yearSlug(t.year)}` },
        { "@type": "ListItem", position: 3, name: `${t.subject}: ${t.title}`, item: url },
      ],
    },
  ];

  return (
    <article className="mx-auto max-w-3xl px-4 py-10 sm:px-6">
      <nav aria-label="Breadcrumb" className="flex flex-wrap items-center gap-1 text-sm text-ink-subtle">
        <Link href="/ks3" className="hover:text-ink">KS3</Link><ChevronRight size={14} />
        <Link href={`/ks3/${yearSlug(t.year)}`} className="hover:text-ink">Year {t.year}</Link><ChevronRight size={14} />
        <span className="text-ink-muted">{t.subject}</span>
      </nav>
      <span className="eyebrow mt-5 block">Year {t.year} {t.subject} · KS3 notes</span>
      <h1 className="mt-2 text-3xl font-bold tracking-tight text-ink sm:text-4xl">{t.title}</h1>
      <p className="mt-3 text-ink-muted">
        Clear notes with worked examples, then {t.questions.length} practice questions with answers. Written by Beyond Tutors tutors
        for the KS3 National Curriculum.
      </p>

      <div className="mt-8 space-y-4 text-[15px] leading-7 text-ink">
        {blocks(t.body).map((b, i) =>
          b.kind === "h" ? (
            <h2 key={i} className="pt-4 text-lg font-semibold text-ink">{b.text}</h2>
          ) : b.kind === "ul" ? (
            <ul key={i} className="list-disc space-y-1 pl-6 marker:text-brand-500">
              {b.items.map((it, j) => <li key={j}><MathText text={it} /></li>)}
            </ul>
          ) : (
            <p key={i} className="whitespace-pre-wrap [word-spacing:0.15em]"><MathText text={b.text.replace(/ {3,}/g, "     ")} /></p>
          ),
        )}
      </div>

      {t.questions.length > 0 && (
        <section className="mt-12">
          <h2 className="text-2xl font-bold text-ink">Practice questions</h2>
          <p className="mt-1 text-sm text-ink-muted">Try each one, then tap to see the answer and why.</p>
          <ol className="mt-5 space-y-4">
            {t.questions.map((q, i) => (
              <li key={i} className="card p-5">
                <div className="text-xs font-semibold uppercase tracking-wide text-brand-600">Question {i + 1} · {q.topic}</div>
                <p className="mt-2 whitespace-pre-line font-medium text-ink"><MathText text={q.question} /></p>
                <ul className="mt-3 grid gap-2 sm:grid-cols-2">
                  {q.options.map((o, j) => (
                    <li key={j} className="rounded-lg border border-line px-3 py-2 text-sm text-ink">
                      <span className="mr-2 font-semibold text-ink-subtle">{"ABCD"[j]}</span><MathText text={o} />
                    </li>
                  ))}
                </ul>
                <details className="mt-3 rounded-lg bg-canvas p-3 text-sm">
                  <summary className="cursor-pointer font-semibold text-brand-600">Show the answer</summary>
                  <p className="mt-2 flex items-start gap-2 text-ink">
                    <CheckCircle2 size={16} className="mt-0.5 shrink-0 text-emerald-600" />
                    <span><b>{"ABCD"[q.options.indexOf(q.answer)]}: <MathText text={q.answer} /></b></span>
                  </p>
                  <p className="mt-1 text-ink-muted"><MathText text={q.explanation} /></p>
                </details>
              </li>
            ))}
          </ol>
        </section>
      )}

      <aside className="mt-12 rounded-2xl border border-brand-200 bg-brand-50 p-6">
        <h2 className="text-xl font-bold text-ink">See where your child really stands</h2>
        <p className="mt-2 text-sm text-ink-muted">
          Notenix KS3 gives Year {t.year} students timed tests in Maths, Science and English, homework help from tutors,
          and a progress report for parents. Try it free for a week, no card needed.
        </p>
        <Button href="/ks3/trial" className="mt-4">Start a free week <ArrowRight size={16} /></Button>
      </aside>

      {others.length > 0 && (
        <section className="mt-12">
          <h2 className="text-lg font-semibold text-ink">More Year {t.year} topics</h2>
          <ul className="mt-3 grid gap-2 sm:grid-cols-2">
            {others.map((o) => (
              <li key={o.key}>
                <Link href={topicPath(o)} className="block rounded-lg border border-line px-4 py-3 text-sm hover:border-brand-400">
                  <span className="text-ink-subtle">{o.subject}:</span> <span className="font-medium text-ink">{o.title}</span>
                </Link>
              </li>
            ))}
          </ul>
        </section>
      )}

      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
    </article>
  );
}
