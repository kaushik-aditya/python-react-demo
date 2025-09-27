import type { Recipe } from "../types/recipe";

export async function getRecipes(search?: string): Promise<Recipe[]> {
  let url = "/api/recipes/";
  if (search && search.length >= 3) {
    url += `?search=${encodeURIComponent(search)}`;
  }

  const resp = await fetch(url);
  if (!resp.ok) {
    // only throw for real errors (network/server)
    throw new Error(`HTTP ${resp.status} ${resp.statusText}`);
  }

  const data: Recipe[] = await resp.json();

  // Explicitly handle "no data found"
  if (Array.isArray(data) && data.length === 0) {
    // Not an error — just return empty list
    return [];
  }

  return data;
}
