import { defineConfig } from "vite";
import { resolve } from "node:path";

export default defineConfig({
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
});
