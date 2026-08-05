import Ajv2020 from "ajv/dist/2020";
import { customizeValidator } from "@rjsf/validator-ajv8";

export const jsonSchemaValidator = customizeValidator({
  AjvClass: Ajv2020,
  ajvOptionsOverrides: { strict: false },
});
