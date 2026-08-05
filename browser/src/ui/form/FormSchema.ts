import type { FormValues } from "./FormValues";

export type FormSchemaProperty = {
  additionalProperties?: boolean | FormSchemaProperty;
  default?: unknown;
  enum?: unknown[];
  items?: FormSchemaProperty;
  maxItems?: number;
  maxLength?: number;
  minItems?: number;
  minLength?: number;
  nullable?: boolean;
  pattern?: string;
  properties?: Record<string, FormSchemaProperty>;
  required?: string[];
  title?: string;
  type?: string | string[];
};

export type FormSchema = FormSchemaProperty;

function schemaTypes(schema: FormSchemaProperty): string[] {
  if (Array.isArray(schema.type)) return schema.type;
  if (schema.type) return [schema.type];
  if (schema.properties) return ["object"];
  if (schema.items) return ["array"];
  return [];
}

function validateValue(
  schema: FormSchemaProperty,
  value: unknown,
  path: string,
): string | undefined {
  const types = schemaTypes(schema);
  if (value === null) {
    return types.includes("null") || schema.nullable
      ? undefined
      : `${path}: Required`;
  }

  const type = types.find((candidate) => candidate !== "null");
  if (type === "object") {
    if (typeof value !== "object" || Array.isArray(value))
      return `${path}: Enter an object`;
    const record = value as Record<string, unknown>;
    for (const name of schema.required ?? []) {
      if (!Object.hasOwn(record, name) || record[name] === "")
        return `${path}.${name}: Required`;
    }
    for (const [name, childValue] of Object.entries(record)) {
      const childSchema =
        schema.properties?.[name] ??
        (typeof schema.additionalProperties === "object"
          ? schema.additionalProperties
          : undefined);
      if (!childSchema) continue;
      const error = validateValue(childSchema, childValue, `${path}.${name}`);
      if (error) return error;
    }
  }
  if (type === "array") {
    if (!Array.isArray(value)) return `${path}: Enter a list`;
    if (schema.minItems != null && value.length < schema.minItems)
      return `${path}: Add at least ${schema.minItems} items`;
    if (schema.maxItems != null && value.length > schema.maxItems)
      return `${path}: Use at most ${schema.maxItems} items`;
    if (schema.items) {
      for (const [index, item] of value.entries()) {
        const error = validateValue(schema.items, item, `${path}[${index}]`);
        if (error) return error;
      }
    }
  }
  if (type === "string" && typeof value !== "string")
    return `${path}: Enter text`;
  if (
    (type === "number" || type === "integer") &&
    (typeof value !== "number" || !Number.isFinite(value))
  )
    return `${path}: Enter a number`;
  if (type === "integer" && !Number.isInteger(value))
    return `${path}: Enter a whole number`;
  if (type === "boolean" && typeof value !== "boolean")
    return `${path}: Choose true or false`;
  if (schema.enum && !schema.enum.includes(value))
    return `${path}: Choose an allowed value`;
  if (schema.minLength != null && String(value).length < schema.minLength)
    return `${path}: Use at least ${schema.minLength} characters`;
  if (schema.maxLength != null && String(value).length > schema.maxLength)
    return `${path}: Use at most ${schema.maxLength} characters`;
  if (schema.pattern && !new RegExp(schema.pattern).test(String(value)))
    return `${path}: Use the required format`;
  return undefined;
}

export function validateForm(
  schema: FormSchema | undefined,
  values: FormValues,
): Record<string, string> {
  if (!schema) return {};

  return Object.fromEntries(
    Object.entries(schema.properties ?? {}).flatMap(([name, property]) => {
      const value = values[name];
      if (schema.required?.includes(name) && (value == null || value === ""))
        return [[name, "Required"]];
      if (value == null || value === "") return [];
      const error = validateValue(property, value, name);
      return error ? [[name, error]] : [];
    }),
  );
}
