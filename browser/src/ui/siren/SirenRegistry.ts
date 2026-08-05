import type { ComponentType } from "react";
import { SirenStructuredInput } from "./inputs/SirenStructuredInput";
import type { SirenActionFormProps } from "./SirenActionForm";
import type { SirenEntityProps } from "./SirenEntity";
import type { SirenFieldProps } from "./SirenField";

export const sirenRegistry = {
  actions: new Map<string, ComponentType<SirenActionFormProps>>(),
  entities: new Map<string, ComponentType<SirenEntityProps>>(),
  fields: new Map<string, ComponentType<SirenFieldProps>>([
    ["list", SirenStructuredInput],
    ["object", SirenStructuredInput],
  ]),
};
