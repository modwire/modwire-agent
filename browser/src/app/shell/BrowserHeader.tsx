import { Burger, Group, Text, ThemeIcon } from "@mantine/core";
import { IconBolt } from "@tabler/icons-react";

type BrowserHeaderProps = {
  navigationOpened: boolean;
  onNavigationToggle: () => void;
};

export function BrowserHeader({ navigationOpened, onNavigationToggle }: BrowserHeaderProps) {
  return (
    <Group h="100%" px="md">
      <Burger
        aria-label="Toggle navigation"
        hiddenFrom="sm"
        opened={navigationOpened}
        onClick={onNavigationToggle}
        size="sm"
      />
      <Group gap="xs">
        <ThemeIcon radius="xl" size="lg" variant="light">
          <IconBolt size={18} stroke={1.75} />
        </ThemeIcon>
        <Text fw={700}>Modwire</Text>
      </Group>
    </Group>
  );
}
