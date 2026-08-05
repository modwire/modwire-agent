import { Action, Field } from "@siren-js/client";
import { describe, expect, it } from "vitest";
import { applyActionValues } from "../ActionValues";

function field(name: string, value: unknown): Field {
  return Object.assign(new Field(), { name, value });
}

describe("applyActionValues", () => {
  it("applies values based on presence instead of truthiness", () => {
    const action = Object.assign(new Action(), {
      fields: [
        field("enabled", true),
        field("limit", 10),
        field("description", "Existing"),
        field("example_items", ["existing"]),
        field("example_document", { existing: true }),
        field("omitted_value", "Keep me"),
      ],
    });

    applyActionValues(action, {
      description: "",
      enabled: false,
      example_document: {},
      example_items: [],
      limit: 0,
    });

    expect(
      Object.fromEntries(
        action.fields.map((actionField) => [
          actionField.name,
          actionField.value,
        ]),
      ),
    ).toEqual({
      description: "",
      enabled: false,
      example_document: {},
      example_items: [],
      limit: 0,
      omitted_value: "Keep me",
    });
  });
});
