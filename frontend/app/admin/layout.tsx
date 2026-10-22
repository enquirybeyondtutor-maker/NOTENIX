import { privatePage } from "@/lib/meta";

export const metadata = privatePage("Admin");

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
