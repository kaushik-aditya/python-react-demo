import React from "react";
import { cx } from "../../utils/classNames";

type Option = {
  value: string;
  label: string;
};

type CustomSelectorProps = Omit<
  React.SelectHTMLAttributes<HTMLSelectElement>,
  "onChange"
> & {
  options: Option[];
  value?: string;
  defaultValue?: string;
  onChange?: (value: string) => void;
};

const CustomSelector: React.FC<CustomSelectorProps> = ({
  className,
  options,
  value,
  defaultValue,
  onChange,
  ...rest
}) => {
  return (
    <select
      className={cx(
        "rounded-xl bg-white text-gray-800 px-4 py-2 shadow focus:ring-2 focus:ring-blue-400",
        className
      )}
      value={value}
      defaultValue={defaultValue}
      onChange={(e) => onChange?.(e.target.value)}
      {...rest}
    >
      {options.map((opt) => (
        <option key={opt.value} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
  );
};

export default CustomSelector;
