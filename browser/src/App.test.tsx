import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App, resolveApiUrl } from "./App";
import { CONTENT_ROLE } from "./models/recordContent.generated";

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

  it("upgrades same-host API links on an HTTPS page", () => {
    expect(resolveApiUrl("http://modwire.example/api/scaffoldings", "https://modwire.example/browser/").href)
      .toBe("https://modwire.example/api/scaffoldings");
    expect(resolveApiUrl("http://other.example/api/scaffoldings", "https://modwire.example/browser/").href)
      .toBe("http://other.example/api/scaffoldings");
  });

  it("aborts in-flight API work when the browser unmounts", async () => {
    localStorage.setItem("modwire-api-key", "secret");
    let signal: AbortSignal | null = null;
    vi.spyOn(globalThis, "fetch").mockImplementation((_, init) => {
      signal = init?.signal as AbortSignal;
      return new Promise<Response>(() => undefined);
    });

    const view = render(<App />);
    await waitFor(() => expect(signal).not.toBeNull());
    view.unmount();

    expect(signal!.aborted).toBe(true);
  });

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
        : href.includes("/records/architecture/aggregates") ? { properties: { ...records.entities[0].properties, sources: ["https://example.test"], content: [{ role: CONTENT_ROLE.PARAGRAPH, content: "An aggregate owns consistency.", language: "text", metadata: {} }] } }
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

  it("renders typed list, snippet, and image record blocks", async () => {
    localStorage.setItem("modwire-api-key", "secret");
    vi.spyOn(globalThis, "fetch").mockImplementation(async (input) => {
      const href = String(input);
      const body = href.includes("/catalog") ? collection
        : href.endsWith("/records") ? records
        : href.endsWith("/sections") ? sections
        : href.endsWith("/languages") ? languages
        : href.endsWith("/variables") ? variables
        : href.endsWith("/templates") ? templates
        : href.includes("/records/architecture/aggregates") ? { properties: {
          ...records.entities[0].properties,
          sources: [],
          content: [
            { role: CONTENT_ROLE.SUBHEADING, content: "Rules", language: "en", metadata: {} },
            { role: CONTENT_ROLE.LIST, content: ["Keep boundaries explicit", "Protect invariants"], language: "en", metadata: {} },
            { role: CONTENT_ROLE.SNIPPET, content: "class Aggregate: pass", language: "python", metadata: {} },
            { role: CONTENT_ROLE.IMAGE, content: "https://example.test/aggregate.png", language: "url", metadata: { alt: "Aggregate boundary", title: "Boundary" } },
          ],
        } }
        : href.includes("/forms/react") ? schema
        : root;
      return new Response(JSON.stringify(body), { status: 200 });
    });
    render(<App />);
    fireEvent.click(await screen.findByRole("tab", { name: "Records" }));

    expect(await screen.findByRole("heading", { name: "Rules" })).toBeInTheDocument();
    expect(screen.getByRole("list")).toHaveTextContent("Keep boundaries explicitProtect invariants");
    const snippet = document.querySelector("code.language-python");
    expect(snippet).toHaveTextContent("class Aggregate: pass");
    expect(snippet?.querySelector(".hljs-keyword")).toHaveTextContent("class");
    expect(screen.getByRole("img", { name: "Aggregate boundary" })).toHaveAttribute("src", "https://example.test/aggregate.png");
    expect(screen.getByText("Boundary")).toBeInTheDocument();
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
