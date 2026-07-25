import { Entity, type SirenAction, type SirenEntity } from "siren-parser";
import type { SirenDocument } from "./types";
import { canonicalSirenUrl } from "./url";

export const SIREN_ACCEPT = "application/vnd.siren+json, application/json";

export type SirenResource = {
  document: SirenDocument;
  entity: SirenEntity;
  status: number;
  url: string;
};

export type SirenEmptyResponse = {
  kind: "empty";
  status: 204;
  url: string;
};

export type SirenRepresentationResponse = {
  kind: "representation";
  resource: SirenResource;
};

export type SirenResponse = SirenEmptyResponse | SirenRepresentationResponse;

export type SirenRequest = {
  body?: BodyInit | null;
  headers?: HeadersInit;
  method?: string;
  signal?: AbortSignal;
  url: string;
};

export type SirenActionRequest = {
  action: SirenAction;
  body?: BodyInit | null;
  headers?: HeadersInit;
  signal?: AbortSignal;
};

export class SirenResponseError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly url: string,
    readonly document?: SirenDocument,
  ) {
    super(message);
    this.name = "SirenResponseError";
  }
}

function responseMessage(entity: SirenEntity, fallback: string): string {
  const detail = entity.properties?.detail;
  return typeof detail === "string" && detail ? detail : fallback;
}

function isJson(response: Response): boolean {
  return (response.headers.get("content-type") ?? "").includes("json");
}

function canonicalResourceUrl(entity: SirenEntity, fallback: string): string {
  return canonicalSirenUrl(entity.getLinkByRel("self")?.href ?? fallback);
}

export async function requestSiren({ body, headers, method = "GET", signal, url: value }: SirenRequest): Promise<SirenResponse> {
  const url = canonicalSirenUrl(value);
  const requestHeaders = new Headers(headers);
  requestHeaders.set("Accept", requestHeaders.get("Accept") ?? SIREN_ACCEPT);
  const response = await fetch(url, { body, headers: requestHeaders, method, signal });

  if (response.status === 204) {
    return { kind: "empty", status: 204, url: response.url ? canonicalSirenUrl(response.url) : url };
  }

  if (!isJson(response)) {
    throw new SirenResponseError(`Expected a JSON response, received ${response.statusText || response.status}.`, response.status, url);
  }

  let document: SirenDocument;
  try {
    document = (await response.json()) as SirenDocument;
  } catch {
    throw new SirenResponseError("The response declared JSON but could not be parsed.", response.status, url);
  }

  let entity: SirenEntity;
  try {
    entity = Entity(document);
  } catch {
    throw new SirenResponseError("The JSON response is not a valid Siren representation.", response.status, url, document);
  }

  const resourceUrl = canonicalResourceUrl(entity, response.url ? canonicalSirenUrl(response.url) : url);
  if (!response.ok) {
    throw new SirenResponseError(responseMessage(entity, response.statusText || `Request failed with ${response.status}.`), response.status, resourceUrl, document);
  }

  return { kind: "representation", resource: { document, entity, status: response.status, url: resourceUrl } };
}

export async function fetchSirenResource(value: string, signal: AbortSignal): Promise<SirenResource> {
  const response = await requestSiren({ signal, url: value });
  if (response.kind === "empty") {
    throw new SirenResponseError("A resource request returned no representation.", response.status, response.url);
  }
  return response.resource;
}

export function executeSirenAction({ action, body, headers, signal }: SirenActionRequest): Promise<SirenResponse> {
  const actionHeaders = new Headers(headers);
  if (body && action.type && !actionHeaders.has("Content-Type")) {
    actionHeaders.set("Content-Type", action.type);
  }
  return requestSiren({ body, headers: actionHeaders, method: action.method ?? "GET", signal, url: action.href });
}
