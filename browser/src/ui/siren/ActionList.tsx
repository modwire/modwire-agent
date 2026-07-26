import type { Action } from "@siren-js/client";
import { ActionForm } from "./ActionForm";

export type ActionListProps = {
  actions: Action[];
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function ActionList({ actions, onSubmit }: ActionListProps) {
  if (!actions.length) {
    return null;
  }

  return (
    <section aria-label="Resource actions">
      {actions.map((action) => (
        <ActionForm action={action} key={`${action.method}-${action.href}-${action.name}`} onSubmit={onSubmit} />
      ))}
    </section>
  );
}
