import { MantineProvider } from "@mantine/core";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { Entity } from "siren-parser";
import { afterEach, expect, it, vi } from "vitest";
import type { SirenResource } from "../../siren/client";
import { ResourcePage } from "../components/ResourcePage";

afterEach(cleanup);

function resource(document: object): SirenResource {
  return {
    document: document as SirenResource["document"],
    entity: Entity(document),
    status: 200,
    url: "http://localhost:8000/siren/records",
  };
}

function renderPage(document: object, onNavigate = vi.fn()) {
  render(
    <MantineProvider>
      <ResourcePage isLoading={false} onNavigate={onNavigate} resource={resource(document)} />
    </MantineProvider>,
  );

  return onNavigate;
}

it("renders entity properties, classes, structured values, links, and embedded entities", () => {
  const onNavigate = renderPage({
    class: ["record"],
    title: "Record",
    properties: { title: "HTTP", metadata: { method: "GET", fields: ["path"] } },
    links: [{ rel: ["self"], href: "/siren/records/http" }],
    entities: [
      {
        rel: ["related"],
        class: ["tag"],
        title: "network",
        properties: { title: "network" },
        links: [{ rel: ["self"], href: "/siren/tags/network" }],
      },
    ],
  });

  expect(screen.getByRole("heading", { name: "Record" })).toBeVisible();
  expect(screen.getByText("record")).toBeVisible();
  expect(screen.getByText("metadata")).toBeVisible();
  expect(screen.getByDisplayValue(/"method": "GET"/)).toBeVisible();
  expect(screen.getByRole("heading", { name: "network" })).toBeVisible();

  fireEvent.click(screen.getByRole("button", { name: /\/siren\/records\/http/ }));
  expect(onNavigate).toHaveBeenCalledWith("/siren/records/http");
});

it("renders collections as a flat list without repeating collection or item metadata", () => {
  const onNavigate = renderPage({
    class: ["collection"],
    title: "Records",
    entities: [
      {
        rel: ["item"],
        class: ["record"],
        title: "HTTP",
        properties: { date: "2026-07-26" },
        links: [{ rel: ["self"], href: "/siren/records/http" }],
      },
      { rel: ["item"], class: ["record"], title: "No target", properties: { title: "No target" } },
    ],
  });

  expect(screen.getByRole("list")).toBeVisible();
  expect(screen.getAllByRole("listitem")).toHaveLength(2);
  expect(screen.queryByRole("heading", { name: "Records" })).not.toBeInTheDocument();
  expect(screen.queryByText("collection")).not.toBeInTheDocument();
  expect(screen.getByRole("button", { name: "HTTP" })).toBeVisible();
  expect(screen.getByText("2026-07-26")).toBeVisible();
  expect(screen.getByText("No target")).toBeVisible();

  fireEvent.click(screen.getByRole("button", { name: "HTTP" }));
  expect(onNavigate).toHaveBeenCalledWith("/siren/records/http");
  expect(screen.queryByRole("button", { name: /No target/ })).not.toBeInTheDocument();
});

it("renders an empty representation and an advertised error representation", () => {
  const { rerender } = render(
    <MantineProvider>
      <ResourcePage isLoading={false} onNavigate={vi.fn()} resource={resource({ class: ["empty"] })} />
    </MantineProvider>,
  );

  expect(screen.getByText("empty")).toBeVisible();

  rerender(
    <MantineProvider>
      <ResourcePage
        isLoading={false}
        onNavigate={vi.fn()}
        resource={resource({ class: ["error"], properties: { detail: "Request failed" } })}
      />
    </MantineProvider>,
  );

  expect(screen.getByText("Request failed")).toBeVisible();
});

it("renders an accessible loading state", () => {
  render(
    <MantineProvider>
      <ResourcePage isLoading onNavigate={vi.fn()} resource={null} />
    </MantineProvider>,
  );

  expect(screen.getByLabelText("Loading resource")).toBeVisible();
});
