import { AppShell } from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";
import { useSirenNavigation } from "../../navigation/hooks/useSirenNavigation";
import { BrowserAside } from "./BrowserAside";
import { BrowserHeader } from "./BrowserHeader";
import { BrowserMain } from "./BrowserMain";
import { BrowserNavbar } from "./BrowserNavbar";

export function BrowserShell() {
  const [navigationOpened, { toggle: toggleNavigation }] = useDisclosure(false);
  const navigation = useSirenNavigation();

  return (
    <AppShell
      aside={{ width: 320, breakpoint: "lg", collapsed: { mobile: true, desktop: true } }}
      header={{ height: 60 }}
      navbar={{
        width: 300,
        breakpoint: "sm",
        collapsed: { mobile: !navigationOpened },
      }}
      padding="md"
    >
      <AppShell.Header>
        <BrowserHeader
          canGoBack={navigation.canGoBack}
          canGoForward={navigation.canGoForward}
          isLoading={navigation.isLoading}
          navigationOpened={navigationOpened}
          onBack={navigation.goBack}
          onForward={navigation.goForward}
          onNavigate={navigation.navigate}
          onNavigationToggle={toggleNavigation}
          resourceUrl={navigation.resourceUrl}
        />
      </AppShell.Header>
      <AppShell.Navbar aria-label="Root navigation">
        <BrowserNavbar
          isLoading={navigation.isLoading}
          links={navigation.links}
          onNavigate={navigation.navigate}
          resourceUrl={navigation.resourceUrl}
        />
      </AppShell.Navbar>
      <AppShell.Aside>
        <BrowserAside />
      </AppShell.Aside>
      <BrowserMain
        error={navigation.error}
        isLoading={navigation.isLoading}
        onNavigate={navigation.navigate}
        onRetry={navigation.retry}
        resource={navigation.resource}
      />
    </AppShell>
  );
}
