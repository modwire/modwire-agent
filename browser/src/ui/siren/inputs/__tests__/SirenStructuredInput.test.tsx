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
import {
  SirenActionForm,
  STRUCTURED_FORM_EXTENSION,
} from "../../SirenActionForm";

const exampleDocumentSchema = {
  additionalProperties: true,
  properties: {
    count: { type: "number" },
    enabled: { type: "boolean" },
    example_items: {
      items: {
        properties: {
          active: { type: "boolean" },
          label: { minLength: 1, type: "string" },
          weight: { type: "number" },
        },
        required: ["active", "label", "weight"],
        type: "object",
      },
      type: "array",
    },
    example_property: { minLength: 1, type: "string" },
    notes: { type: "string" },
    nullable_value: { type: ["string", "null"] },
  },
  required: ["count", "enabled", "example_items", "example_property"],
  type: "object",
};

function action(fields: Field[]): Action {
  return Object.assign(new Action(), {
    fields,
    href: "/example-resources",
    method: "POST",
    name: "create_example_resource",
    title: "Create example resource",
    type: "application/json",
    [STRUCTURED_FORM_EXTENSION]: {
      controls: [
        {
          control: "https://modwire.dev/siren/controls/object/v1",
          location: "body",
          mediaType: "application/json",
          name: "example_document",
          required: true,
          schema: exampleDocumentSchema,
        },
      ],
      version: "1",
    },
  });
}

function field(name: string, type: string, value?: unknown): Field {
  return Object.assign(new Field(), { name, type, value });
}

afterEach(cleanup);

describe("SirenStructuredInput", () => {
  it("edits nested values and preserves their JSON types", async () => {
    const onSubmit = vi.fn();
    const exampleAction = action([
      field("title", "text", "Example"),
      field("example_document", "object", {
        arbitrary: { nested: [true, 2, "example", null] },
        count: 0,
        enabled: false,
        example_items: [],
        example_property: "Initial",
      }),
    ]);

    render(
      <MantineProvider>
        <SirenActionForm action={exampleAction} onSubmit={onSubmit} />
      </MantineProvider>,
    );

    fireEvent.change(
      screen.getByRole("textbox", {
        name: "example_document.example_property",
      }),
      { target: { value: "Updated" } },
    );
    fireEvent.click(
      screen.getByRole("checkbox", { name: "example_document.enabled" }),
    );
    fireEvent.click(
      screen.getByRole("button", {
        name: "Add item to example_document.example_items",
      }),
    );
    fireEvent.change(
      screen.getByRole("textbox", {
        name: "example_document.example_items[0].label",
      }),
      { target: { value: "Discarded" } },
    );
    fireEvent.click(
      screen.getByRole("button", {
        name: "Add item to example_document.example_items",
      }),
    );
    fireEvent.change(
      screen.getByRole("textbox", {
        name: "example_document.example_items[1].label",
      }),
      { target: { value: "Kept" } },
    );
    fireEvent.change(
      screen.getByRole("textbox", {
        name: "example_document.example_items[1].weight",
      }),
      { target: { value: "2.5" } },
    );
    fireEvent.click(
      screen.getByRole("checkbox", {
        name: "example_document.example_items[1].active",
      }),
    );
    fireEvent.click(
      screen.getByRole("button", {
        name: "Remove item 1 from example_document.example_items",
      }),
    );
    fireEvent.click(screen.getByRole("button", { name: "Add notes" }));
    fireEvent.change(
      screen.getByRole("textbox", { name: "example_document.notes" }),
      { target: { value: "Temporary" } },
    );
    fireEvent.click(screen.getByRole("button", { name: "Remove notes" }));
    fireEvent.click(screen.getByRole("button", { name: "Add nullable_value" }));
    fireEvent.click(
      screen.getByRole("checkbox", {
        name: "example_document.nullable_value is null",
      }),
    );
    fireEvent.click(
      screen.getByRole("button", { name: "Create example resource" }),
    );

    await waitFor(() =>
      expect(onSubmit).toHaveBeenCalledWith(exampleAction, {
        example_document: {
          arbitrary: { nested: [true, 2, "example", null] },
          count: 0,
          enabled: true,
          example_items: [{ active: true, label: "Kept", weight: 2.5 }],
          example_property: "Updated",
          nullable_value: null,
        },
        title: "Example",
      }),
    );
  });

  it("adds missing structured controls and reports nested required fields", async () => {
    const onSubmit = vi.fn();
    const exampleAction = action([field("title", "text", "Example")]);

    render(
      <MantineProvider>
        <SirenActionForm action={exampleAction} onSubmit={onSubmit} />
      </MantineProvider>,
    );

    expect(
      screen.getByRole("textbox", {
        name: "example_document.example_property",
      }),
    ).toBeInTheDocument();

    fireEvent.click(
      screen.getByRole("button", { name: "Create example resource" }),
    );

    expect(
      await screen.findAllByText("example_document.example_property: Required"),
    ).toHaveLength(2);
    expect(onSubmit).not.toHaveBeenCalled();

    fireEvent.change(
      screen.getByRole("textbox", {
        name: "example_document.example_property",
      }),
      { target: { value: "Ready" } },
    );
    fireEvent.click(
      screen.getByRole("button", { name: "Create example resource" }),
    );

    await waitFor(() => expect(onSubmit).toHaveBeenCalledOnce());
    expect(exampleAction.fields.map((actionField) => actionField.name)).toEqual(
      ["title", "example_document"],
    );
  });
});
