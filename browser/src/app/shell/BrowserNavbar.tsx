import { AppShell, NavLink, Stack } from "@mantine/core";
import type { SirenLink } from "siren-parser";
import { linkLabel } from "../../navigation/functions/representationLabel";

type BrowserNavbarProps = {
  isLoading: boolean;
  links: SirenLink[];
  onNavigate: (url: string) => void;
  resourceUrl: string;
};

export function BrowserNavbar({ isLoading, links, onNavigate, resourceUrl }: BrowserNavbarProps) {
  return (
    <AppShell.Section grow p="md">
      <Stack data-testid="root-navigation" gap="xs">
        {links.map((link) => (
          <NavLink
            active={link.href === resourceUrl}
            component="button"
            description={link.rel.join(" ")}
            disabled={isLoading}
            key={link.href}
            label={linkLabel(link)}
            onClick={() => onNavigate(link.href)}
            type="button"
          />
        ))}
      </Stack>
    </AppShell.Section>
  );
}
