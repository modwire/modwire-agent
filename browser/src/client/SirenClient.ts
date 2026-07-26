import { ActionFiller, follow, parse, submit, type Action, type Entity, type Href, type Target } from "@siren-js/client";

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
  private readonly baseUrl: Href;
  private readonly headers: Headers;

  constructor({ baseUrl = window.location.origin, headers }: SirenClientOptions = {}) {
    this.baseUrl = baseUrl;
    this.headers = new Headers(headers);
  }

  async get<T extends object = object>(target: Target, options: SirenRequestOptions = {}): Promise<Entity<T>> {
    const response = await follow(target, { baseUrl: this.baseUrl, requestInit: this.requestInit(options) });
    return this.entity<T>(response);
  }

  async execute<T extends object = object>(
    action: Action,
    values: Record<string, unknown> = {},
    options: SirenRequestOptions = {},
  ): Promise<Entity<T> | null> {
    await action.accept(new ActionFiller(values));
    const response = await submit(action, { baseUrl: this.baseUrl, requestInit: this.requestInit(options) });

    if (response.status === 204) {
      return null;
    }

    return this.entity<T>(response);
  }

  private async entity<T extends object>(response: Response): Promise<Entity<T>> {
    if (!response.ok) {
      throw new SirenResponseError(response.status, response.url, response.statusText || `Request failed with ${response.status}.`);
    }

    return parse<T>(response);
  }

  private requestInit({ headers, signal }: SirenRequestOptions): RequestInit {
    const requestHeaders = new Headers(this.headers);
    new Headers(headers).forEach((value, name) => requestHeaders.set(name, value));
    requestHeaders.set("Accept", requestHeaders.get("Accept") ?? SIREN_ACCEPT);
    return { headers: requestHeaders, signal };
  }
}
