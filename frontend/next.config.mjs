export default {
  reactStrictMode: true,
  // Keep transpilePackages if monorepo packages need transpilation
  transpilePackages: ["@geariq/shared"],
  eslint: {
    // Prevent ESLint from blocking builds on Vercel for this POC
    ignoreDuringBuilds: true,
  },
  typescript: {
    // Allow production builds even if there are type errors (POC only)
    ignoreBuildErrors: true,
  },
};
