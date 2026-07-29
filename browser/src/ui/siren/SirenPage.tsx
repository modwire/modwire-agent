import { Center, Loader, Text } from "@mantine/core";
import type { Action, Entity, Target } from "@siren-js/client";
import { SirenEntity } from "./SirenEntity";

export type SirenPageProps = {
  entity: Entity | null;
  isLoading: boolean;
  onFollow: (target: Target) => void;
  onSubmit: (action: Action, values: Record<string, unknown>) => void;
};

export function SirenPage({
  entity,
  isLoading,
  onFollow,
  onSubmit,
}: SirenPageProps) {
  if (isLoading)
    return (
      <Center>
        <Loader aria-label="Loading resource" />
      </Center>
    );
  if (!entity) return <Text>No resource selected.</Text>;
  return (
    <SirenEntity entity={entity} onFollow={onFollow} onSubmit={onSubmit} />
  );
}
