import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from "@testing-library/react";
import { StrictMode } from "react";
import { afterEach, expect, it, vi } from "vitest";
import { App } from "../App";

const sirenClient = vi.hoisted(() => ({
  execute: vi.fn(),
  get: vi.fn(),
}));

vi.mock("../../client/SirenClient", () => ({
  SirenClient: class {
    execute = sirenClient.execute;
    get = sirenClient.get;
  },
}));

const rootEntity = {
  actions: [],
  class: ["api", "entry-point"],
  entities: [],
  links: [
    { href: "/example-siren/", rel: ["self"], title: "Modwire API" },
    {
      href: "/example-resources",
      rel: ["collection"],
      title: "Example resources",
    },
  ],
  properties: { title: "Modwire API" },
  title: "Modwire API",
};

afterEach(() => {
  cleanup();
  vi.resetAllMocks();
  window.history.replaceState(null, "", "/");
});

it("loads the configured root once for navigation and content", async () => {
  sirenClient.get.mockResolvedValue(rootEntity);

  const { container } = render(
    <StrictMode>
      <App rootTarget="/example-siren/" />
    </StrictMode>,
  );

  expect(container.querySelector("header")).not.toBeNull();
  expect(container.querySelector("main")).not.toBeNull();
  expect(container.querySelector("footer")).not.toBeNull();
  expect(
    await screen.findByRole("heading", { name: "Modwire API" }),
  ).toBeInTheDocument();
  expect(
    screen.getByRole("link", { name: "Example resources" }),
  ).toBeInTheDocument();
  expect(sirenClient.get).toHaveBeenCalledTimes(1);
  expect(sirenClient.get).toHaveBeenCalledWith("/example-siren/");
});

it("loads the root once alongside a deep-linked resource", async () => {
  window.history.replaceState(null, "", "/#/example-resources");
  sirenClient.get.mockImplementation(async (target: string) =>
    target === "/example-siren/"
      ? rootEntity
      : {
          actions: [],
          class: ["example-resource"],
          entities: [],
          links: [],
          properties: {},
          title: "Current example resource",
        },
  );

  render(<App rootTarget="/example-siren/" />);

  expect(
    await screen.findByRole("heading", { name: "Current example resource" }),
  ).toBeInTheDocument();
  expect(
    screen.getByRole("link", { name: "Example resources" }),
  ).toBeInTheDocument();
  await waitFor(() => expect(sirenClient.get).toHaveBeenCalledTimes(2));
  expect(
    sirenClient.get.mock.calls.filter(
      ([target]) => target === "/example-siren/",
    ),
  ).toHaveLength(1);
});

it("shows a root failure and retries without reloading the page", async () => {
  sirenClient.get
    .mockRejectedValueOnce(new Error("Entry point unavailable"))
    .mockResolvedValueOnce(rootEntity);

  render(<App rootTarget="/example-siren/" />);

  expect(await screen.findByRole("alert")).toHaveTextContent(
    "Entry point unavailable",
  );
  fireEvent.click(screen.getByRole("button", { name: "Retry" }));

  expect(
    await screen.findByRole("heading", { name: "Modwire API" }),
  ).toBeInTheDocument();
  expect(window.location.pathname).toBe("/");
  expect(sirenClient.get).toHaveBeenCalledTimes(2);
});

it("retries failed navigation without replacing a deep-linked resource", async () => {
  window.history.replaceState(null, "", "/#/example-resources");
  sirenClient.get.mockImplementation(async (target: string) => {
    if (target === "/example-siren/" && sirenClient.get.mock.calls.length === 1)
      throw new Error("Navigation unavailable");
    return target === "/example-siren/"
      ? rootEntity
      : {
          actions: [],
          class: ["example-resource"],
          entities: [],
          links: [],
          properties: {},
          title: "Current example resource",
        };
  });

  render(<App rootTarget="/example-siren/" />);

  expect(
    await screen.findByRole("heading", { name: "Current example resource" }),
  ).toBeInTheDocument();
  expect(screen.getByRole("alert")).toHaveTextContent("Navigation unavailable");
  fireEvent.click(screen.getByRole("button", { name: "Retry navigation" }));

  expect(
    await screen.findByRole("link", { name: "Example resources" }),
  ).toBeInTheDocument();
  expect(
    screen.getByRole("heading", { name: "Current example resource" }),
  ).toBeInTheDocument();
  expect(window.location.hash).toBe("#/example-resources");
});

it("keeps an action form mounted while showing structured submission errors", async () => {
  let rejectSubmission: (reason: unknown) => void = () => undefined;
  sirenClient.get.mockResolvedValue({
    ...rootEntity,
    actions: [
      {
        fields: [
          {
            name: "example_property",
            title: "Example property",
            type: "text",
          },
        ],
        href: "/example-resources",
        method: "POST",
        name: "create-example",
        title: "Create example",
      },
    ],
  });
  sirenClient.execute.mockReturnValue(
    new Promise((_resolve, reject) => {
      rejectSubmission = reject;
    }),
  );

  render(<App rootTarget="/example-siren/" />);

  fireEvent.click(
    await screen.findByRole("button", { name: "Create example" }),
  );
  expect(
    screen.getByRole("heading", { name: "Modwire API" }),
  ).toBeInTheDocument();

  rejectSubmission(
    Object.assign(new Error("Validation failed"), {
      fieldErrors: { example_property: "This value is required." },
    }),
  );

  expect(await screen.findByText("This value is required.")).toBeVisible();
  expect(
    screen.getByRole("heading", { name: "Modwire API" }),
  ).toBeInTheDocument();
  expect(screen.queryByText("Unable to load resource")).not.toBeInTheDocument();
});
