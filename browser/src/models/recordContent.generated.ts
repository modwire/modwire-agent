// Generated from records.models.content.Content.Role. Do not edit by hand.
export const CONTENT_ROLE = {
  HEADING: "heading",
  SUBHEADING: "subheading",
  PARAGRAPH: "paragraph",
  LIST: "list",
  MARKDOWN: "markdown",
  SNIPPET: "snippet",
  IMAGE: "image",
} as const;

type ContentRole = typeof CONTENT_ROLE[keyof typeof CONTENT_ROLE];
type ContentMetadata = Record<string, unknown>;

type TextContent = {
  role: Exclude<ContentRole, typeof CONTENT_ROLE.LIST>;
  content: string;
  language: string;
  metadata: ContentMetadata;
};

type ListContent = {
  role: typeof CONTENT_ROLE.LIST;
  content: string[];
  language: string;
  metadata: ContentMetadata;
};

export type RecordContent = TextContent | ListContent;
