import {
  ActionFiller,
  follow,
  parse,
  submit,
  type Action as LibraryAction,
  type EmbeddedEntity,
  type EmbeddedLink,
  type Entity as LibraryEntity,
  type Field as LibraryField,
  type Href,
  type Link as LibraryLink,
  type Target,
} from "@siren-js/client";
import type { SirenAction } from "./SirenAction";
import type { SirenEntity } from "./SirenEntity";
import type { SirenField } from "./SirenField";
import type { SirenLink } from "./SirenLink";
import type { SirenSubEntity } from "./SirenSubEntity";

export const SIREN_ACCEPT = "application/vnd.siren+json, application/json";

export type SirenClientOptions = {
  baseUrl?: Href;
  headers?: HeadersInit;
};

export type SirenRequestOptions = {
  headers?: HeadersInit;
  signal?: AbortSignal;
};

export class SirenResponseError extends Error {
  constructor(
    readonly status: number,
    readonly url: string,
    message: string,
  ) {
    super(message);
    this.name = "SirenResponseError";
  }
}

export class SirenClient {
  private readonly actions = new WeakMap<SirenAction, LibraryAction>();
  private readonly baseUrl: Href;
  private readonly headers: Headers;

  constructor({ baseUrl = window.location.origin, headers }: SirenClientOptions = {}) {
    this.baseUrl = baseUrl;
    this.headers = new Headers(headers);
  }

  async get(target: Target, options: SirenRequestOptions = {}): Promise<SirenEntity> {
    const response = await follow(target, { baseUrl: this.baseUrl, requestInit: this.requestInit(options) });
    return this.entity(response);
  }

  async execute(
    action: SirenAction,
    values: Record<string, unknown> = {},
    options: SirenRequestOptions = {},
  ): Promise<SirenEntity | null> {
    const source = this.actions.get(action);

    if (!source) {
      throw new TypeError("The Siren action was not provided by this client.");
    }

    await source.accept(new ActionFiller(values));
    const response = await submit(source, { baseUrl: this.baseUrl, requestInit: this.requestInit(options) });

    if (response.status === 204) {
      return null;
    }

    return this.entity(response);
  }

  private async entity(response: Response): Promise<SirenEntity> {
    if (!response.ok) {
      throw new SirenResponseError(response.status, response.url, response.statusText || `Request failed with ${response.status}.`);
    }

    return this.normalizeEntity(await parse(response));
  }

  private requestInit({ headers, signal }: SirenRequestOptions): RequestInit {
    const requestHeaders = new Headers(this.headers);
    new Headers(headers).forEach((value, name) => requestHeaders.set(name, value));
    requestHeaders.set("Accept", requestHeaders.get("Accept") ?? SIREN_ACCEPT);
    return { headers: requestHeaders, signal };
  }

  private normalizeAction(action: LibraryAction): SirenAction {
    if (typeof action.href !== "string" || !action.href) {
      throw new TypeError("A Siren action requires an href.");
    }

    if (typeof action.name !== "string" || !action.name) {
      throw new TypeError("A Siren action requires a name.");
    }

    const normalized = {
      class: Array.isArray(action.class) ? action.class.filter((value): value is string => typeof value === "string") : [],
      fields: Array.isArray(action.fields) ? action.fields.map((field) => this.normalizeField(field)) : [],
      href: action.href,
      method: typeof action.method === "string" && action.method ? action.method : "GET",
      name: action.name,
      title: typeof action.title === "string" && action.title ? action.title : action.name,
      type: typeof action.type === "string" && action.type ? action.type : "application/x-www-form-urlencoded",
    } satisfies SirenAction;

    this.actions.set(normalized, action);
    return normalized;
  }

  private normalizeEntity(entity: LibraryEntity): SirenEntity {
    return {
      actions: Array.isArray(entity.actions) ? entity.actions.map((action) => this.normalizeAction(action)) : [],
      class: Array.isArray(entity.class) ? entity.class.filter((value): value is string => typeof value === "string") : [],
      entities: Array.isArray(entity.entities) ? entity.entities.map((item) => this.normalizeSubEntity(item)) : [],
      links: Array.isArray(entity.links) ? entity.links.map((link) => this.normalizeLink(link)) : [],
      properties:
        typeof entity.properties === "object" && entity.properties !== null && !Array.isArray(entity.properties)
          ? (entity.properties as Record<string, unknown>)
          : {},
      title: typeof entity.title === "string" && entity.title ? entity.title : "Resource",
    };
  }

  private normalizeField(field: LibraryField): SirenField {
    if (typeof field.name !== "string" || !field.name) {
      throw new TypeError("A Siren action field requires a name.");
    }

    return {
      class: Array.isArray(field.class) ? field.class.filter((value): value is string => typeof value === "string") : [],
      name: field.name,
      title: typeof field.title === "string" && field.title ? field.title : field.name,
      type: typeof field.type === "string" && field.type ? field.type : "text",
      value: field.value ?? "",
    };
  }

  private normalizeLink(link: LibraryLink): SirenLink {
    if (typeof link.href !== "string" || !link.href) {
      throw new TypeError("A Siren link requires an href.");
    }

    if (!Array.isArray(link.rel) || !link.rel.every((value) => typeof value === "string")) {
      throw new TypeError("A Siren link requires relations.");
    }

    return {
      class: Array.isArray(link.class) ? link.class.filter((value): value is string => typeof value === "string") : [],
      href: link.href,
      rel: link.rel,
      title: typeof link.title === "string" && link.title ? link.title : link.href,
      type: typeof link.type === "string" ? link.type : "",
    };
  }

  private normalizeSubEntity(entity: EmbeddedEntity | EmbeddedLink): SirenSubEntity {
    return {
      class: Array.isArray(entity.class) ? entity.class.filter((value): value is string => typeof value === "string") : [],
      rel: Array.isArray(entity.rel) ? entity.rel.filter((value): value is string => typeof value === "string") : [],
      title:
        typeof entity.title === "string" && entity.title
          ? entity.title
          : Array.isArray(entity.class) && entity.class.length
            ? entity.class.join(" ")
            : "Resource",
    };
  }
}
