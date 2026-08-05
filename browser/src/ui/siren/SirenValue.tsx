import { Box, SimpleGrid, Text } from "@mantine/core";

export type SirenValueProps = { value: unknown };

export function SirenValue({ value }: SirenValueProps) {
  if (value === null) return <Text c="dimmed">None</Text>;
  if (typeof value === "boolean") return <Text>{value ? "Yes" : "No"}</Text>;
  if (typeof value === "string" || typeof value === "number")
    return <Text>{String(value)}</Text>;
  if (Array.isArray(value)) {
    return (
      <Box component="ol" m={0} pl="xl">
        {value.map((item, index) => (
          <li key={index}>
            <SirenValue value={item} />
          </li>
        ))}
      </Box>
    );
  }
  if (typeof value === "object") {
    return (
      <SimpleGrid cols={{ base: 1, sm: 2 }} component="dl">
        {Object.entries(value).map(([name, item]) => (
          <div key={name}>
            <Text component="dt" fw={600}>
              {name}
            </Text>
            <Box component="dd">
              <SirenValue value={item} />
            </Box>
          </div>
        ))}
      </SimpleGrid>
    );
  }
  return <Text c="dimmed">None</Text>;
}
