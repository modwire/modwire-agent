import type { Link, Target } from "@siren-js/client";
import { AppShell, Group, Text } from "@mantine/core";
import { Navigation } from "./Navigation";

export type AppHeaderProps = {
  links: Link[];
  onFollow: (target: Target) => void;
  target: Target;
};

export function AppHeader({ links, onFollow, target }: AppHeaderProps) {
  return (
    <AppShell.Header>
      <Group h="100%" justify="space-between" px="md">
        <Text fw={700}>Modwire</Text>
        <Navigation links={links} onFollow={onFollow} target={target} />
      </Group>
    </AppShell.Header>
  );
}
