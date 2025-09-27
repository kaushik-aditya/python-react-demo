# Recipe App — Refactored (Atomic Design)

This `src/` is refactored to follow **Atomic Design** with a clean layout:

- **Sidebar**: app name, Google-style search bar, dynamic filters (max cook time, tags, sort)
- **Navbar**: top filters (e.g., cuisine selector)
- **Main**: existing Recipe Grid (kept simple, styled to match)

## Structure

```
src/
  components/
    atoms/ (CustomButton, CustomInput, CustomSelector, CustomCheckbox, Icon)
    molecules/ (SearchBar, FilterGroup, ToastContainer, RecipeCard)
    organisms/ (Sidebar, Navbar, RecipeGrid)
    templates/ (DefaultLayout)
  config/
  context/ (ToastProvider)
  services/ (api.ts)
  types/ (recipe.ts)
  utils/ (debounce, classNames)
  pages/ (Home.tsx)
  App.tsx, main.tsx, index.css
```

## Run & Build

Assumes Vite + React + Tailwind:

```bash
# install
npm i

# env
cp .env.example .env
# then set VITE_API_URL=http://localhost:8000 (or your backend)

# dev
npm run dev

# test
npm run test

# build
npm run build
```

### Environment

- `VITE_API_URL`: backend base URL (e.g., `http://localhost:8000`)
- `VITE_DEFAULT_PAGE_SIZE`: optional page size (defaults to 30)

## Notes

- **Lazy loading**: image `loading="lazy"` in `RecipeCard`.
- **Exception handling**: API wrapper throws; `Home` toasts user-friendly errors.
- **SPA**: Single page driven by `Home.tsx`.
- **Responsive**: Tailwind grid & layout.
- **Config externalized**: see `config/index.ts`.
- **Tests**: vitest placeholder to extend with your logic.

```

```
