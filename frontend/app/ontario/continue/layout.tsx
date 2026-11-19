import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Continue Notenix Ontario",
  description: "Keep tracking your child through Grades 5 to 7: Math and Language tests, homework help, notes and a monthly progress report.",
  robots: { index: false },
};

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
