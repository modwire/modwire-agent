declare module "siren-parser" {
  export interface SirenField {
    name: string;
    value?: unknown;
    class?: string[];
    type?: string;
    title?: string;
    min?: number;
    max?: number;
  }

  export interface SirenAction {
    name: string;
    href: string;
    class?: string[];
    method?: string;
    title?: string;
    type?: string;
    fields?: SirenField[];
    hasFieldByName(name: string | RegExp): boolean;
    getFieldByName(name: string | RegExp): SirenField | undefined;
  }

  export interface SirenLink {
    rel: string[];
    href: string;
    class?: string[];
    title?: string;
    type?: string;
    hasClass(name: string): boolean;
  }

  export interface SirenEntity {
    rel?: string[];
    title?: string;
    type?: string;
    properties?: Record<string, unknown>;
    class?: string[];
    actions?: SirenAction[];
    links?: SirenLink[];
    entities?: SirenEntity[];
    hasActionByName(name: string | RegExp): boolean;
    hasClass(name: string | RegExp): boolean;
    hasSubEntityByRel(rel: string | RegExp): boolean;
    hasLinkByRel(rel: string | RegExp): boolean;
    hasProperty(property: string): boolean;
    getActionByName(name: string | RegExp): SirenAction | undefined;
    getLinkByRel(rel: string | RegExp): SirenLink | undefined;
    getLinksByRel(rel: string | RegExp): SirenLink[];
    getSubEntityByRel(rel: string | RegExp): SirenEntity | undefined;
    getSubEntitiesByRel(rel: string | RegExp): SirenEntity[];
  }

  export function Entity(siren: string | object): SirenEntity;
}
