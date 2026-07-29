import { Button, Fieldset, Stack } from "@mantine/core";
import type { Action } from "@siren-js/client";
import { Form } from "../form/Form";
import { FormField } from "../form/FormField";
import type { FormSchema } from "../form/FormSchema";
import { SirenField } from "./SirenField";

export type SirenActionFormProps = {
  action: Action;
  onSubmit: (
    action: Action,
    values: Record<string, unknown>,
  ) => Promise<void> | void;
};

export function SirenActionForm({ action, onSubmit }: SirenActionFormProps) {
  const form = action["x-form"];
  const schema =
    typeof form === "object" && form !== null
      ? ((form as Record<string, unknown>)["schema"] as FormSchema)
      : undefined;

  return (
    <Form onSubmit={(values) => onSubmit(action, values)} schema={schema}>
      {(errors) => (
        <Fieldset legend={action.title}>
          <Stack gap="sm">
            {action.fields.map((field) => (
              <FormField
                error={errors[field.name]}
                key={field.name}
                label={field.title ?? field.name}
              >
                <SirenField field={field} />
              </FormField>
            ))}
            <Button type="submit">{action.title}</Button>
          </Stack>
        </Fieldset>
      )}
    </Form>
  );
}
