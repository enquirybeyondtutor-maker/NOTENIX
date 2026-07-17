"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useEffect } from "react";
import { Menu, X, Zap, BarChart3, Brain, TrendingUp, CreditCard, LogOut, Trophy } from "lucide-react";
import { getUser, logout } from "@/lib/api";

export default function Navbar() {
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [loggedIn, setLoggedIn] = useState(false);

  useEffect(() => { setLoggedIn(!!getUser()); }, [pathname]);

  const isAuthPage = pathname === "/login" || pathname === "/register";
  const isLanding = pathname === "/";
  if (isAuthPage) return null;

  const navLinks = [
    { href: "/dashboard", label: "Dashboard", icon: BarChart3 },
    { href: "/quiz", label: "New Quiz", icon: Brain },
    { href: "/progress", label: "Progress", icon: TrendingUp },
    { href: "/leaderboard", label: "Leaderboard", icon: Trophy },
    { href: "/pricing", label: "Pricing", icon: CreditCard },
  ];
  const landingLinks = [
    { href: "#features", label: "Features" },
    { href: "#how", label: "How it works" },
    { href: "/pricing", label: "Pricing" },
  ];

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 border-b border-purple-100 bg-white/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5" aria-label="Notenix home">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-purple-600 to-pink-500 flex items-center justify-center shadow-purple">
            <Zap size={18} className="text-white" />
          </div>
          <span className="text-lg font-bold"><span className="text-purple-600">Note</span>nix</span>
        </Link>

        {isLanding && !loggedIn ? (
          <div className="hidden md:flex items-center gap-1">
            {landingLinks.map(({ href, label }) => (
              <Link key={href} href={href} className="px-3.5 py-2 text-sm font-medium text-gray-500 hover:text-purple-600">{label}</Link>
            ))}
          </div>
        ) : (
          <div className="hidden md:flex items-center gap-1">
            {navLinks.map(({ href, label, icon: Icon }) => (
              <Link key={href} href={href}
                className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-sm font-medium transition-all ${
                  pathname === href ? "bg-purple-50 text-purple-600 border border-purple-200" : "text-gray-500 hover:text-purple-600 hover:bg-purple-50"
                }`}>
                <Icon size={15} />{label}
              </Link>
            ))}
          </div>
        )}

        <div className="flex items-center gap-3">
          {loggedIn ? (
            <>
              <button className="md:hidden text-gray-500" onClick={() => setMobileOpen(!mobileOpen)} aria-label="Menu">
                {mobileOpen ? <X size={20} /> : <Menu size={20} />}
              </button>
              <button onClick={logout} className="hidden md:flex items-center gap-1.5 text-sm text-gray-500 hover:text-purple-600">
                <LogOut size={14} /> Logout
              </button>
            </>
          ) : (
            <>
              <Link href="/login" className="hidden md:block text-sm font-medium text-gray-600 hover:text-purple-600 px-3 py-2">Login</Link>
              <Link href="/register"><button className="btn-primary text-sm py-2.5 px-5">Get Started Free →</button></Link>
            </>
          )}
        </div>
      </div>

      {mobileOpen && loggedIn && (
        <div className="md:hidden border-t border-purple-100 bg-white px-4 py-3 space-y-1">
          {navLinks.map(({ href, label, icon: Icon }) => (
            <Link key={href} href={href} onClick={() => setMobileOpen(false)}
              className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-gray-600 hover:text-purple-600 hover:bg-purple-50">
              <Icon size={16} /> {label}
            </Link>
          ))}
          <button onClick={logout} className="flex items-center gap-3 px-3 py-2.5 w-full text-left text-sm text-gray-600 hover:text-purple-600">
            <LogOut size={16} /> Logout
          </button>
        </div>
      )}
    </nav>
  );
}
