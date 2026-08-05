import { Checkbox, NumberInput, Select, Stack, TextInput } from "@mantine/core";
import type { FormSchemaProperty } from "../../../form/FormSchema";
import { JsonArrayEditor } from "./JsonArrayEditor";
import { JsonObjectEditor } from "./JsonObjectEditor";
import {
  initialValue,
  isJsonValue,
  JSON_TYPES,
  schemaTypes,
  valueType,
} from "./JsonValue";
import type { JsonEditorProps } from "./JsonValue";

function withType(
  schema: FormSchemaProperty,
  type: string,
): FormSchemaProperty {
  return { ...schema, type };
}

export function JsonEditor({ onChange, path, schema, value }: JsonEditorProps) {
  const types = schemaTypes(schema);
  const allowsNull = types.includes("null") || schema.nullable === true;
  const type = types.find((candidate) => candidate !== "null");

  if (!type) {
    const selectedType = valueType(value);
    return (
      <Stack gap="xs">
        <Select
          aria-label={`${path} type`}
          data={JSON_TYPES}
          onChange={(nextType) =>
            nextType && onChange(initialValue({ type: nextType }))
          }
          value={selectedType}
        />
        {selectedType === "null" ? null : (
          <JsonEditor
            onChange={onChange}
            path={path}
            schema={withType(schema, selectedType)}
            value={value}
          />
        )}
      </Stack>
    );
  }

  if (allowsNull && value === null) {
    return (
      <Checkbox
        checked
        label={`${path} is null`}
        onChange={(event) =>
          onChange(event.currentTarget.checked ? null : initialValue(schema))
        }
      />
    );
  }

  const nullControl = allowsNull ? (
    <Checkbox
      checked={false}
      label={`${path} is null`}
      onChange={(event) => event.currentTarget.checked && onChange(null)}
    />
  ) : null;
  const renderEditor = (props: JsonEditorProps) => <JsonEditor {...props} />;

  if (type === "object") {
    return (
      <JsonObjectEditor
        nullControl={nullControl}
        onChange={onChange}
        path={path}
        renderEditor={renderEditor}
        schema={schema}
        value={value}
      />
    );
  }

  if (type === "array") {
    return (
      <JsonArrayEditor
        nullControl={nullControl}
        onChange={onChange}
        path={path}
        renderEditor={renderEditor}
        schema={schema}
        value={value}
      />
    );
  }

  if (schema.enum) {
    const selectedIndex = schema.enum.findIndex(
      (candidate) => JSON.stringify(candidate) === JSON.stringify(value),
    );
    return (
      <Stack gap="xs">
        {nullControl}
        <Select
          aria-label={path}
          data={schema.enum.map((candidate, index) => ({
            label: String(candidate),
            value: String(index),
          }))}
          onChange={(index) => {
            const candidate =
              index == null ? undefined : schema.enum?.[Number(index)];
            if (isJsonValue(candidate)) onChange(candidate);
          }}
          value={selectedIndex < 0 ? null : String(selectedIndex)}
        />
      </Stack>
    );
  }

  if (type === "boolean") {
    return (
      <Stack gap="xs">
        {nullControl}
        <Checkbox
          checked={value === true}
          label={path}
          onChange={(event) => onChange(event.currentTarget.checked)}
        />
      </Stack>
    );
  }

  if (type === "number" || type === "integer") {
    return (
      <Stack gap="xs">
        {nullControl}
        <NumberInput
          allowDecimal={type !== "integer"}
          aria-label={path}
          onChange={(nextValue) => onChange(nextValue)}
          value={
            typeof value === "number" || typeof value === "string" ? value : ""
          }
        />
      </Stack>
    );
  }

  return (
    <Stack gap="xs">
      {nullControl}
      <TextInput
        aria-label={path}
        onChange={(event) => onChange(event.currentTarget.value)}
        value={typeof value === "string" ? value : ""}
      />
    </Stack>
  );
}
