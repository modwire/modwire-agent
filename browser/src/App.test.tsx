import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { App } from "./App";

describe("App", () => {
  it("renders the project title and primary journey", () => {
    render(<App />);

    expect(screen.getByRole("heading", { name: "Modwire API Browser" })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /explore react/i })).toHaveAttribute("href", "https://react.dev");
  });
});
