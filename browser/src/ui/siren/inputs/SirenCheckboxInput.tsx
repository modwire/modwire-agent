import type { Field } from "@siren-js/client";

export type SirenCheckboxInputProps = { field: Field };

export function SirenCheckboxInput({ field }: SirenCheckboxInputProps) {
  return <input defaultChecked={field.value === true} name={field.name} type="checkbox" />;
}
