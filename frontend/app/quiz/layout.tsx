import { privatePage } from "@/lib/meta";

export const metadata = privatePage("Quiz");

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
