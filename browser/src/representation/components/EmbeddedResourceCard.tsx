import { Button, Card, Stack, Title } from "@mantine/core";
import type { SirenLink, SirenSubEntity } from "siren-parser";
import { linkLabel } from "../../navigation/functions/representationLabel";
import { resourceLabel } from "../functions/resourceLabel";
import { PropertyGrid } from "./PropertyGrid";
import { ResourceClasses } from "./ResourceClasses";

type EmbeddedResourceCardProps = {
  resource: SirenSubEntity;
  onNavigate: (url: string) => void;
};

function targetFor(resource: SirenSubEntity): SirenLink | undefined {
  return "href" in resource ? resource : resource.getLinkByRel("self");
}

export function EmbeddedResourceCard({ resource, onNavigate }: EmbeddedResourceCardProps) {
  const label = resourceLabel(resource);
  const target = targetFor(resource);
  const properties = "properties" in resource ? resource.properties : undefined;

  return (
    <Card p="md" withBorder>
      <Stack gap="sm">
        {label ? <Title order={3}>{label}</Title> : null}
        <ResourceClasses classes={resource.class} />
        <PropertyGrid properties={properties} />
        {target ? (
          <Button onClick={() => onNavigate(target.href)} variant="default">
            {linkLabel(target)}
          </Button>
        ) : null}
      </Stack>
    </Card>
  );
}
