import type { SirenAction } from "../../client/SirenAction";
import type { SirenEntity } from "../../client/SirenEntity";
import type { SirenLink } from "../../client/SirenLink";
import { ActionList } from "./ActionList";
import { LinkList } from "./LinkList";

export type CollectionViewProps = {
  entity: SirenEntity;
  onFollow: (link: SirenLink) => void;
  onSubmit: (action: SirenAction, values: Record<string, unknown>) => void;
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
