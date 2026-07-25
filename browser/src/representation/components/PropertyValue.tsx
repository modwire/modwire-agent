import { Text } from "@mantine/core";
import { StructuredValue } from "./StructuredValue";

type PropertyValueProps = {
  value: unknown;
};

export function PropertyValue({ value }: PropertyValueProps) {
  if (typeof value === "object" && value !== null) {
    return <StructuredValue value={value} />;
  }

  if (typeof value === "string") {
    return <Text>{value}</Text>;
  }

  return <Text>{JSON.stringify(value)}</Text>;
}
