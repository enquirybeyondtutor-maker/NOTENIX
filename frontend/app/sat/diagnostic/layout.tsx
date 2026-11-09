import type { Metadata } from "next";
import { SITE } from "@/lib/site";

export const metadata: Metadata = {
  title: "Free SAT Diagnostic Test (34 minutes, Score Estimate) | Notenix",
  description: "Take a free 34-minute Digital SAT diagnostic: 26 Reading & Writing and Math questions with Desmos, an estimated score band out of 1600 and your weakest skills. No sign-up needed.",
  alternates: { canonical: `${SITE}/sat/diagnostic` },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
