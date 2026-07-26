import { useState } from "react";
import type { Field } from "@siren-js/client";

export type SirenObjectInputProps = { field: Field };

export function SirenObjectInput({ field }: SirenObjectInputProps) {
  const [entries, setEntries] = useState<[string, string][]>(() =>
    field.value !== null && typeof field.value === "object" && !Array.isArray(field.value)
      ? Object.entries(field.value).map(([key, value]) => [key, String(value)])
      : [["", ""]],
  );

  return (
    <div>
      <input
        data-siren-type="object"
        name={field.name}
        type="hidden"
        value={JSON.stringify(Object.fromEntries(entries.filter(([key]) => key !== "")))}
      />
      {entries.map(([key, value], index) => (
        <div key={`${field.name}-${index}`}>
          <input
            aria-label="Key"
            onChange={(event) =>
              setEntries(entries.map((entry, entryIndex) => (entryIndex === index ? [event.target.value, entry[1]] : entry)))
            }
            placeholder="Key"
            type="text"
            value={key}
          />
          <span>:</span>
          <input
            aria-label="Value"
            onChange={(event) =>
              setEntries(entries.map((entry, entryIndex) => (entryIndex === index ? [entry[0], event.target.value] : entry)))
            }
            placeholder="Value"
            type="text"
            value={value}
          />
          <button onClick={() => setEntries(entries.filter((_, entryIndex) => entryIndex !== index))} type="button">
            Remove
          </button>
        </div>
      ))}
      <button onClick={() => setEntries([...entries, ["", ""]])} type="button">
        Add
      </button>
    </div>
  );
}
