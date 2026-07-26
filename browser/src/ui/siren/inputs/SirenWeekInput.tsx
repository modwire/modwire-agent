import type { Field } from "@siren-js/client";

export type SirenWeekInputProps = { field: Field };

export function SirenWeekInput({ field }: SirenWeekInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="week" />;
}
