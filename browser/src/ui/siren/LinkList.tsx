import type { Link, Target } from "@siren-js/client";

export type LinkListProps = {
  links: Link[];
  onFollow: (target: Target) => void;
};

export function LinkList({ links, onFollow }: LinkListProps) {
  const displayedLinks = links.filter((link) => !link.rel.includes("self"));

  if (!displayedLinks.length) {
    return null;
  }

  return (
    <nav aria-label="Resource links">
      <ul>
        {displayedLinks.map((link) => (
          <li key={`${link.rel.join("-")}-${link.href}`}>
            <button onClick={() => onFollow(link)} type="button">
              {link.title}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
}
