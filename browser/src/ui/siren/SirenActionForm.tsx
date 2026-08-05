import { Button, Fieldset, Stack } from "@mantine/core";
import { Field, type Action } from "@siren-js/client";
import { Form } from "../form/Form";
import { FormField } from "../form/FormField";
import type { FormSchema, FormSchemaProperty } from "../form/FormSchema";
import { SirenField } from "./SirenField";

export type SirenActionFormProps = {
  action: Action;
  onSubmit: (
    action: Action,
    values: Record<string, unknown>,
  ) => Promise<void> | void;
};

function structuredFieldType(
  schema: FormSchemaProperty,
): "list" | "object" | undefined {
  const types = Array.isArray(schema.type)
    ? schema.type
    : schema.type
      ? [schema.type]
      : [];
  if (types.includes("object") || schema.properties) return "object";
  if (types.includes("array") || schema.items) return "list";
  return undefined;
}

function actionFields(action: Action, schema?: FormSchema): Field[] {
  const fields = [...action.fields];
  const present = new Set(fields.map((field) => field.name));

  for (const [name, property] of Object.entries(schema?.properties ?? {})) {
    const type = structuredFieldType(property);
    if (!type || present.has(name)) continue;
    fields.push(
      Object.assign(new Field(), {
        name,
        title: property.title ?? name,
        type,
      }),
    );
  }

  return fields;
}

export function SirenActionForm({ action, onSubmit }: SirenActionFormProps) {
  const form = action["x-form"];
  const schema =
    typeof form === "object" && form !== null
      ? ((form as Record<string, unknown>)["schema"] as FormSchema)
      : undefined;
  const fields = actionFields(action, schema);

  return (
    <Form
      onSubmit={(values) => {
        action.fields = fields;
        return onSubmit(action, values);
      }}
      schema={schema}
    >
      {(errors) => (
        <Fieldset legend={action.title}>
          <Stack gap="sm">
            {fields.map((field) => (
              <FormField
                error={errors[field.name]}
                key={field.name}
                label={field.title ?? field.name}
              >
                <SirenField
                  field={field}
                  schema={schema?.properties?.[field.name]}
                />
              </FormField>
            ))}
            <Button type="submit">{action.title}</Button>
          </Stack>
        </Fieldset>
      )}
    </Form>
  );
}
