import type { Field } from "@siren-js/client";

export type SirenDateTimeLocalInputProps = { field: Field };

export function SirenDateTimeLocalInput({ field }: SirenDateTimeLocalInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="datetime-local" />;
}
