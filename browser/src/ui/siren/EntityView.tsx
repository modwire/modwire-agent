import type { Action, Entity, Link } from "@siren-js/client";
import { ActionList } from "./ActionList";
import { LinkList } from "./LinkList";

export type EntityViewProps = {
  entity: Entity;
  onFollow: (link: Link) => void;
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function EntityView({ entity, onFollow, onSubmit }: EntityViewProps) {
  return (
    <article aria-label={entity.title ?? "Resource"}>
      <h1>{entity.title ?? "Resource"}</h1>
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
