import React from "react";
import TagChips from "../molecules/TagChips";
import CustomSelector from "../atoms/CustomSelector";

type Props = {
  availableTags: string[];
  selectedTags: string[];
  onToggleTag: (tag: string) => void;
  sortOrder: "asc" | "desc";
  onSortChange: (s: "asc" | "desc") => void;
};

const Sidebar: React.FC<Props> = ({
  availableTags,
  selectedTags,
  onToggleTag,
  sortOrder,
  onSortChange,
}) => {
  return (
    <div className="flex flex-col gap-6">
      <section>
        <h2 className="font-semibold mb-2 text-gray-700">Sort By</h2>
        <CustomSelector
          options={[
            { value: "asc", label: "Cook Time: Low to High" },
            { value: "desc", label: "Cook Time: High to Low" },
          ]}
          value={sortOrder}
          onChange={(val) => onSortChange(val as "asc" | "desc")}
        />
      </section>
      {/* Tags section */}
      <section>
        <h2 className="font-semibold mb-2 text-gray-700">Tags</h2>
        <TagChips
          availableTags={availableTags}
          selectedTags={selectedTags}
          onToggleTag={onToggleTag}
        />
      </section>
      
    </div>
  );
};

export default Sidebar;
