import { Paper, Stack, Title } from "@mantine/core";
import type { Action, Entity, Target } from "@siren-js/client";
import { sirenRegistry } from "./SirenRegistry";
import { SirenActions } from "./SirenActions";
import { SirenCollection } from "./SirenCollection";
import { SirenProperties } from "./SirenProperties";

export type SirenEntityProps = {
  entity: Entity;
  onFollow: (target: Target) => void;
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function SirenEntity({ entity, onFollow, onSubmit }: SirenEntityProps) {
  const EntityComponent = entity.class
    .map((className) => sirenRegistry.entities.get(className))
    .find(Boolean);

  if (EntityComponent) {
    return (
      <EntityComponent
        entity={entity}
        onFollow={onFollow}
        onSubmit={onSubmit}
      />
    );
  }

  if (entity.class.includes("collection")) {
    return (
      <SirenCollection
        entity={entity}
        onFollow={onFollow}
        onSubmit={onSubmit}
      />
    );
  }

  return (
    <Paper component="article" aria-label={entity.title} p="md" shadow="xs">
      <Stack>
        <Title order={1}>{entity.title}</Title>
        <SirenProperties entity={entity} />
        <SirenActions actions={entity.actions} onSubmit={onSubmit} />
      </Stack>
    </Paper>
  );
}
