import type { Action, Entity, Target } from "@siren-js/client";
import { Center, Loader, Text } from "@mantine/core";
import { EntityDispatcher } from "./EntityDispatcher";

export type SirenBrowserProps = {
  entity: Entity | null;
  isLoading: boolean;
  onFollow: (target: Target) => void;
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function SirenBrowser({ entity, isLoading, onFollow, onSubmit }: SirenBrowserProps) {
  if (isLoading) {
    return <Center><Loader aria-label="Loading resource" /></Center>;
  }

  if (!entity) {
    return <Text>No resource selected.</Text>;
  }

  return <EntityDispatcher entity={entity} onFollow={onFollow} onSubmit={onSubmit} />;
}
