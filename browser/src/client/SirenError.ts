import { parse, type Entity } from "@siren-js/client";

type ErrorProperties = Record<string, unknown>;

function record(value: unknown): ErrorProperties | undefined {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as ErrorProperties)
    : undefined;
}

function location(value: unknown): (string | number)[] {
  const values = Array.isArray(value)
    ? value.filter(
        (item): item is string | number =>
          typeof item === "string" || typeof item === "number",
      )
    : typeof value === "string" || typeof value === "number"
      ? [value]
      : [];
  while (
    ["body", "cookie", "header", "path", "query"].includes(String(values[0]))
  )
    values.shift();
  return values;
}

function locationLabel(values: (string | number)[]): string {
  return values.reduce<string>(
    (result, value) =>
      typeof value === "number"
        ? `${result}[${value}]`
        : result
          ? `${result}.${value}`
          : value,
    "",
  );
}

function violationMessage(value: ErrorProperties): string | undefined {
  const message = value.msg ?? value.message ?? value.detail;
  return typeof message === "string" && message.trim()
    ? message.trim()
    : undefined;
}

function detailValues(properties: ErrorProperties): unknown {
  return (
    properties.detail ??
    properties.errors ??
    properties.message ??
    properties.error
  );
}

function errorDetails(
  entity: Entity,
  fieldNames: Set<string>,
): { details: string[]; fieldErrors: Record<string, string> } {
  const details: string[] = [];
  const fieldErrors: Record<string, string> = {};
  const value = detailValues(entity.properties as ErrorProperties);
  const values = Array.isArray(value) ? value : [value];

  values.forEach((item) => {
    if (typeof item === "string" && item.trim()) {
      details.push(item.trim());
      return;
    }
    const violation = record(item);
    if (!violation) return;
    const message = violationMessage(violation);
    if (!message) return;
    const path = location(
      violation.location ?? violation.loc ?? violation.path,
    );
    const label = locationLabel(path);
    details.push(label ? `${label}: ${message}` : message);
    const fieldName = path.find(
      (segment): segment is string =>
        typeof segment === "string" && fieldNames.has(segment),
    );
    if (fieldName)
      fieldErrors[fieldName] = [fieldErrors[fieldName], message]
        .filter(Boolean)
        .join(" ");
  });

  if (!details.length && value != null) {
    let serialized: string | undefined;
    try {
      serialized = JSON.stringify(value);
    } catch {
      serialized = undefined;
    }
    if (serialized) details.push(serialized);
  }
  return { details, fieldErrors };
}

function supportsStructuredError(response: Response): boolean {
  const mediaType = response.headers.get("Content-Type")?.split(";", 1)[0];
  return (
    mediaType?.endsWith("/json") === true ||
    mediaType?.endsWith("+json") === true
  );
}

export class SirenResponseError extends Error {
  constructor(
    readonly status: number,
    readonly url: string,
    message: string,
    readonly title?: string,
    readonly details: string[] = [],
    readonly fieldErrors: Record<string, string> = {},
    readonly entity?: Entity,
  ) {
    super(message);
    this.name = "SirenResponseError";
  }
}

export async function sirenResponseError(
  response: Response,
  fields: string[] = [],
): Promise<SirenResponseError> {
  const fallback =
    response.statusText || `Request failed with ${response.status}.`;
  if (!supportsStructuredError(response))
    return new SirenResponseError(response.status, response.url, fallback);

  try {
    const payload = (await response.clone().json()) as Record<string, unknown>;
    const entity = await parse(payload);
    const { details, fieldErrors } = errorDetails(entity, new Set(fields));
    const title = entity.title?.trim() || undefined;
    const detail = details.join(" ");
    const message = [title, detail].filter(Boolean).join(": ") || fallback;
    return new SirenResponseError(
      response.status,
      response.url,
      message,
      title,
      details,
      fieldErrors,
      entity,
    );
  } catch {
    return new SirenResponseError(response.status, response.url, fallback);
  }
}
