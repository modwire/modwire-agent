import { AppShell, Stack } from "@mantine/core";
import { BrowserBreadcrumbs } from "../../navigation/components/BrowserBreadcrumbs";
import { NavigationError } from "../../navigation/components/NavigationError";

type VisitedResource = {
  label: string;
  url: string;
};

type BrowserMainProps = {
  error: Error | null;
  onNavigate: (url: string) => void;
  onRetry: () => void;
  resources: VisitedResource[];
};

export function BrowserMain({ error, onNavigate, onRetry, resources }: BrowserMainProps) {
  return (
    <AppShell.Main>
      <Stack gap="md">
        <BrowserBreadcrumbs onNavigate={onNavigate} resources={resources} />
        <NavigationError error={error} onRetry={onRetry} />
      </Stack>
    </AppShell.Main>
  );
}
