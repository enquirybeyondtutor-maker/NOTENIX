"use client";
import { usePathname } from "next/navigation";
import Navbar from "./Navbar";

export default function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isAuthPage = pathname === "/login" || pathname === "/register";
  return (
    <>
      <Navbar />
      <main className={!isAuthPage ? "pt-16 min-h-screen" : "min-h-screen"}>{children}</main>
    </>
  );
}
