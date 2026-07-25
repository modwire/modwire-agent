import type { SirenLink } from "siren-parser";

function resourcePath(url: string): string {
  const parsed = new URL(url, window.location.origin);
  return `${parsed.pathname}${parsed.search}`;
}

export function linkLabel(link: SirenLink): string {
  return link.title ?? resourcePath(link.href);
}
