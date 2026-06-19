/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: {
    optimizePackageImports: ["framer-motion", "recharts", "lucide-react"],
  },
};

module.exports = nextConfig;
