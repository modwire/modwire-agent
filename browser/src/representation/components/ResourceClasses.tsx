import { Badge, Group } from "@mantine/core";

type ResourceClassesProps = {
  classes: string[] | undefined;
};

export function ResourceClasses({ classes }: ResourceClassesProps) {
  if (!classes?.length) {
    return null;
  }

  return (
    <Group gap="xs">
      {classes.map((resourceClass) => (
        <Badge key={resourceClass} variant="light">
          {resourceClass}
        </Badge>
      ))}
    </Group>
  );
}
