import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowRight, ChevronRight, Clock } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { RichText } from "@/components/RichText";
import { SITE } from "@/lib/site";
import { GUIDES, guideBySlug } from "@/lib/guides";

type Params = { slug: string };
export const dynamicParams = false;

export function generateStaticParams(): Params[] {
  return GUIDES.map((g) => ({ slug: g.slug }));
}

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const g = guideBySlug((await params).slug);
  if (!g) return {};
  return {
    title: g.title,
    description: g.description,
    alternates: { canonical: `${SITE}/guides/${g.slug}` },
    openGraph: { title: g.title, description: g.description, url: `${SITE}/guides/${g.slug}`, type: "article",
      publishedTime: g.published, modifiedTime: g.updated },
  };
}

const fmt = (d: string) => new Date(d + "T12:00:00Z").toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" });

export default async function GuidePage({ params }: { params: Promise<Params> }) {
  const g = guideBySlug((await params).slug);
  if (!g) notFound();
  const url = `${SITE}/guides/${g.slug}`;
  const others = GUIDES.filter((o) => o.slug !== g.slug);
  const jsonLd = [
    {
      "@context": "https://schema.org", "@type": "Article", headline: g.title, description: g.description, url,
      datePublished: g.published, dateModified: g.updated, inLanguage: "en-GB",
      author: { "@type": "Organization", name: "Team Notenix", url: SITE },
      publisher: { "@type": "Organization", name: "Notenix", url: SITE, logo: { "@type": "ImageObject", url: `${SITE}/brand/notenix-email-logo.png` } },
      mainEntityOfPage: url,
    },
    {
      "@context": "https://schema.org", "@type": "FAQPage",
      mainEntity: g.faq.map((f) => ({ "@type": "Question", name: f.q, acceptedAnswer: { "@type": "Answer", text: f.a } })),
    },
    {
      "@context": "https://schema.org", "@type": "BreadcrumbList",
      itemListElement: [
        { "@type": "ListItem", position: 1, name: "Guides", item: `${SITE}/guides` },
        { "@type": "ListItem", position: 2, name: g.title, item: url },
      ],
    },
  ];

  return (
    <article className="mx-auto max-w-3xl px-4 py-10 sm:px-6">
      <nav aria-label="Breadcrumb" className="flex items-center gap-1 text-sm text-ink-subtle">
        <Link href="/guides" className="hover:text-ink">Parent guides</Link><ChevronRight size={14} /><span className="text-ink-muted">{g.tag}</span>
      </nav>
      <h1 className="mt-4 text-3xl font-bold tracking-tight text-ink sm:text-4xl">{g.title}</h1>
      <div className="mt-3 flex flex-wrap items-center gap-3 text-sm text-ink-subtle">
        <span>Team Notenix</span><span>·</span><span>Updated {fmt(g.updated)}</span><span>·</span>
        <span className="inline-flex items-center gap-1"><Clock size={14} /> {g.minutes} min read</span>
      </div>

      <div className="mt-8 space-y-4 text-[16px] leading-7 text-ink-muted">
        {g.intro.map((p, i) => <p key={i} className="text-lg leading-8 text-ink"><RichText text={p} /></p>)}
        {g.sections.map((s) => (
          <section key={s.h} className="space-y-3 pt-4">
            <h2 className="text-xl font-bold text-ink">{s.h}</h2>
            {s.p?.map((p, i) => <p key={i}><RichText text={p} /></p>)}
            {s.list && (
              <ul className="list-disc space-y-2 pl-6 marker:text-brand-500">
                {s.list.map((li, i) => <li key={i}><RichText text={li} /></li>)}
              </ul>
            )}
            {s.after?.map((p, i) => <p key={i}><RichText text={p} /></p>)}
          </section>
        ))}
      </div>

      <aside className="mt-12 rounded-2xl border border-brand-200 bg-brand-50 p-6">
        <h2 className="text-xl font-bold text-ink">Know where your child stands in 7 days</h2>
        <p className="mt-2 text-sm text-ink-muted">Baseline tests in Maths, Science and English, homework help from tutors, and a progress report emailed to you on day 7. Free, no card.</p>
        <Button href="/ks3/trial" className="mt-4">Start a free week <ArrowRight size={16} /></Button>
      </aside>

      <section className="mt-12">
        <h2 className="text-xl font-bold text-ink">Questions parents ask</h2>
        <div className="mt-4 space-y-3">
          {g.faq.map((f) => (
            <details key={f.q} className="card p-5">
              <summary className="cursor-pointer font-semibold text-ink">{f.q}</summary>
              <p className="mt-2 text-sm text-ink-muted">{f.a}</p>
            </details>
          ))}
        </div>
      </section>

      <section className="mt-12">
        <h2 className="text-lg font-semibold text-ink">More guides for parents</h2>
        <ul className="mt-3 space-y-2">
          {others.map((o) => (
            <li key={o.slug}><Link href={`/guides/${o.slug}`} className="font-medium text-brand-700 hover:underline">{o.title}</Link></li>
          ))}
        </ul>
      </section>

      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
    </article>
  );
}
