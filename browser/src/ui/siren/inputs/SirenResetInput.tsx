import type { Field } from "@siren-js/client";

export type SirenResetInputProps = { field: Field };

export function SirenResetInput({ field }: SirenResetInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="reset" />;
}
