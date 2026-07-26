import type { Field } from "@siren-js/client";
import { Checkbox, FileInput, Radio, Textarea, TextInput } from "@mantine/core";

export type InputProps = { field: Field };

export function Input({ field }: InputProps) {
  if (field.type === "checkbox") {
    return <Checkbox defaultChecked={field.value === true} name={field.name} />;
  }

  if (field.type === "radio") {
    return <Radio defaultChecked={field.value === true} name={field.name} />;
  }

  if (field.type === "file") {
    return <FileInput name={field.name} />;
  }

  if (field.type === "hidden") {
    return <input defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type="hidden" />;
  }

  if (field.type === "textarea") {
    return <Textarea defaultValue={field.value == null ? "" : String(field.value)} name={field.name} />;
  }

  return <TextInput defaultValue={field.value == null ? "" : String(field.value)} name={field.name} type={field.type} />;
}
