"use client";
import { useEffect } from "react";
import { usePathname } from "next/navigation";
import Navbar from "./Navbar";
import Footer from "./Footer";

export default function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname() || "/";

  // The free Render API sleeps when idle. Wake it the moment anyone opens the site, so it's
  // usually up by the time they sign in or open a test. Fire-and-forget, once per tab.
  useEffect(() => {
    try {
      if (sessionStorage.getItem("notenix_warm")) return;
      sessionStorage.setItem("notenix_warm", "1");
    } catch {}
    fetch("/api/ping", { cache: "no-store" }).catch(() => {});
  }, []);
  const isAuthPage = pathname === "/login" || pathname === "/register" || pathname === "/verify-email" || pathname === "/reset-password";

  // App surfaces get the nav but not the marketing footer.
  const isAppSurface =
    pathname.startsWith("/dashboard") ||
    pathname.startsWith("/tests") ||
    pathname.startsWith("/homework") ||
    pathname.startsWith("/teacher") ||
    pathname.startsWith("/admin") ||
    pathname.startsWith("/quiz") ||
    pathname.startsWith("/progress") ||
    pathname.startsWith("/practice") ||
    pathname.startsWith("/marking") ||
    pathname.startsWith("/settings") ||
    pathname.startsWith("/requests") ||
    pathname.startsWith("/pay") ||
    pathname.startsWith("/leaderboard");

  return (
    <>
      <Navbar />
      <main className={isAuthPage ? "min-h-screen" : "min-h-screen pt-16 print:min-h-0 print:pt-0"}>{children}</main>
      {!isAuthPage && !isAppSurface && <Footer />}
    </>
  );
}
