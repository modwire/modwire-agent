import { useCallback, useEffect, useState, type ReactElement } from "react";
import type { Action, Target } from "@siren-js/client";
import { SirenClient } from "../client/SirenClient";
import { SirenBrowser } from "../ui/siren/SirenBrowser";
import { AppProviders } from "./providers/AppProviders";

const ROOT_RESOURCE = "/siren/";

export function App(): ReactElement {
  const [client] = useState(() => new SirenClient());
  const [entity, setEntity] = useState<Awaited<ReturnType<SirenClient["get"]>> | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [target, setTarget] = useState<Target>(ROOT_RESOURCE);

  const load = useCallback(
    async (nextTarget: Target) => {
      setError(null);
      setIsLoading(true);

      try {
        setEntity(await client.get(nextTarget));
      } catch (reason) {
        setError(reason instanceof Error ? reason : new Error("Unable to load the Siren resource."));
      } finally {
        setIsLoading(false);
      }
    },
    [client],
  );

  useEffect(() => {
    void load(target);
  }, [load, target]);

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
      setError(reason instanceof Error ? reason : new Error("Unable to submit the Siren action."));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AppProviders>
      <main>
        {error ? <p role="alert">{error.message}</p> : null}
        <SirenBrowser entity={entity} isLoading={isLoading} onFollow={setTarget} onSubmit={submit} />
      </main>
    </AppProviders>
  );
}
