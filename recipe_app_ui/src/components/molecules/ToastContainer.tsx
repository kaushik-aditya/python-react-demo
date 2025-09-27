import React from "react";
import { useToast } from "../../context/ToastContext";
import { XCircle, CheckCircle, Info } from "lucide-react"; // icons

const typeStyles = {
  error: "bg-red-100 border-red-400 text-red-700",
  success: "bg-green-100 border-green-400 text-green-700",
  info: "bg-blue-100 border-blue-400 text-blue-700",
};

const typeIcons: Record<string, React.ReactNode> = {
  error: <XCircle className="h-5 w-5 text-red-500" />,
  success: <CheckCircle className="h-5 w-5 text-green-500" />,
  info: <Info className="h-5 w-5 text-blue-500" />,
};

export default function ToastContainer() {
  const { toasts, remove } = useToast();

  return (
    <div className="fixed bottom-4 left-4 space-y-3 z-50">
      {toasts.map((t) => (
        <div
          key={t.id}
          className={`flex items-center gap-2 px-4 py-2 border rounded-lg shadow-md ${typeStyles[t.type || "info"]}`}
        >
          {typeIcons[t.type || "info"]}
          <span className="text-sm font-medium">{t.message}</span>
          <button
            onClick={() => remove(t.id)}
            className="ml-auto text-xs font-bold opacity-60 hover:opacity-100"
          >
            ×
          </button>
        </div>
      ))}
    </div>
  );
}
