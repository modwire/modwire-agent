import { useState } from "react";
import type { Field } from "@siren-js/client";
import { Button, Group, Stack, TextInput } from "@mantine/core";

export type SirenStringListInputProps = { field: Field };

export function SirenStringListInput({ field }: SirenStringListInputProps) {
  const [values, setValues] = useState(() =>
    Array.isArray(field.value) &&
    field.value.every((value) => typeof value === "string")
      ? field.value
      : [""],
  );

  return (
    <Stack gap="xs">
      <input name={field.name} type="hidden" value="" />
      {values.map((value, index) => (
        <Group key={`${field.name}-${index}`}>
          <TextInput
            name={field.name}
            onChange={(event) =>
              setValues(
                values.map((item, itemIndex) =>
                  itemIndex === index ? event.target.value : item,
                ),
              )
            }
            value={value}
          />
          <Button
            onClick={() =>
              setValues(values.filter((_, itemIndex) => itemIndex !== index))
            }
            size="xs"
            type="button"
            variant="subtle"
          >
            Remove
          </Button>
        </Group>
      ))}
      <Button
        onClick={() => setValues([...values, ""])}
        size="xs"
        type="button"
        variant="light"
      >
        Add
      </Button>
    </Stack>
  );
}
