import type { Action, Entity, Target } from "@siren-js/client";
import { EntityDispatcher } from "./EntityDispatcher";

export type SirenBrowserProps = {
  entity: Entity | null;
  isLoading: boolean;
  onFollow: (target: Target) => void;
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function SirenBrowser({ entity, isLoading, onFollow, onSubmit }: SirenBrowserProps) {
  if (isLoading) {
    return <p role="status">Loading resource…</p>;
  }

  if (!entity) {
    return <p>No resource selected.</p>;
  }

  return <EntityDispatcher entity={entity} onFollow={onFollow} onSubmit={onSubmit} />;
}
