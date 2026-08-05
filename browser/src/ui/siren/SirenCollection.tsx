import { Paper, Stack, Title } from "@mantine/core";
import type { Action, Entity, Target } from "@siren-js/client";
import { SirenCollectionItem } from "./SirenCollectionItem";
import { SirenActions } from "./SirenActions";
import { collectionLabel, itemTitle } from "./SirenLabels";

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
  const label = collectionLabel(entity);
  const titleCounts = new Map<string, number>();
  entity.entities.forEach((item) => {
    const itemLabel = itemTitle(item);
    if (itemLabel)
      titleCounts.set(itemLabel, (titleCounts.get(itemLabel) ?? 0) + 1);
  });

  return (
    <Paper component="section" aria-label={label} p="md" shadow="xs">
      <Stack>
        <Title order={1}>{label}</Title>
        <ul>
          {entity.entities.map((item, index) => (
            <li key={`${item.rel.join("-")}-${index}`}>
              <SirenCollectionItem
                ambiguousTitle={
                  (titleCounts.get(itemTitle(item) ?? "") ?? 0) > 1
                }
                index={index}
                item={item}
                onFollow={onFollow}
              />
            </li>
          ))}
        </ul>
        <SirenActions actions={entity.actions} onSubmit={onSubmit} />
      </Stack>
    </Paper>
  );
}
