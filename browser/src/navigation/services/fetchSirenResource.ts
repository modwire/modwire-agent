import { Entity, type SirenEntity } from "siren-parser";
import { normalizeResourceUrl } from "../functions/resourceUrl";

export type SirenResource = {
  entity: SirenEntity;
  url: string;
};

function errorDetail(entity: SirenEntity, statusText: string): string {
  const detail = entity.properties?.detail;
  return typeof detail === "string" && detail ? detail : statusText;
}

export async function fetchSirenResource(value: string, signal: AbortSignal): Promise<SirenResource> {
  const url = normalizeResourceUrl(value);
  const response = await fetch(url, {
    headers: { Accept: "application/vnd.siren+json, application/json" },
    signal,
  });
  const contentType = response.headers.get("content-type") ?? "";

  if (!contentType.includes("json")) {
    throw new TypeError(response.statusText);
  }

  const document: unknown = await response.json();
  const entity = Entity(document as object);

  if (!response.ok) {
    throw new Error(errorDetail(entity, response.statusText));
  }

  return {
    entity,
    url: response.url ? normalizeResourceUrl(response.url) : url,
  };
}
