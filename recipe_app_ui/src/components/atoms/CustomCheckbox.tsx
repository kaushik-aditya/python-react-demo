import React from "react";

type Props = React.InputHTMLAttributes<HTMLInputElement> & { label?: string };

const CustomCheckbox: React.FC<Props> = ({ label, ...rest }) => (
  <label className="inline-flex items-center gap-2 cursor-pointer select-none">
    <input type="checkbox" className="w-4 h-4 accent-blue-500" {...rest} />
    {label && <span className="text-sm text-white/90">{label}</span>}
  </label>
);

export default CustomCheckbox;
