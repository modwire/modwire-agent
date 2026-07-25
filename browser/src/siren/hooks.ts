import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect } from "react";
import type { SirenResponse } from "./client";
import { executeSirenAction, fetchSirenResource, type SirenResource } from "./client";
import { canonicalSirenUrl } from "./url";

export function sirenResourceQueryKey(url: string): readonly ["siren-resource", string] {
  return ["siren-resource", canonicalSirenUrl(url)];
}

export function useSirenResource(url: string) {
  const queryClient = useQueryClient();
  const query = useQuery({
    queryKey: sirenResourceQueryKey(url),
    queryFn: ({ signal }) => fetchSirenResource(url, signal),
    retry: false,
  });

  useEffect(() => {
    if (query.data) {
      queryClient.setQueryData<SirenResource>(sirenResourceQueryKey(query.data.url), query.data);
    }
  }, [query.data, queryClient]);

  return query;
}

function updateResourceCache(queryClient: ReturnType<typeof useQueryClient>, response: SirenResponse): void {
  if (response.kind === "representation") {
    queryClient.setQueryData<SirenResource>(sirenResourceQueryKey(response.resource.url), response.resource);
  }
}

export function useSirenAction() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: executeSirenAction,
    onSuccess: (response, request) => {
      updateResourceCache(queryClient, response);
      void queryClient.invalidateQueries({ queryKey: sirenResourceQueryKey(request.action.href) });
    },
  });
}
