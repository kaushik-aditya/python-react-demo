import React from "react";
import { Menu } from "lucide-react";
import SearchBar from "../molecules/SearchBar";

type NavbarProps = {
  onToggleSidebar: () => void;
  onSearch: (q: string) => void;
  loading?: boolean;
};

const Navbar: React.FC<NavbarProps> = ({ onToggleSidebar, onSearch, loading }) => {
  return (
    <header className="w-full bg-white border-b shadow-sm flex items-center px-4 py-3 gap-4">
      {/* Toggle button */}
      <button
        onClick={onToggleSidebar}
        className="p-2 rounded-lg hover:bg-gray-100"
        aria-label="Toggle sidebar"
      >
        <Menu className="h-6 w-6 text-gray-700" />
      </button>

      {/* App name */}
      <h1 className="text-xl font-bold bg-gradient-to-r from-indigo-500 to-pink-500 bg-clip-text text-transparent">
        RecipeApp
      </h1>

      {/* Search bar */}
      <div className="flex-1 max-w-xl mx-auto">
        <SearchBar onSearch={onSearch} loading={loading} placeholder="Search recipes..." />
      </div>
    </header>
  );
};

export default Navbar;
