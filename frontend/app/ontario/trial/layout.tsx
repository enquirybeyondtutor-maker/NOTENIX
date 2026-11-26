import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Free 1-Week Ontario Trial: Grades 5–7 Math and Language",
  alternates: { canonical: "https://www.notenix.com/ontario/trial" },
  description:
    "Free for 1 week, no card: Ontario curriculum baseline tests in Math and Language for Grades 5, 6 and 7, homework help from Beyond Tutors tutors, grade-level notes and a progress report emailed to parents.",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
