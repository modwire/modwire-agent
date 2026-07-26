import type { Field } from "@siren-js/client";

export type SirenImageInputProps = { field: Field };

export function SirenImageInput({ field }: SirenImageInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="image" />;
}
