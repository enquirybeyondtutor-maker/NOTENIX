import type { Metadata } from "next";
import { EXAM_BY_SLUG } from "@/lib/exams";
import { SITE } from "@/lib/site";
import { hasEngine } from "@/lib/examApi";

export async function generateMetadata({ params }: { params: Promise<{ exam: string }> }): Promise<Metadata> {
  const slug = (await params).exam;
  const exam = EXAM_BY_SLUG[slug];
  if (!exam || !hasEngine(slug)) return { robots: { index: false, follow: false } };
  const title = `Free ${exam.name} Diagnostic Test with a Score Estimate`;
  const description = `A free, timed ${exam.name} diagnostic in the style of both papers. Get an estimated score band and the skills costing you the most marks. No account needed.`;
  const url = `${SITE}/${slug}/diagnostic`;
  return { title, description, alternates: { canonical: url },
           openGraph: { type: "website", url, siteName: "Notenix", title, description } };
}

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
