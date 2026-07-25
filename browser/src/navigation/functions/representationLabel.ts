import type { SirenEntity, SirenLink } from "siren-parser";

function resourcePath(url: string): string {
  const parsed = new URL(url, window.location.origin);
  return `${parsed.pathname}${parsed.search}`;
}

export function linkLabel(link: SirenLink): string {
  return link.title ?? resourcePath(link.href);
}

export function representationLabel(entity: SirenEntity, url: string): string {
  if (entity.title) {
    return entity.title;
  }

  const title = entity.properties?.title;

  if (typeof title === "string" && title) {
    return title;
  }

  return resourcePath(url);
}
