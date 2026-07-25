import { ActionIcon, Box, Burger, Group, Text, TextInput, ThemeIcon } from "@mantine/core";
import { IconArrowLeft, IconArrowRight, IconBolt, IconExternalLink } from "@tabler/icons-react";
import { useEffect, useState } from "react";

type BrowserHeaderProps = {
  canGoBack: boolean;
  canGoForward: boolean;
  isLoading: boolean;
  navigationOpened: boolean;
  onBack: () => void;
  onForward: () => void;
  onNavigate: (url: string) => void;
  onNavigationToggle: () => void;
  resourceUrl: string;
};

export function BrowserHeader({
  canGoBack,
  canGoForward,
  isLoading,
  navigationOpened,
  onBack,
  onForward,
  onNavigate,
  onNavigationToggle,
  resourceUrl,
}: BrowserHeaderProps) {
  const [address, setAddress] = useState(resourceUrl);

  useEffect(() => setAddress(resourceUrl), [resourceUrl]);

  return (
    <Group h="100%" px="md" wrap="nowrap">
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
      <Box
        component="form"
        flex={1}
        maw={720}
        onSubmit={(event) => {
          event.preventDefault();
          onNavigate(address);
        }}
      >
        <TextInput
          aria-label="Resource address"
          onChange={(event) => setAddress(event.currentTarget.value)}
          rightSection={
            <ActionIcon aria-label="Open resource" loading={isLoading} type="submit" variant="subtle">
              <IconExternalLink size={18} />
            </ActionIcon>
          }
          value={address}
        />
      </Box>
      <Group gap={4} wrap="nowrap">
        <ActionIcon aria-label="Back" disabled={!canGoBack} onClick={onBack} variant="subtle">
          <IconArrowLeft size={18} />
        </ActionIcon>
        <ActionIcon aria-label="Forward" disabled={!canGoForward} onClick={onForward} variant="subtle">
          <IconArrowRight size={18} />
        </ActionIcon>
      </Group>
    </Group>
  );
}
