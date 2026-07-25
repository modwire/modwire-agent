import type { SirenSubEntity } from "siren-parser";

export function resourceLabel(resource: SirenSubEntity): string | undefined {
  return resource.title;
}
