import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Create a free account",
  description: "Create a free Notenix account to sit SAT, ESAT, TMUA, GCSE and A-Level practice tests.",
  robots: { index: false, follow: true },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
