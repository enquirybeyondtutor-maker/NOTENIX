import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Continue Notenix SAT",
  description: "Keep your SAT practice going until test day: adaptive practice tests, skill drills and your study plan.",
  robots: { index: false },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
