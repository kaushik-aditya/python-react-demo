import { http, HttpResponse } from "msw";
import recipes from "./recipes.mock.json";
console.log("✅ MSW handler.ts loaded");
export const handlers = [
  // Match GET all
  http.get("*/api/recipes", () => {
    console.log("📦 GET /api/recipes");
    return HttpResponse.json(recipes, { status: 200 });
  }),

  // Match GET by ID
  http.get("*/api/recipes/:id", ({ params }) => {
    const recipe = recipes.find(r => r.id === Number(params.id));
    return recipe
      ? HttpResponse.json(recipe, { status: 200 })
      : HttpResponse.json({ message: "Not Found" }, { status: 404 });
  }),

  // Example error
  http.get("*/api/error", () => {
    return HttpResponse.json({ message: "Internal Server Error" }, { status: 500 });
  }),
];
