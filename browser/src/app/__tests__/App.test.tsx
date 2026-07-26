import { cleanup, render, waitFor } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";
import { App } from "../App";

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  window.history.replaceState(null, "", "/");
});

it("mounts the browser application", () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ title: "Modwire API", links: [], properties: { title: "Modwire API" } }), {
        headers: { "content-type": "application/vnd.siren+json" },
      }),
    ),
  );
  const { container } = render(<App />);

  expect(container.querySelector("header")).not.toBeNull();
  expect(container.querySelector("nav")).not.toBeNull();
  expect(container.querySelector("main")).not.toBeNull();
  expect(container.querySelector("aside")).not.toBeNull();
  return waitFor(() => expect(fetch).toHaveBeenCalled());
});
