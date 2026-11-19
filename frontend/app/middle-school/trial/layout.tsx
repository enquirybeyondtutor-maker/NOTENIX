import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Free 1-Week Middle School Trial: Grades 5–7 Math and ELA",
  description:
    "Free for 1 week, no card: Common Core baseline tests in Math and English Language Arts for Grades 5, 6 and 7, homework help from Beyond Tutors tutors, grade-level notes and a progress report emailed to parents.",
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
