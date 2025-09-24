import React from "react";
import RecipeCard, { Recipe } from "../molecules/RecipeCard";

export default function RecipeGrid({ recipes }: { recipes: Recipe[] }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mt-4">
      {recipes.map((r) => (
        <RecipeCard key={r.id} {...r} />
      ))}
    </div>
  );
}
