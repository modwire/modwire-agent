const RESOURCE_PARAMETER = "resource";

export function rootResourceUrl(): string {
  return new URL("/siren/", window.location.origin).href;
}

export function normalizeResourceUrl(value: string): string {
  const address = value.trim();
  const resourceUrl = address.startsWith("/") ? new URL(address, window.location.origin) : new URL(address);

  if (resourceUrl.protocol !== "http:" && resourceUrl.protocol !== "https:") {
    throw new TypeError(resourceUrl.protocol);
  }

  return resourceUrl.href;
}

export function resourceUrlFromLocation(rootUrl: string): string {
  const resourceUrl = new URL(window.location.href).searchParams.get(RESOURCE_PARAMETER);

  if (!resourceUrl) {
    return rootUrl;
  }

  try {
    return normalizeResourceUrl(resourceUrl);
  } catch {
    return rootUrl;
  }
}

export function resourceLocation(resourceUrl: string): string {
  const location = new URL(window.location.href);
  location.searchParams.set(RESOURCE_PARAMETER, resourceUrl);
  return `${location.pathname}${location.search}${location.hash}`;
}
