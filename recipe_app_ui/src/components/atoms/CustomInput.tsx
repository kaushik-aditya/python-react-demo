import React from "react";
import { cx } from "../../utils/classNames";

type Props = React.InputHTMLAttributes<HTMLInputElement>;

const CustomInput = React.forwardRef<HTMLInputElement, Props>(function CustomInput({ className, ...rest }, ref) {
  return (
    <input
      ref={ref}
      className={cx(
        "w-full rounded-full bg-white text-gray-800 placeholder-gray-400",
        "px-5 py-3 outline-none shadow focus:ring-2 focus:ring-blue-400",
        className
      )}
      {...rest}
    />
  );
});

export default CustomInput;
