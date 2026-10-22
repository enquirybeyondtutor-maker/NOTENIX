import type { Metadata } from "next";
import { SITE } from "@/lib/site";

export const metadata: Metadata = {
  title: "Pricing: Free Practice Tests & Tutor-Marked Mocks",
  description: "Start free with SAT, ESAT, TMUA, GCSE and A-Level practice. Upgrade to Pro or request tutor-marked mocks. Pay from any country by bank transfer.",
  alternates: { canonical: `${SITE}/pricing` },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
