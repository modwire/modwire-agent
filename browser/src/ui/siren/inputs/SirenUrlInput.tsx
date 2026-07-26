import type { Field } from "@siren-js/client";

export type SirenUrlInputProps = { field: Field };

export function SirenUrlInput({ field }: SirenUrlInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="url" />;
}
