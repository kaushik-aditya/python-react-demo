import React from "react";

export type Recipe = {
  id: number;
  name: string;
  cuisine: string;
  cook_time_minutes: number;
  tags: string; // comma-separated from backend
};

export default function RecipeCard({ name, cuisine, cook_time_minutes, tags }: Recipe) {
  const tagList = tags ? tags.split(",") : [];
  return (
    <div className="p-4 shadow rounded bg-white border flex flex-col gap-2">
      <h3 className="text-lg font-bold">{name}</h3>
      <p className="text-sm text-gray-700">{cuisine}</p>
      <p className="text-sm">Cook Time: <b>{cook_time_minutes}</b> mins</p>
      <div className="flex flex-wrap gap-1">
        {tagList.map((t) => (
          <span key={t} className="px-2 py-0.5 border rounded text-xs">{t}</span>
        ))}
      </div>
    </div>
  );
}
