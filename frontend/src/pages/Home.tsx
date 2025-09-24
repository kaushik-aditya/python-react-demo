import React, { useMemo, useState, lazy, Suspense } from "react";
import SearchBar from "../components/atoms/SearchBar";
import { Recipe } from "../components/molecules/RecipeCard";
const RecipeGrid = lazy(() => import("../components/organisms/RecipeGrid"));

type SortOrder = "asc" | "desc";

export default function Home() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [sortOrder, setSortOrder] = useState<SortOrder>("asc");

  const uniqueTags = useMemo(() => {
    const set = new Set<string>();
    recipes.forEach((r) => r.tags?.split(",").forEach((t) => t && set.add(t)));
    return Array.from(set).sort();
  }, [recipes]);

  const filteredSorted = useMemo(() => {
    let list = recipes;
    if (selectedTags.length) {
      list = list.filter((r) => {
        const rtags = r.tags?.split(",") || [];
        return selectedTags.every((t) => rtags.includes(t));
      });
    }
    return list.slice().sort((a, b) => {
      const diff = (a.cook_time_minutes || 0) - (b.cook_time_minutes || 0);
      return sortOrder === "asc" ? diff : -diff;
    });
  }, [recipes, selectedTags, sortOrder]);

  const handleSearch = async (query: string) => {
    if (query.length < 3) return;
    const resp = await fetch(`/api/recipes?search=${encodeURIComponent(query)}`);
    const data = await resp.json();
    setRecipes(data);
    setSelectedTags([]);
  };

  const toggleTag = (t: string) => {
    setSelectedTags((prev) =>
      prev.includes(t) ? prev.filter((x) => x !== t) : [...prev, t]
    );
  };

  return (
    <div className="p-4 max-w-6xl mx-auto">
      <SearchBar onSearch={handleSearch} />

      <div className="mt-4 flex flex-wrap items-center gap-3">
        <div className="flex items-center gap-2">
          <label className="text-sm">Sort by cook time:</label>
          <select
            value={sortOrder}
            onChange={(e) => setSortOrder(e.target.value as SortOrder)}
            className="border rounded p-1"
            aria-label="Sort by cook time"
          >
            <option value="asc">Ascending</option>
            <option value="desc">Descending</option>
          </select>
        </div>

        <div className="flex flex-wrap gap-2 items-center">
          <span className="text-sm">Filter by tags:</span>
          {uniqueTags.map((t) => (
            <button
              key={t}
              onClick={() => toggleTag(t)}
              className={`px-2 py-1 rounded border text-sm ${selectedTags.includes(t) ? "bg-gray-200" : ""}`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      <Suspense fallback={<div className="mt-4">Loading recipes...</div>}>
        <RecipeGrid recipes={filteredSorted} />
      </Suspense>
    </div>
  );
}
