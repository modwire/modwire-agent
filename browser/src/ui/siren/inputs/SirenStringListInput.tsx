import { useState } from "react";
import type { Field } from "@siren-js/client";

export type SirenStringListInputProps = { field: Field };

export function SirenStringListInput({ field }: SirenStringListInputProps) {
  const [values, setValues] = useState(() =>
    Array.isArray(field.value) && field.value.every((value) => typeof value === "string") ? field.value : [""],
  );

  return (
    <div>
      <input name={field.name} type="hidden" value="" />
      {values.map((value, index) => (
        <div key={`${field.name}-${index}`}>
          <input
            name={field.name}
            onChange={(event) => setValues(values.map((item, itemIndex) => (itemIndex === index ? event.target.value : item)))}
            type="text"
            value={value}
          />
          <button onClick={() => setValues(values.filter((_, itemIndex) => itemIndex !== index))} type="button">
            Remove
          </button>
        </div>
      ))}
      <button onClick={() => setValues([...values, ""])} type="button">
        Add
      </button>
    </div>
  );
}
