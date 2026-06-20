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
    || pathname === "/forgot-password" || pathname === "/reset-password"
    || pathname?.startsWith("/verify-email") || pathname?.startsWith("/shared");
  const isLanding = pathname === "/";

  const navLinks = [
    { href: "/dashboard", label: "Dashboard", icon: BarChart3 },
    { href: "/quiz/create", label: "New Quiz", icon: Brain },
    { href: "/progress", label: "Progress", icon: BookOpen },
    { href: "/leaderboard", label: "Leaderboard", icon: Trophy },
    { href: "/pricing", label: "Pricing", icon: CreditCard },
  ];

  const landingLinks = [
    { href: "#features", label: "Features" },
    { href: "#subjects", label: "Subjects" },
    { href: "/pricing", label: "Pricing" },
  ];

  return (
    <html lang="en">
      <head>
        <title>Notenix — AI GCSE & A-Level Quiz Platform</title>
        <meta name="description" content="Master GCSE and A-Level subjects with AI-generated quizzes, spaced repetition, and personalised analysis." />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
      </head>
      <body className="min-h-screen bg-[#F5F3FF] text-[#1E1B4B]">
        {!isAuthPage && (
          <nav className="fixed top-0 left-0 right-0 z-50 border-b border-purple-100 bg-white/80 backdrop-blur-xl">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
              {/* Logo */}
              <Link href="/" className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-purple-600 to-pink-500 flex items-center justify-center shadow-purple">
                  <Zap size={18} className="text-white" />
                </div>
                <span className="text-lg font-bold text-[#1E1B4B]">
                  <span className="text-purple-600">Note</span>nix
                </span>
              </Link>

              {/* Desktop nav */}
              {isLanding ? (
                <div className="hidden md:flex items-center gap-1">
                  {landingLinks.map(({ href, label }) => (
                    <Link key={href} href={href} className="nav-link">{label}</Link>
                  ))}
                </div>
              ) : (
                <div className="hidden md:flex items-center gap-1">
                  {navLinks.map(({ href, label, icon: Icon }) => (
                    <Link key={href} href={href}
                      className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-sm font-medium transition-all ${
                        pathname === href
                          ? "bg-purple-50 text-purple-600 border border-purple-200"
                          : "text-gray-500 hover:text-purple-600 hover:bg-purple-50"
                      }`}>
                      <Icon size={15} />{label}
                    </Link>
                  ))}
                </div>
              )}

              {/* Right side */}
              <div className="flex items-center gap-3">
                {isLanding ? (
                  <>
                    <Link href="/login" className="hidden md:block text-sm font-medium text-gray-600 hover:text-purple-600 transition-colors px-3 py-2">
                      Login
                    </Link>
                    <Link href="/register">
                      <button className="btn-primary text-sm py-2.5 px-5">
                        Get Started Free →
                      </button>
                    </Link>
                  </>
                ) : (
                  <>
                    <button className="md:hidden text-gray-500 hover:text-purple-600" onClick={() => setMobileOpen(!mobileOpen)}>
                      {mobileOpen ? <X size={20} /> : <Menu size={20} />}
                    </button>
                    <Link href="/login" className="hidden md:flex items-center gap-1.5 text-sm text-gray-500 hover:text-purple-600 transition-colors">
                      <LogOut size={14} /> Logout
                    </Link>
                  </>
                )}
              </div>
            </div>

            {/* Mobile menu */}
            {mobileOpen && !isLanding && (
              <div className="md:hidden border-t border-purple-100 bg-white px-4 py-3 space-y-1">
                {navLinks.map(({ href, label, icon: Icon }) => (
                  <Link key={href} href={href}
                    className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-gray-600 hover:text-purple-600 hover:bg-purple-50"
                    onClick={() => setMobileOpen(false)}>
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
