import react from "@vitejs/plugin-react";
import { resolve } from "node:path";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  base: "/static/browser/",
  build: {
    outDir: resolve(import.meta.dirname, "../src/modwire_agent/browser/adapters/http/static/browser"),
    emptyOutDir: true,
    rollupOptions: {
      output: {
        entryFileNames: "browser.js",
        assetFileNames: "browser.[ext]",
      },
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: "./src/test/setup.ts",
  },
});
