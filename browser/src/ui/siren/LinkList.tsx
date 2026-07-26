import type { SirenLink } from "../../client/SirenLink";

export type LinkListProps = {
  links: SirenLink[];
  onFollow: (link: SirenLink) => void;
};

export function LinkList({ links, onFollow }: LinkListProps) {
  if (!links.length) {
    return null;
  }

  return (
    <nav aria-label="Resource links">
      <ul>
        {links.map((link) => (
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
