import type { ComponentType } from "react";
import type { Field } from "@siren-js/client";
import { SirenButtonInput } from "./SirenButtonInput";
import { SirenCheckboxInput } from "./SirenCheckboxInput";
import { SirenColorInput } from "./SirenColorInput";
import { SirenDateInput } from "./SirenDateInput";
import { SirenDateTimeLocalInput } from "./SirenDateTimeLocalInput";
import { SirenEmailInput } from "./SirenEmailInput";
import { SirenFileInput } from "./SirenFileInput";
import { SirenHiddenInput } from "./SirenHiddenInput";
import { SirenImageInput } from "./SirenImageInput";
import { SirenMonthInput } from "./SirenMonthInput";
import { SirenNumberInput } from "./SirenNumberInput";
import { SirenObjectInput } from "./SirenObjectInput";
import { SirenPasswordInput } from "./SirenPasswordInput";
import { SirenRadioInput } from "./SirenRadioInput";
import { SirenRangeInput } from "./SirenRangeInput";
import { SirenResetInput } from "./SirenResetInput";
import { SirenSearchInput } from "./SirenSearchInput";
import { SirenStringListInput } from "./SirenStringListInput";
import { SirenSubmitInput } from "./SirenSubmitInput";
import { SirenTelInput } from "./SirenTelInput";
import { SirenTextInput } from "./SirenTextInput";
import { SirenTextarea } from "./SirenTextarea";
import { SirenTimeInput } from "./SirenTimeInput";
import { SirenUrlInput } from "./SirenUrlInput";
import { SirenWeekInput } from "./SirenWeekInput";

export type SirenInputProps = { field: Field };

const inputRegistry: Record<string, ComponentType<SirenInputProps>> = {
  button: SirenButtonInput,
  checkbox: SirenCheckboxInput,
  color: SirenColorInput,
  date: SirenDateInput,
  "datetime-local": SirenDateTimeLocalInput,
  email: SirenEmailInput,
  file: SirenFileInput,
  hidden: SirenHiddenInput,
  image: SirenImageInput,
  list: SirenStringListInput,
  month: SirenMonthInput,
  number: SirenNumberInput,
  object: SirenObjectInput,
  password: SirenPasswordInput,
  radio: SirenRadioInput,
  range: SirenRangeInput,
  reset: SirenResetInput,
  search: SirenSearchInput,
  submit: SirenSubmitInput,
  tel: SirenTelInput,
  text: SirenTextInput,
  textarea: SirenTextarea,
  time: SirenTimeInput,
  url: SirenUrlInput,
  week: SirenWeekInput,
};

export function SirenInput({ field }: SirenInputProps) {
  const Input = inputRegistry[field.type] ?? SirenTextInput;

  return <Input field={field} />;
}
