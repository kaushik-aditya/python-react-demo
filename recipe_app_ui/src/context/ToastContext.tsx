import React, { createContext, useCallback, useContext, useState } from "react";

export type Toast = { id: string; type?: "success"|"error"|"info"; message: string; };
type ToastCtx = {
  toasts: Toast[];
  push: (t: Omit<Toast, "id">) => void;
  remove: (id: string) => void;
};

const Ctx = createContext<ToastCtx | null>(null);

export const ToastProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const remove = useCallback((id: string) => {
    setToasts((xs) => xs.filter(t => t.id !== id));
  }, []);

  const push = useCallback((t: Omit<Toast, "id">) => {
    const id = Math.random().toString(36).slice(2);
    setToasts((xs) => [...xs, { ...t, id }]);
    setTimeout(() => remove(id), 3000);
  }, [remove]);

  return <Ctx.Provider value={{ toasts, push, remove }}>{children}</Ctx.Provider>;
};

export function useToast() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("ToastProvider missing");
  return ctx;
}
