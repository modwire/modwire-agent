import { Paper, Stack, Title } from "@mantine/core";
import type { Action, Entity, Target } from "@siren-js/client";
import { SirenCollectionItem } from "./SirenCollectionItem";
import { SirenActions } from "./SirenActions";

export type SirenCollectionProps = {
  entity: Entity;
  onFollow: (target: Target) => void;
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function SirenCollection({
  entity,
  onFollow,
  onSubmit,
}: SirenCollectionProps) {
  return (
    <Paper component="section" aria-label={entity.title} p="md" shadow="xs">
      <Stack>
        <Title order={1}>{entity.title}</Title>
        <ul>
          {entity.entities.map((item, index) => (
            <li key={`${item.rel.join("-")}-${index}`}>
              <SirenCollectionItem item={item} onFollow={onFollow} />
            </li>
          ))}
        </ul>
        <SirenActions actions={entity.actions} onSubmit={onSubmit} />
      </Stack>
    </Paper>
  );
}
