import { MantineProvider } from "@mantine/core";
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";
import { Form } from "../Form";

afterEach(cleanup);

it("preserves falsy and empty form values", async () => {
  const onSubmit = vi.fn();

  render(
    <MantineProvider>
      <Form onSubmit={onSubmit}>
        {() => (
          <>
            <input name="enabled" type="checkbox" />
            <input defaultValue="0" name="limit" type="number" />
            <input defaultValue="" name="description" type="text" />
            <input
              data-siren-type="array"
              name="example_items"
              type="hidden"
              value=""
            />
            <input
              data-siren-type="object"
              name="example_document"
              type="hidden"
              value="{}"
            />
            <button type="submit">Submit</button>
          </>
        )}
      </Form>
    </MantineProvider>,
  );

  fireEvent.click(screen.getByRole("button", { name: "Submit" }));

  await waitFor(() =>
    expect(onSubmit).toHaveBeenCalledWith({
      description: "",
      enabled: false,
      example_document: {},
      example_items: [],
      limit: 0,
    }),
  );
  expect(onSubmit.mock.calls[0][0]).not.toHaveProperty("omitted_value");
});
