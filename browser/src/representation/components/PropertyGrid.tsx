import { Paper, SimpleGrid, Stack, Text } from "@mantine/core";
import { PropertyValue } from "./PropertyValue";

type PropertyGridProps = {
  properties: Record<string, unknown> | undefined;
};

export function PropertyGrid({ properties }: PropertyGridProps) {
  const entries = Object.entries(properties ?? {});

  if (!entries.length) {
    return null;
  }

  return (
    <SimpleGrid cols={{ base: 1, sm: 2 }}>
      {entries.map(([name, value]) => (
        <Paper key={name} p="md" withBorder>
          <Stack gap="xs">
            <Text fw={600}>{name}</Text>
            <PropertyValue value={value} />
          </Stack>
        </Paper>
      ))}
    </SimpleGrid>
  );
}
