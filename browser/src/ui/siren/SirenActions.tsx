import { Stack } from "@mantine/core";
import type { Action } from "@siren-js/client";
import { sirenRegistry } from "./SirenRegistry";
import { SirenActionForm } from "./SirenActionForm";

export type SirenActionsProps = {
  actions: Action[];
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function SirenActions({ actions, onSubmit }: SirenActionsProps) {
  const displayedActions = actions.filter(
    (action) => action.method !== "GET" || action.fields.length > 0,
  );

  if (!displayedActions.length) return null;

  return (
    <Stack>
      {displayedActions.map((action) => {
        const ActionForm =
          sirenRegistry.actions.get(action.name) ?? SirenActionForm;
        return (
          <ActionForm
            action={action}
            key={`${action.method}-${action.href}-${action.name}`}
            onSubmit={onSubmit}
          />
        );
      })}
    </Stack>
  );
}
