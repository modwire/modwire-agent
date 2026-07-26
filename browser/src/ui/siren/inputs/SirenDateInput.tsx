import type { Field } from "@siren-js/client";

export type SirenDateInputProps = { field: Field };

export function SirenDateInput({ field }: SirenDateInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="date" />;
}
