import type { Field } from "@siren-js/client";

export type SirenColorInputProps = { field: Field };

export function SirenColorInput({ field }: SirenColorInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="color" />;
}
