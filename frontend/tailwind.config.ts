import type { Config } from "tailwindcss";

/**
 * Notenix design system — "Clean corporate SaaS".
 * Neutral slate base + a single confident indigo brand accent.
 * Semantic tokens are CSS-variable backed (see globals.css).
 */
const config: Config = {
  darkMode: "class",
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}", "./lib/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          50: "#EEF2FF", 100: "#E0E7FF", 200: "#C7D2FE", 300: "#A5B4FC", 400: "#818CF8",
          500: "#6366F1", 600: "#4F46E5", 700: "#4338CA", 800: "#3730A3", 900: "#312E81", 950: "#1E1B4B",
        },
        surface: "rgb(var(--surface) / <alpha-value>)",
        canvas: "rgb(var(--canvas) / <alpha-value>)",
        line: "rgb(var(--line) / <alpha-value>)",
        "line-strong": "rgb(var(--line-strong) / <alpha-value>)",
        ink: {
          DEFAULT: "rgb(var(--ink) / <alpha-value>)",
          muted: "rgb(var(--ink-muted) / <alpha-value>)",
          subtle: "rgb(var(--ink-subtle) / <alpha-value>)",
        },
        // Legacy aliases so not-yet-migrated pages keep rendering (now indigo-tinted).
        purple: {
          50: "#EEF2FF", 100: "#E0E7FF", 200: "#C7D2FE", 400: "#818CF8",
          500: "#6366F1", 600: "#4F46E5", 700: "#4338CA", 800: "#3730A3", 900: "#1E1B4B",
        },
        pink: { 400: "#818CF8", 500: "#6366F1", 600: "#4F46E5" },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        display: ["Plus Jakarta Sans", "Inter", "sans-serif"],
      },
      borderRadius: { lg: "0.625rem", xl: "0.875rem", "2xl": "1.125rem" },
      boxShadow: {
        xs: "0 1px 2px rgba(15, 23, 42, 0.06)",
        sm: "0 1px 3px rgba(15, 23, 42, 0.08), 0 1px 2px rgba(15, 23, 42, 0.04)",
        card: "0 1px 3px rgba(15, 23, 42, 0.06), 0 1px 2px rgba(15, 23, 42, 0.04)",
        md: "0 4px 12px rgba(15, 23, 42, 0.08)",
        lg: "0 12px 32px rgba(15, 23, 42, 0.10)",
        xl: "0 24px 48px rgba(15, 23, 42, 0.14)",
        // legacy
        purple: "0 4px 15px rgba(79, 70, 229, 0.25)",
      },
      animation: {
        "fade-in": "fadeIn 0.4s ease-out both",
        "slide-up": "slideUp 0.5s cubic-bezier(0.16,1,0.3,1) both",
        shimmer: "shimmer 2s linear infinite",
        float: "float 6s ease-in-out infinite",
      },
      keyframes: {
        fadeIn: { "0%": { opacity: "0" }, "100%": { opacity: "1" } },
        slideUp: { "0%": { opacity: "0", transform: "translateY(16px)" }, "100%": { opacity: "1", transform: "translateY(0)" } },
        shimmer: { "0%": { backgroundPosition: "-1000px 0" }, "100%": { backgroundPosition: "1000px 0" } },
        float: { "0%, 100%": { transform: "translateY(0px)" }, "50%": { transform: "translateY(-10px)" } },
      },
    },
  },
  plugins: [],
};

export default config;
