import type { MetadataRoute } from "next";
import { SITE } from "@/lib/site";
import { EXAMS } from "@/lib/exams";

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();
  return [
    { url: SITE, lastModified: now, changeFrequency: "weekly", priority: 1 },
    ...EXAMS.map((e) => ({ url: `${SITE}/${e.slug}`, lastModified: now, changeFrequency: "weekly" as const, priority: 0.9 })),
    { url: `${SITE}/request`, lastModified: now, changeFrequency: "monthly", priority: 0.8 },
    { url: `${SITE}/ks3`, lastModified: now, changeFrequency: "monthly", priority: 0.9 },
    { url: `${SITE}/pricing`, lastModified: now, changeFrequency: "monthly", priority: 0.6 },
    ...["terms", "privacy", "refunds"].map((p) => ({ url: `${SITE}/${p}`, lastModified: now, changeFrequency: "yearly" as const, priority: 0.2 })),
  ];
}
