import React, { Suspense } from "react";
import type { Recipe } from "../../types/recipe";
import RecipeCard from "../molecules/RecipeCard";

const RecipeGrid: React.FC<{ recipes: Recipe[] }> = ({ recipes }) => {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {recipes.map(r => <RecipeCard key={r.id} recipe={r} />)}
    </div>
  );
};

export default RecipeGrid;
