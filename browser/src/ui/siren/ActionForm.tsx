import type { Action } from "@siren-js/client";
import { SirenInput } from "./inputs/SirenInput";

export type ActionFormProps = {
  action: Action;
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function ActionForm({ action, onSubmit }: ActionFormProps) {
  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        const formData = new FormData(event.currentTarget);
        onSubmit(
          action,
          Object.fromEntries(
            [...new Set(formData.keys())].map((name) => {
              const values = formData.getAll(name);
              const controls = event.currentTarget.elements.namedItem(name);
              const control = controls instanceof RadioNodeList ? controls.item(0) : controls;
              if (control instanceof HTMLElement && control.dataset.sirenType === "object") {
                return [name, JSON.parse(String(values[0]))];
              }
              return [name, values.length > 1 ? values.filter((value) => value !== "") : values[0]];
            }),
          ),
        );
      }}
    >
      <fieldset>
        <legend>{action.title}</legend>
        {action.fields.map((field) => (
          <label key={field.name}>
            {field.title ?? field.name}
            <SirenInput field={field} />
          </label>
        ))}
        <button type="submit">{action.title}</button>
      </fieldset>
    </form>
  );
}
