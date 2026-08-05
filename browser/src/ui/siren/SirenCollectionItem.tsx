import { EmbeddedLink, type SubEntity, type Target } from "@siren-js/client";
import { Anchor } from "@mantine/core";
import { collectionItemLabel } from "./SirenLabels";

export type SirenCollectionItemProps = {
  ambiguousTitle: boolean;
  index: number;
  item: SubEntity;
  onFollow: (target: Target) => void;
};

export function SirenCollectionItem({
  ambiguousTitle,
  index,
  item,
  onFollow,
}: SirenCollectionItemProps) {
  const target =
    item instanceof EmbeddedLink
      ? item
      : item.links.find((link) => link.rel.includes("self"));
  const label = collectionItemLabel(item, index, ambiguousTitle);

  if (!target) {
    return <span>{label}</span>;
  }

  return (
    <Anchor
      href={`#${target.href}`}
      onClick={(event) => {
        event.preventDefault();
        onFollow(target);
      }}
    >
      {label}
    </Anchor>
  );
}
