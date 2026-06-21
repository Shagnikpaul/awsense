import path from "path";
import { fileURLToPath } from "url";
import { defineConfig, mergeConfig } from "vite";
import react from "@vitejs/plugin-react";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// https://vite.dev/config/
const f = defineConfig({
  plugins: [react({ jsxRuntime: "automatic" })],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});

export default mergeConfig(
  f,
  defineConfig({
    test: {
      environment: "jsdom",
      globals: true,
      setupFiles: "./src/test/setup.js", //or which ever runtime enviroment you're using
    },
  }),
);
