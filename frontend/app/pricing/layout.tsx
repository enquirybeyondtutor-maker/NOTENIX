import type { Metadata } from "next";
import { SITE } from "@/lib/site";

export const metadata: Metadata = {
  title: "Pricing: £49 a Year per Course for Beyond Tutors Students, £149 for Everyone Else",
  description: "Notenix is £49 a year for Beyond Tutors students (free during your trial class) and £149 a year per course for any other student (e.g. IGCSE Chemistry, A-Level Maths, TMUA): practice papers, quizzes, revision resources and timed tests with instant marking.",
  alternates: { canonical: `${SITE}/pricing` },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
