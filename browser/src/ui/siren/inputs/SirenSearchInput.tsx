import type { Field } from "@siren-js/client";

export type SirenSearchInputProps = { field: Field };

export function SirenSearchInput({ field }: SirenSearchInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="search" />;
}
