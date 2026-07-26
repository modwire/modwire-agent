import type { FormValues } from "./FormValues";

export type FormSchema = {
  properties?: Record<
    string,
    {
      enum?: unknown[];
      maxLength?: number;
      minLength?: number;
      pattern?: string;
      type?: string;
    }
  >;
  required?: string[];
};

export function validateForm(
  schema: FormSchema | undefined,
  values: FormValues,
): Record<string, string> {
  if (!schema) return {};

  return Object.fromEntries(
    Object.entries(schema.properties ?? {}).flatMap(([name, property]) => {
      const value = values[name];
      if (
        schema.required?.includes(name) &&
        (value == null ||
          value === "" ||
          (Array.isArray(value) && !value.length))
      )
        return [[name, "Required"]];
      if (value == null || value === "") return [];
      if (property.type === "array" && !Array.isArray(value))
        return [[name, "Enter a list"]];
      if (
        property.type === "object" &&
        (typeof value !== "object" || Array.isArray(value))
      )
        return [[name, "Enter an object"]];
      if (property.type === "number" && !Number.isFinite(Number(value)))
        return [[name, "Enter a number"]];
      if (property.enum && !property.enum.includes(value))
        return [[name, "Choose an allowed value"]];
      if (
        property.minLength != null &&
        String(value).length < property.minLength
      )
        return [[name, `Use at least ${property.minLength} characters`]];
      if (
        property.maxLength != null &&
        String(value).length > property.maxLength
      )
        return [[name, `Use at most ${property.maxLength} characters`]];
      if (property.pattern && !new RegExp(property.pattern).test(String(value)))
        return [[name, "Use the required format"]];
      return [];
    }),
  );
}
