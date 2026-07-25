import { afterEach, expect, it, vi } from "vitest";
import type { SirenAction } from "siren-parser";
import { executeSirenAction, requestSiren, SirenResponseError } from "../client";

afterEach(() => vi.unstubAllGlobals());

it("accepts and parses a Siren representation at one boundary", async () => {
  const selfUrl = new URL("/siren/records/42", window.location.origin).href;
  const fetchMock = vi.fn().mockResolvedValue(
    new Response(JSON.stringify({ title: "HTTP", links: [{ rel: ["self"], href: selfUrl }] }), {
      headers: { "content-type": "application/vnd.siren+json" },
    }),
  );
  vi.stubGlobal("fetch", fetchMock);

  const response = await requestSiren({ url: "/siren/records/42" });

  expect(response).toMatchObject({ kind: "representation", resource: { url: selfUrl, status: 200 } });
  expect(fetchMock).toHaveBeenCalledWith(
    selfUrl,
    expect.objectContaining({ headers: expect.any(Headers), method: "GET" }),
  );
  expect((fetchMock.mock.calls[0][1].headers as Headers).get("Accept")).toContain("application/vnd.siren+json");
});

it("surfaces Siren error details with the response document", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ class: ["error"], properties: { detail: "Only a user can resolve this." } }), {
        headers: { "content-type": "application/vnd.siren+json" },
        status: 422,
        statusText: "Unprocessable Entity",
      }),
    ),
  );

  await expect(requestSiren({ url: "/siren/content-proposals/42" })).rejects.toMatchObject({
    document: { properties: { detail: "Only a user can resolve this." } },
    message: "Only a user can resolve this.",
    status: 422,
  });
});

it("gives non-JSON and 204 responses explicit outcomes", async () => {
  const fetchMock = vi
    .fn()
    .mockResolvedValueOnce(new Response("Not JSON", { headers: { "content-type": "text/plain" } }))
    .mockResolvedValueOnce(new Response(null, { status: 204 }));
  vi.stubGlobal("fetch", fetchMock);

  await expect(requestSiren({ url: "/siren/download" })).rejects.toBeInstanceOf(SirenResponseError);
  await expect(requestSiren({ method: "DELETE", url: "/siren/records/42" })).resolves.toMatchObject({
    kind: "empty",
    status: 204,
  });
});

it("preserves aborted requests and executes the advertised action method", async () => {
  const aborted = new DOMException("Aborted", "AbortError");
  const fetchMock = vi
    .fn()
    .mockRejectedValueOnce(aborted)
    .mockResolvedValueOnce(
      new Response(JSON.stringify({ title: "HTTP", links: [{ rel: ["self"], href: "/siren/records/42" }] }), {
        headers: { "content-type": "application/vnd.siren+json" },
      }),
    );
  vi.stubGlobal("fetch", fetchMock);

  await expect(requestSiren({ signal: new AbortController().signal, url: "/siren/records" })).rejects.toBe(aborted);
  await executeSirenAction({
    action: { href: "/siren/records/42", method: "PATCH", name: "rename_record", type: "application/json" } as SirenAction,
    body: JSON.stringify({ title: "Renamed" }),
  });

  expect(fetchMock).toHaveBeenLastCalledWith(
    new URL("/siren/records/42", window.location.origin).href,
    expect.objectContaining({ method: "PATCH" }),
  );
  expect((fetchMock.mock.calls[1][1].headers as Headers).get("Content-Type")).toBe("application/json");
});
