import type { Action, Entity, Link } from "@siren-js/client";
import { ActionList } from "./ActionList";
import { LinkList } from "./LinkList";

export type CollectionViewProps = {
  entity: Entity;
  onFollow: (link: Link) => void;
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function CollectionView({ entity, onFollow, onSubmit }: CollectionViewProps) {
  return (
    <section aria-label={entity.title}>
      <h1>{entity.title}</h1>
      <ul>
        {entity.entities.map((item, index) => (
          <li key={`${item.rel.join("-")}-${index}`}>{item.title}</li>
        ))}
      </ul>
      <LinkList links={entity.links.filter((link) => !link.rel.includes("self"))} onFollow={onFollow} />
      <ActionList
        actions={entity.actions.filter((action) => action.method !== "GET" || action.fields.length > 0)}
        onSubmit={onSubmit}
      />
    </section>
  );
}
