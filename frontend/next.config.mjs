export default {
  reactStrictMode: true,
  experimental: {
    appDir: true
  },
  // Keep transpilePackages if monorepo packages need transpilation
  transpilePackages: ["@geariq/shared"],
};
