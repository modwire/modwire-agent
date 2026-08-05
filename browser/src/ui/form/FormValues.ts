export type FormValues = Record<string, unknown>;

function controls(
  form: HTMLFormElement,
  name: string,
): (HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement)[] {
  const control = form.elements.namedItem(name);
  const elements =
    control instanceof RadioNodeList ? Array.from(control) : [control];

  return elements.filter(
    (
      element,
    ): element is HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement =>
      element instanceof HTMLInputElement ||
      element instanceof HTMLSelectElement ||
      element instanceof HTMLTextAreaElement,
  );
}

export function readFormValues(form: HTMLFormElement): FormValues {
  const formData = new FormData(form);
  const checkboxNames = Array.from(form.elements).flatMap((element) =>
    element instanceof HTMLInputElement &&
    element.type === "checkbox" &&
    element.name
      ? [element.name]
      : [],
  );
  const names = new Set([...formData.keys(), ...checkboxNames]);

  return Object.fromEntries(
    [...names].map((name) => {
      const entries = formData.getAll(name);
      const fieldControls = controls(form, name);
      const sirenType = fieldControls.find(
        (control) => control.dataset.sirenType,
      )?.dataset.sirenType;

      if (sirenType === "object" || sirenType === "json") {
        return [name, JSON.parse(String(entries[0]))];
      }
      if (sirenType === "array") {
        return [name, entries.filter((value) => value !== "")];
      }

      const checkboxes = fieldControls.filter(
        (control): control is HTMLInputElement =>
          control instanceof HTMLInputElement && control.type === "checkbox",
      );
      if (checkboxes.length === 1) {
        return [name, checkboxes[0].checked];
      }
      if (checkboxes.length > 1) {
        return [name, entries.filter((value) => value !== "")];
      }

      const number = fieldControls.find(
        (control) =>
          control instanceof HTMLInputElement && control.type === "number",
      );
      if (number && entries[0] !== "") {
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
