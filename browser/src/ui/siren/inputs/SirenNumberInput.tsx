import type { Field } from "@siren-js/client";

export type SirenNumberInputProps = { field: Field };

export function SirenNumberInput({ field }: SirenNumberInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="number" />;
}
