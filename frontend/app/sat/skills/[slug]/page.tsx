import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowRight } from "lucide-react";
import { SITE } from "@/lib/site";
import { Button } from "@/components/ui/Button";
import { MathText } from "@/components/MathText";
import SkillSamples from "@/components/sat/SkillSamples";
import skills from "@/lib/sat-skills.json";

// Public, indexable page per SAT skill: what the skill tests, 3 free practice questions with
// explanations (from backend/sat_content/drills.py, copied here at build by drills.py).
type Skill = (typeof skills)[number];
const BY_SLUG: Record<string, Skill> = Object.fromEntries(skills.map((s) => [s.slug, s]));
const plain = (s: string) => s.replace(/\$([^$]+)\$/g, "$1").replace(/\\[a-z]+/g, "");

export const dynamicParams = false;
export function generateStaticParams() {
  return skills.map((s) => ({ slug: s.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const s = BY_SLUG[(await params).slug];
  if (!s) return {};
  const title = `SAT ${s.skill}: Free Practice Questions with Explanations`;
  const description = `${plain(s.about)} Free Digital SAT ${s.skill} practice questions with worked explanations, plus a free SAT diagnostic.`;
  const url = `${SITE}/sat/skills/${s.slug}`;
  return { title, description, alternates: { canonical: url }, openGraph: { type: "article", url, title, description, siteName: "Notenix" } };
}

export default async function SatSkillPage({ params }: { params: Promise<{ slug: string }> }) {
  const s = BY_SLUG[(await params).slug];
  if (!s) notFound();
  const related = skills.filter((x) => x.domain === s.domain && x.slug !== s.slug);
  const section = s.section === "rw" ? "Reading and Writing" : "Math";
  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Notenix SAT", item: `${SITE}/sat` },
      { "@type": "ListItem", position: 2, name: "SAT skills", item: `${SITE}/sat/skills` },
      { "@type": "ListItem", position: 3, name: s.skill, item: `${SITE}/sat/skills/${s.slug}` },
    ],
  };
  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6">
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <nav className="text-sm text-ink-subtle"><Link href="/sat" className="hover:text-ink">SAT</Link> / <Link href="/sat/skills" className="hover:text-ink">Skills</Link> / {s.skill}</nav>
      <span className="eyebrow mt-6 block">{section} · {s.domain}</span>
      <h1 className="mt-2 text-3xl font-bold tracking-tight text-ink sm:text-4xl">SAT {s.skill}</h1>
      <p className="mt-3 text-lg text-ink-muted"><MathText text={s.about} /></p>
      <p className="mt-3 text-ink-muted">
        {s.skill} is one of the skills in the {s.domain} area of the Digital SAT {section} section. Try these three questions,
        then take the free diagnostic to see how this skill compares with the rest of your SAT.
      </p>

      <h2 className="mb-4 mt-10 text-xl font-bold text-ink">Free {s.skill} practice questions</h2>
      <SkillSamples questions={s.samples as any} />

      <div className="card mt-10 flex flex-col items-start gap-4 bg-brand-50/60 p-6 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <div className="font-semibold text-ink">Find your weakest SAT skills</div>
          <p className="text-sm text-ink-muted">A free 34-minute diagnostic gives you a score band out of 1600 and the skills costing you the most points.</p>
        </div>
        <Button href="/sat/diagnostic">Take the free diagnostic <ArrowRight size={16} /></Button>
      </div>

      {related.length > 0 && (
        <>
          <h2 className="mb-3 mt-10 text-lg font-bold text-ink">More {s.domain} skills</h2>
          <div className="flex flex-wrap gap-2">
            {related.map((r) => <Link key={r.slug} href={`/sat/skills/${r.slug}`} className="rounded-full border border-line px-3 py-1.5 text-sm text-ink hover:border-brand-300 hover:text-brand-700">{r.skill}</Link>)}
          </div>
        </>
      )}
    </div>
  );
}
