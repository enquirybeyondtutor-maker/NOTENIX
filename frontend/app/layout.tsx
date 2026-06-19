"use client";
import "./globals.css";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { Menu, X, Zap, BookOpen, BarChart3, Brain, CreditCard, LogOut, Trophy } from "lucide-react";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  const isAuthPage = pathname === "/login" || pathname === "/register"
    || pathname === "/forgot-password" || pathname === "/reset-password" || pathname?.startsWith("/verify-email") || pathname?.startsWith("/shared");
  const isLanding = pathname === "/";

  const navLinks = [
    { href: "/dashboard", label: "Dashboard", icon: BarChart3 },
    { href: "/quiz/create", label: "New Quiz", icon: Brain },
    { href: "/progress", label: "Progress", icon: BookOpen },
    { href: "/leaderboard", label: "Leaderboard", icon: Trophy },
    { href: "/pricing", label: "Pricing", icon: CreditCard },
  ];

  return (
    <html lang="en" className="dark">
      <head>
        <title>Notenix — AI GCSE & A-Level Quiz Platform</title>
        <meta name="description" content="Master GCSE and A-Level subjects with AI-generated quizzes, spaced repetition, and personalised analysis." />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body className="min-h-screen bg-[#050510] text-slate-100">
        {!isAuthPage && (
          <nav className="fixed top-0 left-0 right-0 z-50 border-b border-white/5 bg-[#050510]/80 backdrop-blur-xl">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
              <Link href="/" className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center">
                  <Zap size={16} className="text-white" />
                </div>
                <span className="font-orbitron text-lg font-bold gradient-text tracking-wider">NOTENIX</span>
              </Link>

              {!isLanding && (
                <div className="hidden md:flex items-center gap-1">
                  {navLinks.map(({ href, label, icon: Icon }) => (
                    <Link key={href} href={href} className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${pathname === href ? "bg-purple-500/20 text-purple-400 border border-purple-500/30" : "text-slate-400 hover:text-white hover:bg-white/5"}`}>
                      <Icon size={15} />
                      {label}
                    </Link>
                  ))}
                </div>
              )}

              <div className="flex items-center gap-3">
                {isLanding ? (
                  <>
                    <Link href="/login" className="text-sm text-slate-400 hover:text-white transition-colors px-4 py-2">Login</Link>
                    <Link href="/register" className="btn-neon relative text-sm font-semibold px-5 py-2 rounded-lg text-white z-10">
                      <span className="relative z-10">Get Started Free</span>
                    </Link>
                  </>
                ) : (
                  <>
                    <button className="md:hidden text-slate-400 hover:text-white" onClick={() => setMobileOpen(!mobileOpen)}>
                      {mobileOpen ? <X size={20} /> : <Menu size={20} />}
                    </button>
                    <Link href="/login" className="hidden md:flex items-center gap-2 text-sm text-slate-400 hover:text-white transition-colors">
                      <LogOut size={15} /> Logout
                    </Link>
                  </>
                )}
              </div>
            </div>

            {mobileOpen && !isLanding && (
              <div className="md:hidden border-t border-white/5 bg-[#050510]/95 px-4 py-3 space-y-1">
                {navLinks.map(({ href, label, icon: Icon }) => (
                  <Link key={href} href={href} className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-slate-400 hover:text-white hover:bg-white/5" onClick={() => setMobileOpen(false)}>
                    <Icon size={16} /> {label}
                  </Link>
                ))}
              </div>
            )}
          </nav>
        )}

        <main className={!isAuthPage ? "pt-16 min-h-screen" : "min-h-screen"}>
          {children}
        </main>
      </body>
    </html>
  );
}
