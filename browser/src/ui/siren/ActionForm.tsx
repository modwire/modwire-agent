import type { Action } from "@siren-js/client";
import { Button, Fieldset, Stack, Text } from "@mantine/core";
import { SirenInput } from "./inputs/SirenInput";

export type ActionFormProps = {
  action: Action;
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function ActionForm({ action, onSubmit }: ActionFormProps) {
  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        onSubmit(
          action,
          Object.fromEntries(
            [...new Set(formData.keys())].map((name) => {
              const values = formData.getAll(name);
              const controls = event.currentTarget.elements.namedItem(name);
              const control = controls instanceof RadioNodeList ? controls.item(0) : controls;
              if (control instanceof HTMLElement && control.dataset.sirenType === "object") {
                return [name, JSON.parse(String(values[0]))];
              }
              return [name, values.length > 1 ? values.filter((value) => value !== "") : values[0]];
            }),
          ),
        );
      }}
    >
      <Fieldset legend={action.title}>
        <Stack gap="sm">
        {action.fields.map((field) => (
          <label key={field.name}>
            <Text component="span">{field.title ?? field.name}</Text>
            <SirenInput field={field} />
          </label>
        ))}
        <Button type="submit">{action.title}</Button>
        </Stack>
      </Fieldset>
    </form>
  );
}
