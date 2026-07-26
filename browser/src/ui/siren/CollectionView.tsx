import type { Action, Entity, Target } from "@siren-js/client";
import { ActionList } from "./ActionList";
import { CollectionItem } from "./CollectionItem";
import { LinkList } from "./LinkList";

export type CollectionViewProps = {
  entity: Entity;
  onFollow: (target: Target) => void;
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function CollectionView({ entity, onFollow, onSubmit }: CollectionViewProps) {
  return (
    <section aria-label={entity.title}>
      <h1>{entity.title}</h1>
      <ul>
        {entity.entities.map((item, index) => (
          <li key={`${item.rel.join("-")}-${index}`}>
            <CollectionItem item={item} onFollow={onFollow} />
          </li>
        ))}
      </ul>
      <LinkList links={entity.links} onFollow={onFollow} />
      <ActionList actions={entity.actions} onSubmit={onSubmit} />
    </section>
  );
}
