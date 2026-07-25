export function canonicalSirenUrl(value: string): string {
  const address = value.trim();
  const url = address.startsWith("/") ? new URL(address, window.location.origin) : new URL(address);

  if (url.protocol !== "http:" && url.protocol !== "https:") {
    throw new TypeError(url.protocol);
  }

  return url.href;
}
