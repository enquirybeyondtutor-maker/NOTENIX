import type { Metadata } from "next";
import { SITE } from "@/lib/site";

export const metadata: Metadata = {
  title: "Create a free account",
  description: "Create a free Notenix account to sit SAT, ESAT, TMUA, GCSE and A-Level practice tests.",
  alternates: { canonical: `${SITE}/register` },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
