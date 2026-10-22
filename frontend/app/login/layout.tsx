import type { Metadata } from "next";
import { SITE } from "@/lib/site";

export const metadata: Metadata = {
  title: "Sign in",
  description: "Sign in to Notenix to sit your practice tests and see tutor feedback.",
  alternates: { canonical: `${SITE}/login` },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
