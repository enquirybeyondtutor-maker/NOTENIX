import { privatePage } from "@/lib/meta";

export const metadata = privatePage("My tests");

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
