import type { Field } from "@siren-js/client";

export type SirenRangeInputProps = { field: Field };

export function SirenRangeInput({ field }: SirenRangeInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="range" />;
}
