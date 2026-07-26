import type { Field } from "@siren-js/client";

export type SirenButtonInputProps = { field: Field };

export function SirenButtonInput({ field }: SirenButtonInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="button" />;
}
