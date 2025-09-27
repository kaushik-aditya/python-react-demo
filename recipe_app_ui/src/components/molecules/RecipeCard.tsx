import React from "react";
import type { Recipe } from "../../types/recipe";

const RecipeCard: React.FC<{ recipe: Recipe }> = ({ recipe }) => {
  return (
    <div className="rounded-2xl bg-[var(--card)] border border-white/10 overflow-hidden hover:border-white/20 transition">
      <div className="aspect-video bg-black/30">
        {recipe.image ? (
          <img
            src={recipe.image}
            alt={recipe.name}
            loading="lazy"
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full grid place-items-center text-white/40 text-sm">
            No image
          </div>
        )}
      </div>
      <div className="p-4 space-y-2">
        <div className="font-semibold">{recipe.name}</div>
        <div className="text-xs text-white/60">
          {recipe.cuisine} • {recipe.difficulty} • {recipe.servings} servings
        </div>
        <div className="text-xs text-white/60">
          Prep {recipe.prep_time_minutes}m • Cook {recipe.cook_time_minutes}m
        </div>
        {recipe.tags?.length ? (
          <div className="flex flex-wrap gap-1 pt-1">
            {recipe.tags!.slice(0, 5).map(t => (
              <span key={t} className="text-[10px] px-2 py-0.5 rounded-full bg-white/10 border border-white/10">{t}</span>
            ))}
          </div>
        ) : null}
      </div>
    </div>
  );
};

export default RecipeCard;
