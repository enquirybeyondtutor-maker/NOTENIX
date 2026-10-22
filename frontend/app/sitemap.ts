import type { MetadataRoute } from "next";
import { SITE } from "@/lib/site";
import { EXAMS } from "@/lib/exams";

export default function sitemap(): MetadataRoute.Sitemap {
  const now = new Date();
  return [
    { url: SITE, lastModified: now, changeFrequency: "weekly", priority: 1 },
    ...EXAMS.map((e) => ({ url: `${SITE}/${e.slug}`, lastModified: now, changeFrequency: "weekly" as const, priority: 0.9 })),
    { url: `${SITE}/request`, lastModified: now, changeFrequency: "monthly", priority: 0.8 },
    { url: `${SITE}/pricing`, lastModified: now, changeFrequency: "monthly", priority: 0.6 },
  ];
}
