/** @type {import('next').NextConfig} */
const BACKEND = process.env.BACKEND_URL || "https://notenix-eu.onrender.com"; // Frankfurt, next to the Neon database in London

const nextConfig = {
  async redirects() {
    // India exam pages were removed (Nov 2026); send old links and search results home.
    return ["jee", "neet", "cbse", "icse"].map((s) => ({ source: `/${s}`, destination: "/", permanent: true }));
  },
  async rewrites() {
    // Same-origin proxy: browser calls /api/* on notenix.com, Next forwards to Render.
    // This eliminates CORS entirely.
    return [{ source: "/api/:path*", destination: `${BACKEND}/:path*` }];
  },
};

module.exports = nextConfig;
