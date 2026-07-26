import type { Action } from "@siren-js/client";
import { Stack } from "@mantine/core";
import { ActionForm } from "./ActionForm";

export type ActionListProps = {
  actions: Action[];
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function ActionList({ actions, onSubmit }: ActionListProps) {
  const displayedActions = actions.filter((action) => action.method !== "GET" || action.fields.length > 0);

  if (!displayedActions.length) {
    return null;
  }

  return (
    <section aria-label="Resource actions">
      <Stack>
        {displayedActions.map((action) => (
          <ActionForm action={action} key={`${action.method}-${action.href}-${action.name}`} onSubmit={onSubmit} />
        ))}
      </Stack>
    </section>
  );
}
