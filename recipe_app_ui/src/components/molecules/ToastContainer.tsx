import React from "react";
import { useToast } from "../../context/ToastContext";

const ToastContainer: React.FC = () => {
  const { toasts, remove } = useToast();
  return (
    <div className="fixed top-4 right-4 space-y-3 z-50">
      {toasts.map(t => (
        <div
          key={t.id}
          className={
            "rounded-xl px-4 py-3 shadow border " +
            (t.type === "error" ? "bg-red-600/90 border-red-400" :
             t.type === "success" ? "bg-green-600/90 border-green-400" :
             "bg-slate-700/90 border-slate-500")
          }
          onClick={() => remove(t.id)}
        >
          {t.message}
        </div>
      ))}
    </div>
  );
};

export default ToastContainer;
