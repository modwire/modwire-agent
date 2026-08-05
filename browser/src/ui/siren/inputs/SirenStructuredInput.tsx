import { Stack } from "@mantine/core";
import type { IChangeEvent } from "@rjsf/core";
import RjsfForm from "@rjsf/mantine";
import type { RJSFSchema } from "@rjsf/utils";
import type { Field } from "@siren-js/client";
import { useState } from "react";
import type { FormSchemaProperty } from "../../form/FormSchema";
import { jsonSchemaValidator } from "../../form/JsonSchemaValidator";
import { useFormValue } from "../../form/FormValueRegistry";

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
  const [value, setValue] = useState<unknown>(field.value);
  const publishValue = useFormValue(field.name, value);

  const updateValue = (event: IChangeEvent) => {
    setValue(event.formData);
    publishValue(event.formData);
  };

  return (
    <Stack gap="xs">
      <RjsfForm
        formData={value}
        idPrefix={field.name}
        onChange={updateValue}
        schema={effectiveSchema as RJSFSchema}
        tagName="div"
        validator={jsonSchemaValidator}
      >
        <></>
      </RjsfForm>
    </Stack>
  );
}
