import React from "react";
import cx from "classnames";

type Variant = "primary" | "secondary" | "danger";

interface CustomButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
}

const base =
  "px-4 py-2 rounded-lg font-medium focus:outline-none transition-colors disabled:opacity-50";

const variants: Record<Variant, string> = {
  primary: "bg-blue-600 text-white hover:bg-blue-700",
  secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300",
  danger: "bg-red-600 text-white hover:bg-red-700"
};

const CustomButton: React.FC<CustomButtonProps> = ({
  className,
  variant = "primary",
  ...rest
}) => {
  return (
    <button
      className={cx(base, variants[variant], className)}
      {...rest}
    />
  );
};

export default CustomButton;
