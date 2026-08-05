import { MantineProvider } from "@mantine/core";
import { Action, Field } from "@siren-js/client";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import {
  SirenActionForm,
  STRUCTURED_FORM_EXTENSION,
} from "../../SirenActionForm";

const exampleDocumentSchema = {
  additionalProperties: false,
  properties: {
    count: { type: "number" },
    enabled: { type: "boolean" },
    example_items: {
      items: {
        additionalProperties: false,
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
  it("renders the advertised schema and submits nested JSON values", async () => {
    const onSubmit = vi.fn();
    const exampleAction = action([
      field("title", "text", "Example"),
      field("example_document", "object", {
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
      screen.getByRole("textbox", { name: "example_property" }),
      { target: { value: "Updated" } },
    );
    fireEvent.click(screen.getByRole("checkbox", { name: "enabled" }));

    const items = screen.getByRole("group", { name: "example_items" });
    fireEvent.click(within(items).getByRole("button", { name: "Add Item" }));
    fireEvent.change(within(items).getByRole("textbox", { name: "label" }), {
      target: { value: "Nested" },
    });
    fireEvent.change(within(items).getByRole("textbox", { name: "weight" }), {
      target: { value: "2.5" },
    });
    fireEvent.click(within(items).getByRole("checkbox", { name: "active" }));
    fireEvent.click(
      screen.getByRole("button", { name: "Create example resource" }),
    );

    await waitFor(() =>
      expect(onSubmit).toHaveBeenCalledWith(exampleAction, {
        example_document: {
          count: 0,
          enabled: true,
          example_items: [{ active: true, label: "Nested", weight: 2.5 }],
          example_property: "Updated",
        },
        title: "Example",
      }),
    );
  });

  it("adds an advertised structured control omitted from official fields", () => {
    const exampleAction = action([field("title", "text", "Example")]);

    render(
      <MantineProvider>
        <SirenActionForm action={exampleAction} onSubmit={vi.fn()} />
      </MantineProvider>,
    );

    expect(
      screen.getByRole("textbox", { name: "example_property" }),
    ).toBeInTheDocument();
    expect(screen.getByRole("textbox", { name: "count" })).toBeInTheDocument();
    expect(
      screen.getByRole("checkbox", { name: "enabled" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("group", { name: "example_items" }),
    ).toBeInTheDocument();
    expect(exampleAction.fields.map((actionField) => actionField.name)).toEqual(
      ["title"],
    );
  });

  it("renders and submits an advertised list control", async () => {
    const onSubmit = vi.fn();
    const exampleAction = Object.assign(new Action(), {
      fields: [field("example_items", "list", ["Initial"])],
      href: "/example-resources",
      method: "POST",
      name: "create_example_resource",
      title: "Create example resource",
      type: "application/json",
      [STRUCTURED_FORM_EXTENSION]: {
        controls: [
          {
            control: "https://modwire.dev/siren/controls/array/v1",
            location: "body",
            mediaType: "application/json",
            name: "example_items",
            required: true,
            schema: { items: { type: "string" }, type: "array" },
          },
        ],
        version: "1",
      },
    });

    render(
      <MantineProvider>
        <SirenActionForm action={exampleAction} onSubmit={onSubmit} />
      </MantineProvider>,
    );

    fireEvent.change(screen.getByRole("textbox"), {
      target: { value: "Updated" },
    });
    fireEvent.click(
      screen.getByRole("button", { name: "Create example resource" }),
    );

    await waitFor(() =>
      expect(onSubmit).toHaveBeenCalledWith(exampleAction, {
        example_items: ["Updated"],
      }),
    );
  });
});
