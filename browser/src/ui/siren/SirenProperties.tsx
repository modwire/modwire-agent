import { Box, SimpleGrid, Text } from "@mantine/core";
import type { Entity } from "@siren-js/client";
import { SirenValue } from "./SirenValue";

export type SirenPropertiesProps = { entity: Entity };

export function SirenProperties({ entity }: SirenPropertiesProps) {
  return (
    <SimpleGrid cols={{ base: 1, sm: 2 }} component="dl">
      {Object.entries(entity.properties).map(([name, value]) => (
        <div key={name}>
          <Text component="dt" fw={600}>
            {name}
          </Text>
          <Box component="dd">
            <SirenValue value={value} />
          </Box>
        </div>
      ))}
    </SimpleGrid>
  );
}
