import type { SirenAction } from "../../client/SirenAction";
import type { SirenEntity } from "../../client/SirenEntity";
import type { SirenLink } from "../../client/SirenLink";
import { ActionList } from "./ActionList";
import { LinkList } from "./LinkList";

export type EntityViewProps = {
  entity: SirenEntity;
  onFollow: (link: SirenLink) => void;
  onSubmit: (action: SirenAction, values: Record<string, unknown>) => void;
};

export function EntityView({ entity, onFollow, onSubmit }: EntityViewProps) {
  return (
    <article aria-label={entity.title}>
      <h1>{entity.title}</h1>
      <dl>
        {Object.entries(entity.properties).map(([name, value]) => (
          <div key={name}>
            <dt>{name}</dt>
            <dd>{typeof value === "string" ? value : JSON.stringify(value)}</dd>
          </div>
        ))}
      </dl>
      <LinkList links={entity.links} onFollow={onFollow} />
      <ActionList actions={entity.actions} onSubmit={onSubmit} />
    </article>
  );
}
