import type { SirenAction } from "./SirenAction";
import type { SirenLink } from "./SirenLink";
import type { SirenSubEntity } from "./SirenSubEntity";

export type SirenEntity = {
  actions: SirenAction[];
  class: string[];
  entities: SirenSubEntity[];
  links: SirenLink[];
  properties: Record<string, unknown>;
  title: string;
};
