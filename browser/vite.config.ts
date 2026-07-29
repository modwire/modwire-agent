import react from "@vitejs/plugin-react";
import { resolve } from "node:path";
import type { Plugin } from "vite";
import { defineConfig } from "vitest/config";

function trimOutputWhitespace(): Plugin {
  return {
    name: "trim-output-whitespace",
    enforce: "post",
    generateBundle(_, bundle) {
      for (const file of Object.values(bundle)) {
        if (file.type === "chunk") {
          file.code = file.code.replace(/[ \t]+$/gm, "");
        }
      }
    },
  };
}

export default defineConfig({
  plugins: [react(), trimOutputWhitespace()],
  base: "/static/browser/",
  build: {
    outDir: resolve(
      import.meta.dirname,
      "../src/modwire_agent/browser/adapters/http/static/browser",
    ),
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
