import { Stack } from "@mantine/core";
import type { Field } from "@siren-js/client";
import { useState } from "react";
import type { FormSchemaProperty } from "../../form/FormSchema";
import { useFormValue } from "../../form/FormValueRegistry";
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
  const publishValue = useFormValue(field.name, value);

  const updateValue = (nextValue: JsonValue) => {
    setValue(nextValue);
    publishValue(nextValue);
  };

  return (
    <Stack gap="xs">
      <JsonEditor
        onChange={updateValue}
        path={field.name}
        schema={effectiveSchema}
        value={value}
      />
    </Stack>
  );
}
