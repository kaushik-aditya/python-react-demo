import React, { useState } from "react";

type Props = { onSearch: (query: string) => void };

export default function SearchBar({ onSearch }: Props) {
  const [query, setQuery] = useState("");

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && query.trim().length >= 3) {
      onSearch(query.trim());
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <input
        aria-label="Search recipes"
        type="text"
        placeholder="Search recipes by name or cuisine..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        className="p-3 border rounded w-full shadow-sm"
      />
      <div className="text-sm text-gray-500 mt-1">Type at least 3 characters and press Enter</div>
    </div>
  );
}
