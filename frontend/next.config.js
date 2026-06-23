/** @type {import('next').NextConfig} */
const BACKEND = process.env.BACKEND_URL || "https://notenix-api-v2.onrender.com";

const nextConfig = {
  async rewrites() {
    // Same-origin proxy: browser calls /api/* on notenix.com, Next forwards to Render.
    // This eliminates CORS entirely.
    return [{ source: "/api/:path*", destination: `${BACKEND}/:path*` }];
  },
};

module.exports = nextConfig;
