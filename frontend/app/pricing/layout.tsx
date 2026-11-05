import type { Metadata } from "next";
import { SITE } from "@/lib/site";

export const metadata: Metadata = {
  title: "Pricing: £49 a Year for Beyond Tutors Students, £149 for Everyone Else",
  description: "Notenix is £49 a year for Beyond Tutors students (free during your trial class) and £149 a year full access for any other student: notes, worksheets, topic questions and timed tests with instant marking.",
  alternates: { canonical: `${SITE}/pricing` },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
