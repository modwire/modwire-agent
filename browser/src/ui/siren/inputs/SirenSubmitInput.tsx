import type { Field } from "@siren-js/client";

export type SirenSubmitInputProps = { field: Field };

export function SirenSubmitInput({ field }: SirenSubmitInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="submit" />;
}
