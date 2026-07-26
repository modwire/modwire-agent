import { useState } from "react";
import type { Field } from "@siren-js/client";
import { Button, Group, Stack, Text, TextInput } from "@mantine/core";

export type SirenObjectInputProps = { field: Field };

export function SirenObjectInput({ field }: SirenObjectInputProps) {
  const [entries, setEntries] = useState<[string, string][]>(() =>
    field.value !== null && typeof field.value === "object" && !Array.isArray(field.value)
      ? Object.entries(field.value).map(([key, value]) => [key, String(value)])
      : [["", ""]],
  );

  return (
    <Stack gap="xs">
      <input
        data-siren-type="object"
        name={field.name}
        type="hidden"
        value={JSON.stringify(Object.fromEntries(entries.filter(([key]) => key !== "")))}
      />
      {entries.map(([key, value], index) => (
        <Group key={`${field.name}-${index}`}>
          <TextInput
            aria-label="Key"
            onChange={(event) =>
              setEntries(entries.map((entry, entryIndex) => (entryIndex === index ? [event.target.value, entry[1]] : entry)))
            }
            placeholder="Key"
            value={key}
          />
          <Text>:</Text>
          <TextInput
            aria-label="Value"
            onChange={(event) =>
              setEntries(entries.map((entry, entryIndex) => (entryIndex === index ? [entry[0], event.target.value] : entry)))
            }
            placeholder="Value"
            value={value}
          />
          <Button onClick={() => setEntries(entries.filter((_, entryIndex) => entryIndex !== index))} size="xs" type="button" variant="subtle">
            Remove
          </Button>
        </Group>
      ))}
      <Button onClick={() => setEntries([...entries, ["", ""]])} size="xs" type="button" variant="light">
        Add
      </Button>
    </Stack>
  );
}
