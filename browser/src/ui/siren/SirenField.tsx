import type { Field } from "@siren-js/client";
import type { FormSchemaProperty } from "../form/FormSchema";
import { Input } from "../input/Input";
import { sirenRegistry } from "./SirenRegistry";

export type SirenFieldProps = {
  field: Field;
  schema?: FormSchemaProperty;
};

export function SirenField({ field, schema }: SirenFieldProps) {
  const FieldComponent = sirenRegistry.fields.get(field.type) ?? Input;

  return <FieldComponent field={field} schema={schema} />;
}
