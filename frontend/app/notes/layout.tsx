import { privatePage } from "@/lib/meta";

export const metadata = privatePage("Class notes");

export default function Layout({ children }: { children: React.ReactNode }) {
  return children;
}
