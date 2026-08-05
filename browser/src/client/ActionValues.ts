import type { Action } from "@siren-js/client";

export function applyActionValues(
  action: Action,
  values: Record<string, unknown>,
): void {
  action.fields.forEach((field) => {
    if (Object.hasOwn(values, field.name)) {
      field.value = values[field.name];
    }
  });
}
