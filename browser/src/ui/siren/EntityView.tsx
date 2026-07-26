import type { Action, Entity, Target } from "@siren-js/client";
import { Paper, SimpleGrid, Stack, Text, Title } from "@mantine/core";
import { ActionList } from "./ActionList";
import { LinkList } from "./LinkList";

export type EntityViewProps = {
  entity: Entity;
  onFollow: (target: Target) => void;
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function EntityView({ entity, onFollow, onSubmit }: EntityViewProps) {
  return (
    <Paper component="article" aria-label={entity.title} p="md" shadow="xs">
      <Stack>
      <Title order={1}>{entity.title}</Title>
      <SimpleGrid cols={{ base: 1, sm: 2 }} component="dl">
        {Object.entries(entity.properties).map(([name, value]) => (
          <div key={name}>
            <Text component="dt" fw={600}>{name}</Text>
            <Text component="dd">{typeof value === "string" ? value : JSON.stringify(value)}</Text>
          </div>
        ))}
      </SimpleGrid>
      <LinkList links={entity.links} onFollow={onFollow} />
      <ActionList actions={entity.actions} onSubmit={onSubmit} />
      </Stack>
    </Paper>
  );
}
