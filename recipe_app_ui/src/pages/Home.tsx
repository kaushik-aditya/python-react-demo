import React, { Suspense, useEffect, useMemo, useState } from "react";
import DefaultLayout from "../components/templates/DefaultLayout";
import type { Recipe } from "../types/recipe";
import { ToastProvider, useToast } from "../context/ToastContext";
import { getRecipes } from "../services/api";
import { useInView } from "react-intersection-observer";

// Lazy load components
const Sidebar = React.lazy(() => import("../components/organisms/Sidebar"));
const Navbar = React.lazy(() => import("../components/organisms/Navbar"));
const RecipeGrid = React.lazy(() => import("../components/organisms/RecipeGrid"));
const ToastContainer = React.lazy(() => import("../components/molecules/ToastContainer"));

function SkeletonRecipeCard() {
  return (
    <div className="border rounded-lg p-4 animate-pulse">
      <div className="h-32 bg-gray-300 rounded-md mb-4"></div>
      <div className="h-4 bg-gray-300 rounded w-3/4 mb-2"></div>
      <div className="h-4 bg-gray-300 rounded w-1/2"></div>
    </div>
  );
}

type SortOrder = "asc" | "desc";

function HomeInner() {
  const [allRecipes, setAllRecipes] = useState<Recipe[]>([]);
  const [visibleRecipes, setVisibleRecipes] = useState<Recipe[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [sortOrder, setSortOrder] = useState<SortOrder>("asc");
  const [loading, setLoading] = useState(false);
  const { push } = useToast();

  const { ref, inView } = useInView({ threshold: 1 });

  // Fetch all recipes once
  const fetchRecipes = async (query?: string) => {
    try {
      setLoading(true);
      const data = await getRecipes(query);
      setAllRecipes(data);
      setVisibleRecipes(data.slice(0, 6)); // show first 6
      if (data.length === 0) {
        push({ type: "info", message: "No recipes found." });
      } else {
        push({ type: "success", message: "Recipes loaded successfully!" });
      }    
    } catch (e: any) {
      setAllRecipes([]);
      setVisibleRecipes([]);
      push({ type: "error", message: e?.message ?? "Failed to fetch recipes" });
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (query: string) => {
    if (query.length === 0 || query.length >= 3) {
      fetchRecipes(query);
    }
  };

  // Infinite scroll (client-side reveal)
  useEffect(() => {
    if (inView && !loading) {
      const more = filteredSorted.slice(
        visibleRecipes.length,
        visibleRecipes.length + 6
      );
      if (more.length > 0) {
        setVisibleRecipes((prev) => [...prev, ...more]);
      }
    }
  }, [inView]);

  const availableTags = useMemo(() => {
    const set = new Set<string>();
    allRecipes.forEach((r) => r.tags?.forEach((t) => set.add(t.trim())));
    return Array.from(set).sort();
  }, [allRecipes]);

  const filteredSorted = useMemo(() => {
    let list = allRecipes;
    if (selectedTags.length) {
      list = list.filter((r) => selectedTags.every((t) => r.tags?.includes(t)));
    }
    return list.slice().sort((a, b) => {
      const diff = (a.cook_time_minutes || 0) - (b.cook_time_minutes || 0);
      return sortOrder === "asc" ? diff : -diff;
    });
  }, [allRecipes, selectedTags, sortOrder]);

  // Reset visible recipes when filter/sort changes
  useEffect(() => {
    setVisibleRecipes(filteredSorted.slice(0, 6));
  }, [filteredSorted]);

  const handleToggleTag = (t: string) => {
    setSelectedTags((xs) =>
      xs.includes(t) ? xs.filter((y) => y !== t) : [...xs, t]
    );
  };

  return (
    <DefaultLayout
      sidebar={
        <Suspense fallback={<div className="p-4">Loading sidebar...</div>}>
          <Sidebar
            availableTags={availableTags}
            selectedTags={selectedTags}
            onToggleTag={handleToggleTag}
            sortOrder={sortOrder}
            onSortChange={setSortOrder}
          />
        </Suspense>
      }
      navbar={
        <Suspense fallback={<div className="p-4">Loading navbar...</div>}>
          <Navbar onToggleSidebar={() => {}} onSearch={handleSearch} loading={loading} />
        </Suspense>
      }
    >
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {Array.from({ length: 6 }).map((_, i) => (
            <SkeletonRecipeCard key={i} />
          ))}
        </div>
      ) : (
        <Suspense
          fallback={
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
              {Array.from({ length: 6 }).map((_, i) => (
                <SkeletonRecipeCard key={i} />
              ))}
            </div>
          }
        >
          <RecipeGrid recipes={visibleRecipes} />
        </Suspense>
      )}

      {/* Scroll sentinel */}
      {visibleRecipes.length < filteredSorted.length && (
        <div ref={ref} className="h-8" />
      )}
    </DefaultLayout>
  );
}

export default function Home() {
  return (
    <ToastProvider>
      <HomeInner />
      <Suspense fallback={<div>Loading toasts...</div>}>
        <ToastContainer />
      </Suspense>
    </ToastProvider>
  );
}
