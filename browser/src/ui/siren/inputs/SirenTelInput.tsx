import type { Field } from "@siren-js/client";

export type SirenTelInputProps = { field: Field };

export function SirenTelInput({ field }: SirenTelInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="tel" />;
}
