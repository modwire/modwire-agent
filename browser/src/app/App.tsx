import { AppShell } from "@mantine/core";
import type { ReactElement } from "react";
import { AppProviders } from "./providers/AppProviders";

export function App(): ReactElement {
  return (
    <AppProviders>
      <AppShell padding="md">
        <AppShell.Main />
      </AppShell>
    </AppProviders>
  );
}
