import type { Field } from "@siren-js/client";

export type SirenTextInputProps = {
  field: Field;
};

export function SirenTextInput({ field }: SirenTextInputProps) {
  return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="text" />;
}
