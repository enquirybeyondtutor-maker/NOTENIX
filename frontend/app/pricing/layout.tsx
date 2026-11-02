import type { Metadata } from "next";
import { SITE } from "@/lib/site";

export const metadata: Metadata = {
  title: "Pricing: Notenix for Beyond Tutors Students, £49 a Year",
  description: "Notenix comes with Beyond Tutors classes: free during your trial class, then £49 a year for homework, tests, class notes and progress reports.",
  alternates: { canonical: `${SITE}/pricing` },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
