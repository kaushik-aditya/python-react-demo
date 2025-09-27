import type { Recipe } from "../types/recipe";

export async function getRecipes(search?: string): Promise<Recipe[]> {
  let url = "/api/recipes/";
  if (search && search.length >= 3) {
    url += `?search=${encodeURIComponent(search)}`;
  }

  const resp = await fetch(url);

  if (resp.status === 404) {
    // 404 = not found → return empty list
    return [];
  }

  if (!resp.ok) {
    // other errors → throw with status info
    throw new Error(`HTTP ${resp.status} ${resp.statusText}`);
  }

  return resp.json();
}