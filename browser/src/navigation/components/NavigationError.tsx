import { ActionIcon, Alert, Group, Text } from "@mantine/core";
import { IconRefresh } from "@tabler/icons-react";

type NavigationErrorProps = {
  error: Error | null;
  onRetry: () => void;
};

export function NavigationError({ error, onRetry }: NavigationErrorProps) {
  if (!error) {
    return null;
  }

  return (
    <Alert color="red">
      <Group justify="space-between" wrap="nowrap">
        <Text>{error.message}</Text>
        <ActionIcon aria-label="Retry" color="red" onClick={onRetry} variant="subtle">
          <IconRefresh size={18} />
        </ActionIcon>
      </Group>
    </Alert>
  );
}
