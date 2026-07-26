import type { Field } from "@siren-js/client";

export type SirenRadioInputProps = { field: Field };

export function SirenRadioInput({ field }: SirenRadioInputProps) {
  return <input defaultChecked={field.value === true} name={field.name} type="radio" />;
}
