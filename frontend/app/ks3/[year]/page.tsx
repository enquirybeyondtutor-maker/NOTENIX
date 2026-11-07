import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowRight, BookOpen } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { SITE } from "@/lib/site";
import { SUBJECTS, YEARS, topicPath, topicsFor, yearSlug } from "@/lib/ks3Topics";

type Params = { year: string };
export const dynamicParams = false;

export function generateStaticParams(): Params[] {
  return YEARS.map((y) => ({ year: yearSlug(y) }));
}

const yearOf = (slug: string) => YEARS.find((y) => yearSlug(y) === slug);

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const y = yearOf((await params).year);
  if (!y) return {};
  return {
    title: `Year ${y} Revision Notes and Practice Questions: Maths, Science, English (KS3)`,
    description: `Free Year ${y} KS3 notes with worked examples and practice questions in Maths, Science and English. Written by Beyond Tutors tutors for the National Curriculum.`,
    alternates: { canonical: `${SITE}/ks3/${yearSlug(y)}` },
  };
}

export default async function YearPage({ params }: { params: Promise<Params> }) {
  const y = yearOf((await params).year);
  if (!y) notFound();
  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6">
      <span className="eyebrow">KS3 · Year {y}</span>
      <h1 className="mt-2 text-3xl font-bold tracking-tight text-ink sm:text-4xl">Year {y} notes and practice questions</h1>
      <p className="mt-3 max-w-2xl text-ink-muted">
        Short, clear notes for each Year {y} topic, with worked examples and practice questions you can check straight away.
      </p>
      <div className="mt-10 grid gap-6 md:grid-cols-3">
        {SUBJECTS.map((s) => (
          <section key={s} className="card p-5">
            <h2 className="flex items-center gap-2 font-semibold text-ink"><BookOpen size={16} className="text-brand-600" /> {s}</h2>
            <ul className="mt-3 space-y-2">
              {topicsFor(y, s).map((t) => (
                <li key={t.key}><Link href={topicPath(t)} className="text-sm font-medium text-brand-700 hover:underline">{t.title}</Link></li>
              ))}
            </ul>
          </section>
        ))}
      </div>
      <div className="mt-8 flex flex-wrap gap-3 text-sm">
        {YEARS.filter((o) => o !== y).map((o) => (
          <Link key={o} href={`/ks3/${yearSlug(o)}`} className="rounded-full border border-line px-3 py-1 text-ink-muted hover:border-brand-400">Year {o} topics</Link>
        ))}
      </div>
      <aside className="mt-12 rounded-2xl border border-brand-200 bg-brand-50 p-6">
        <h2 className="text-xl font-bold text-ink">Track Year {y} progress, free for a week</h2>
        <p className="mt-2 text-sm text-ink-muted">Timed tests in all three subjects, homework help from tutors and a progress report for parents.</p>
        <Button href="/ks3/trial" className="mt-4">Start a free week <ArrowRight size={16} /></Button>
      </aside>
    </div>
  );
}
