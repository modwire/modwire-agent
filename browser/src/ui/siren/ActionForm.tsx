import type { Action } from "@siren-js/client";

export type ActionFormProps = {
  action: Action;
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function ActionForm({ action, onSubmit }: ActionFormProps) {
  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit(action, Object.fromEntries(new FormData(event.currentTarget)));
      }}
    >
      <fieldset>
        <legend>{action.title}</legend>
        {action.fields.map((field) => (
          <label key={field.name}>
            {field.title}
            <input
              defaultValue={String(field.value)}
              name={field.name}
              type={field.type}
            />
          </label>
        ))}
        <button type="submit">{action.title}</button>
      </fieldset>
    </form>
  );
}
