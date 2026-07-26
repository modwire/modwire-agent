import type { SirenAction } from "../../client/SirenAction";
import type { SirenEntity } from "../../client/SirenEntity";
import type { SirenLink } from "../../client/SirenLink";
import { EntityDispatcher } from "./EntityDispatcher";

export type SirenBrowserProps = {
  entity: SirenEntity | null;
  isLoading: boolean;
  onFollow: (link: SirenLink) => void;
  onSubmit: (action: SirenAction, values: Record<string, unknown>) => void;
};

export function SirenBrowser({ entity, isLoading, onFollow, onSubmit }: SirenBrowserProps) {
  if (isLoading) {
    return <p role="status">Loading resource…</p>;
  }

  if (!entity) {
    return <p>No resource selected.</p>;
  }

  return <EntityDispatcher entity={entity} onFollow={onFollow} onSubmit={onSubmit} />;
}
