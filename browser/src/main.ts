import SirenParse, { type SirenAction, type SirenEntity, type SirenField, type SirenLink } from "siren-parser";
import "./style.css";

type SirenDocument = Record<string, unknown>;
type RequestOptions = { method?: string; body?: BodyInit; headers?: Record<string, string> };
type HistoryItem = { method: string; status: string; url: string };
type ActionRequest = { url: string; options: RequestOptions };
type EntityLike = SirenEntity | SirenLink;

const root = document.querySelector<HTMLDivElement>("#app");

if (!root) {
  throw new Error("The Siren Browser needs an #app element.");
}

const app: HTMLDivElement = root;

const state: {
  document: SirenDocument | null;
  entity: SirenEntity | null;
  url: string;
  status: string;
  history: HistoryItem[];
  actorId: string;
  actorType: string;
  loading: boolean;
  controller: AbortController | null;
} = {
  document: null,
  entity: null,
  url: new URL("/siren/", window.location.origin).href,
  status: "Ready",
  history: [],
  actorId: localStorage.getItem("modwire-siren-actor-id") || "",
  actorType: localStorage.getItem("modwire-siren-actor-type") || "agent",
  loading: false,
  controller: null,
};

const specialClasses = new Set(["api", "entry-point", "collection", "entity", "command", "error"]);

function escapeHtml(value: unknown): string {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function pretty(value: unknown): string {
  return JSON.stringify(value ?? {}, null, 2);
}

function humanize(value: string): string {
  return value
    .replaceAll(/[_-]+/g, " ")
    .replaceAll(/\b\w/g, (letter) => letter.toUpperCase());
}

function pathLabel(url: string): string {
  const parts = new URL(url, window.location.href).pathname.split("/").filter(Boolean);
  const resource = parts.at(-1) || "siren";
  return humanize(resource);
}

function resourceKind(entity: EntityLike): string {
  const kind = entity.class?.find((name) => !specialClasses.has(name));
  return kind ? humanize(kind) : "Resource";
}

function pluralize(value: string): string {
  return value.endsWith("s") ? value : `${value}s`;
}

function resourceName(entity: EntityLike, collection = false): string {
  if (entity.class?.includes("api")) {
    return String((entity as SirenEntity).properties?.title || "Modwire API");
  }
  if (entity.class?.includes("error")) {
    return "Request failed";
  }
  if (entity.title) {
    return entity.title;
  }
  const properties = (entity as SirenEntity).properties || {};
  const identifier = properties.title || properties.name || properties.id;
  const label = collection || entity.class?.includes("collection") ? pluralize(resourceKind(entity)) : resourceKind(entity);
  return identifier ? `${label}: ${String(identifier)}` : label;
}

function route(url: string): string {
  const parsed = new URL(url, window.location.href);
  return `${parsed.pathname}${parsed.search}`;
}

function propertyValue(value: unknown): string {
  if (typeof value === "string") return value;
  if (typeof value === "number" || typeof value === "boolean") return String(value);
  return Array.isArray(value) ? `${value.length} item${value.length === 1 ? "" : "s"}` : "Structured value";
}

function valueForField(field: SirenField): string {
  if (field.value === undefined || field.value === null) return "";
  return typeof field.value === "string" ? field.value : JSON.stringify(field.value);
}

function linkLabel(link: SirenLink): string {
  if (link.title) return link.title;
  if (link.rel.includes("collection")) return `Open ${pathLabel(link.href)}`;
  if (link.rel.includes("self")) return "Refresh this resource";
  return humanize(link.rel.join(" "));
}

function properties(entity: SirenEntity): string {
  const entries = Object.entries(entity.properties || {});
  if (!entries.length) return "";
  const visible = entries.slice(0, 8);
  const remaining = entries.slice(8);
  const content = visible
    .map(([key, value]) => `<div><dt>${escapeHtml(humanize(key))}</dt><dd>${escapeHtml(propertyValue(value))}</dd></div>`)
    .join("");
  const overflow = remaining.length
    ? `<details class="structured"><summary>${remaining.length} more properties</summary><pre>${escapeHtml(pretty(Object.fromEntries(remaining)))}</pre></details>`
    : "";
  return `<dl class="properties">${content}</dl>${overflow}`;
}

function navigation(links: SirenLink[]): string {
  if (!links.length) return "";
  return `<section class="navigation"><h3>Navigate</h3>${links
    .map(
      (link) =>
        `<button class="link-button" type="button" data-navigate="${escapeHtml(link.href)}" ${state.loading ? "disabled" : ""}><span>${escapeHtml(linkLabel(link))}</span><small>${escapeHtml(route(link.href))}</small></button>`,
    )
    .join("")}</section>`;
}

function fieldInput(field: SirenField, id: string): string {
  const type = field.type || "text";
  if (type === "checkbox") {
    return `<label class="checkbox"><input id="${id}" name="${escapeHtml(field.name)}" type="checkbox" ${field.value ? "checked" : ""} />${escapeHtml(field.title || humanize(field.name))}</label>`;
  }
  if (type === "textarea") {
    return `<label>${escapeHtml(field.title || humanize(field.name))}<textarea id="${id}" name="${escapeHtml(field.name)}" placeholder="${escapeHtml(field.title || humanize(field.name))}">${escapeHtml(valueForField(field))}</textarea></label>`;
  }
  return `<label>${escapeHtml(field.title || humanize(field.name))}<input id="${id}" name="${escapeHtml(field.name)}" type="${escapeHtml(type)}" value="${escapeHtml(valueForField(field))}" placeholder="${escapeHtml(field.title || humanize(field.name))}" /></label>`;
}

function actionForm(action: SirenAction, id: string): string {
  const inputs = (action.fields || []).map((field, index) => fieldInput(field, `field-${id}-${index}`)).join("");
  return `<details class="action"><summary><span>${escapeHtml(humanize(action.name))}</span><small>${escapeHtml(action.method || "GET")}</small></summary><form class="action-form" data-action="${escapeHtml(encodeURIComponent(JSON.stringify(action)))}">${inputs || "<p class=\"muted\">No input is required.</p>"}<button type="submit" ${state.loading ? "disabled" : ""}>Run action</button></form></details>`;
}

function actions(entity: SirenEntity): string {
  const available = entity.actions || [];
  if (!available.length) return "";
  return `<section class="actions"><h3>Actions</h3>${available.map((action, index) => actionForm(action, String(index))).join("")}</section>`;
}

function embeddedEntity(entity: EntityLike): string {
  const navigable = "href" in entity ? entity : entity.getLinkByRel("self");
  const action = navigable
    ? `<button type="button" class="entity-button" data-navigate="${escapeHtml(navigable.href)}" ${state.loading ? "disabled" : ""}>Open</button>`
    : "";
  const properties = "properties" in entity ? entity.properties || {} : {};
  const summary = Object.entries(properties)
    .slice(0, 3)
    .map(([key, value]) => `${humanize(key)}: ${propertyValue(value)}`)
    .join(" · ");
  return `<article class="embedded"><div><p class="eyebrow">${escapeHtml(resourceKind(entity))}</p><h4>${escapeHtml(resourceName(entity))}</h4><p class="muted">${escapeHtml(summary || entity.rel?.map(humanize).join(" · ") || "Embedded resource")}</p></div>${action}</article>`;
}

function embedded(entity: SirenEntity): string {
  const items = entity.entities || [];
  if (!items.length) return "";
  return `<section class="embedded-resources"><h3>${entity.class?.includes("collection") ? "Resources" : "Embedded resources"}</h3><div class="embedded-list">${items.map(embeddedEntity).join("")}</div></section>`;
}

function card(entity: SirenEntity): string {
  return `<section class="entity">
    <header><div><p class="eyebrow">${escapeHtml(resourceKind(entity))}</p><h2>${escapeHtml(resourceName(entity))}</h2></div><span class="class-badge">${escapeHtml(entity.class?.join(" · ") || "resource")}</span></header>
    ${properties(entity)}
    ${navigation(entity.links || [])}
    ${actions(entity)}
    ${embedded(entity)}
  </section>`;
}

function render(): void {
  app.innerHTML = `<main>
    <header class="masthead"><div><p class="eyebrow">Modwire Agent</p><h1>Siren Browser</h1><p>Explore resources and run the actions the API advertises.</p></div><div class="status ${state.loading ? "loading" : ""}">${escapeHtml(state.status)}</div></header>
    <section class="connection"><form id="address-form"><label>Resource address<input id="address" type="url" value="${escapeHtml(state.url)}" spellcheck="false" /></label><button type="submit" ${state.loading ? "disabled" : ""}>Open</button></form><div class="actor-fields"><label>Actor ID<input id="actor-id" value="${escapeHtml(state.actorId)}" placeholder="optional" /></label><label>Actor type<select id="actor-type"><option value="agent" ${state.actorType === "agent" ? "selected" : ""}>agent</option><option value="user" ${state.actorType === "user" ? "selected" : ""}>user</option></select></label></div></section>
    <section class="workspace"><div class="resource">${state.entity ? card(state.entity) : `<div class="empty"><h2>Open a Siren resource</h2><p>The browser checks each representation with <code>siren-parser</code> before showing it.</p></div>`}</div><aside><h2>Recent requests</h2>${state.history.length ? `<ol>${state.history.map((item) => `<li><button type="button" data-navigate="${escapeHtml(item.url)}" ${state.loading ? "disabled" : ""}><strong>${escapeHtml(item.method)}</strong> ${escapeHtml(pathLabel(item.url))}</button><small>${escapeHtml(item.status)} · ${escapeHtml(route(item.url))}</small></li>`).join("")}</ol>` : "<p class=\"muted\">No requests yet.</p>"}<details class="raw"><summary>Raw Siren document</summary><pre>${escapeHtml(state.document ? pretty(state.document) : "")}</pre></details></aside></section>
  </main>`;
}

function headers(contentType?: string): Record<string, string> {
  const result: Record<string, string> = { Accept: "application/vnd.siren+json, application/json" };
  if (contentType) result["Content-Type"] = contentType;
  if (state.actorId) {
    result["X-Actor-Id"] = state.actorId;
    result["X-Actor-Type"] = state.actorType;
  }
  return result;
}

function addHistory(method: string, status: string, url: string): void {
  state.history.unshift({ method, status, url });
  state.history = state.history.slice(0, 12);
}

async function request(url: string, options: RequestOptions, signal: AbortSignal): Promise<void> {
  const response = await fetch(url, {
    ...options,
    signal,
    headers: { ...headers(options.body ? "application/json" : undefined), ...options.headers },
  });
  state.url = response.url || url;
  state.status = `${response.status} ${response.statusText || "response"}`;
  addHistory(options.method || "GET", state.status, state.url);
  if (response.status === 204) return;
  const contentType = response.headers.get("content-type") || "";
  if (!contentType.includes("json")) {
    throw new Error("The response is not JSON and cannot be displayed as Siren.");
  }
  const document = (await response.json()) as SirenDocument;
  state.entity = SirenParse(document);
  state.document = document;
}

async function perform(url: string, options: RequestOptions = {}): Promise<void> {
  state.controller?.abort();
  const controller = new AbortController();
  state.controller = controller;
  state.loading = true;
  state.status = options.method && options.method !== "GET" ? `Running ${options.method}…` : "Loading…";
  render();
  try {
    await request(url, options, controller.signal);
  } catch (error) {
    if (controller.signal.aborted) return;
    state.status = error instanceof Error ? error.message : String(error);
  } finally {
    if (state.controller === controller) {
      state.controller = null;
      state.loading = false;
      render();
    }
  }
}

function actionFrom(form: HTMLFormElement): SirenAction {
  return JSON.parse(decodeURIComponent(form.dataset.action || "")) as SirenAction;
}

function payloadFrom(form: HTMLFormElement, action: SirenAction): Record<string, unknown> {
  const payload: Record<string, unknown> = {};
  const fields = new Map((action.fields || []).map((field) => [field.name, field]));
  for (const [key, value] of new FormData(form).entries()) {
    if (typeof value !== "string") continue;
    const field = fields.get(key);
    if (field?.type === "checkbox") {
      payload[key] = true;
    } else if (field?.type === "number" && value !== "") {
      payload[key] = Number(value);
    } else if (value.startsWith("{") || value.startsWith("[")) {
      try {
        payload[key] = JSON.parse(value) as unknown;
      } catch {
        payload[key] = value;
      }
    } else {
      payload[key] = value;
    }
  }
  for (const field of action.fields || []) {
    if (field.type === "checkbox" && !(field.name in payload)) payload[field.name] = false;
  }
  return payload;
}

function requestFor(action: SirenAction, payload: Record<string, unknown>): ActionRequest {
  const method = action.method || "GET";
  if (method === "GET" || method === "HEAD") {
    const url = new URL(action.href, window.location.href);
    for (const [key, value] of Object.entries(payload)) {
      url.searchParams.set(key, typeof value === "string" ? value : JSON.stringify(value));
    }
    return { url: url.href, options: { method } };
  }
  if (action.type === "application/json") {
    return {
      url: action.href,
      options: { method, body: JSON.stringify(payload), headers: { "Content-Type": action.type } },
    };
  }
  const body = new URLSearchParams(
    Object.entries(payload).map(([key, value]) => [key, typeof value === "string" ? value : JSON.stringify(value)]),
  );
  return {
    url: action.href,
    options: { method, body, headers: { "Content-Type": action.type || "application/x-www-form-urlencoded" } },
  };
}

app.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!(event.target instanceof HTMLFormElement) || state.loading) return;
  if (event.target.id === "address-form") {
    const address = event.target.querySelector<HTMLInputElement>("#address");
    if (address) void perform(address.value);
    return;
  }
  if (!event.target.matches(".action-form")) return;
  const action = actionFrom(event.target);
  const payload = payloadFrom(event.target, action);
  const actionRequest = requestFor(action, payload);
  void perform(actionRequest.url, actionRequest.options);
});

app.addEventListener("click", (event) => {
  if (state.loading || !(event.target instanceof Element)) return;
  const button = event.target.closest<HTMLElement>("[data-navigate]");
  if (!button?.dataset.navigate) return;
  event.preventDefault();
  void perform(button.dataset.navigate);
});

app.addEventListener("change", (event) => {
  if (event.target instanceof HTMLInputElement && event.target.id === "actor-id") {
    state.actorId = event.target.value;
    localStorage.setItem("modwire-siren-actor-id", state.actorId);
  }
  if (event.target instanceof HTMLSelectElement && event.target.id === "actor-type") {
    state.actorType = event.target.value;
    localStorage.setItem("modwire-siren-actor-type", state.actorType);
  }
});

render();
void perform(state.url);
