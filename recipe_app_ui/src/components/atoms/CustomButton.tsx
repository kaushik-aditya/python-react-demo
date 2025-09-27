import React from "react";
import cx from "classnames";

type Variant = "primary" | "secondary" | "danger" | "icon";

interface CustomButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
}

const base =
  "px-4 py-2 rounded-lg font-medium focus:outline-none transition-colors disabled:opacity-50";

const variants: Record<Variant, string> = {
  primary: "bg-blue-600 text-white hover:bg-blue-700",
  secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300",
  danger: "bg-red-600 text-white hover:bg-red-700",
  icon: "p-2 rounded-full hover:bg-gray-100 text-gray-500" // ✅ new
};

const CustomButton: React.FC<CustomButtonProps> = ({
  className,
  variant = "primary",
  ...rest
}) => {
  return (
    <button className={cx(base, variants[variant], className)} {...rest} />
  );
};

export default CustomButton;
