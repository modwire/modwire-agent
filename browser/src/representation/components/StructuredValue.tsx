import { JsonInput } from "@mantine/core";

type StructuredValueProps = {
  value: object;
};

export function StructuredValue({ value }: StructuredValueProps) {
  return <JsonInput formatOnBlur={false} minRows={2} readOnly value={JSON.stringify(value, null, 2)} />;
}
