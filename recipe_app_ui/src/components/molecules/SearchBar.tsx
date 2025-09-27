import React, { useRef, useState } from "react";
import CustomInput from "../atoms/CustomInput";
import CustomButton from "../atoms/CustomButton";
import { SearchIcon } from "../atoms/Icon";

type Props = {
  onSearch: (q: string) => void;
  minLength?: number;
  placeholder?: string;
};

const SearchBar: React.FC<Props> = ({
  onSearch,
  minLength = 3,
  placeholder = "Search recipes..."
}) => {
  const [q, setQ] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  const triggerSearch = () => {
    if (q.length >= minLength) {
      onSearch(q);
    }
  };

  return (
    <div className="w-full relative">
      <div
        className="
          flex items-center gap-2
          bg-white/90
          rounded-full
          border border-gray-200
          px-4 py-2
          shadow-sm
          hover:shadow-md
          transition-shadow
        "
      >
        {/* Input */}
        <CustomInput
          ref={inputRef}
          value={q}
          onChange={(e) => setQ(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") triggerSearch();
          }}
          placeholder={placeholder}
          className="
            flex-1 bg-transparent text-gray-900 
            placeholder-gray-500 
            border-0 outline-none 
            focus:ring-0
          "
        />

        {/* Search button with icon */}
        <CustomButton
          type="button"
          variant="icon"
          onClick={triggerSearch}
          disabled={q.length < minLength} // ✅ disable until minLength reached
        >
          <SearchIcon className="h-5 w-5" />
        </CustomButton>
      </div>
    </div>
  );
};

export default SearchBar;
