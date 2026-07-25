import { render } from "@testing-library/react";
import { expect, it } from "vitest";
import { App } from "./App";

it("mounts the browser application", () => {
  const { container } = render(<App />);

  expect(container.querySelector("header")).not.toBeNull();
  expect(container.querySelector("nav")).not.toBeNull();
  expect(container.querySelector("main")).not.toBeNull();
  expect(container.querySelector("aside")).not.toBeNull();
  expect(container).toHaveTextContent("Modwire");
});
