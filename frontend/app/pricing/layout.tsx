import type { Metadata } from "next";
import { SITE } from "@/lib/site";

export const metadata: Metadata = {
  title: "Pricing: £49 a Year for Beyond Tutors Students, from £99 for Everyone Else",
  description: "Notenix is £49 a year per course for Beyond Tutors students. For any other student: GCSE £99 a subject or £349 for all four, SAT £99, other courses (IGCSE, A-Level, TMUA, ESAT) £149 a year, KS3 £149 a year. Practice papers, revision resources and timed tests, marked by tutors.",
  alternates: { canonical: `${SITE}/pricing` },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
