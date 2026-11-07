import type { MetadataRoute } from "next";
import { SITE } from "@/lib/site";
import { EXAMS } from "@/lib/exams";
import { TOPICS, YEARS, topicPath, yearSlug } from "@/lib/ks3Topics";
import { GUIDES } from "@/lib/guides";

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();
  return [
    { url: SITE, lastModified: now, changeFrequency: "weekly", priority: 1 },
    ...EXAMS.map((e) => ({ url: `${SITE}/${e.slug}`, lastModified: now, changeFrequency: "weekly" as const, priority: 0.9 })),
    { url: `${SITE}/request`, lastModified: now, changeFrequency: "monthly", priority: 0.8 },
    { url: `${SITE}/ks3`, lastModified: now, changeFrequency: "monthly", priority: 0.9 },
    ...YEARS.map((y) => ({ url: `${SITE}/ks3/${yearSlug(y)}`, lastModified: now, changeFrequency: "monthly" as const, priority: 0.8 })),
    ...TOPICS.map((t) => ({ url: `${SITE}${topicPath(t)}`, lastModified: now, changeFrequency: "monthly" as const, priority: 0.7 })),
    { url: `${SITE}/guides`, lastModified: now, changeFrequency: "weekly", priority: 0.7 },
    ...GUIDES.map((g) => ({ url: `${SITE}/guides/${g.slug}`, lastModified: new Date(g.updated), changeFrequency: "monthly" as const, priority: 0.7 })),
    { url: `${SITE}/pricing`, lastModified: now, changeFrequency: "monthly", priority: 0.6 },
    ...["terms", "privacy", "refunds"].map((p) => ({ url: `${SITE}/${p}`, lastModified: now, changeFrequency: "yearly" as const, priority: 0.2 })),
  ];
}
