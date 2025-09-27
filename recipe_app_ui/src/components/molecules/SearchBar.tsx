import React, { useEffect, useMemo, useRef, useState } from "react";
import CustomInput from "../atoms/CustomInput";
import { SearchIcon } from "../atoms/Icon";
import { debounce } from "../../utils/debounce";

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
  const debounced = useMemo(() => debounce(onSearch, 350), [onSearch]);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (q.length >= minLength) debounced(q);
  }, [q, minLength, debounced]);

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
        {/* Search icon */}
        
        {/* Input */}
        <CustomInput
          ref={inputRef}
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder={placeholder}
          className="
            flex-1 bg-transparent text-gray-900 
            placeholder-gray-500 
            border-0 outline-none 
            focus:ring-0
          "
        />
        <SearchIcon className="text-gray-500 h-5 w-5" />

      </div>
    </div>
  );
};

export default SearchBar;
