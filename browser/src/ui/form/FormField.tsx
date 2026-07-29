import { Input } from "@mantine/core";
import type { ReactNode } from "react";

export type FormFieldProps = {
  children: ReactNode;
  error?: string;
  label: string;
};

export function FormField({ children, error, label }: FormFieldProps) {
  return (
    <Input.Wrapper error={error} label={label}>
      {children}
    </Input.Wrapper>
  );
}
