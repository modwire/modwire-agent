import type { ReactElement } from "react";
import { AppProviders } from "./providers/AppProviders";
import { BrowserShell } from "./shell/BrowserShell";

export function App(): ReactElement {
  return (
    <AppProviders>
      <BrowserShell />
    </AppProviders>
  );
}
