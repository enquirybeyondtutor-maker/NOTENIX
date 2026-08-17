"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useEffect } from "react";
import { Menu, X, LayoutDashboard, ClipboardList, LineChart, Users, FilePlus2, LogOut, Trophy, Shield, PenLine, CheckSquare, BookOpen, type LucideIcon } from "lucide-react";
import { getUser, logout, authAPI } from "@/lib/api";
import { Logo } from "./ui/Logo";
import { Button } from "./ui/Button";
import { cn } from "@/lib/utils";

type NavItem = { href: string; label: string; icon?: LucideIcon };

const STUDENT_LINKS: NavItem[] = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/tests", label: "My Tests", icon: ClipboardList },
  { href: "/homework", label: "Homework", icon: BookOpen },
  { href: "/progress", label: "Progress", icon: LineChart },
  { href: "/leaderboard", label: "Leaderboard", icon: Trophy },
];

const TEACHER_LINKS: NavItem[] = [
  { href: "/teacher", label: "Overview", icon: LayoutDashboard },
  { href: "/teacher/tests", label: "Tests", icon: ClipboardList },
  { href: "/teacher/homework", label: "Homework", icon: BookOpen },
  { href: "/teacher/tests/new", label: "Create", icon: FilePlus2 },
  { href: "/teacher/students", label: "Students", icon: Users },
];

const PUBLIC_LINKS: NavItem[] = [
  { href: "/#features", label: "Features" },
  { href: "/#how", label: "How it works" },
  { href: "/pricing", label: "Pricing" },
];

export default function Navbar() {
  const pathname = usePathname() || "/";
  const [open, setOpen] = useState(false);
  const [user, setUser] = useState<any | null>(null);

  useEffect(() => {
    const cached = getUser();
    setUser(cached);
    // Only refresh from server when we actually have a session token.
    const hasToken = typeof window !== "undefined" && !!localStorage.getItem("notenix_token");
    if (!hasToken) return;
    authAPI
      .me()
      .then(({ data }) => {
        setUser(data);
        try {
          localStorage.setItem("notenix_user", JSON.stringify(data));
        } catch {}
      })
      .catch(() => {});
  }, [pathname]);

  useEffect(() => setOpen(false), [pathname]);

  if (pathname === "/login" || pathname === "/register" || pathname === "/verify-email" || pathname === "/reset-password") return null;

  const isAuthed = !!user;
  const isTeacher = user?.role === "teacher" || user?.role === "admin";
  let links = !isAuthed ? PUBLIC_LINKS : isTeacher ? [...TEACHER_LINKS] : [...STUDENT_LINKS];
  if (isAuthed && isTeacher && user?.can_mark) {
    links = [...links, { href: "/marking", label: "Marking", icon: CheckSquare }];
  }
  if (isAuthed && !isTeacher && user?.can_write_practice) {
    // insert Practice right after My Tests
    links = [...STUDENT_LINKS.slice(0, 2), { href: "/practice", label: "Practice", icon: PenLine }, ...STUDENT_LINKS.slice(2)];
  }
  if (isAuthed && user?.is_admin) {
    links = [...links, { href: "/admin", label: "Admin", icon: Shield }];
  }

  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-line bg-white/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6">
        <div className="flex items-center gap-8">
          <Logo />
          <nav className="hidden items-center gap-1 md:flex">
            {links.map(({ href, label }) => {
              const active = pathname === href || (href !== "/" && !href.includes("#") && pathname.startsWith(href));
              return (
                <Link
                  key={href}
                  href={href}
                  className={cn(
                    "rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                    active ? "bg-brand-50 text-brand-700" : "text-ink-muted hover:bg-slate-100 hover:text-ink"
                  )}
                >
                  {label}
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="flex items-center gap-2">
          {isAuthed ? (
            <div className="hidden items-center gap-3 md:flex">
              <div className="flex items-center gap-2.5 rounded-lg border border-line py-1.5 pl-1.5 pr-3">
                <span className="grid h-7 w-7 place-items-center rounded-md bg-brand-600 text-xs font-semibold text-white">
                  {(user.full_name?.[0] || "U").toUpperCase()}
                </span>
                <div className="leading-tight">
                  <div className="text-xs font-semibold text-ink">{user.full_name?.split(" ")[0] || "Account"}</div>
                  <div className="text-[10px] uppercase tracking-wide text-ink-subtle">{user.role || "student"}</div>
                </div>
              </div>
              <button
                onClick={logout}
                className="grid h-9 w-9 place-items-center rounded-lg text-ink-subtle transition-colors hover:bg-slate-100 hover:text-ink"
                title="Sign out"
              >
                <LogOut size={16} />
              </button>
            </div>
          ) : (
            <div className="hidden items-center gap-2 md:flex">
              <Button href="/login" variant="ghost" size="sm">Sign in</Button>
              <Button href="/register" size="sm">Get started</Button>
            </div>
          )}

          <button
            className="grid h-9 w-9 place-items-center rounded-lg text-ink-muted hover:bg-slate-100 md:hidden"
            onClick={() => setOpen(!open)}
            aria-label="Menu"
          >
            {open ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {open && (
        <div className="border-t border-line bg-white px-4 py-3 md:hidden">
          <nav className="space-y-1">
            {links.map(({ href, label }) => (
              <Link
                key={href}
                href={href}
                className="block rounded-lg px-3 py-2.5 text-sm font-medium text-ink-muted hover:bg-slate-100 hover:text-ink"
              >
                {label}
              </Link>
            ))}
          </nav>
          <div className="mt-3 border-t border-line pt-3">
            {isAuthed ? (
              <button
                onClick={logout}
                className="flex w-full items-center gap-2 rounded-lg px-3 py-2.5 text-sm font-medium text-red-600 hover:bg-red-50"
              >
                <LogOut size={16} /> Sign out
              </button>
            ) : (
              <div className="flex flex-col gap-2">
                <Button href="/login" variant="secondary">Sign in</Button>
                <Button href="/register">Get started</Button>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
