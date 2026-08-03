"use client";
import { usePathname } from "next/navigation";
import Navbar from "./Navbar";
import Footer from "./Footer";

export default function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname() || "/";
  const isAuthPage = pathname === "/login" || pathname === "/register";

  // App surfaces get the nav but not the marketing footer.
  const isAppSurface =
    pathname.startsWith("/dashboard") ||
    pathname.startsWith("/tests") ||
    pathname.startsWith("/teacher") ||
    pathname.startsWith("/admin") ||
    pathname.startsWith("/quiz") ||
    pathname.startsWith("/progress") ||
    pathname.startsWith("/leaderboard");

  return (
    <>
      <Navbar />
      <main className={isAuthPage ? "min-h-screen" : "min-h-screen pt-16"}>{children}</main>
      {!isAuthPage && !isAppSurface && <Footer />}
    </>
  );
}
