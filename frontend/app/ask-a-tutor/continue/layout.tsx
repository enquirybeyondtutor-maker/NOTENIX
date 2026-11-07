import type { Metadata } from "next";

export const metadata: Metadata = { title: "Choose an Ask a Tutor plan", robots: { index: false } };

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
