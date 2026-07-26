import type { Field } from "@siren-js/client";

export type SirenHiddenInputProps = { field: Field };

export function SirenHiddenInput({ field }: SirenHiddenInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="hidden" />;
}
