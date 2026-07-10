export type SirenLink = { rel: string[]; href: string; title?: string; type?: string }
export type SirenField = { name: string; type?: string; title?: string; description?: string; required?: boolean; value?: unknown; options?: {value: unknown; title: string}[]; schema?: unknown }
export type SirenAction = { name: string; title?: string; method?: string; href: string; type?: string; fields?: SirenField[] }
export type SirenEntity = { class?: string[]; rel?: string[]; properties?: Record<string, unknown>; links?: SirenLink[]; entities?: SirenEntity[]; actions?: SirenAction[] }
