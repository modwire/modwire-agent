import { expect, Page, test } from "@playwright/test";

const root = { links: [
  { rel: ["scaffoldings"], href: "/api/scaffoldings" },
  { rel: ["records"], href: "/api/records" },
  { rel: ["sections"], href: "/api/sections" },
  { rel: ["languages"], href: "/api/languages" },
  { rel: ["variables"], href: "/api/variables" },
  { rel: ["templates"], href: "/api/templates" },
] };

async function openBrowser(page: Page) {
  await page.addInitScript(() => localStorage.setItem("modwire-api-key", "browser-test-key"));
  await page.route("**/api/**", async (route) => {
    const url = new URL(route.request().url());
    const path = url.pathname.replace(/\/$/, "");
    let body: object = root;
    if (path === "/api/scaffoldings") body = {
      entities: [{
        properties: { id: "react", name: "React app", description: "Small web app", language: "ts" },
        links: [{ rel: ["self"], href: "/api/scaffoldings/react" }],
      }],
      actions: [{ name: "create_scaffolding", method: "POST", href: "/api/scaffoldings" }],
    };
    else if (path === "/api/scaffoldings/react") body = {
      properties: { id: "react", name: "React app", description: "Small web app", language: "ts" },
      actions: [
        { name: "get_scaffolding_schema", method: "GET", href: "/api/scaffoldings/react/schema" },
        { name: "preview_scaffolding", method: "POST", href: "/api/scaffoldings/react/preview" },
      ],
    };
    else if (path === "/api/scaffoldings/react/schema") body = {
      properties: {
        properties: {
          project_name: { type: "string", description: "Project name", default: "demo" },
          include_tests: { type: "boolean", description: "Include tests", default: true },
        },
        required: ["project_name"],
      },
    };
    else if (path === "/api/scaffoldings/react/preview") {
      const request = route.request().postDataJSON() as { values: { project_name: string }; template_overrides: unknown[] };
      const name = request.values.project_name;
      body = { properties: { files: [
        { template_id: "readme", path: "README.md", source: `# ${name}`, html: `<pre># ${name}</pre>`, language: "markdown" },
        { template_id: "main", path: "src/main.tsx", source: `export const name = '${name}';`, html: `<pre>export const name = '${name}';</pre>`, language: "tsx" },
        { template_id: "test", path: "src/__tests__/main.test.tsx", source: `test('${name}')`, html: `<pre>test('${name}')</pre>`, language: "tsx" },
      ] } };
    }
    else if (path === "/api/templates") body = {
      entities: [
        { properties: { id: "main", scaffolding: "react", relative_path: "src/main.tsx", file_content: "export const name = '{{ project_name }}';", write_mode: "managed" } },
        { properties: { id: "readme", scaffolding: "react", relative_path: "README.md", file_content: "# {{ project_name }}", write_mode: "managed" } },
      ],
      actions: [{ name: "create_template", method: "POST", href: "/api/templates" }],
    };
    else if (path === "/api/languages") body = { entities: [{ properties: { id: "ts", name: "TypeScript" } }] };
    else if (["/api/records", "/api/sections", "/api/variables"].includes(path)) body = { entities: [], actions: [] };
    await route.fulfill({ status: 200, contentType: "application/vnd.siren+json", body: JSON.stringify(body) });
  });
  await page.goto("/browser/");
  await expect(page.getByRole("heading", { name: "React app" })).toBeVisible();
}

test.beforeEach(async ({ page }) => {
  await openBrowser(page);
});

test("starts in Preview mode with an explicit empty state", async ({ page }) => {
  await expect(page.getByRole("tab", { name: "Preview" })).toHaveAttribute("aria-selected", "true");
  await expect(page.getByText("Render the scaffolding to browse its files.")).toBeVisible();
  await expect(page.getByRole("button", { name: "Render preview" })).toBeVisible();
  await expect(page.getByText("Variables", { exact: true })).toBeHidden();
  await expect(page.getByRole("combobox", { name: "Template file" })).toBeHidden();
});

test("renders a nested, sorted file tree and selects the first file", async ({ page }) => {
  const previewRequest = page.waitForRequest((request) => request.url().endsWith("/api/scaffoldings/react/preview"));
  await page.getByRole("button", { name: "Render preview" }).click();

  const request = await previewRequest;
  expect(request.method()).toBe("POST");
  expect(request.headers().apikey).toBe("browser-test-key");
  expect(request.postDataJSON()).toEqual({
    values: { project_name: "demo", include_tests: true },
    template_overrides: [],
  });

  const tree = page.getByLabel("Rendered files");
  await expect(tree.getByRole("button")).toHaveText(["src", "__tests__", "main.test.tsx", "main.tsx", "README.md"]);
  await expect(tree.getByRole("button", { name: "src" })).toBeDisabled();
  await expect(tree.getByRole("button", { name: "__tests__" })).toBeDisabled();
  await expect(tree.getByRole("button", { name: "README.md" })).toHaveAttribute("data-selected", "true");
  await expect(page.getByText("README.md", { exact: true }).last()).toBeVisible();
  await expect(page.getByText("# demo", { exact: true })).toBeVisible();
  await expect(page.getByRole("button", { name: "Render again" })).toBeVisible();
});

test("switches the rendered result when a tree file is selected", async ({ page }) => {
  await page.getByRole("button", { name: "Render preview" }).click();
  const tree = page.getByLabel("Rendered files");

  await tree.getByRole("button", { name: "main.test.tsx" }).click();
  await expect(tree.getByRole("button", { name: "main.test.tsx" })).toHaveAttribute("data-selected", "true");
  await expect(tree.getByRole("button", { name: "README.md" })).toHaveAttribute("data-selected", "false");
  await expect(page.getByText("src/__tests__/main.test.tsx", { exact: true })).toBeVisible();
  await expect(page.getByText("test('demo')", { exact: true })).toBeVisible();

  await tree.getByRole("button", { name: "main.tsx", exact: true }).click();
  await expect(page.getByText("src/main.tsx", { exact: true })).toBeVisible();
  await expect(page.getByText("export const name = 'demo';", { exact: true })).toBeVisible();
  await expect(page.getByText("test('demo')", { exact: true })).toBeHidden();
});

test("shows variables and switches raw template sources in Build mode", async ({ page }) => {
  await page.getByRole("tab", { name: "Build" }).click();

  await expect(page.getByRole("tab", { name: "Build" })).toHaveAttribute("aria-selected", "true");
  await expect(page.getByLabel("Project name")).toHaveValue("demo");
  await expect(page.getByRole("button", { name: "Include tests: Enabled" })).toBeVisible();
  await expect(page.getByText("Render the scaffolding to browse its files.")).toBeHidden();

  const templates = page.getByRole("combobox", { name: "Template file" });
  await expect(templates.locator("option")).toHaveText(["src/main.tsx", "README.md"]);
  await expect(page.getByText("export const name = '{{ project_name }}';", { exact: true })).toBeVisible();
  await templates.selectOption("1");
  await expect(page.getByText("# {{ project_name }}", { exact: true })).toBeVisible();
  await expect(page.getByText("export const name = '{{ project_name }}';", { exact: true })).toBeHidden();
});

test("uses Build values when rendering and refreshes an existing preview", async ({ page }) => {
  await page.getByRole("tab", { name: "Build" }).click();
  await page.getByLabel("Project name").fill("acme");
  await page.getByRole("button", { name: "Include tests: Enabled" }).click();
  await page.getByRole("tab", { name: "Preview" }).click();

  const firstRequest = page.waitForRequest((request) => request.url().endsWith("/preview"));
  await page.getByRole("button", { name: "Render preview" }).click();
  expect((await firstRequest).postDataJSON()).toEqual({
    values: { project_name: "acme", include_tests: false },
    template_overrides: [],
  });
  await expect(page.getByText("# acme", { exact: true })).toBeVisible();

  await page.getByRole("tab", { name: "Build" }).click();
  await page.getByLabel("Project name").fill("renamed");
  await page.getByRole("tab", { name: "Preview" }).click();
  await expect(page.getByText("# acme", { exact: true })).toBeVisible();

  const refreshRequest = page.waitForRequest((request) => request.url().endsWith("/preview"));
  await page.getByRole("button", { name: "Render again" }).click();
  expect((await refreshRequest).postDataJSON()).toMatchObject({ values: { project_name: "renamed" } });
  await expect(page.getByText("# renamed", { exact: true })).toBeVisible();
  await expect(page.getByText("# acme", { exact: true })).toBeHidden();
});
