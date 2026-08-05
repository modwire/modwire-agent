import { Button, Fieldset, Stack } from "@mantine/core";
import type { ReactNode } from "react";
import { initialValue } from "./JsonValue";
import type { JsonEditorProps, JsonEditorRenderer } from "./JsonValue";

type JsonArrayEditorProps = JsonEditorProps & {
  nullControl: ReactNode;
  renderEditor: JsonEditorRenderer;
};

export function JsonArrayEditor({
  nullControl,
  onChange,
  path,
  renderEditor,
  schema,
  value,
}: JsonArrayEditorProps) {
  const items = Array.isArray(value) ? value : [];
  const itemSchema = schema.items ?? {};

  return (
    <Stack gap="sm">
      {nullControl}
      {items.map((item, index) => (
        <Fieldset key={index} legend={`Item ${index + 1}`}>
          <Stack gap="xs">
            {renderEditor({
              onChange: (itemValue) =>
                onChange(
                  items.map((current, itemIndex) =>
                    itemIndex === index ? itemValue : current,
                  ),
                ),
              path: `${path}[${index}]`,
              schema: itemSchema,
              value: item,
            })}
            <Button
              onClick={() =>
                onChange(items.filter((_, itemIndex) => itemIndex !== index))
              }
              size="xs"
              type="button"
              variant="subtle"
            >
              Remove item {index + 1} from {path}
            </Button>
          </Stack>
        </Fieldset>
      ))}
      <Button
        onClick={() => onChange([...items, initialValue(itemSchema)])}
        size="xs"
        type="button"
        variant="light"
      >
        Add item to {path}
      </Button>
    </Stack>
  );
}
