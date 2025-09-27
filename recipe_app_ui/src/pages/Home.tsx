import { useEffect, useMemo, useState } from "react";
import DefaultLayout from "../components/templates/DefaultLayout";
import Sidebar from "../components/organisms/Sidebar";
import Navbar from "../components/organisms/Navbar";
import RecipeGrid from "../components/organisms/RecipeGrid";
import type { Recipe } from "../types/recipe";
import { ToastProvider, useToast } from "../context/ToastContext";
import ToastContainer from "../components/molecules/ToastContainer";
import { getRecipes } from "../services/api"; // ✅ imported service

type SortOrder = "asc" | "desc";

function HomeInner() {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [sortOrder, setSortOrder] = useState<SortOrder>("asc");
  const { push } = useToast();

  const fetchRecipes = async (query?: string) => {
    try {
      const data = await getRecipes(query);
      setRecipes(data);
      if (!query) {
        setSelectedTags([]); // reset filters only on fresh load
      }
    } catch (e: any) {
      push({ type: "error", message: e?.message ?? "Failed to fetch recipes" });
    }
  };

  // ✅ Initial load
  useEffect(() => {
    fetchRecipes();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ✅ Handle search
  const handleSearch = (query: string) => {
    fetchRecipes(query);
  };

  // ✅ Available tags extracted from recipes
  const availableTags = useMemo(() => {
    const set = new Set<string>();
    recipes.forEach((r) => r.tags?.forEach((t) => set.add(t.trim())));
    return Array.from(set).sort();
  }, [recipes]);

  // ✅ Apply tag filtering + sort in-memory
  const filteredSorted = useMemo(() => {
    let list = recipes;
    if (selectedTags.length) {
      list = list.filter((r) => selectedTags.every((t) => r.tags?.includes(t)));
    }
    return list.slice().sort((a, b) => {
      const diff = (a.cook_time_minutes || 0) - (b.cook_time_minutes || 0);
      return sortOrder === "asc" ? diff : -diff;
    });
  }, [recipes, selectedTags, sortOrder]);

  const handleToggleTag = (t: string) => {
    setSelectedTags((xs) =>
      xs.includes(t) ? xs.filter((y) => y !== t) : [...xs, t]
    );
  };

  return (
    <DefaultLayout
      sidebar={
        <Sidebar
          availableTags={availableTags}
          selectedTags={selectedTags}
          onToggleTag={handleToggleTag}
          sortOrder={sortOrder}
          onSortChange={setSortOrder}
        />
      }
      navbar={<Navbar onToggleSidebar={() => {}} onSearch={handleSearch} />}
    >
      <RecipeGrid recipes={filteredSorted} />
    </DefaultLayout>
  );
}

export default function Home() {
  return (
    <ToastProvider>
      <HomeInner />
      <ToastContainer />
    </ToastProvider>
  );
}
