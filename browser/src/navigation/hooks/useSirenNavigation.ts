import { useQuery } from "@tanstack/react-query";
import { useCallback, useEffect, useState } from "react";
import type { SirenLink } from "siren-parser";
import { representationLabel } from "../functions/representationLabel";
import { normalizeResourceUrl, resourceLocation, resourceUrlFromLocation, rootResourceUrl } from "../functions/resourceUrl";
import { fetchSirenResource, type SirenResource } from "../services/fetchSirenResource";

type BrowserHistoryState = {
  modwireSirenPosition?: number;
  modwireSirenResourceUrl?: string;
};

type VisitedResource = {
  label: string;
  url: string;
};

export type SirenNavigation = {
  canGoBack: boolean;
  canGoForward: boolean;
  error: Error | null;
  isLoading: boolean;
  links: SirenLink[];
  navigate: (url: string) => void;
  resources: VisitedResource[];
  resource: SirenResource | null;
  resourceUrl: string;
  retry: () => void;
  goBack: () => void;
  goForward: () => void;
};

function historyState(): BrowserHistoryState {
  return typeof window.history.state === "object" && window.history.state ? window.history.state : {};
}

function errorFrom(value: unknown): Error {
  return value instanceof Error ? value : new Error(String(value));
}

export function useSirenNavigation(): SirenNavigation {
  const [rootUrl] = useState(rootResourceUrl);
  const [resourceUrl, setResourceUrl] = useState(() => resourceUrlFromLocation(rootUrl));
  const [error, setError] = useState<Error | null>(null);
  const [resources, setResources] = useState<VisitedResource[]>([]);
  const [position, setPosition] = useState(() => historyState().modwireSirenPosition ?? 0);
  const [highestPosition, setHighestPosition] = useState(position);
  const rootQuery = useQuery({
    queryKey: ["siren-resource", rootUrl],
    queryFn: ({ signal }) => fetchSirenResource(rootUrl, signal),
    retry: false,
  });
  const resourceQuery = useQuery({
    queryKey: ["siren-resource", resourceUrl],
    queryFn: ({ signal }) => fetchSirenResource(resourceUrl, signal),
    retry: false,
  });

  const navigate = useCallback(
    (value: string) => {
      try {
        const nextUrl = normalizeResourceUrl(value);
        const nextPosition = position + 1;

        window.history.pushState(
          { modwireSirenPosition: nextPosition, modwireSirenResourceUrl: nextUrl },
          "",
          resourceLocation(nextUrl),
        );
        setPosition(nextPosition);
        setHighestPosition(nextPosition);
        setError(null);
        setResourceUrl(nextUrl);
      } catch (navigationError) {
        setError(errorFrom(navigationError));
      }
    },
    [position],
  );

  const goBack = useCallback(() => window.history.back(), []);
  const goForward = useCallback(() => window.history.forward(), []);
  const retry = useCallback(() => void resourceQuery.refetch(), [resourceQuery.refetch]);

  useEffect(() => {
    window.history.replaceState(
      { modwireSirenPosition: position, modwireSirenResourceUrl: resourceUrl },
      "",
      resourceLocation(resourceUrl),
    );
  }, []);

  useEffect(() => {
    const receiveHistory = (event: PopStateEvent) => {
      const state = event.state as BrowserHistoryState | null;
      const nextUrl = state?.modwireSirenResourceUrl ?? resourceUrlFromLocation(rootUrl);

      try {
        setResourceUrl(normalizeResourceUrl(nextUrl));
        setPosition(state?.modwireSirenPosition ?? 0);
        setError(null);
      } catch (navigationError) {
        setError(errorFrom(navigationError));
      }
    };

    window.addEventListener("popstate", receiveHistory);
    return () => window.removeEventListener("popstate", receiveHistory);
  }, [rootUrl]);

  useEffect(() => {
    if (!resourceQuery.data) {
      return;
    }

    const resource = {
      label: representationLabel(resourceQuery.data.entity, resourceQuery.data.url),
      url: resourceQuery.data.url,
    };

    setResources((current) =>
      current.some((item) => item.url === resource.url)
        ? current.map((item) => (item.url === resource.url ? resource : item))
        : [...current, resource],
    );
  }, [resourceQuery.data]);

  useEffect(() => {
    if (resourceQuery.error) {
      setError(errorFrom(resourceQuery.error));
    }
  }, [resourceQuery.error]);

  return {
    canGoBack: position > 0,
    canGoForward: position < highestPosition,
    error,
    goBack,
    goForward,
    isLoading: resourceQuery.isFetching,
    links: rootQuery.data?.entity.links ?? [],
    navigate,
    resources,
    resource: resourceQuery.data ?? null,
    resourceUrl,
    retry,
  };
}
