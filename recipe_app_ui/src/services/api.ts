import type { Recipe } from "../types/recipe";

const BASE_URL = "/api"; // will be proxied in vite.config.ts

// ✅ Fetch all recipes (with optional search)
export async function getRecipes(search?: string): Promise<Recipe[]> {
  let url = `${BASE_URL}/recipes/`;
  if (search && search.length >= 3) {
    url += `?search=${encodeURIComponent(search)}`;
  }

  const resp = await fetch(url);
  if (!resp.ok) throw new Error("Failed to fetch recipes");
  return resp.json();
}
