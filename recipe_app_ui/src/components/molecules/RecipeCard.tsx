import { Star, Clock } from "lucide-react";
import type { Recipe } from "../../types/recipe";

export default function RecipeCard({
  name,
  cuisine,
  cook_time_minutes,
  tags,
  image,
  rating,
  review_count,
}: Recipe) {
  return (
    <div className="bg-white rounded-2xl shadow-md hover:shadow-xl border transition overflow-hidden flex flex-col group">
      {/* 🖼️ Recipe image */}
      <div className="relative">
        {image && (
          <img
            src={image}
            alt={name}
            className="h-52 w-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        )}
        {rating !== undefined && (
          <div className="absolute top-2 right-2 bg-white/90 px-2 py-1 rounded-full flex items-center gap-1 text-yellow-500 text-sm shadow">
            <Star className="w-4 h-4 fill-yellow-400" />
            <span className="font-medium">{rating.toFixed(1)}</span>
          </div>
        )}
      </div>

      {/* 📖 Content */}
      <div className="p-5 flex flex-col gap-3 flex-1">
        <h3 className="text-lg font-semibold text-gray-900 line-clamp-2 group-hover:text-indigo-600 transition">
          {name}
        </h3>
        <p className="text-sm text-gray-500">{cuisine}</p>

        {/* Time + Reviews */}
        <div className="flex items-center justify-between text-sm text-gray-600">
          <div className="flex items-center gap-1">
            <Clock className="w-4 h-4 text-indigo-500" />
            <span>{cook_time_minutes} mins</span>
          </div>
          {review_count !== undefined && (
            <span className="text-gray-400">({review_count} reviews)</span>
          )}
        </div>

        {/* 🏷️ Tags */}
        {tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mt-auto">
            {tags.map((t) => (
              <span
                key={t}
                className="px-2.5 py-1 rounded-full bg-indigo-50 text-indigo-600 text-xs font-medium border border-indigo-100 shadow-sm"
              >
                {t}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
