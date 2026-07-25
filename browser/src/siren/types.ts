export type SirenProperty = boolean | null | number | string | SirenProperty[] | { [key: string]: SirenProperty };

export type SirenFieldDocument = {
  class?: string[];
  name: string;
  title?: string;
  type?: string;
  value?: unknown;
};

export type SirenActionDocument = {
  class?: string[];
  fields?: SirenFieldDocument[];
  href: string;
  method?: string;
  name: string;
  title?: string;
  type?: string;
};

export type SirenLinkDocument = {
  class?: string[];
  href: string;
  rel: string[];
  title?: string;
  type?: string;
};

export type SirenEntityDocument = {
  actions?: SirenActionDocument[];
  class?: string[];
  entities?: Array<SirenEntityDocument | SirenLinkDocument>;
  links?: SirenLinkDocument[];
  properties?: Record<string, SirenProperty>;
  rel?: string[];
  title?: string;
  type?: string;
};

export type SirenDocument = SirenEntityDocument;
