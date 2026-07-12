import { ReactNode } from "react";
import { Group, Panel, Separator } from "react-resizable-panels";

type EditorPanelsProps = {
  id: string;
  label: string;
  primary: ReactNode;
  secondary: ReactNode;
  primarySize?: string;
  primaryMinSize?: string;
};

export function EditorPanels({
  id,
  label,
  primary,
  secondary,
  primarySize = "280px",
  primaryMinSize = "220px",
}: EditorPanelsProps) {
  return (
    <Group id={id} orientation="horizontal" className="editor-panels" aria-label={label}>
      <Panel id={`${id}-primary`} defaultSize={primarySize} minSize={primaryMinSize} className="editor-panel">
        {primary}
      </Panel>
      <Separator className="panel-resize-handle" aria-label={`Resize ${label}`}>
        <span />
      </Separator>
      <Panel id={`${id}-secondary`} minSize="320px" className="editor-panel">
        {secondary}
      </Panel>
    </Group>
  );
}
