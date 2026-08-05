import { Button, Fieldset, Stack } from "@mantine/core";
import { Field, type Action } from "@siren-js/client";
import { Form } from "../form/Form";
import { FormField } from "../form/FormField";
import type { FormSchema, FormSchemaProperty } from "../form/FormSchema";
import { SirenField } from "./SirenField";

export const STRUCTURED_FORM_EXTENSION =
  "https://modwire.dev/siren/structured-form/v1";

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

function record(value: unknown): Record<string, unknown> | undefined {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : undefined;
}

function structuredFormSchema(action: Action): FormSchema | undefined {
  const extension = record(action[STRUCTURED_FORM_EXTENSION]);
  const controls = Array.isArray(extension?.controls)
    ? extension.controls.flatMap((value) => {
        const control = record(value);
        const schema = record(control?.schema);
        return typeof control?.name === "string" &&
          control.location === "body" &&
          schema
          ? [
              {
                name: control.name,
                required: control.required === true,
                schema: schema as FormSchemaProperty,
              },
            ]
          : [];
      })
    : [];
  if (controls.length) {
    return {
      properties: Object.fromEntries(
        controls.map((control) => [control.name, control.schema]),
      ),
      required: controls
        .filter((control) => control.required === true)
        .map((control) => control.name),
      type: "object",
    };
  }

  const legacy = record(action["x-form"]);
  return record(legacy?.schema) as FormSchema | undefined;
}

export function SirenActionForm({ action, onSubmit }: SirenActionFormProps) {
  const schema = structuredFormSchema(action);
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
