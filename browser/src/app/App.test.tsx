import { render } from "@testing-library/react";
import { expect, it } from "vitest";
import { App } from "./App";

it("mounts the browser application", () => {
  const { container } = render(<App />);

  expect(container.querySelector("#modwire-siren-browser")).not.toBeNull();
});
