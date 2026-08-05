import type { Field } from "@siren-js/client";
import { JsonEditor, type JsonData } from "json-edit-react";
import { useState } from "react";
import { useFormValue } from "../../form/FormValueRegistry";

export type SirenJsonInputProps = {
  field: Field;
};

export function SirenJsonInput({ field }: SirenJsonInputProps) {
  const [value, setValue] = useState<JsonData>(field.value);
  const publishValue = useFormValue(field.name, value);

  const updateValue = (nextValue: JsonData) => {
    setValue(nextValue);
    publishValue(nextValue);
  };

  return (
    <JsonEditor
      data={value}
      rootName={field.name}
      setData={updateValue}
      showCollectionCount="when-closed"
      showIconTooltips
    />
  );
}
