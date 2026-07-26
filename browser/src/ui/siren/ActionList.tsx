import type { SirenAction } from "../../client/SirenAction";
import { ActionForm } from "./ActionForm";

export type ActionListProps = {
  actions: SirenAction[];
  onSubmit: (action: SirenAction, values: Record<string, unknown>) => void;
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
