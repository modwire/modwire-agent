import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";
import { App } from "../App";

const sirenClient = vi.hoisted(() => ({
  execute: vi.fn(),
  get: vi.fn(),
}));

vi.mock("../../client/SirenClient", () => ({
  SirenClient: class {
    execute = sirenClient.execute;
    get = sirenClient.get;
  },
}));

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
  window.history.replaceState(null, "", "/");
});

it("loads and renders the Siren entry point", async () => {
  sirenClient.get.mockResolvedValue({
    actions: [],
    class: ["api", "entry-point"],
    entities: [],
    links: [],
    properties: { title: "Modwire API" },
    title: "Modwire API",
  });

  const { container } = render(<App />);

  expect(container.querySelector("header")).not.toBeNull();
  expect(container.querySelector("main")).not.toBeNull();
  expect(container.querySelector("footer")).not.toBeNull();
  expect(
    await screen.findByRole("heading", { name: "Modwire API" }),
  ).toBeInTheDocument();
  expect(sirenClient.get).toHaveBeenCalledWith("/siren/");
});
