import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { act, renderHook, waitFor } from "@testing-library/react";
import type { ReactNode } from "react";
import { afterEach, expect, it, vi } from "vitest";
import type { SirenAction } from "siren-parser";
import type { SirenResource } from "../client";
import { sirenResourceQueryKey, useSirenAction, useSirenResource } from "../hooks";

afterEach(() => vi.unstubAllGlobals());

function wrapper(queryClient: QueryClient) {
  return function QueryProvider({ children }: { children: ReactNode }) {
    return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
  };
}

it("uses canonical resource URLs for cache keys", () => {
  expect(sirenResourceQueryKey("/siren/records")).toEqual([
    "siren-resource",
    new URL("/siren/records", window.location.origin).href,
  ]);
});

it("also caches a fetched representation under its advertised self URL", async () => {
  const selfUrl = new URL("/siren/records/42", window.location.origin).href;
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ title: "HTTP", links: [{ rel: ["self"], href: selfUrl }] }), {
        headers: { "content-type": "application/vnd.siren+json" },
      }),
    ),
  );
  const queryClient = new QueryClient();
  const { result } = renderHook(() => useSirenResource("/siren/record-alias"), { wrapper: wrapper(queryClient) });

  await waitFor(() => expect(result.current.data?.url).toBe(selfUrl));
  expect(queryClient.getQueryData<SirenResource>(sirenResourceQueryKey(selfUrl))).toMatchObject({ url: selfUrl });
});

it("replaces the affected representation in the query cache after an action", async () => {
  const resourceUrl = new URL("/siren/records/42", window.location.origin).href;
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ title: "Renamed", links: [{ rel: ["self"], href: resourceUrl }] }), {
        headers: { "content-type": "application/vnd.siren+json" },
      }),
    ),
  );
  const queryClient = new QueryClient();
  const { result } = renderHook(() => useSirenAction(), { wrapper: wrapper(queryClient) });

  await act(async () => {
    await result.current.mutateAsync({
      action: { href: resourceUrl, method: "PATCH", name: "rename_record" } as SirenAction,
    });
  });

  expect(queryClient.getQueryData<SirenResource>(sirenResourceQueryKey(resourceUrl))).toMatchObject({
    document: { title: "Renamed" },
    url: resourceUrl,
  });
});
