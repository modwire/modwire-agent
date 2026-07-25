import { Card } from "@mantine/core";
import type { SirenEntity } from "siren-parser";
import { ResourceClasses } from "./ResourceClasses";

type EmptyRepresentationProps = {
  entity: SirenEntity;
};

export function EmptyRepresentation({ entity }: EmptyRepresentationProps) {
  return (
    <Card p="md" withBorder>
      <ResourceClasses classes={entity.class} />
    </Card>
  );
}
