// Centralized runtime config
export const CONFIG = {
  API_BASE_URL: import.meta.env.VITE_API_URL ?? "",
  DEFAULT_PAGE_SIZE: Number(import.meta.env.VITE_DEFAULT_PAGE_SIZE ?? 30),
};
