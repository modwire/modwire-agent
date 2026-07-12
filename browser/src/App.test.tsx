import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "./App";

const root = { links: [
  { rel: ["scaffoldings"], href: "http://api.test/catalog" },
  { rel: ["records"], href: "http://api.test/records" },
  { rel: ["sections"], href: "http://api.test/sections" },
  { rel: ["languages"], href: "http://api.test/languages" },
  { rel: ["variables"], href: "http://api.test/variables" },
  { rel: ["templates"], href: "http://api.test/templates" },
] };
const collection = { entities: [{ properties: { id: "react", name: "React app", description: "A production-ready UI", language: "ts" }, links: [{ rel: ["self"], href: "http://api.test/catalog/react" }] }], actions: [{ name: "create_scaffolding", method: "POST", href: "http://api.test/catalog" }] };
const records = { entities: [{ properties: { slug: "architecture/aggregates", section_slug: "architecture", title: "Aggregates", description: "Consistency boundaries", tag_slugs: ["event-sourcing"] }, links: [{ rel: ["self"], href: "http://api.test/records/architecture/aggregates" }] }] };
const sections = { entities: [{ properties: { slug: "architecture", title: "Architecture", description: "Patterns", tag_slugs: [] } }] };
const languages = { entities: [{ properties: { id: "ts", name: "TypeScript" } }] };
const variables = { entities: [], actions: [{ name: "create_variable", method: "POST", href: "http://api.test/variables" }] };
const templates = { entities: [], actions: [{ name: "create_template", method: "POST", href: "http://api.test/templates" }] };
const resource = { properties: collection.entities[0].properties, actions: [
  { name: "get_scaffolding_schema", method: "GET", href: "http://api.test/forms/react" },
  { name: "preview_scaffolding", method: "POST", href: "http://api.test/render/react" },
] };
const schema = { properties: { properties: { project_name: { type: "string", description: "Project name", default: "demo" } }, required: ["project_name"] } };

describe("App", () => {
  beforeEach(() => { localStorage.clear(); vi.restoreAllMocks(); });
  afterEach(cleanup);

  it("asks for an API key before showing the workspace", () => {
    render(<App />);
    expect(screen.getByRole("heading", { name: "Modwire Studio" })).toBeInTheDocument();
    expect(screen.getByLabelText(/API key/)).toBeInTheDocument();
  });

  it("loads scaffoldings and renders a preview", async () => {
    localStorage.setItem("modwire-api-key", "secret");
    vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(JSON.stringify(root), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(collection), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(records), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(sections), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(languages), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(variables), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(templates), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(resource), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(schema), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ properties: { files: [{ template_id: "1", path: "src/main.tsx", source: "hello", html: "<pre>hello</pre>", language: "tsx" }] } }), { status: 200 }));
    render(<App />);
    expect(await screen.findByRole("heading", { name: "React app" })).toBeInTheDocument();
    fireEvent.click(await screen.findByRole("button", { name: "Render preview" }));
    expect(await screen.findByRole("button", { name: "main.tsx" })).toBeInTheDocument();
    await waitFor(() => expect(fetch).toHaveBeenLastCalledWith(expect.objectContaining({ href: "http://api.test/render/react" }), expect.objectContaining({ method: "POST" })));
  });

  it("discovers and browses records through Siren links", async () => {
    localStorage.setItem("modwire-api-key", "secret");
    vi.spyOn(globalThis, "fetch").mockImplementation(async (input) => {
      const href = String(input);
      const body = href.includes("/catalog") ? collection
        : href.endsWith("/records") ? records
        : href.endsWith("/sections") ? sections
        : href.endsWith("/languages") ? languages
        : href.endsWith("/variables") ? variables
        : href.endsWith("/templates") ? templates
        : href.includes("/records/architecture/aggregates") ? { properties: { ...records.entities[0].properties, sources: ["https://example.test"], content: [{ role: "paragraph", content: "An aggregate owns consistency.", language: "text", metadata: {} }] } }
        : href.endsWith("/catalog/react") ? resource
        : href.includes("/forms/react") ? schema
        : root;
      return new Response(JSON.stringify(body), { status: 200 });
    });
    render(<App />);
    fireEvent.click(await screen.findByRole("tab", { name: "Records" }));
    expect(await screen.findByRole("heading", { name: "Aggregates" })).toBeInTheDocument();
    expect(screen.getByText("An aggregate owns consistency.")).toBeInTheDocument();
    expect(screen.getAllByText("Architecture")).toHaveLength(2);
  });

  it("opens API-backed scaffolding and structured variable forms", async () => {
    localStorage.setItem("modwire-api-key", "secret");
    vi.spyOn(globalThis, "fetch").mockImplementation(async (input) => {
      const href = String(input);
      const body = href.includes("/catalog/react") ? resource
        : href.includes("/forms/react") ? { properties: { properties: { nodes: { type: "array", description: "Nodes", default: [{ id: "input", label: "Input" }] } }, required: [] } }
        : href.endsWith("/catalog") ? collection
        : href.endsWith("/records") ? records
        : href.endsWith("/sections") ? sections
        : href.endsWith("/languages") ? languages
        : href.endsWith("/variables") ? variables
        : href.endsWith("/templates") ? templates
        : root;
      return new Response(JSON.stringify(body), { status: 200 });
    });
    render(<App />);
    fireEvent.click(await screen.findByRole("tab", { name: "Build" }));
    expect(await screen.findByLabelText("Id")).toHaveValue("input");
    expect(screen.getByLabelText("Label")).toHaveValue("Input");
    fireEvent.click(screen.getByRole("button", { name: "New scaffolding" }));
    expect(screen.getByRole("dialog", { name: "New scaffolding" })).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText(/Name/), { target: { value: "New scaffold" } });
    fireEvent.change(screen.getByLabelText(/Description/), { target: { value: "New scaffold description" } });
    fireEvent.click(screen.getByRole("button", { name: "Create" }));
    await waitFor(() => {
      const calls = vi.mocked(fetch).mock.calls;
      expect(calls.some(([url, init]) => String(url).endsWith("/catalog") && init?.method === "POST")).toBe(true);
      expect(calls.some(([url, init]) => String(url).endsWith("/templates") && init?.method === "POST")).toBe(true);
    });
  });
});
