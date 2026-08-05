import { Action, Field } from "@siren-js/client";
import { HttpResponse, http } from "msw";
import { setupServer } from "msw/node";
import { afterAll, afterEach, beforeAll, describe, expect, it } from "vitest";
import { SIREN_ACCEPT, SIREN_ACTOR_HEADERS, SirenClient } from "../SirenClient";

const server = setupServer();

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

function field(name: string, value: unknown): Field {
  return Object.assign(new Field(), { name, type: "text", value });
}

describe("SirenClient", () => {
  it("negotiates Siren and sends the configured actor headers", async () => {
    server.use(
      http.get("http://example.test/api/", ({ request }) => {
        expect(request.headers.get("Accept")).toBe(SIREN_ACCEPT);
        expect(request.headers.get("X-Actor-Id")).toBe(
          SIREN_ACTOR_HEADERS["X-Actor-Id"],
        );
        expect(request.headers.get("X-Actor-Type")).toBe(
          SIREN_ACTOR_HEADERS["X-Actor-Type"],
        );
        return HttpResponse.json(
          {
            class: ["api", "entry-point"],
            properties: { title: "Example API" },
            title: "Example API",
          },
          { headers: { "Content-Type": "application/vnd.siren+json" } },
        );
      }),
    );

    const entity = await new SirenClient({
      baseUrl: "http://example.test",
    }).get("/api/");

    expect(entity.class).toEqual(["api", "entry-point"]);
    expect(entity.title).toBe("Example API");
  });

  it("submits structured and falsy JSON values without coercion", async () => {
    server.use(
      http.post("http://example.test/api/examples", async ({ request }) => {
        expect(request.headers.get("Content-Type")).toBe("application/json");
        expect(await request.json()).toEqual({
          description: "",
          enabled: false,
          example_document: {},
          example_items: [],
          limit: 0,
        });
        return new HttpResponse(null, { status: 204 });
      }),
    );
    const action = Object.assign(new Action(), {
      fields: [
        field("description", "Existing"),
        field("enabled", true),
        field("example_document", { existing: true }),
        field("example_items", ["existing"]),
        field("limit", 10),
      ],
      href: "/api/examples",
      method: "POST",
      name: "create-example",
      type: "application/json",
    });

    const result = await new SirenClient({
      baseUrl: "http://example.test",
    }).execute(action, {
      description: "",
      enabled: false,
      example_document: {},
      example_items: [],
      limit: 0,
    });

    expect(result).toBeNull();
  });
});
