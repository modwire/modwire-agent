import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import hljs from "highlight.js/lib/core";
import bash from "highlight.js/lib/languages/bash";
import css from "highlight.js/lib/languages/css";
import javascript from "highlight.js/lib/languages/javascript";
import json from "highlight.js/lib/languages/json";
import markdown from "highlight.js/lib/languages/markdown";
import python from "highlight.js/lib/languages/python";
import typescript from "highlight.js/lib/languages/typescript";
import xml from "highlight.js/lib/languages/xml";
import yaml from "highlight.js/lib/languages/yaml";
import "highlight.js/styles/github-dark.css";
import { useMemo } from "react";
import { CONTENT_ROLE, RecordContent } from "../models/recordContent.generated";

hljs.registerLanguage("bash", bash);
hljs.registerLanguage("css", css);
hljs.registerLanguage("javascript", javascript);
hljs.registerLanguage("json", json);
hljs.registerLanguage("markdown", markdown);
hljs.registerLanguage("python", python);
hljs.registerLanguage("typescript", typescript);
hljs.registerLanguage("xml", xml);
hljs.registerLanguage("yaml", yaml);

function SyntaxBlock({ source, language }: { source: string; language: string }) {
  const html = useMemo(() => {
    if (!hljs.getLanguage(language)) return hljs.highlightAuto(source).value;
    return hljs.highlight(source, { language, ignoreIllegals: true }).value;
  }, [language, source]);

  return (
    <Box className="record-snippet">
      <Typography component="span" className="record-snippet-language">{language}</Typography>
      <Box component="pre"><code className={`hljs language-${language}`} dangerouslySetInnerHTML={{ __html: html }} /></Box>
    </Box>
  );
}

export function RecordBlock({ block }: { block: RecordContent }) {
  if (block.role === CONTENT_ROLE.HEADING) return <Typography component="h2" variant="h5" fontWeight={800}>{block.content}</Typography>;
  if (block.role === CONTENT_ROLE.SUBHEADING) return <Typography component="h3" variant="h6" fontWeight={750}>{block.content}</Typography>;
  if (block.role === CONTENT_ROLE.LIST) return (
    <Box component="ul" sx={{ my: 0, pl: 3 }}>
      {block.content.map((item, index) => <li key={`${index}-${item}`}><Typography>{item}</Typography></li>)}
    </Box>
  );
  if (block.role === CONTENT_ROLE.SNIPPET) return <SyntaxBlock source={block.content} language={block.language} />;
  if (block.role === CONTENT_ROLE.IMAGE) return (
    <Box component="figure" sx={{ m: 0 }}>
      <Box component="img" src={block.content} alt={String(block.metadata.alt || "")} sx={{ display: "block", maxWidth: "100%", borderRadius: 1 }} />
      {block.metadata.title ? <Typography component="figcaption" variant="caption" color="text.secondary">{String(block.metadata.title)}</Typography> : null}
    </Box>
  );
  return <Typography sx={{ whiteSpace: "pre-wrap" }}>{block.content}</Typography>;
}
