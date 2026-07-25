import { Anchor, Breadcrumbs } from "@mantine/core";

type VisitedResource = {
  label: string;
  url: string;
};

type BrowserBreadcrumbsProps = {
  resources: VisitedResource[];
  onNavigate: (url: string) => void;
};

export function BrowserBreadcrumbs({ resources, onNavigate }: BrowserBreadcrumbsProps) {
  if (!resources.length) {
    return null;
  }

  return (
    <Breadcrumbs>
      {resources.map((resource) => (
        <Anchor
          component="button"
          key={resource.url}
          onClick={() => onNavigate(resource.url)}
          type="button"
        >
          {resource.label}
        </Anchor>
      ))}
    </Breadcrumbs>
  );
}
