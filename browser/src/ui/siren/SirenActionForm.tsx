import { Button, Fieldset, Stack, Text } from "@mantine/core";
import { useState } from "react";
import type { Action } from "@siren-js/client";
import { SirenField } from "./SirenField";

export type SirenActionFormProps = {
  action: Action;
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function SirenActionForm({ action, onSubmit }: SirenActionFormProps) {
  const [errors, setErrors] = useState<Record<string, string>>({});

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        const values = Object.fromEntries(
          [...new Set(formData.keys())].map((name) => {
            const values = formData.getAll(name);
            const controls = event.currentTarget.elements.namedItem(name);
            const control =
              controls instanceof RadioNodeList ? controls.item(0) : controls;
            if (
              control instanceof HTMLElement &&
              control.dataset.sirenType === "object"
            ) {
              return [name, JSON.parse(String(values[0]))];
            }
            return [
              name,
              values.length > 1
                ? values.filter((value) => value !== "")
                : values[0],
            ];
          }),
        );
        const form = action["x-form"];
        const schema =
          typeof form === "object" && form !== null
            ? (form as Record<string, unknown>)["schema"]
            : undefined;
        const required: unknown[] =
          typeof schema === "object" &&
          schema !== null &&
          Array.isArray((schema as Record<string, unknown>)["required"])
            ? ((schema as Record<string, unknown>)["required"] as unknown[])
            : [];
        const nextErrors = Object.fromEntries(
          required
            .filter((name): name is string => typeof name === "string")
            .filter(
              (name) =>
                values[name] == null ||
                values[name] === "" ||
                (Array.isArray(values[name]) && !values[name].length),
            )
            .map((name) => [name, "Required"]),
        );

        setErrors(nextErrors);
        if (!Object.keys(nextErrors).length) {
          onSubmit(action, values);
        }
      }}
    >
      <Fieldset legend={action.title}>
        <Stack gap="sm">
          {action.fields.map((field) => (
            <label key={field.name}>
              <Text component="span">{field.title ?? field.name}</Text>
              <SirenField field={field} />
              {errors[field.name] ? (
                <Text c="red" size="sm">
                  {errors[field.name]}
                </Text>
              ) : null}
            </label>
          ))}
          <Button type="submit">{action.title}</Button>
        </Stack>
      </Fieldset>
    </form>
  );
}
