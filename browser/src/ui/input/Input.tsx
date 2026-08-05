import type { Field } from "@siren-js/client";
import {
  Checkbox,
  FileInput,
  Radio,
  Stack,
  Textarea,
  TextInput,
} from "@mantine/core";
import { useId } from "react";
import type { FormSchemaProperty } from "../form/FormSchema";

export type InputProps = { field: Field; schema?: FormSchemaProperty };

type RadioChoice = {
  selected?: boolean;
  value: string | number | boolean;
};

function radioChoices(field: Field): RadioChoice[] {
  if (!Array.isArray(field.value)) return [];

  return field.value.filter(
    (choice): choice is RadioChoice =>
      typeof choice === "object" &&
      choice !== null &&
      "value" in choice &&
      ["string", "number", "boolean"].includes(typeof choice.value),
  );
}

export function Input({ field }: InputProps) {
  const inputId = useId();

  if (field.type === "checkbox") {
    return <Checkbox defaultChecked={field.value === true} name={field.name} />;
  }

  if (field.type === "radio") {
    const choices = radioChoices(field);
    const selected = choices.find((choice) => choice.selected);

    return (
      <Radio.Group
        defaultValue={selected == null ? null : String(selected.value)}
        name={field.name}
      >
        <Stack gap="xs">
          {choices.map((choice, index) => {
            const value = String(choice.value);

            return (
              <Radio
                id={`${inputId}-${index}`}
                key={`${value}-${index}`}
                label={value}
                value={value}
              />
            );
          })}
        </Stack>
      </Radio.Group>
    );
  }

  if (field.type === "file") {
    return <FileInput name={field.name} />;
  }

  if (field.type === "hidden") {
    return (
      <input
        defaultValue={field.value == null ? "" : String(field.value)}
        name={field.name}
        type="hidden"
      />
    );
  }

  if (field.type === "textarea") {
    return (
      <Textarea
        defaultValue={field.value == null ? "" : String(field.value)}
        name={field.name}
      />
    );
  }

  return (
    <TextInput
      defaultValue={field.value == null ? "" : String(field.value)}
      name={field.name}
      type={field.type}
    />
  );
}
