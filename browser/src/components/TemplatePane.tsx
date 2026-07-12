import Box from "@mui/material/Box";
import Divider from "@mui/material/Divider";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";

export type TemplateSource = { id: string; scaffolding: string; relative_path: string; file_content: string; write_mode: string };

type TemplatePaneProps = {
  templates: TemplateSource[];
  activeTemplate: number;
  onSelect: (index: number) => void;
};

export function TemplatePane({ templates, activeTemplate, onSelect }: TemplatePaneProps) {
  const selected = templates[activeTemplate];
  return (
    <Paper className="panel template-panel" elevation={0}>
      {selected ? <>
        <Box className="preview-toolbar"><label className="file-select"><span>Template</span><select aria-label="Template file" value={activeTemplate} onChange={(event) => onSelect(Number(event.target.value))}>{templates.map((template, index) => <option value={index} key={template.id}>{template.relative_path}</option>)}</select></label></Box>
        <Divider />
        <Box component="pre" className="template-view">{selected.file_content}</Box>
      </> : <Box className="preview-empty"><Typography variant="body2" color="text.secondary">No templates in this scaffolding.</Typography></Box>}
    </Paper>
  );
}
