import { NavLink, Stack } from "@mantine/core";
import type { SirenLink } from "siren-parser";
import { linkLabel } from "../../navigation/functions/representationLabel";

type RepresentationLinksProps = {
  links: SirenLink[] | undefined;
  onNavigate: (url: string) => void;
};

export function RepresentationLinks({ links, onNavigate }: RepresentationLinksProps) {
  if (!links?.length) {
    return null;
  }

  return (
    <Stack gap="xs">
      {links.map((link) => (
        <NavLink
          component="button"
          description={link.rel.join(" ")}
          key={link.href}
          label={linkLabel(link)}
          onClick={() => onNavigate(link.href)}
          type="button"
        />
      ))}
    </Stack>
  );
}
