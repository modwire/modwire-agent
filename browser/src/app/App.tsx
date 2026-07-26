import { AppShell } from "@mantine/core";
import { useCallback, useEffect, useState, type ReactElement } from "react";
import type { Action, Target } from "@siren-js/client";
import { SirenClient } from "../client/SirenClient";
import { SirenPage } from "../ui/siren/SirenPage";
import { AppFooter } from "./AppFooter";
import { AppHeader } from "./AppHeader";
import { AppProviders } from "./providers/AppProviders";

const ROOT_RESOURCE = "/siren/";

export function App(): ReactElement {
  const [client] = useState(() => new SirenClient());
  const [entity, setEntity] = useState<Awaited<
    ReturnType<SirenClient["get"]>
  > | null>(null);
  const [firstEntity, setFirstEntity] = useState<Awaited<
    ReturnType<SirenClient["get"]>
  > | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [target, setTarget] = useState<Target>(
    () => window.location.hash.slice(1) || ROOT_RESOURCE,
  );

  const load = useCallback(
    async (nextTarget: Target) => {
      setError(null);
      setIsLoading(true);

      try {
        const nextEntity = await client.get(nextTarget);
        setEntity(nextEntity);
      } catch (reason) {
        setError(
          reason instanceof Error
            ? reason
            : new Error("Unable to load the Siren resource."),
        );
      } finally {
        setIsLoading(false);
      }
    },
    [client],
  );

  useEffect(() => {
    void load(target);
  }, [load, target]);

  useEffect(() => {
    const onHashChange = () =>
      setTarget(window.location.hash.slice(1) || ROOT_RESOURCE);

    window.addEventListener("hashchange", onHashChange);
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  useEffect(() => {
    void client.get(ROOT_RESOURCE).then(setFirstEntity);
  }, [client]);

  const follow = (nextTarget: Target) => {
    const href = (
      typeof nextTarget === "string" ? nextTarget : nextTarget.href
    ).toString();
    window.location.hash = href;
    setTarget(href);
  };

  const submit = async (action: Action, values: Record<string, unknown>) => {
    setError(null);
    setIsLoading(true);

    try {
      const response = await client.execute(action, values);
      if (response) {
        setEntity(response);
      } else {
        await load(target);
      }
    } catch (reason) {
      const submissionError =
        reason instanceof Error
          ? reason
          : new Error("Unable to submit the Siren action.");
      setError(submissionError);
      throw submissionError;
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AppProviders>
      <AppShell footer={{ height: 48 }} header={{ height: 60 }} padding="md">
        <AppHeader
          links={firstEntity?.links ?? []}
          onFollow={follow}
          target={target}
        />
        <AppShell.Main>
          {error ? <p role="alert">{error.message}</p> : null}
          <SirenPage
            entity={entity}
            isLoading={isLoading}
            onFollow={follow}
            onSubmit={submit}
          />
        </AppShell.Main>
        <AppFooter />
      </AppShell>
    </AppProviders>
  );
}
