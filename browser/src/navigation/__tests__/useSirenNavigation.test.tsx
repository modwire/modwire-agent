import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";
import { App } from "../../app/App";

const rootUrl = new URL("/siren/", window.location.origin).href;
const recordsUrl = new URL("/siren/records", window.location.origin).href;

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  window.history.replaceState(null, "", "/");
});

it("navigates from advertised root links and records browser history", async () => {
  const fetchMock = vi.fn((input: string) =>
    Promise.resolve(
      new Response(
        JSON.stringify(
          input === rootUrl
            ? {
                class: ["api", "entry-point"],
                links: [{ href: recordsUrl, rel: ["collection"] }],
                properties: { title: "Modwire API" },
              }
            : { class: ["collection"], links: [], properties: { title: "Records" } },
        ),
        { headers: { "content-type": "application/vnd.siren+json" } },
      ),
    ),
  );
  vi.stubGlobal("fetch", fetchMock);

  render(<App />);

  const navigation = await within(await screen.findByTestId("root-navigation")).findByRole("button", {
    name: /\/siren\/records/,
  });
  fireEvent.click(navigation);

  await waitFor(() => expect(fetchMock).toHaveBeenCalledWith(recordsUrl, expect.any(Object)));
  expect(window.location.search).toContain(encodeURIComponent(recordsUrl));
  expect(screen.getByLabelText("Back")).toBeEnabled();
  expect(await screen.findByRole("button", { name: "Records" })).toBeVisible();

  fireEvent.click(screen.getByLabelText("Back"));

  await waitFor(() => expect(screen.getByLabelText("Resource address")).toHaveValue(rootUrl));
  expect(screen.getByLabelText("Back")).toBeDisabled();
  expect(screen.getByLabelText("Forward")).toBeEnabled();
});

it("keeps invalid pasted resource addresses recoverable", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue(
      new Response(JSON.stringify({ links: [], properties: { title: "Modwire API" } }), {
        headers: { "content-type": "application/vnd.siren+json" },
      }),
    ),
  );
  render(<App />);

  const address = await screen.findByLabelText("Resource address");
  fireEvent.change(address, { target: { value: "not a URL" } });
  fireEvent.submit(address.closest("form")!);

  expect(await screen.findByRole("alert")).toHaveTextContent("Invalid URL");
  expect(screen.getByLabelText("Retry")).toBeVisible();
});

it("opens a pasted Siren resource path", async () => {
  const fetchMock = vi.fn().mockResolvedValue(
    new Response(JSON.stringify({ class: ["collection"], links: [], properties: { title: "Records" } }), {
      headers: { "content-type": "application/vnd.siren+json" },
    }),
  );
  vi.stubGlobal("fetch", fetchMock);
  render(<App />);

  const address = await screen.findByLabelText("Resource address");
  fireEvent.change(address, { target: { value: "/siren/records" } });
  fireEvent.submit(address.closest("form")!);

  await waitFor(() => expect(fetchMock).toHaveBeenCalledWith(recordsUrl, expect.any(Object)));
  expect(address).toHaveValue(recordsUrl);
});

it("surfaces Siren navigation errors with their advertised detail", async () => {
  const fetchMock = vi.fn((input: string) =>
    Promise.resolve(
      new Response(
        JSON.stringify(
          input === rootUrl
            ? {
                class: ["api", "entry-point"],
                links: [{ href: recordsUrl, rel: ["collection"] }],
                properties: { title: "Modwire API" },
              }
            : { class: ["error"], links: [{ href: recordsUrl, rel: ["self"] }], properties: { detail: "Request failed." } },
        ),
        {
          headers: { "content-type": "application/vnd.siren+json" },
          status: input === rootUrl ? 200 : 422,
        },
      ),
    ),
  );
  vi.stubGlobal("fetch", fetchMock);
  render(<App />);

  fireEvent.click(
    await within(await screen.findByTestId("root-navigation")).findByRole("button", { name: /\/siren\/records/ }),
  );

  expect(await screen.findByRole("alert")).toHaveTextContent("Request failed.");
  expect(screen.getByLabelText("Retry")).toBeVisible();
});
