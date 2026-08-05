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
          form.setErrors({
            _form:
              reason instanceof Error
                ? reason.message
                : "Unable to submit the form.",
          });
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
