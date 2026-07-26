import type { Field } from "@siren-js/client";

export type SirenPasswordInputProps = { field: Field };

export function SirenPasswordInput({ field }: SirenPasswordInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="password" />;
}
