import { Card, SimpleGrid, Stack, Title } from "@mantine/core";
import type { SirenEntity } from "siren-parser";
import { EmbeddedResourceCard } from "./EmbeddedResourceCard";
import { PropertyGrid } from "./PropertyGrid";
import { RepresentationLinks } from "./RepresentationLinks";
import { ResourceClasses } from "./ResourceClasses";

type CollectionRepresentationProps = {
  entity: SirenEntity;
  onNavigate: (url: string) => void;
};

export function CollectionRepresentation({ entity, onNavigate }: CollectionRepresentationProps) {
  return (
    <Stack gap="md">
      <Card p="md" withBorder>
        <Stack gap="md">
          {entity.title ? <Title order={2}>{entity.title}</Title> : null}
          <ResourceClasses classes={entity.class} />
          <PropertyGrid properties={entity.properties} />
          <RepresentationLinks links={entity.links} onNavigate={onNavigate} />
        </Stack>
      </Card>
      {entity.entities?.length ? (
        <SimpleGrid cols={{ base: 1, md: 2 }}>
          {entity.entities.map((resource, index) => (
            <EmbeddedResourceCard
              key={"href" in resource ? resource.href : `${resource.rel?.join("-") ?? "resource"}-${index}`}
              onNavigate={onNavigate}
              resource={resource}
            />
          ))}
        </SimpleGrid>
      ) : null}
    </Stack>
  );
}
