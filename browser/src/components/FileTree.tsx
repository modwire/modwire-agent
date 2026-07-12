import DescriptionOutlined from "@mui/icons-material/DescriptionOutlined";
import FolderOutlined from "@mui/icons-material/FolderOutlined";
import Box from "@mui/material/Box";
import { useMemo } from "react";

export type PreviewFile = { template_id: string; path: string; source: string; html: string; language: string };

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

export function FileTree({ files, activeFile, onSelect }: { files: PreviewFile[]; activeFile: number; onSelect: (index: number) => void }) {
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
