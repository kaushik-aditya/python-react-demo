// vite-env.d.ts
/// <reference types="vite/client" />

declare module "@tailwindcss/vite"; // Tailwind Vite plugin has no types

// If lucide-react ever complains (usually ships its own types, but just in case):
// declare module "lucide-react";
