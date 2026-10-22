import { privatePage } from "@/lib/meta";

export const metadata = privatePage("Homework");

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
