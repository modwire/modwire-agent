import type { Link, Target } from "@siren-js/client";
import { Button, Group } from "@mantine/core";

export type LinkListProps = {
  activeTarget?: Target;
  links: Link[];
  onFollow: (target: Target) => void;
};

export function LinkList({ activeTarget, links, onFollow }: LinkListProps) {
  const displayedLinks = links.filter((link) => !link.rel.includes("self"));
  const activeUrl = activeTarget == null ? null : new URL(activeTarget.toString(), window.location.origin);

  if (!displayedLinks.length) {
    return null;
  }

  return (
    <nav aria-label="Resource links">
      <Group gap="xs">
        {displayedLinks.map((link) => {
          const linkUrl = new URL(link.href.toString(), window.location.origin);

          return (
            <Button
              component="a"
              href={`#${link.href}`}
              key={`${link.rel.join("-")}-${link.href}`}
              onClick={(event) => {
                event.preventDefault();
                onFollow(link);
              }}
              variant={activeUrl?.pathname === linkUrl.pathname && activeUrl.search === linkUrl.search ? "filled" : "subtle"}
            >
              {link.title}
            </Button>
          );
        })}
      </Group>
    </nav>
  );
}
