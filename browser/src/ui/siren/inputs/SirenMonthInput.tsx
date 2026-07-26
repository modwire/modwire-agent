import type { Field } from "@siren-js/client";

export type SirenMonthInputProps = { field: Field };

export function SirenMonthInput({ field }: SirenMonthInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="month" />;
}
