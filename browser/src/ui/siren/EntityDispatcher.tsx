import type { Action, Entity, Target } from "@siren-js/client";
import { CollectionView } from "./CollectionView";
import { EntityView } from "./EntityView";

export type EntityDispatcherProps = {
  entity: Entity;
  onFollow: (target: Target) => void;
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function EntityDispatcher({ entity, onFollow, onSubmit }: EntityDispatcherProps) {
  if (entity.class.includes("collection")) {
    return <CollectionView entity={entity} onFollow={onFollow} onSubmit={onSubmit} />;
  }

  return <EntityView entity={entity} onFollow={onFollow} onSubmit={onSubmit} />;
}
