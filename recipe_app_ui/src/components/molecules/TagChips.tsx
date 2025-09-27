import React from "react";

type TagChipsProps = {
  availableTags: string[];
  selectedTags: string[];
  onToggleTag: (tag: string) => void;
};

const TagChips: React.FC<TagChipsProps> = ({
  availableTags,
  selectedTags,
  onToggleTag,
}) => {
  return (
    <div className="flex flex-wrap gap-2">
      {availableTags.map((tag) => {
        const isActive = selectedTags.includes(tag);
        return (
          <button
            key={tag}
            onClick={() => onToggleTag(tag)}
            className={`px-3 py-1 rounded-full border text-sm transition-colors ${
              isActive
                ? "bg-indigo-500 text-white border-indigo-500"
                : "bg-gray-100 text-gray-700 border-gray-300 hover:bg-gray-200"
            }`}
          >
            {tag}
          </button>
        );
      })}
    </div>
  );
};

export default TagChips;
