// src/tests/App.test.tsx
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import App from "../App";

// 🔌 Check MSW itself works
it("fetches recipes via MSW", async () => {
  const resp = await fetch("/api/recipes/");
  const data = await resp.json();

  console.log("📦 Recipes:", data.length);
  expect(Array.isArray(data)).toBe(true);
  expect(data.length).toBeGreaterThan(0);
  expect(data[0]).toHaveProperty("name");
});

describe("App integration", () => {
  it("renders the app title", async () => {
    render(<App />);
    // because Navbar is lazy-loaded, wait until it’s in the DOM
    expect(await screen.findByText("RecipeApp")).toBeInTheDocument();
  });

  it("renders recipes from the API", async () => {
    render(<App />);
    // wait for mocked recipes from recipes.mock.json
    expect(await screen.findByText(/Chocolate Chip Cookies/i)).toBeInTheDocument();
    expect(await screen.findByText(/Chicken Alfredo Pasta/i)).toBeInTheDocument();
  });

  it("renders some tags in the sidebar", async () => {
    render(<App />);
    // Just check if any one known tag is shown
    expect(await screen.findByRole("button", { name: "Baking" }))
      .toBeInTheDocument();
  });
});
