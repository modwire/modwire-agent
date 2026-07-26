import type { ComponentType } from "react";
import { SirenObjectInput } from "./inputs/SirenObjectInput";
import { SirenStringListInput } from "./inputs/SirenStringListInput";
import type { SirenActionFormProps } from "./SirenActionForm";
import type { SirenEntityProps } from "./SirenEntity";
import type { SirenFieldProps } from "./SirenField";

export const sirenRegistry = {
  actions: new Map<string, ComponentType<SirenActionFormProps>>(),
  entities: new Map<string, ComponentType<SirenEntityProps>>(),
  fields: new Map<string, ComponentType<SirenFieldProps>>([
    ["list", SirenStringListInput],
    ["object", SirenObjectInput],
  ]),
};
