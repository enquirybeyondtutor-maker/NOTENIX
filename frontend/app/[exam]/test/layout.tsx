import { privatePage } from "@/lib/meta";

export const metadata = privatePage("Practice test");

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
