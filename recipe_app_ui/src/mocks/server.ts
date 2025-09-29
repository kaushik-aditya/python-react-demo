// src/mocks/server.ts
import { setupServer } from "msw/node";
import { handlers } from "./handler";
console.log("✅ MSW server.ts loaded");
// Setup server with your handlers
export const server = setupServer(...handlers);


