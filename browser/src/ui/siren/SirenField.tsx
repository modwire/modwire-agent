import type { Field } from "@siren-js/client";
import { Input } from "../input/Input";
import { sirenRegistry } from "./SirenRegistry";

export type SirenFieldProps = { field: Field };

export function SirenField({ field }: SirenFieldProps) {
  const FieldComponent = sirenRegistry.fields.get(field.type) ?? Input;

  return <FieldComponent field={field} />;
}
