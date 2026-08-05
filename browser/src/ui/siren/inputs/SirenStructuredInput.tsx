import { Stack } from "@mantine/core";
import type { Field } from "@siren-js/client";
import { useState } from "react";
import type { FormSchemaProperty } from "../../form/FormSchema";
import { JsonEditor } from "./structured/JsonEditor";
import { normalizeValue } from "./structured/JsonValue";
import type { JsonValue } from "./structured/JsonValue";

export type SirenStructuredInputProps = {
  field: Field;
  schema?: FormSchemaProperty;
};

export function SirenStructuredInput({
  field,
  schema = {},
}: SirenStructuredInputProps) {
  const effectiveSchema: FormSchemaProperty =
    Object.keys(schema).length > 0
      ? schema
      : { type: field.type === "list" ? "array" : "object" };
  const [value, setValue] = useState<JsonValue>(() =>
    normalizeValue(field.value, effectiveSchema),
  );

  return (
    <Stack gap="xs">
      <input
        data-siren-type="json"
        name={field.name}
        type="hidden"
        value={JSON.stringify(value)}
      />
      <JsonEditor
        onChange={setValue}
        path={field.name}
        schema={effectiveSchema}
        value={value}
      />
    </Stack>
  );
}
