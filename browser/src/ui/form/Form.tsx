import { useForm } from "@mantine/form";
import { useMemo, useRef, type FormEvent, type ReactNode } from "react";
import { FormErrors } from "./FormErrors";
import type { FormSchema } from "./FormSchema";
import { validateForm } from "./FormSchema";
import type { FormControl, FormValues } from "./FormValues";
import { readFormValues } from "./FormValues";
import { FormValueProvider } from "./FormValueRegistry";

export type FormProps = {
  children: (errors: Record<string, string>) => ReactNode;
  controls: readonly FormControl[];
  onSubmit: (values: FormValues) => Promise<void> | void;
  schema?: FormSchema;
};

function submittedErrors(reason: unknown): Record<string, string> {
  const message =
    reason instanceof Error ? reason.message : "Unable to submit the form.";
  if (!(reason instanceof Error) || !("fieldErrors" in reason))
    return { _form: message };
  const value = reason.fieldErrors;
  const fieldErrors =
    typeof value === "object" && value !== null
      ? Object.fromEntries(
          Object.entries(value).filter(
            (entry): entry is [string, string] => typeof entry[1] === "string",
          ),
        )
      : {};
  return { ...fieldErrors, _form: message };
}

export function Form({ children, controls, onSubmit, schema }: FormProps) {
  const form = useForm<FormValues>({ initialValues: {} });
  const registeredValues = useRef(new Map<string, unknown>());
  const registry = useMemo(
    () => ({
      remove: (name: string) => registeredValues.current.delete(name),
      set: (name: string, value: unknown) =>
        registeredValues.current.set(name, value),
    }),
    [],
  );

  return (
    <FormValueProvider registry={registry}>
      <form
        noValidate
        onSubmit={async (event: FormEvent<HTMLFormElement>) => {
          event.preventDefault();
          const values = readFormValues(
            new FormData(event.currentTarget),
            controls,
            registeredValues.current,
          );
          const errors = validateForm(schema, values);
          form.setValues(values);
          form.setErrors(errors);
          if (Object.keys(errors).length) return;
          try {
            await onSubmit(values);
          } catch (reason) {
            form.setErrors(submittedErrors(reason));
          }
        }}
      >
        <FormErrors
          errors={Object.fromEntries(
            Object.entries(form.errors).map(([name, error]) => [
              name,
              String(error),
            ]),
          )}
        />
        {children(
          Object.fromEntries(
            Object.entries(form.errors).map(([name, error]) => [
              name,
              String(error),
            ]),
          ),
        )}
      </form>
    </FormValueProvider>
  );
}
