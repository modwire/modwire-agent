import { EmbeddedLink, type SubEntity, type Target } from "@siren-js/client";

export type CollectionItemProps = {
  item: SubEntity;
  onFollow: (target: Target) => void;
};

export function CollectionItem({ item, onFollow }: CollectionItemProps) {
  const target = item instanceof EmbeddedLink ? item : item.links.find((link) => link.rel.includes("self"));
  const label = (item.title ?? item.class.join(" ")) || "Resource";

  if (!target) {
    return <span>{label}</span>;
  }

  return (
    <a
      href={target.href}
      onClick={(event) => {
        event.preventDefault();
        onFollow(target);
      }}
    >
      {label}
    </a>
  );
}
