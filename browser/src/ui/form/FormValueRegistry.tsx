import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  type ReactNode,
} from "react";

export type FormValueRegistry = {
  remove: (name: string) => void;
  set: (name: string, value: unknown) => void;
};

const FormValueContext = createContext<FormValueRegistry | undefined>(
  undefined,
);

export function FormValueProvider({
  children,
  registry,
}: {
  children: ReactNode;
  registry: FormValueRegistry;
}) {
  return (
    <FormValueContext.Provider value={registry}>
      {children}
    </FormValueContext.Provider>
  );
}

export function useFormValue(name: string, value: unknown) {
  const registry = useContext(FormValueContext);
  if (!registry) throw new Error("Form value used outside Form.");

  useEffect(() => {
    registry.set(name, value);
    return () => registry.remove(name);
  }, [name, registry, value]);

  return useCallback(
    (nextValue: unknown) => registry.set(name, nextValue),
    [name, registry],
  );
}
