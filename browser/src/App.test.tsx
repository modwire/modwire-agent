import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { App } from "./App";

const collection = { entities: [{ properties: { id: "react", name: "React app", description: "A production-ready UI", language: "ts" } }] };
const schema = { properties: { properties: { project_name: { type: "string", description: "Project name", default: "demo" } }, required: ["project_name"] } };

describe("App", () => {
  beforeEach(() => { localStorage.clear(); vi.restoreAllMocks(); });

  it("asks for an API key before showing the workspace", () => {
    render(<App />);
    expect(screen.getByRole("heading", { name: "Modwire Studio" })).toBeInTheDocument();
    expect(screen.getByLabelText(/API key/)).toBeInTheDocument();
  });

  it("loads scaffoldings and renders a preview", async () => {
    localStorage.setItem("modwire-api-key", "secret");
    vi.spyOn(globalThis, "fetch")
      .mockResolvedValueOnce(new Response(JSON.stringify(collection), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify(schema), { status: 200 }))
      .mockResolvedValueOnce(new Response(JSON.stringify({ properties: { files: [{ template_id: "1", path: "src/main.tsx", source: "hello", html: "<pre>hello</pre>", language: "tsx" }] } }), { status: 200 }));
    render(<App />);
    expect(await screen.findByRole("heading", { name: "React app" })).toBeInTheDocument();
    expect(await screen.findByLabelText(/Project name/)).toHaveValue("demo");
    fireEvent.click(screen.getByRole("button", { name: /generate preview/i }));
    expect(await screen.findByRole("tab", { name: "src/main.tsx" })).toBeInTheDocument();
    await waitFor(() => expect(fetch).toHaveBeenLastCalledWith(expect.stringContaining("scaffoldings/react/preview"), expect.objectContaining({ method: "POST" })));
  });
});
