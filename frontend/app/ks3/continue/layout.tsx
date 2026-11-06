import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Continue Notenix KS3",
  description: "Keep tracking your child from Year 7 to GCSE: half-termly tests, homework help, KS3 notes and a monthly progress report.",
  robots: { index: false },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
