import { useState } from "react";
import type { Action } from "@siren-js/client";

export type ActionFormProps = {
  action: Action;
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function ActionForm({ action, onSubmit }: ActionFormProps) {
  const [values, setValues] = useState<Record<string, unknown>>(() =>
    Object.fromEntries(action.fields.map((field) => [field.name, field.value ?? ""])),
  );

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit(action, values);
      }}
    >
      <fieldset>
        <legend>{action.title ?? action.name}</legend>
        {action.fields.map((field) => (
          <label key={field.name}>
            {field.title ?? field.name}
            <input
              name={field.name}
              onChange={(event) => setValues((current) => ({ ...current, [field.name]: event.currentTarget.value }))}
              type={field.type}
              value={String(values[field.name] ?? "")}
            />
          </label>
        ))}
        <button type="submit">{action.title ?? action.name}</button>
      </fieldset>
    </form>
  );
}
