import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // To avoid Turbopack issues, we'll use standard webpack by running with NODE_ENV
  // The configuration is kept minimal to avoid invalid options
};

export default nextConfig;
