import type { ComponentType } from "react";
import type { Field } from "@siren-js/client";
import { Input as GenericInput } from "../../input/Input";
import { SirenObjectInput } from "./SirenObjectInput";
import { SirenStringListInput } from "./SirenStringListInput";

export type SirenInputProps = { field: Field };

const inputRegistry: Record<string, ComponentType<SirenInputProps>> = {
  list: SirenStringListInput,
  object: SirenObjectInput,
};

export function SirenInput({ field }: SirenInputProps) {
  const Input = inputRegistry[field.type] ?? GenericInput;

  return <Input field={field} />;
}
