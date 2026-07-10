import {
  ArrowForward,
  CheckCircleOutline,
  Code,
  ContentCopy,
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
import { FormEvent, useEffect, useMemo, useState } from "react";

type Properties = Record<string, unknown>;
type SirenLink = { rel: string[]; href: string; title?: string };
type SirenAction = { name: string; href: string; method: string; type?: string };
type SirenEntity = { properties?: Properties; entities?: SirenEntity[]; links?: SirenLink[]; actions?: SirenAction[] };
type Scaffolding = { id: string; name: string; description: string; language: string; href: string };
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

function Field({ name, property, required, value, onChange }: {
  name: string;
  property: SchemaProperty;
  required: boolean;
  value: unknown;
  onChange: (value: unknown) => void;
}) {
  const label = name.replaceAll("_", " ").replace(/^./, (letter) => letter.toUpperCase());
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
  const structured = property.type === "array" || property.type === "object";
  return (
    <TextField
      fullWidth
      required={required}
      label={label}
      value={structured ? JSON.stringify(value ?? property.default, null, 2) : String(value ?? "")}
      type={property.type === "integer" || property.type === "number" ? "number" : "text"}
      multiline={structured}
      minRows={structured ? 3 : undefined}
      helperText={property.description}
      onChange={(event) => {
        const raw = event.target.value;
        if (structured) {
          try { onChange(JSON.parse(raw)); } catch { onChange(raw); }
        } else if (property.type === "integer") onChange(Number.parseInt(raw, 10));
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
  const [activeFile, setActiveFile] = useState(0);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(false);
  const [previewing, setPreviewing] = useState(false);
  const [error, setError] = useState("");

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
      const [scaffoldingCollection, recordCollection, sectionCollection] = await Promise.all([
        api<SirenEntity>(link(root, "scaffoldings").href, key),
        api<SirenEntity>(link(root, "records").href, key),
        api<SirenEntity>(link(root, "sections").href, key),
      ]);
      const items = readCollection(scaffoldingCollection);
      const recordItems = readRecords(recordCollection);
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
      setFiles(next); setActiveFile(0);
    } catch (reason) { setError(messageFrom(reason)); }
    finally { setPreviewing(false); }
  }

  if (!apiKey) return (
    <Box className="app-shell">
      <Container maxWidth="sm" sx={{ py: { xs: 8, md: 16 } }}>
        <Stack alignItems="center" spacing={4}>
          <Box className="brand-mark"><Code /></Box>
          <Stack spacing={1} textAlign="center">
            <Typography component="h1" variant="h3" fontWeight={800} letterSpacing="-0.045em">Modwire Studio</Typography>
            <Typography color="text.secondary">Explore and render your project scaffoldings.</Typography>
          </Stack>
          <Paper component="form" onSubmit={connect} className="key-card" elevation={0}>
            <Stack spacing={2.5}>
              <Box><Typography variant="h6" fontWeight={700}>Connect to your workspace</Typography><Typography variant="body2" color="text.secondary">Enter an API key to access the catalog.</Typography></Box>
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
          <Stack direction="row" alignItems="center" justifyContent="space-between" sx={{ px: 2.5, pt: 1.5 }}><Tabs value={area} onChange={(_, value) => { setArea(value); setSearch(""); }} variant="fullWidth"><Tab value="scaffoldings" label="Scaffolds" /><Tab value="records" label="Records" /></Tabs><Tooltip title="Refresh"><IconButton size="small" onClick={() => void loadStudio()}><Refresh fontSize="small" /></IconButton></Tooltip></Stack>
          <TextField size="small" placeholder="Search catalog" value={search} onChange={(e) => setSearch(e.target.value)} sx={{ m: 2, mt: 1.5 }} InputProps={{ startAdornment: <InputAdornment position="start"><Search fontSize="small" /></InputAdornment> }} />
          <Stack className="catalog" spacing={0.75}>
            {area === "scaffoldings" && filtered.map((item) => <Button key={item.id} className="catalog-item" data-selected={selectedId === item.id} onClick={() => setSelectedId(item.id)}><Stack alignItems="flex-start"><Typography fontWeight={700} textTransform="none">{item.name}</Typography><Typography variant="caption" color="text.secondary" noWrap>{item.description || "No description"}</Typography></Stack></Button>)}
            {area === "records" && filteredRecords.map((item) => <Button key={item.slug} className="catalog-item" data-selected={selectedRecordSlug === item.slug} onClick={() => setSelectedRecordSlug(item.slug)}><Stack alignItems="flex-start"><Typography fontWeight={700} textTransform="none">{item.title}</Typography><Typography variant="caption" color="text.secondary" noWrap>{sectionTitles[item.section_slug] || item.section_slug}</Typography></Stack></Button>)}
            {!loading && area === "scaffoldings" && filtered.length === 0 && <Typography color="text.secondary" variant="body2" sx={{ px: 2.5, py: 3 }}>No scaffoldings found.</Typography>}
            {!loading && area === "records" && filteredRecords.length === 0 && <Typography color="text.secondary" variant="body2" sx={{ px: 2.5, py: 3 }}>No records found.</Typography>}
          </Stack>
        </Paper>
        <Box component="main" className="main-pane">
          {error && <Alert severity="error" onClose={() => setError("")} sx={{ mb: 2 }}>{error}</Alert>}
          {loading && area === "scaffoldings" && !selected && <Stack alignItems="center" py={12}><CircularProgress /></Stack>}
          {area === "scaffoldings" && selected && <>
            <Stack direction={{ xs: "column", md: "row" }} justifyContent="space-between" gap={2} mb={3}>
              <Box><Chip icon={<FolderOutlined />} label="Scaffolding" size="small" variant="outlined" /><Typography component="h1" variant="h4" fontWeight={800} mt={1}>{selected.name}</Typography><Typography color="text.secondary">{selected.description}</Typography></Box>
              <Button variant="contained" size="large" disabled={previewing || loading} onClick={() => void preview()} startIcon={previewing ? <CircularProgress size={18} color="inherit" /> : <Code />}>{previewing ? "Rendering…" : "Generate preview"}</Button>
            </Stack>
            <Box className="content-grid">
              <Paper className="panel form-panel" elevation={0}><Stack direction="row" spacing={1} alignItems="center" mb={2.5}><Tune color="primary" /><Typography variant="h6" fontWeight={750}>Configure</Typography></Stack><Stack spacing={2.5}>{schema && Object.entries(schema.properties).map(([name, property]) => <Field key={name} name={name} property={property} required={schema.required.includes(name)} value={values[name]} onChange={(value) => setValues((current) => ({ ...current, [name]: value }))} />)}{schema && Object.keys(schema.properties).length === 0 && <Typography color="text.secondary">This scaffolding has no variables. It is ready to render.</Typography>}</Stack></Paper>
              <Paper className="panel preview-panel" elevation={0}>
                {files.length ? <><Stack direction="row" alignItems="center" justifyContent="space-between" px={2}><Tabs value={activeFile} onChange={(_, value) => setActiveFile(value)} variant="scrollable" scrollButtons="auto">{files.map((file) => <Tab key={file.path} label={file.path} />)}</Tabs><Tooltip title="Copy source"><IconButton onClick={() => void navigator.clipboard.writeText(files[activeFile].source)}><ContentCopy fontSize="small" /></IconButton></Tooltip></Stack><Divider /><Box className="code-view" dangerouslySetInnerHTML={{ __html: files[activeFile].html }} /></> : <Stack className="preview-empty" alignItems="center" justifyContent="center" textAlign="center" spacing={1.5}><Box className="empty-icon"><Code /></Box><Typography variant="h6" fontWeight={700}>Your preview will appear here</Typography><Typography variant="body2" color="text.secondary" maxWidth={320}>Configure the variables, then generate a complete, syntax-highlighted project.</Typography></Stack>}
              </Paper>
            </Box>
          </>}
          {area === "records" && selectedRecord && <>
            <Stack gap={1} mb={3}>
              <Box><Chip icon={<MenuBookOutlined />} label={sectionTitles[selectedRecord.section_slug] || "Record"} size="small" variant="outlined" /><Typography component="h1" variant="h4" fontWeight={800} mt={1}>{selectedRecord.title}</Typography></Box>
              <Typography color="text.secondary" maxWidth={900}>{selectedRecord.description}</Typography>
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
    </Box>
  );
}
