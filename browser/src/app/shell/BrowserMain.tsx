import { AppShell, Stack } from "@mantine/core";
import { NavigationError } from "../../navigation/components/NavigationError";
import type { SirenResource } from "../../siren/client";
import { ResourcePage } from "../../representation/components/ResourcePage";

type BrowserMainProps = {
  error: Error | null;
  isLoading: boolean;
  onNavigate: (url: string) => void;
  onRetry: () => void;
  resource: SirenResource | null;
};

export function BrowserMain({ error, isLoading, onNavigate, onRetry, resource }: BrowserMainProps) {
  return (
    <AppShell.Main>
      <Stack gap="md">
        <NavigationError error={error} onRetry={onRetry} />
        <ResourcePage isLoading={isLoading} onNavigate={onNavigate} resource={resource} />
      </Stack>
    </AppShell.Main>
  );
}
