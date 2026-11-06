import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Free 1-Week KS3 Trial: Beat the Year 7 Dip",
  description:
    "Free for 1 week, no card: Year 7–9 baseline tests in Maths, Science and English, homework help from Beyond Tutors tutors, KS3 notes and a progress report emailed to parents.",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
