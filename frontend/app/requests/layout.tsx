import { privatePage } from "@/lib/meta";

export const metadata = privatePage("My test requests");

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
