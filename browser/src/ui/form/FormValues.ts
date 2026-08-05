export type FormValues = Record<string, unknown>;

export type FormControl = {
  name: string;
  valueType?: "array" | "boolean" | "number";
};

export function readFormValues(
  formData: FormData,
  controls: readonly FormControl[],
  registeredValues: ReadonlyMap<string, unknown>,
): FormValues {
  return Object.fromEntries(
    controls.map(({ name, valueType }) => {
      if (registeredValues.has(name)) return [name, registeredValues.get(name)];
      const entries = formData.getAll(name);

      if (valueType === "array") {
        return [name, entries.filter((value) => value !== "")];
      }
      if (valueType === "boolean") return [name, entries.length > 0];
      if (valueType === "number" && entries[0] !== "") {
        return [name, Number(entries[0])];
      }

      return [
        name,
        entries.length > 1
          ? entries.filter((value) => value !== "")
          : entries[0],
      ];
    }),
  );
}
