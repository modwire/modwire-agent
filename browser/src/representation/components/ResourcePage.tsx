import type { SirenResource } from "../../siren/client";
import { CollectionRepresentation } from "./CollectionRepresentation";
import { EmptyRepresentation } from "./EmptyRepresentation";
import { EntityRepresentation } from "./EntityRepresentation";
import { RepresentationLoading } from "./RepresentationLoading";

type ResourcePageProps = {
  isLoading: boolean;
  onNavigate: (url: string) => void;
  resource: SirenResource | null;
};

export function ResourcePage({ isLoading, onNavigate, resource }: ResourcePageProps) {
  if (isLoading) {
    return <RepresentationLoading />;
  }

  if (!resource) {
    return null;
  }

  const { entity } = resource;

  if (entity.class?.includes("collection")) {
    return <CollectionRepresentation entity={entity} onNavigate={onNavigate} resourceUrl={resource.url} />;
  }

  if (entity.class?.includes("error") || entity.properties || entity.links?.length || entity.entities?.length) {
    return <EntityRepresentation entity={entity} onNavigate={onNavigate} />;
  }

  return <EmptyRepresentation entity={entity} />;
}
