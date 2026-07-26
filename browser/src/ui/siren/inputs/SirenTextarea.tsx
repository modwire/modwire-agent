import type { Field } from "@siren-js/client";

export type SirenTextareaProps = { field: Field };

export function SirenTextarea({ field }: SirenTextareaProps) {
  return <textarea defaultValue={field.value == null ? "" : String(field.value)} name={field.name} />;
}
