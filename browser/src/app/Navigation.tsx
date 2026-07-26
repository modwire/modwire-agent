import type { Link, Target } from "@siren-js/client";
import { LinkList } from "../ui/siren/LinkList";

export type NavigationProps = {
  links: Link[];
  onFollow: (target: Target) => void;
  target: Target;
};

export function Navigation({ links, onFollow, target }: NavigationProps) {
  return <LinkList activeTarget={target} links={links} onFollow={onFollow} />;
}
