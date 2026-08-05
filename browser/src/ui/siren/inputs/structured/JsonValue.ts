import type { ReactNode } from "react";
import type { FormSchemaProperty } from "../../../form/FormSchema";

export type JsonValue =
  | boolean
  | number
  | string
  | null
  | JsonValue[]
  | { [name: string]: JsonValue };

export type JsonEditorProps = {
  onChange: (value: JsonValue) => void;
  path: string;
  schema: FormSchemaProperty;
  value: JsonValue;
};

export type JsonEditorRenderer = (props: JsonEditorProps) => ReactNode;

export const JSON_TYPES = [
  "string",
  "number",
  "boolean",
  "object",
  "array",
  "null",
];

export function schemaTypes(schema: FormSchemaProperty): string[] {
  if (Array.isArray(schema.type)) return schema.type;
  if (schema.type) return [schema.type];
  if (schema.properties) return ["object"];
  if (schema.items) return ["array"];
  return [];
}

export function valueType(value: JsonValue): string {
  if (value === null) return "null";
  if (Array.isArray(value)) return "array";
  return typeof value;
}

export function isJsonValue(value: unknown): value is JsonValue {
  if (value === null || typeof value === "boolean" || typeof value === "string")
    return true;
  if (typeof value === "number") return Number.isFinite(value);
  if (Array.isArray(value)) return value.every(isJsonValue);
  if (typeof value === "object") return Object.values(value).every(isJsonValue);
  return false;
}

export function initialValue(schema: FormSchemaProperty): JsonValue {
  if (isJsonValue(schema.default)) return structuredClone(schema.default);
  const type = schemaTypes(schema).find((candidate) => candidate !== "null");
  if (type === "object") {
    return Object.fromEntries(
      (schema.required ?? []).map((name) => [
        name,
        initialValue(schema.properties?.[name] ?? {}),
      ]),
    );
  }
  if (type === "array") return [];
  if (type === "boolean") return false;
  if (type === "number" || type === "integer") return 0;
  if (type === "null") return null;
  return "";
}

export function normalizeValue(
  value: unknown,
  schema: FormSchemaProperty,
): JsonValue {
  if (!isJsonValue(value)) return initialValue(schema);
  if (value !== null && !Array.isArray(value) && typeof value === "object") {
    const result = structuredClone(value);
    for (const name of schema.required ?? []) {
      if (!Object.hasOwn(result, name))
        result[name] = initialValue(schema.properties?.[name] ?? {});
    }
    return result;
  }
  return structuredClone(value);
}
