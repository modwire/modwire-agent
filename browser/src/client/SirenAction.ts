import type { SirenField } from "./SirenField";

export type SirenAction = {
  class: string[];
  fields: SirenField[];
  href: string;
  method: string;
  name: string;
  title: string;
  type: string;
};
