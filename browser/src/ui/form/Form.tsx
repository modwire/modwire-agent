import { useForm } from "@mantine/form";
import type { FormEvent, ReactNode } from "react";
import { FormErrors } from "./FormErrors";
import type { FormSchema } from "./FormSchema";
import { validateForm } from "./FormSchema";
import type { FormValues } from "./FormValues";
import { readFormValues } from "./FormValues";

export type FormProps = {
  children: (errors: Record<string, string>) => ReactNode;
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

export function Form({ children, onSubmit, schema }: FormProps) {
  const form = useForm<FormValues>({ initialValues: {} });

  return (
    <form
      noValidate
      onSubmit={async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const values = readFormValues(event.currentTarget);
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
  );
}
