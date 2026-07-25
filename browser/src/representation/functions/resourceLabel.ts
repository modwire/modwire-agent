import type { SirenEntity, SirenSubEntity } from "siren-parser";

function titleProperty(entity: SirenEntity): string | undefined {
  const title = entity.properties?.title;
  return typeof title === "string" && title ? title : undefined;
}

export function resourceLabel(resource: SirenSubEntity): string | undefined {
  if (resource.title) {
    return resource.title;
  }

  if ("properties" in resource) {
    return titleProperty(resource);
  }

  return undefined;
}
