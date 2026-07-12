import ContentCopy from "@mui/icons-material/ContentCopy";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import Paper from "@mui/material/Paper";
import Tooltip from "@mui/material/Tooltip";
import Typography from "@mui/material/Typography";
import { PreviewFile } from "./FileTree";

type PreviewPaneProps = {
  file?: PreviewFile;
  loading: boolean;
  previewing: boolean;
  onPreview: () => void;
};

export function PreviewPane({ file, loading, previewing, onPreview }: PreviewPaneProps) {
  if (!file) return (
    <Paper className="panel preview-panel" elevation={0}>
      <Box className="preview-empty"><Button variant="contained" disabled={previewing || loading} onClick={onPreview}>{previewing ? "Rendering…" : "Render preview"}</Button></Box>
    </Paper>
  );

  return (
    <Paper className="panel preview-panel" elevation={0}>
      <Box className="preview-toolbar">
        <Typography variant="body2" fontWeight={650} noWrap>{file.path}</Typography>
        <Box className="preview-actions">
          <Button size="small" disabled={previewing || loading} onClick={onPreview}>{previewing ? "Rendering…" : "Render again"}</Button>
          <Tooltip title="Copy source"><IconButton aria-label="Copy source" onClick={() => void navigator.clipboard.writeText(file.source)}><ContentCopy fontSize="small" /></IconButton></Tooltip>
        </Box>
      </Box>
      <Divider />
      <Box className="code-view" dangerouslySetInnerHTML={{ __html: file.html }} />
    </Paper>
  );
}
