import type { SirenAction } from "../../client/SirenAction";
import type { SirenEntity } from "../../client/SirenEntity";
import type { SirenLink } from "../../client/SirenLink";
import { CollectionView } from "./CollectionView";
import { EntityView } from "./EntityView";

export type EntityDispatcherProps = {
  entity: SirenEntity;
  onFollow: (link: SirenLink) => void;
  onSubmit: (action: SirenAction, values: Record<string, unknown>) => void;
};

export function EntityDispatcher({ entity, onFollow, onSubmit }: EntityDispatcherProps) {
  if (entity.class.includes("collection")) {
    return <CollectionView entity={entity} onFollow={onFollow} onSubmit={onSubmit} />;
  }

  return <EntityView entity={entity} onFollow={onFollow} onSubmit={onSubmit} />;
}
