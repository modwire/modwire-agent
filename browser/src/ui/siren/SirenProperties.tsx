import { SimpleGrid, Text } from "@mantine/core";
import type { Entity } from "@siren-js/client";

export type SirenPropertiesProps = { entity: Entity };

export function SirenProperties({ entity }: SirenPropertiesProps) {
  return (
    <SimpleGrid cols={{ base: 1, sm: 2 }} component="dl">
      {Object.entries(entity.properties).map(([name, value]) => (
        <div key={name}>
          <Text component="dt" fw={600}>
            {name}
          </Text>
          <Text component="dd">
            {typeof value === "string" ? value : JSON.stringify(value)}
          </Text>
        </div>
      ))}
    </SimpleGrid>
  );
}
