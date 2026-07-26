import type { Field } from "@siren-js/client";

export type SirenTimeInputProps = { field: Field };

export function SirenTimeInput({ field }: SirenTimeInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="time" />;
}
