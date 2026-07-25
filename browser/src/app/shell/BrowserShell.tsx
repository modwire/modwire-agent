import { AppShell } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { BrowserAside } from "./BrowserAside";
import { BrowserHeader } from "./BrowserHeader";
import { BrowserMain } from "./BrowserMain";
import { BrowserNavbar } from "./BrowserNavbar";

export function BrowserShell() {
  const [navigationOpened, { toggle: toggleNavigation }] = useDisclosure(false);

  return (
    <AppShell
      aside={{ width: 320, breakpoint: "lg", collapsed: { mobile: true, desktop: true } }}
      header={{ height: 60 }}
      navbar={{
        width: 300,
        breakpoint: "sm",
        collapsed: { mobile: !navigationOpened, desktop: true },
      }}
      padding="md"
    >
      <AppShell.Header>
        <BrowserHeader navigationOpened={navigationOpened} onNavigationToggle={toggleNavigation} />
      </AppShell.Header>
      <AppShell.Navbar>
        <BrowserNavbar />
      </AppShell.Navbar>
      <AppShell.Aside>
        <BrowserAside />
      </AppShell.Aside>
      <BrowserMain />
    </AppShell>
  );
}
