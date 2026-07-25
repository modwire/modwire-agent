import { AppShell, Stack } from "@mantine/core";
import { BrowserBreadcrumbs } from "../../navigation/components/BrowserBreadcrumbs";
import { NavigationError } from "../../navigation/components/NavigationError";
import type { SirenResource } from "../../navigation/services/fetchSirenResource";
import { ResourcePage } from "../../representation/components/ResourcePage";

type VisitedResource = {
  label: string;
  url: string;
};

type BrowserMainProps = {
  error: Error | null;
  isLoading: boolean;
  onNavigate: (url: string) => void;
  onRetry: () => void;
  resource: SirenResource | null;
  resources: VisitedResource[];
};

export function BrowserMain({ error, isLoading, onNavigate, onRetry, resource, resources }: BrowserMainProps) {
  return (
    <AppShell.Main>
      <Stack gap="md">
        <BrowserBreadcrumbs onNavigate={onNavigate} resources={resources} />
        <NavigationError error={error} onRetry={onRetry} />
        <ResourcePage isLoading={isLoading} onNavigate={onNavigate} resource={resource} />
      </Stack>
    </AppShell.Main>
  );
}
