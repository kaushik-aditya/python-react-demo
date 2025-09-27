import { Clock, ListOrdered, Utensils } from "lucide-react";
import type { Recipe } from "../../types/recipe";

type Props = {
  recipes: Recipe[];
};

export default function RecipeGrid({ recipes }: Props) {
  if (!recipes || recipes.length === 0) {
    return (
      <div className="mt-8 text-center text-gray-500">
        No recipes found. Try searching for something else 🍳
      </div>
    );
  }

  return (
    <div className="mt-6 grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-8">
      {recipes.map((r) => (
        <div
          key={r.id}
          className="bg-white rounded-2xl shadow-md hover:shadow-xl border transition overflow-hidden flex flex-col"
        >
          {/* Image */}
          {r.image && (
            <img
              src={r.image}
              alt={r.name}
              className="h-56 w-full object-cover"
            />
          )}

          <div className="p-6 flex flex-col gap-4 flex-1">
            {/* Header */}
            <div>
              <h2 className="text-xl font-bold text-gray-900 line-clamp-2">
                {r.name}
              </h2>
              <p className="text-sm text-gray-500">{r.cuisine}</p>
            </div>

            {/* Time + Servings */}
            <div className="flex items-center justify-between text-sm text-gray-600">
              <div className="flex items-center gap-1">
                <Clock className="w-4 h-4 text-indigo-500" />
                <span>{r.cook_time_minutes} mins</span>
              </div>
              {r.servings && (
                <div className="flex items-center gap-1">
                  <Utensils className="w-4 h-4 text-indigo-500" />
                  <span>{r.servings} servings</span>
                </div>
              )}
            </div>

            {/* Ingredients */}
            {r.ingredients && r.ingredients.length > 0 && (
              <div>
                <h4 className="text-sm font-semibold text-gray-700 mb-1">
                  Ingredients
                </h4>
                <ul className="list-disc list-inside text-sm text-gray-600 space-y-0.5 max-h-28 overflow-y-auto pr-2">
                  {r.ingredients.map((ing, i) => (
                    <li key={i}>{ing}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Instructions */}
            {r.instructions && r.instructions.length > 0 && (
              <div>
                <h4 className="text-sm font-semibold text-gray-700 mb-1 flex items-center gap-1">
                  <ListOrdered className="w-4 h-4 text-indigo-500" />
                  Steps
                </h4>
                <ol className="list-decimal list-inside text-sm text-gray-600 space-y-1 max-h-40 overflow-y-auto pr-2">
                  {r.instructions.map((step, i) => (
                    <li key={i}>{step}</li>
                  ))}
                </ol>
              </div>
            )}

            {/* Tags */}
            {r.tags && r.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-auto">
                {r.tags.map((t) => (
                  <span
                    key={t}
                    className="px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-600 text-xs font-medium border border-indigo-200"
                  >
                    {t}
                  </span>
                ))}
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
