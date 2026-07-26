import type { Field } from "@siren-js/client";

export type SirenFileInputProps = { field: Field };

export function SirenFileInput({ field }: SirenFileInputProps) {
  return <input name={field.name} type="file" />;
}
