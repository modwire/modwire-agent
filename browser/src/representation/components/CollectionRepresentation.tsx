import { Anchor, List, Text } from "@mantine/core";
import type { SirenEntity, SirenLink, SirenSubEntity } from "siren-parser";
import { linkLabel } from "../../navigation/functions/representationLabel";
import { resourceLabel } from "../functions/resourceLabel";

type CollectionRepresentationProps = {
  entity: SirenEntity;
  onNavigate: (url: string) => void;
  resourceUrl: string;
};

function targetFor(resource: SirenSubEntity): SirenLink | undefined {
  return "href" in resource ? resource : resource.getLinkByRel("self");
}

function pointsToCurrentResource(target: SirenLink, resourceUrl: string): boolean {
  return new URL(target.href, window.location.origin).href === new URL(resourceUrl, window.location.origin).href;
}

function CollectionItem({ onNavigate, resource, resourceUrl }: { onNavigate: (url: string) => void; resource: SirenSubEntity; resourceUrl: string }) {
  const target = targetFor(resource);
  const label = resourceLabel(resource) ?? (target ? linkLabel(target) : "Resource");

  return (
    <List.Item>
      {target && !pointsToCurrentResource(target, resourceUrl) ? (
        <Anchor component="button" onClick={() => onNavigate(target.href)} type="button">
          {label}
        </Anchor>
      ) : (
        <Text span>{label}</Text>
      )}
    </List.Item>
  );
}

export function CollectionRepresentation({ entity, onNavigate, resourceUrl }: CollectionRepresentationProps) {
  if (!entity.entities?.length) {
    return <Text c="dimmed">No items.</Text>;
  }

  return (
    <List spacing="xs" withPadding>
      {entity.entities.map((resource, index) => (
        <CollectionItem
          key={"href" in resource ? resource.href : `${resource.rel?.join("-") ?? "resource"}-${index}`}
          onNavigate={onNavigate}
          resource={resource}
          resourceUrl={resourceUrl}
        />
      ))}
    </List>
  );
}
