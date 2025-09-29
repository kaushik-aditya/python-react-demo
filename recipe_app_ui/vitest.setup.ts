import "@testing-library/jest-dom";
import { cleanup } from "@testing-library/react";
import { afterEach, afterAll } from "vitest";
import { server } from "./src/mocks/server";
console.log("✅ vitest.setup.ts loaded");
// Start the server immediately
server.listen({
  onUnhandledRequest(req) {
    console.error("❌ Unhandled request:", req.method, req.url);
  },
});

// Log intercepted requests
server.events.on("request:start", ({ request }) => {
  console.log("➡️ MSW intercepted:", request.method, request.url);
});

afterEach(() => {
  cleanup();
  server.resetHandlers();
});

afterAll(() => server.close());
