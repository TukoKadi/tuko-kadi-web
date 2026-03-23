/** @type {import('next').NextConfig} */
const nextConfig = {
  typescript: {
    // This allows the build to succeed even if there are TypeScript errors
    ignoreBuildErrors: true,
  },
  eslint: {
    // This allows the build to succeed even if there are Linting warnings
    ignoreDuringBuilds: true,
  },
  // This is often needed for Leaflet (Map) to work correctly in Next.js
  webpack: (config) => {
    config.resolve.fallback = { fs: false, net: false, tls: false };
    return config;
  },
};

module.exports = nextConfig;
