import {
  Add,
  ArrowForward,
  CheckCircleOutline,
  Code,
  ContentCopy,
  DeleteOutline,
  DescriptionOutlined,
  FolderOutlined,
  Key,
  Logout,
  MenuBookOutlined,
  Refresh,
  Search,
  Tune,
} from "@mui/icons-material";
import {
  Alert,
  Box,
  Button,
  Chip,
  CircularProgress,
  Container,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  IconButton,
  InputAdornment,
  Paper,
  Stack,
  Tab,
  Tabs,
  TextField,
  Tooltip,
  Typography,
} from "@mui/material";
import { FormEvent, useEffect, useId, useMemo, useState } from "react";

type Properties = Record<string, unknown>;
type SirenLink = { rel: string[]; href: string; title?: string };
type SirenAction = { name: string; href: string; method: string; type?: string };
type SirenEntity = { properties?: Properties; entities?: SirenEntity[]; links?: SirenLink[]; actions?: SirenAction[] };
type Scaffolding = { id: string; name: string; description: string; language: string; href: string };
type Language = { id: string; name: string };
type RecordSummary = { slug: string; section_slug: string; title: string; description: string; tag_slugs: string[]; href: string };
type RecordContent = { role: string; content: string; language: string; metadata: Properties };
type RecordResource = RecordSummary & { sources: string[]; content: RecordContent[] };
type SectionSummary = { slug: string; title: string; description: string };
type SchemaProperty = {
  type: "string" | "integer" | "number" | "boolean" | "array" | "object";
  description: string;
  default: unknown;
};
type FormSchema = { properties: Record<string, SchemaProperty>; required: string[] };
type PreviewFile = { template_id: string; path: string; source: string; html: string; language: string };
type TemplateSource = { id: string; scaffolding: string; relative_path: string; file_content: string; write_mode: string };

const API_URL = (import.meta.env.VITE_API_URL || "/api/").replace(/\/?$/, "/");

function messageFrom(error: unknown) {
  if (error instanceof Error) return error.message;
  return "Something went wrong. Please try again.";
}

async function api<T>(href: string, apiKey: string, init?: RequestInit): Promise<T> {
  const apiRoot = new URL(API_URL, window.location.origin);
  const response = await fetch(new URL(href, apiRoot), {
    ...init,
    headers: { apikey: apiKey, "Content-Type": "application/json", ...init?.headers },
  });
  const body = response.status === 204 ? null : await response.json();
  if (!response.ok) {
    const detail = body?.detail;
    const errors = detail?.errors;
    throw new Error(errors?.map((item: { message: string }) => item.message).join(" ") || detail || body?.title || `Request failed (${response.status})`);
  }
  return body as T;
}

function readCollection(document: SirenEntity): Scaffolding[] {
  return (document.entities || []).map((entity) => ({
    ...(entity.properties as unknown as Omit<Scaffolding, "href">),
    href: link(entity, "self").href,
  }));
}

function readRecords(document: SirenEntity): RecordSummary[] {
  return (document.entities || []).map((entity) => ({
    ...(entity.properties as unknown as Omit<RecordSummary, "href">),
    href: link(entity, "self").href,
  }));
}

function readTemplates(document: SirenEntity): TemplateSource[] {
  return (document.entities || []).map((entity) => entity.properties as unknown as TemplateSource);
}

function link(document: SirenEntity, relation: string): SirenLink {
  const found = document.links?.find((item) => item.rel.includes(relation));
  if (!found) throw new Error(`The API did not advertise a “${relation}” link.`);
  return found;
}

function action(document: SirenEntity, name: string): SirenAction {
  const found = document.actions?.find((item) => item.name === name);
  if (!found) throw new Error(`The API did not advertise the “${name}” operation.`);
  return found;
}

function fieldLabel(name: string) {
  return name.replaceAll("_", " ").replace(/^./, (letter) => letter.toUpperCase());
}

function asRecord(value: unknown): Record<string, unknown> {
  return value !== null && typeof value === "object" && !Array.isArray(value) ? value as Record<string, unknown> : {};
}

function valueFromInput(raw: string, previous: unknown) {
  if (typeof previous === "number") return Number(raw);
  if (typeof previous === "boolean") return raw === "true";
  return raw;
}

function InlineValue({ label, value, onChange }: { label: string; value: unknown; onChange: (value: unknown) => void }) {
  if (typeof value === "boolean") return (
    <TextField select SelectProps={{ native: true }} size="small" label={fieldLabel(label)} value={String(value)} onChange={(event) => onChange(event.target.value === "true")}>
      <option value="true">true</option><option value="false">false</option>
    </TextField>
  );
  return <TextField size="small" fullWidth label={fieldLabel(label)} type={typeof value === "number" ? "number" : "text"} value={String(value ?? "")} onChange={(event) => onChange(valueFromInput(event.target.value, value))} />;
}

function ArrayEditor({ name, value, defaultValue, onChange }: { name: string; value: unknown; defaultValue: unknown; onChange: (value: unknown[]) => void }) {
  const items = Array.isArray(value) ? value : [];
  const sample = items[0] ?? (Array.isArray(defaultValue) ? defaultValue[0] : "");
  const objectItems = items.some((item) => Object.keys(asRecord(item)).length > 0) || Object.keys(asRecord(sample)).length > 0;
  const add = () => onChange([...items, objectItems ? { ...asRecord(sample) } : ""]);
  const remove = (index: number) => onChange(items.filter((_, itemIndex) => itemIndex !== index));
  const replace = (index: number, next: unknown) => onChange(items.map((item, itemIndex) => itemIndex === index ? next : item));
  return (
    <Box className="structured-field">
      <Stack direction="row" alignItems="center" justifyContent="space-between" mb={1}>
        <Typography variant="subtitle2" fontWeight={750}>{fieldLabel(name)}</Typography>
        <Button size="small" startIcon={<Add />} onClick={add}>Add</Button>
      </Stack>
      <Stack spacing={1}>
        {items.map((item, index) => {
          const object = asRecord(item);
          return <Box className="structured-row" key={index}>
            {objectItems
              ? <Box className="structured-columns">{Object.entries(object).map(([key, entry]) => <InlineValue key={key} label={key} value={entry} onChange={(next) => replace(index, { ...object, [key]: next })} />)}</Box>
              : <InlineValue label={`${fieldLabel(name)} ${index + 1}`} value={item} onChange={(next) => replace(index, next)} />}
            <IconButton aria-label={`Remove ${fieldLabel(name)} ${index + 1}`} size="small" onClick={() => remove(index)}><DeleteOutline fontSize="small" /></IconButton>
          </Box>;
        })}
        {items.length === 0 && <Button className="add-empty" size="small" startIcon={<Add />} onClick={add}>Add item</Button>}
      </Stack>
    </Box>
  );
}

function ObjectEditor({ name, value, onChange }: { name: string; value: unknown; onChange: (value: Record<string, unknown>) => void }) {
  const object = asRecord(value);
  const entries = Object.entries(object);
  const replaceKey = (oldKey: string, nextKey: string) => onChange(Object.fromEntries(entries.map(([key, entry]) => [key === oldKey ? nextKey : key, entry])));
  return (
    <Box className="structured-field">
      <Stack direction="row" alignItems="center" justifyContent="space-between" mb={1}>
        <Typography variant="subtitle2" fontWeight={750}>{fieldLabel(name)}</Typography>
        <Button size="small" startIcon={<Add />} onClick={() => onChange({ ...object, [`key_${entries.length + 1}`]: "" })}>Add</Button>
      </Stack>
      <Stack spacing={1}>{entries.map(([key, entry]) => <Box className="structured-row" key={key}>
        <TextField size="small" label="Key" value={key} onChange={(event) => replaceKey(key, event.target.value)} />
        <InlineValue label="Value" value={entry} onChange={(next) => onChange({ ...object, [key]: next })} />
        <IconButton aria-label={`Remove ${key}`} size="small" onClick={() => onChange(Object.fromEntries(entries.filter(([entryKey]) => entryKey !== key)))}><DeleteOutline fontSize="small" /></IconButton>
      </Box>)}</Stack>
    </Box>
  );
}

function MermaidPreview({ source }: { source: string }) {
  const id = `mermaid-${useId().replaceAll(":", "")}`;
  const [svg, setSvg] = useState("");
  const [renderError, setRenderError] = useState("");
  useEffect(() => {
    let current = true;
    setSvg(""); setRenderError("");
    void import("mermaid").then(async ({ default: mermaid }) => {
      mermaid.initialize({ startOnLoad: false, securityLevel: "strict", theme: "neutral" });
      const result = await mermaid.render(id, source);
      if (current) setSvg(result.svg);
    }).catch((reason) => { if (current) setRenderError(messageFrom(reason)); });
    return () => { current = false; };
  }, [id, source]);
  if (renderError) return <Alert severity="error">{renderError}</Alert>;
  if (!svg) return <Stack alignItems="center" py={8}><CircularProgress size={24} /></Stack>;
  return <Box className="mermaid-view" dangerouslySetInnerHTML={{ __html: svg }} />;
}

type TreeNode = { name: string; path: string; fileIndex?: number; children: TreeNode[] };

function fileTree(files: PreviewFile[]): TreeNode[] {
  const root: TreeNode[] = [];
  files.forEach((file, fileIndex) => {
    let level = root;
    let currentPath = "";
    file.path.split("/").forEach((name, index, parts) => {
      currentPath = currentPath ? `${currentPath}/${name}` : name;
      let node = level.find((item) => item.name === name);
      if (!node) {
        node = { name, path: currentPath, children: [] };
        level.push(node);
      }
      if (index === parts.length - 1) node.fileIndex = fileIndex;
      level = node.children;
    });
  });
  const sort = (nodes: TreeNode[]) => nodes.sort((a, b) => {
    const aFolder = a.fileIndex === undefined;
    const bFolder = b.fileIndex === undefined;
    return aFolder === bFolder ? a.name.localeCompare(b.name) : aFolder ? -1 : 1;
  }).forEach((node) => sort(node.children));
  sort(root);
  return root;
}

function FileTree({ files, activeFile, onSelect }: { files: PreviewFile[]; activeFile: number; onSelect: (index: number) => void }) {
  const nodes = useMemo(() => fileTree(files), [files]);
  const render = (items: TreeNode[], depth = 0): React.ReactNode => items.map((node) => {
    const folder = node.fileIndex === undefined;
    return <Box key={node.path}>
      <button
        className="tree-row"
        data-selected={!folder && node.fileIndex === activeFile}
        disabled={folder}
        style={{ paddingLeft: 12 + depth * 16 }}
        onClick={() => node.fileIndex !== undefined && onSelect(node.fileIndex)}
      >
        {folder ? <FolderOutlined fontSize="inherit" /> : <DescriptionOutlined fontSize="inherit" />}
        <span>{node.name}</span>
      </button>
      {node.children.length > 0 && render(node.children, depth + 1)}
    </Box>;
  });
  return <Box className="file-tree" aria-label="Rendered files">{render(nodes)}</Box>;
}

function Field({ name, property, required, value, onChange }: {
  name: string;
  property: SchemaProperty;
  required: boolean;
  value: unknown;
  onChange: (value: unknown) => void;
}) {
  const label = fieldLabel(name);
  if (property.type === "array") return <ArrayEditor name={name} value={value} defaultValue={property.default} onChange={onChange} />;
  if (property.type === "object") return <ObjectEditor name={name} value={value} onChange={onChange} />;
  if (property.type === "boolean") {
    return (
      <Button
        color={value ? "primary" : "inherit"}
        onClick={() => onChange(!value)}
        startIcon={value ? <CheckCircleOutline /> : <Tune />}
        variant={value ? "contained" : "outlined"}
        sx={{ justifyContent: "flex-start", py: 1.3 }}
      >
        {label}: {value ? "Enabled" : "Disabled"}
      </Button>
    );
  }
  return (
    <TextField
      fullWidth
      required={required}
      label={label}
      size="small"
      value={String(value ?? "")}
      type={property.type === "integer" || property.type === "number" ? "number" : "text"}
      onChange={(event) => {
        const raw = event.target.value;
        if (property.type === "integer") onChange(Number.parseInt(raw, 10));
        else if (property.type === "number") onChange(Number(raw));
        else onChange(raw);
      }}
    />
  );
}

export function App() {
  const [apiKey, setApiKey] = useState(() => localStorage.getItem("modwire-api-key") || "");
  const [keyDraft, setKeyDraft] = useState(apiKey);
  const [scaffoldings, setScaffoldings] = useState<Scaffolding[]>([]);
  const [scaffoldingCollection, setScaffoldingCollection] = useState<SirenEntity | null>(null);
  const [variableCollection, setVariableCollection] = useState<SirenEntity | null>(null);
  const [templateCollection, setTemplateCollection] = useState<SirenEntity | null>(null);
  const [languages, setLanguages] = useState<Language[]>([]);
  const [records, setRecords] = useState<RecordSummary[]>([]);
  const [sections, setSections] = useState<SectionSummary[]>([]);
  const [selectedRecord, setSelectedRecord] = useState<RecordResource | null>(null);
  const [selectedRecordSlug, setSelectedRecordSlug] = useState("");
  const [area, setArea] = useState<"scaffoldings" | "records">("scaffoldings");
  const [selectedResource, setSelectedResource] = useState<SirenEntity | null>(null);
  const [selectedId, setSelectedId] = useState("");
  const [schema, setSchema] = useState<FormSchema | null>(null);
  const [values, setValues] = useState<Record<string, unknown>>({});
  const [files, setFiles] = useState<PreviewFile[]>([]);
  const [templates, setTemplates] = useState<TemplateSource[]>([]);
  const [activeFile, setActiveFile] = useState(0);
  const [activeTemplate, setActiveTemplate] = useState(0);
  const [mode, setMode] = useState<"build" | "preview">("preview");
  const [showMermaidSource, setShowMermaidSource] = useState(false);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const [previewing, setPreviewing] = useState(false);
  const [error, setError] = useState("");
  const [newScaffoldingOpen, setNewScaffoldingOpen] = useState(false);
  const [newScaffolding, setNewScaffolding] = useState({ language_id: "", name: "", description: "", relative_path: "README.md", file_content: "# Generated file.\n" });
  const [newVariableOpen, setNewVariableOpen] = useState(false);
  const [newVariable, setNewVariable] = useState<{ name: string; type: "str" | "int" | "float" | "bool" | "list" | "dict"; description: string; default_value: unknown; required: boolean }>({ name: "", type: "str", description: "", default_value: "", required: false });
  const [saving, setSaving] = useState(false);

  const selected = scaffoldings.find((item) => item.id === selectedId);
  const filtered = useMemo(() => scaffoldings.filter((item) =>
    `${item.name} ${item.description}`.toLowerCase().includes(search.toLowerCase())), [scaffoldings, search]);
  const filteredRecords = useMemo(() => records.filter((item) =>
    `${item.title} ${item.description} ${item.tag_slugs.join(" ")}`.toLowerCase().includes(search.toLowerCase())), [records, search]);
  const sectionTitles = useMemo(() => Object.fromEntries(sections.map((section) => [section.slug, section.title])), [sections]);

  async function loadStudio(key = apiKey) {
    if (!key) return;
    setLoading(true); setError("");
    try {
      const root = await api<SirenEntity>(API_URL, key);
      const [nextScaffoldingCollection, recordCollection, sectionCollection, languageCollection, nextVariableCollection, nextTemplateCollection] = await Promise.all([
        api<SirenEntity>(link(root, "scaffoldings").href, key),
        api<SirenEntity>(link(root, "records").href, key),
        api<SirenEntity>(link(root, "sections").href, key),
        api<SirenEntity>(link(root, "languages").href, key),
        api<SirenEntity>(link(root, "variables").href, key),
        api<SirenEntity>(link(root, "templates").href, key),
      ]);
      const items = readCollection(nextScaffoldingCollection);
      const recordItems = readRecords(recordCollection);
      setScaffoldingCollection(nextScaffoldingCollection);
      setVariableCollection(nextVariableCollection);
      setTemplateCollection(nextTemplateCollection);
      setTemplates(readTemplates(nextTemplateCollection));
      const languageItems = (languageCollection.entities || []).map((entity) => entity.properties as unknown as Language);
      setLanguages(languageItems);
      setNewScaffolding((current) => ({ ...current, language_id: current.language_id || languageItems[0]?.id || "" }));
      setScaffoldings(items);
      setRecords(recordItems);
      setSections((sectionCollection.entities || []).map((entity) => entity.properties as unknown as SectionSummary));
      setSelectedId((current) => items.some((item) => item.id === current) ? current : items[0]?.id || "");
      setSelectedRecordSlug((current) => recordItems.some((item) => item.slug === current) ? current : recordItems[0]?.slug || "");
    } catch (reason) { setError(messageFrom(reason)); }
    finally { setLoading(false); }
  }

  useEffect(() => { void loadStudio(); }, [apiKey]);
  useEffect(() => {
    if (area !== "scaffoldings" || !selectedId || !apiKey) { setSchema(null); setSelectedResource(null); return; }
    setLoading(true); setError(""); setFiles([]);
    const item = scaffoldings.find((candidate) => candidate.id === selectedId);
    if (!item) return;
    void api<SirenEntity>(item.href, apiKey)
      .then(async (resource) => {
        setSelectedResource(resource);
        const document = await api<SirenEntity>(action(resource, "get_scaffolding_schema").href, apiKey);
        const next = document.properties as unknown as FormSchema;
        setSchema(next);
        setValues(Object.fromEntries(Object.entries(next.properties).map(([name, property]) => [name, property.default])));
      })
      .catch((reason) => setError(messageFrom(reason)))
      .finally(() => setLoading(false));
  }, [area, selectedId, apiKey, scaffoldings]);
  useEffect(() => { setActiveTemplate(0); }, [selectedId]);
  useEffect(() => {
    if (area !== "records" || !selectedRecordSlug || !apiKey) { setSelectedRecord(null); return; }
    const item = records.find((candidate) => candidate.slug === selectedRecordSlug);
    if (!item) return;
    setLoading(true); setError("");
    void api<SirenEntity>(item.href, apiKey)
      .then((resource) => setSelectedRecord({ ...item, ...(resource.properties as unknown as RecordResource) }))
      .catch((reason) => setError(messageFrom(reason)))
      .finally(() => setLoading(false));
  }, [area, selectedRecordSlug, apiKey, records]);

  function connect(event: FormEvent) {
    event.preventDefault();
    const key = keyDraft.trim();
    localStorage.setItem("modwire-api-key", key);
    setApiKey(key);
  }

  async function preview() {
    if (!selectedResource) return;
    setPreviewing(true); setError("");
    try {
      const operation = action(selectedResource, "preview_scaffolding");
      const result = await api<SirenEntity>(operation.href, apiKey, {
        method: operation.method, body: JSON.stringify({ values, template_overrides: [] }),
      });
      const next = (result.properties?.files || []) as PreviewFile[];
      setFiles(next); setActiveFile(0); setShowMermaidSource(false);
    } catch (reason) { setError(messageFrom(reason)); }
    finally { setPreviewing(false); }
  }

  const selectedTemplates = templates.filter((template) => template.scaffolding === selectedId);
  const selectedTemplate = selectedTemplates[activeTemplate];

  async function createScaffolding() {
    if (!scaffoldingCollection || !templateCollection) return;
    setSaving(true); setError("");
    try {
      const create = action(scaffoldingCollection, "create_scaffolding");
      const created = await api<SirenEntity>(create.href, apiKey, {
        method: create.method,
        body: JSON.stringify({ language_id: newScaffolding.language_id, name: newScaffolding.name, description: newScaffolding.description }),
      });
      const id = String(created.properties?.id || "");
      const createTemplate = action(templateCollection, "create_template");
      await api<SirenEntity>(createTemplate.href, apiKey, {
        method: createTemplate.method,
        body: JSON.stringify({ scaffolding_id: id, relative_path: newScaffolding.relative_path, file_content: newScaffolding.file_content }),
      });
      setSelectedId(id);
      setNewScaffoldingOpen(false);
      setNewScaffolding((current) => ({ ...current, name: "", description: "", relative_path: "README.md", file_content: "# Generated file.\n" }));
      await loadStudio();
    } catch (reason) { setError(messageFrom(reason)); }
    finally { setSaving(false); }
  }

  async function createVariable() {
    if (!variableCollection || !selected) return;
    setSaving(true); setError("");
    try {
      const create = action(variableCollection, "create_variable");
      await api<SirenEntity>(create.href, apiKey, {
        method: create.method,
        body: JSON.stringify({ ...newVariable, scaffolding_id: selected.id }),
      });
      setNewVariableOpen(false);
      setNewVariable({ name: "", type: "str", description: "", default_value: "", required: false });
      const resource = await api<SirenEntity>(selected.href, apiKey);
      const document = await api<SirenEntity>(action(resource, "get_scaffolding_schema").href, apiKey);
      const next = document.properties as unknown as FormSchema;
      setSchema(next);
      setValues(Object.fromEntries(Object.entries(next.properties).map(([name, property]) => [name, property.default])));
    } catch (reason) { setError(messageFrom(reason)); }
    finally { setSaving(false); }
  }

  if (!apiKey) return (
    <Box className="app-shell">
      <Container maxWidth="sm" sx={{ py: { xs: 8, md: 16 } }}>
        <Stack alignItems="center" spacing={4}>
          <Box className="brand-mark"><Code /></Box>
          <Typography component="h1" variant="h4" fontWeight={800} letterSpacing="-0.035em">Modwire Studio</Typography>
          <Paper component="form" onSubmit={connect} className="key-card" elevation={0}>
            <Stack spacing={2.5}>
              <Typography variant="subtitle1" fontWeight={750}>Connect</Typography>
              <TextField autoFocus required label="API key" type="password" value={keyDraft} onChange={(e) => setKeyDraft(e.target.value)} InputProps={{ startAdornment: <InputAdornment position="start"><Key /></InputAdornment> }} />
              <Button type="submit" size="large" variant="contained" endIcon={<ArrowForward />}>Open studio</Button>
            </Stack>
          </Paper>
        </Stack>
      </Container>
    </Box>
  );

  return (
    <Box className="app-shell">
      <Box component="header" className="topbar">
        <Stack direction="row" alignItems="center" spacing={1.5}><Box className="brand-mark small"><Code /></Box><Typography variant="h6" fontWeight={800}>Modwire</Typography><Chip label="Studio" size="small" /></Stack>
        <Tooltip title="Forget API key"><IconButton onClick={() => { localStorage.removeItem("modwire-api-key"); setApiKey(""); }}><Logout /></IconButton></Tooltip>
      </Box>
      <Box className="workspace">
        <Paper component="aside" className="sidebar" elevation={0} square>
          <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ px: 2, pt: 1.5 }}><Tabs value={area} onChange={(_, value) => { setArea(value); setSearch(""); }} variant="fullWidth"><Tab value="scaffoldings" label="Scaffolds" /><Tab value="records" label="Records" /></Tabs><Tooltip title="Refresh"><IconButton size="small" onClick={() => void loadStudio()}><Refresh fontSize="small" /></IconButton></Tooltip></Stack>
          {area === "scaffoldings" && <Button size="small" startIcon={<Add />} onClick={() => setNewScaffoldingOpen(true)} sx={{ mx: 2, justifyContent: "flex-start" }}>New scaffolding</Button>}
          <TextField size="small" placeholder="Search catalog" value={search} onChange={(e) => setSearch(e.target.value)} sx={{ m: 2, mt: 1.5 }} InputProps={{ startAdornment: <InputAdornment position="start"><Search fontSize="small" /></InputAdornment> }} />
          <Stack className="catalog" spacing={0.75}>
            {area === "scaffoldings" && filtered.map((item) => <Button key={item.id} className="catalog-item" data-selected={selectedId === item.id} onClick={() => setSelectedId(item.id)}><Typography fontWeight={700} textTransform="none" noWrap>{item.name}</Typography></Button>)}
            {area === "records" && filteredRecords.map((item) => <Button key={item.slug} className="catalog-item" data-selected={selectedRecordSlug === item.slug} onClick={() => setSelectedRecordSlug(item.slug)}><Stack alignItems="flex-start"><Typography fontWeight={700} textTransform="none">{item.title}</Typography><Typography variant="caption" color="text.secondary" noWrap>{sectionTitles[item.section_slug] || item.section_slug}</Typography></Stack></Button>)}
            {!loading && area === "scaffoldings" && filtered.length === 0 && <Typography color="text.secondary" variant="body2" sx={{ px: 2.5, py: 3 }}>No scaffoldings found.</Typography>}
            {!loading && area === "records" && filteredRecords.length === 0 && <Typography color="text.secondary" variant="body2" sx={{ px: 2.5, py: 3 }}>No records found.</Typography>}
          </Stack>
        </Paper>
        <Box component="main" className="main-pane">
          {error && <Alert severity="error" onClose={() => setError("")} sx={{ mb: 2 }}>{error}</Alert>}
          {loading && area === "scaffoldings" && !selected && <Stack alignItems="center" py={12}><CircularProgress /></Stack>}
          {area === "scaffoldings" && selected && <>
            <Stack direction={{ xs: "column", md: "row" }} justifyContent="space-between" gap={2} mb={2}>
              <Box><Chip icon={<FolderOutlined />} label="Scaffolding" size="small" variant="outlined" /><Typography component="h1" variant="h5" fontWeight={800} mt={1}>{selected.name}</Typography></Box>
              <Tabs value={mode} onChange={(_, value) => setMode(value)} aria-label="Scaffolding mode"><Tab value="preview" label="Preview" /><Tab value="build" label="Build" /></Tabs>
            </Stack>
            {mode === "preview" ? <Box className="browser-grid">
              <Paper component="aside" className="panel tree-panel" elevation={0}>
                <Box className="panel-heading"><Typography variant="subtitle2">Files</Typography><Typography variant="caption" color="text.secondary">{files.length}</Typography></Box>
                {files.length ? <FileTree files={files} activeFile={activeFile} onSelect={(index) => { setActiveFile(index); setShowMermaidSource(false); }} /> : <Typography variant="body2" color="text.secondary" sx={{ p: 2 }}>Render the scaffolding to browse its files.</Typography>}
              </Paper>
              <Paper className="panel preview-panel" elevation={0}>
                {files.length ? <><Box className="preview-toolbar"><Typography variant="body2" fontWeight={650} noWrap>{files[activeFile].path}</Typography><Stack direction="row" spacing={0.5}>{files[activeFile].path.endsWith(".mermaid") && <Button size="small" onClick={() => setShowMermaidSource((current) => !current)}>{showMermaidSource ? "Diagram" : "Source"}</Button>}<Tooltip title="Copy source"><IconButton aria-label="Copy source" onClick={() => void navigator.clipboard.writeText(files[activeFile].source)}><ContentCopy fontSize="small" /></IconButton></Tooltip></Stack></Box><Divider />{files[activeFile].path.endsWith(".mermaid") && !showMermaidSource ? <MermaidPreview source={files[activeFile].source} /> : <Box className="code-view" dangerouslySetInnerHTML={{ __html: files[activeFile].html }} />}</> : <Box className="preview-empty"><Button variant="contained" disabled={previewing || loading} onClick={() => void preview()}>{previewing ? "Rendering…" : "Render preview"}</Button></Box>}
              </Paper>
            </Box> : <Box className="content-grid">
              <Paper className="panel form-panel" elevation={0}><Stack direction="row" alignItems="center" justifyContent="space-between" mb={2}><Typography variant="subtitle1" fontWeight={700}>Variables</Typography><Button size="small" startIcon={<Add />} onClick={() => setNewVariableOpen(true)}>Add</Button></Stack><Stack spacing={2}>{schema && Object.entries(schema.properties).map(([name, property]) => <Field key={name} name={name} property={property} required={schema.required.includes(name)} value={values[name]} onChange={(value) => setValues((current) => ({ ...current, [name]: value }))} />)}</Stack></Paper>
              <Paper className="panel template-panel" elevation={0}>{selectedTemplate ? <><Box className="preview-toolbar"><label className="file-select"><span>Template</span><select aria-label="Template file" value={activeTemplate} onChange={(event) => setActiveTemplate(Number(event.target.value))}>{selectedTemplates.map((template, index) => <option value={index} key={template.id}>{template.relative_path}</option>)}</select></label></Box><Divider /><Box component="pre" className="template-view">{selectedTemplate.file_content}</Box></> : <Box className="preview-empty"><Typography variant="body2" color="text.secondary">No templates in this scaffolding.</Typography></Box>}</Paper>
            </Box>}
            {mode === "preview" && files.length > 0 && <Button className="render-again" size="small" disabled={previewing || loading} onClick={() => void preview()}>{previewing ? "Rendering…" : "Render again"}</Button>}
          </>}
          {area === "records" && selectedRecord && <>
            <Stack gap={1} mb={3}>
              <Box><Chip icon={<MenuBookOutlined />} label={sectionTitles[selectedRecord.section_slug] || "Record"} size="small" variant="outlined" /><Typography component="h1" variant="h5" fontWeight={800} mt={1}>{selectedRecord.title}</Typography></Box>
              <Stack direction="row" gap={1} flexWrap="wrap">{selectedRecord.tag_slugs.map((tag) => <Chip key={tag} label={tag} size="small" />)}</Stack>
            </Stack>
            <Paper className="panel record-panel" elevation={0}>
              <Stack spacing={2.5}>
                {selectedRecord.content.map((block, index) => block.role === "list"
                  ? <Box component="ul" key={index} sx={{ my: 0, pl: 3 }}>{block.content.split("\n").map((line) => <li key={line}><Typography>{line}</Typography></li>)}</Box>
                  : <Typography key={index} sx={{ whiteSpace: "pre-wrap" }}>{block.content}</Typography>)}
                {selectedRecord.sources.length > 0 && <><Divider /><Typography variant="overline" fontWeight={800}>Sources</Typography>{selectedRecord.sources.map((source) => <Typography component="a" href={source} target="_blank" rel="noreferrer" key={source} color="primary">{source}</Typography>)}</>}
              </Stack>
            </Paper>
          </>}
        </Box>
      </Box>
      <Dialog open={newScaffoldingOpen} onClose={() => setNewScaffoldingOpen(false)} fullWidth maxWidth="sm">
        <DialogTitle>New scaffolding</DialogTitle>
        <DialogContent><Stack spacing={2} pt={1}>
          <TextField select SelectProps={{ native: true }} size="small" label="Language" value={newScaffolding.language_id} onChange={(event) => setNewScaffolding((current) => ({ ...current, language_id: event.target.value }))}>{languages.map((language) => <option key={language.id} value={language.id}>{language.name}</option>)}</TextField>
          <TextField autoFocus required size="small" label="Name" value={newScaffolding.name} onChange={(event) => setNewScaffolding((current) => ({ ...current, name: event.target.value }))} />
          <TextField required size="small" label="Description" value={newScaffolding.description} onChange={(event) => setNewScaffolding((current) => ({ ...current, description: event.target.value }))} />
          <TextField required size="small" label="First output path" value={newScaffolding.relative_path} onChange={(event) => setNewScaffolding((current) => ({ ...current, relative_path: event.target.value }))} />
          <TextField required label="Template" multiline minRows={8} value={newScaffolding.file_content} onChange={(event) => setNewScaffolding((current) => ({ ...current, file_content: event.target.value }))} InputProps={{ sx: { fontFamily: "monospace", fontSize: 13 } }} />
        </Stack></DialogContent>
        <DialogActions><Button onClick={() => setNewScaffoldingOpen(false)}>Cancel</Button><Button variant="contained" disabled={saving || !newScaffolding.language_id || !newScaffolding.name || !newScaffolding.description || !newScaffolding.relative_path || !newScaffolding.file_content} onClick={() => void createScaffolding()}>Create</Button></DialogActions>
      </Dialog>
      <Dialog open={newVariableOpen} onClose={() => setNewVariableOpen(false)} fullWidth maxWidth="sm">
        <DialogTitle>New variable</DialogTitle>
        <DialogContent><Stack spacing={2} pt={1}>
          <TextField autoFocus required size="small" label="Name" value={newVariable.name} onChange={(event) => setNewVariable((current) => ({ ...current, name: event.target.value }))} />
          <TextField select SelectProps={{ native: true }} size="small" label="Type" value={newVariable.type} onChange={(event) => { const type = event.target.value as typeof newVariable.type; const defaults = { str: "", int: 0, float: 0, bool: false, list: [], dict: {} }; setNewVariable((current) => ({ ...current, type, default_value: defaults[type] })); }}><option value="str">String</option><option value="int">Integer</option><option value="float">Number</option><option value="bool">Boolean</option><option value="list">List</option><option value="dict">Dictionary</option></TextField>
          <TextField required size="small" label="Description" value={newVariable.description} onChange={(event) => setNewVariable((current) => ({ ...current, description: event.target.value }))} />
          {newVariable.type === "list" ? <ArrayEditor name="default_value" value={newVariable.default_value} defaultValue={[]} onChange={(default_value) => setNewVariable((current) => ({ ...current, default_value }))} /> : newVariable.type === "dict" ? <ObjectEditor name="default_value" value={newVariable.default_value} onChange={(default_value) => setNewVariable((current) => ({ ...current, default_value }))} /> : newVariable.type === "bool" ? <Button variant={newVariable.default_value ? "contained" : "outlined"} onClick={() => setNewVariable((current) => ({ ...current, default_value: !current.default_value }))}>Default: {newVariable.default_value ? "true" : "false"}</Button> : <TextField size="small" label="Default" type={newVariable.type === "str" ? "text" : "number"} value={String(newVariable.default_value)} onChange={(event) => setNewVariable((current) => ({ ...current, default_value: newVariable.type === "str" ? event.target.value : Number(event.target.value) }))} />}
          <Button variant={newVariable.required ? "contained" : "outlined"} startIcon={newVariable.required ? <CheckCircleOutline /> : <Tune />} onClick={() => setNewVariable((current) => ({ ...current, required: !current.required }))}>Required</Button>
        </Stack></DialogContent>
        <DialogActions><Button onClick={() => setNewVariableOpen(false)}>Cancel</Button><Button variant="contained" disabled={saving || !newVariable.name || !newVariable.description} onClick={() => void createVariable()}>Add variable</Button></DialogActions>
      </Dialog>
    </Box>
  );
}
