import type { Action, Entity, Target } from "@siren-js/client";
import { Paper, Stack, Title } from "@mantine/core";
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
    <Paper component="section" aria-label={entity.title} p="md" shadow="xs">
      <Stack>
      <Title order={1}>{entity.title}</Title>
      <ul>
        {entity.entities.map((item, index) => (
          <li key={`${item.rel.join("-")}-${index}`}>
            <CollectionItem item={item} onFollow={onFollow} />
          </li>
        ))}
      </ul>
      <LinkList links={entity.links} onFollow={onFollow} />
      <ActionList actions={entity.actions} onSubmit={onSubmit} />
      </Stack>
    </Paper>
  );
}
