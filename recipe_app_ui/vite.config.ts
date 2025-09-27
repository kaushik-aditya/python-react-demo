import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()] as any,
  resolve: {
    alias: {
      "@": "/src"
    }
  },  
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "./vitest.setup.ts" // you can create this file if needed
  }
});
