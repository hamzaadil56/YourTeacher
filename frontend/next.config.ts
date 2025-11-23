import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Enable standalone output for Docker
  output: 'standalone',
  
  // Optimize images
  images: {
    remotePatterns: [],
    formats: ['image/avif', 'image/webp'],
  },
  
  // Disable telemetry
  reactStrictMode: true,
  
  // Environment variables that are exposed to the browser
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  },
};

export default nextConfig;
