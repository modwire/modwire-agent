import { MantineProvider } from "@mantine/core";
import { Action, Field } from "@siren-js/client";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { SirenActionForm } from "../../siren/SirenActionForm";
import { Input } from "../Input";

const visibilityField = Object.assign(new Field(), {
  class: [],
  name: "visibility",
  title: "Visibility",
  type: "radio",
  value: [
    { value: "private", selected: false },
    { value: "public", selected: true },
  ],
});

afterEach(cleanup);

describe("radio input", () => {
  it("renders every choice and restores the selected value", () => {
    render(
      <MantineProvider>
        <Input field={visibilityField} />
      </MantineProvider>,
    );

    const privateChoice = screen.getByRole("radio", { name: "private" });
    const publicChoice = screen.getByRole("radio", { name: "public" });

    expect(screen.getAllByRole("radio")).toHaveLength(2);
    expect(privateChoice).toHaveAttribute("name", "visibility");
    expect(publicChoice).toHaveAttribute("name", "visibility");
    expect(privateChoice).not.toBeChecked();
    expect(publicChoice).toBeChecked();

    fireEvent.click(privateChoice);

    expect(privateChoice).toBeChecked();
    expect(publicChoice).not.toBeChecked();
  });

  it("submits the selected choice", async () => {
    const onSubmit = vi.fn();
    const action = Object.assign(new Action(), {
      class: [],
      fields: [visibilityField],
      href: "/example-resources",
      method: "POST",
      name: "create_example_resource",
      title: "Create example resource",
      type: "application/json",
    });

    render(
      <MantineProvider>
        <SirenActionForm action={action} onSubmit={onSubmit} />
      </MantineProvider>,
    );

    fireEvent.click(screen.getByRole("radio", { name: "private" }));
    fireEvent.click(
      screen.getByRole("button", { name: "Create example resource" }),
    );

    await waitFor(() =>
      expect(onSubmit).toHaveBeenCalledWith(action, { visibility: "private" }),
    );
  });
});
