import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "./App";

const root = { links: [{ rel: ["scaffoldings"], href: "http://api.test/catalog" }] };
const collection = { entities: [{ properties: { id: "react", name: "React app", description: "A production-ready UI", language: "ts" }, links: [{ rel: ["self"], href: "http://api.test/catalog/react" }] }] };
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
      .mockResolvedValueOnce(new Response(JSON.stringify(resource), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(schema), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ properties: { files: [{ template_id: "1", path: "src/main.tsx", source: "hello", html: "<pre>hello</pre>", language: "tsx" }] } }), { status: 200 }));
    render(<App />);
    expect(await screen.findByRole("heading", { name: "React app" })).toBeInTheDocument();
    expect(await screen.findByLabelText(/Project name/)).toHaveValue("demo");
    fireEvent.click(screen.getByRole("button", { name: /generate preview/i }));
    expect(await screen.findByRole("tab", { name: "src/main.tsx" })).toBeInTheDocument();
    await waitFor(() => expect(fetch).toHaveBeenLastCalledWith(expect.objectContaining({ href: "http://api.test/render/react" }), expect.objectContaining({ method: "POST" })));
  });
});
