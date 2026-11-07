import type { Metadata } from "next";
import Link from "next/link";
import { ArrowRight, Clock } from "lucide-react";
import { SITE } from "@/lib/site";
import { GUIDES } from "@/lib/guides";
import { YEARS, yearSlug } from "@/lib/ks3Topics";

export const metadata: Metadata = {
  title: "Guides for Parents: Year 7, KS3 and Homework Help",
  description: "Practical guides for parents of secondary school children: the Year 7 dip, what Year 7 covers, parents' evening questions and helping with maths homework.",
  alternates: { canonical: `${SITE}/guides` },
};

export default function GuidesIndex() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6">
      <span className="eyebrow">For parents</span>
      <h1 className="mt-2 text-3xl font-bold tracking-tight text-ink sm:text-4xl">Guides for parents</h1>
      <p className="mt-3 max-w-2xl text-ink-muted">Clear, practical help for supporting your child through Years 7, 8 and 9, written by Team Notenix with Beyond Tutors tutors.</p>
      <div className="mt-10 grid gap-5 sm:grid-cols-2">
        {GUIDES.map((g) => (
          <Link key={g.slug} href={`/guides/${g.slug}`} className="card group flex flex-col p-6 transition hover:border-brand-300">
            <span className="text-xs font-semibold uppercase tracking-wide text-brand-600">{g.tag}</span>
            <h2 className="mt-2 text-lg font-semibold text-ink group-hover:text-brand-700">{g.title}</h2>
            <p className="mt-2 flex-1 text-sm text-ink-muted">{g.description}</p>
            <span className="mt-4 inline-flex items-center gap-1 text-xs text-ink-subtle"><Clock size={13} /> {g.minutes} min read</span>
          </Link>
        ))}
      </div>
      <section className="mt-12 card p-6">
        <h2 className="font-semibold text-ink">Free KS3 notes and practice questions</h2>
        <p className="mt-1 text-sm text-ink-muted">Topic-by-topic notes with worked examples and practice questions.</p>
        <div className="mt-4 flex flex-wrap gap-3">
          {YEARS.map((y) => (
            <Link key={y} href={`/ks3/${yearSlug(y)}`} className="inline-flex items-center gap-1 rounded-full border border-line px-4 py-1.5 text-sm font-medium text-ink hover:border-brand-400">
              Year {y} topics <ArrowRight size={14} />
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
