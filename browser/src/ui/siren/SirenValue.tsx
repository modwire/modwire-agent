import { Text } from "@mantine/core";
import JsonView from "@uiw/react-json-view";

export type SirenValueProps = { value: unknown };

export function SirenValue({ value }: SirenValueProps) {
  if (value === null) return <Text c="dimmed">None</Text>;
  if (typeof value === "boolean") return <Text>{value ? "Yes" : "No"}</Text>;
  if (typeof value === "string" || typeof value === "number")
    return <Text>{String(value)}</Text>;
  if (typeof value === "object") {
    return (
      <JsonView
        collapsed={false}
        displayDataTypes={false}
        enableClipboard={false}
        value={value}
      />
    );
  }
  return <Text c="dimmed">None</Text>;
}
