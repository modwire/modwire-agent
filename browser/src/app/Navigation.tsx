import type { Link, Target } from "@siren-js/client";
import { SirenNavigation } from "../ui/siren/SirenNavigation";

export type NavigationProps = {
  links: Link[];
  onFollow: (target: Target) => void;
  target: Target;
};

export function Navigation({ links, onFollow, target }: NavigationProps) {
  return (
    <SirenNavigation activeTarget={target} links={links} onFollow={onFollow} />
  );
}
