import type { Field } from "@siren-js/client";

export type SirenEmailInputProps = { field: Field };

export function SirenEmailInput({ field }: SirenEmailInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="email" />;
}
