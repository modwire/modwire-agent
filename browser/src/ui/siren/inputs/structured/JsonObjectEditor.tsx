import { Button, Fieldset, Stack, TextInput } from "@mantine/core";
import type { ReactNode } from "react";
import { initialValue } from "./JsonValue";
import type {
  JsonEditorProps,
  JsonEditorRenderer,
  JsonValue,
} from "./JsonValue";

type JsonObjectEditorProps = JsonEditorProps & {
  nullControl: ReactNode;
  renderEditor: JsonEditorRenderer;
};

export function JsonObjectEditor({
  nullControl,
  onChange,
  path,
  renderEditor,
  schema,
  value,
}: JsonObjectEditorProps) {
  const objectValue =
    value !== null && !Array.isArray(value) && typeof value === "object"
      ? value
      : {};
  const properties = schema.properties ?? {};
  const knownNames = new Set(Object.keys(properties));
  const additionalSchema =
    typeof schema.additionalProperties === "object"
      ? schema.additionalProperties
      : {};
  const additionalNames = Object.keys(objectValue).filter(
    (name) => !knownNames.has(name),
  );
  const setProperty = (name: string, propertyValue: JsonValue) =>
    onChange({ ...objectValue, [name]: propertyValue });
  const removeProperty = (name: string) => {
    const nextValue = { ...objectValue };
    delete nextValue[name];
    onChange(nextValue);
  };

  return (
    <Stack gap="sm">
      {nullControl}
      {Object.entries(properties).map(([name, propertySchema]) => {
        const required = schema.required?.includes(name) ?? false;
        if (!Object.hasOwn(objectValue, name)) {
          return (
            <Button
              key={name}
              onClick={() => setProperty(name, initialValue(propertySchema))}
              size="xs"
              type="button"
              variant="light"
            >
              Add {propertySchema.title ?? name}
              {required ? " *" : ""}
            </Button>
          );
        }

        return (
          <Fieldset
            key={name}
            legend={`${propertySchema.title ?? name}${required ? " *" : ""}`}
          >
            <Stack gap="xs">
              {renderEditor({
                onChange: (propertyValue) => setProperty(name, propertyValue),
                path: `${path}.${name}`,
                schema: propertySchema,
                value: objectValue[name],
              })}
              {required ? null : (
                <Button
                  onClick={() => removeProperty(name)}
                  size="xs"
                  type="button"
                  variant="subtle"
                >
                  Remove {propertySchema.title ?? name}
                </Button>
              )}
            </Stack>
          </Fieldset>
        );
      })}
      {additionalNames.map((name, index) => (
        <Fieldset key={name} legend={name}>
          <Stack gap="xs">
            <TextInput
              aria-label={`${path} property ${index + 1} name`}
              onChange={(event) => {
                const nextName = event.currentTarget.value;
                if (
                  !nextName ||
                  nextName === name ||
                  Object.hasOwn(objectValue, nextName)
                )
                  return;
                const nextValue = {
                  ...objectValue,
                  [nextName]: objectValue[name],
                };
                delete nextValue[name];
                onChange(nextValue);
              }}
              value={name}
            />
            {renderEditor({
              onChange: (propertyValue) => setProperty(name, propertyValue),
              path: `${path}.${name}`,
              schema: additionalSchema,
              value: objectValue[name],
            })}
            <Button
              onClick={() => removeProperty(name)}
              size="xs"
              type="button"
              variant="subtle"
            >
              Remove {name}
            </Button>
          </Stack>
        </Fieldset>
      ))}
      {schema.additionalProperties === false ? null : (
        <Button
          onClick={() => {
            let index = 1;
            while (Object.hasOwn(objectValue, `example_property_${index}`))
              index += 1;
            setProperty(
              `example_property_${index}`,
              initialValue(additionalSchema),
            );
          }}
          size="xs"
          type="button"
          variant="light"
        >
          Add property to {path}
        </Button>
      )}
    </Stack>
  );
}
