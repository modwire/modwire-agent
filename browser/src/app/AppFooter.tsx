import { AppShell, Group, Text } from "@mantine/core";

export type AppFooterProps = Record<string, never>;

export function AppFooter(_: AppFooterProps) {
  return (
    <AppShell.Footer>
      <Group h="100%" px="md">
        <Text c="dimmed" size="sm">
          Enclosure
        </Text>
      </Group>
    </AppShell.Footer>
  );
}
