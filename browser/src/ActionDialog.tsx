import { useEffect, useState } from 'react'
import { Alert, Button, Checkbox, Dialog, DialogActions, DialogContent, DialogTitle, FormControlLabel, MenuItem, Stack, TextField } from '@mui/material'
import type { SirenAction, SirenField } from './types'

const initial = (field: SirenField) => field.type === 'checkbox' ? Boolean(field.value) : field.type === 'json' ? JSON.stringify(field.value ?? (field.schema && (field.schema as {type?: string}).type === 'array' ? [] : {}), null, 2) : field.value ?? ''

export function ActionDialog({ action, onClose, onComplete }: {action: SirenAction | null; onClose: () => void; onComplete: (href?: string) => void}) {
  const [values, setValues] = useState<Record<string, unknown>>({})
  const [error, setError] = useState('')
  const fields = action?.fields ?? []
  useEffect(() => setValues(Object.fromEntries(fields.map(field => [field.name, initial(field)]))), [action])
  if (!action) return null
  const submit = async () => {
    setError('')
    try {
      const parsed = Object.fromEntries(fields.filter(f => !f.name.includes('{')).map(field => {
        let value = values[field.name]
        if (field.type === 'json' && typeof value === 'string') value = JSON.parse(value)
        if (field.type === 'number' && value !== '') value = Number(value)
        return [field.name, value]
      }))
      const method = action.method ?? 'GET'
      const target = new URL(action.href)
      if (method === 'GET') Object.entries(parsed).forEach(([name, value]) => {
        if (value === '' || value === undefined) return
        if (Array.isArray(value)) value.forEach(item => target.searchParams.append(name, String(item)))
        else target.searchParams.set(name, String(value))
      })
      const response = await fetch(target, { method, headers: {'apikey': sessionStorage.getItem('modwire.apikey') ?? '', 'Content-Type': action.type ?? 'application/json', Accept: 'application/vnd.siren+json'}, body: ['GET', 'DELETE'].includes(method) ? undefined : JSON.stringify(parsed) })
      if (!response.ok) { const body = await response.json().catch(() => ({})); throw new Error(typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail ?? body)) }
      onComplete(response.headers.get('Location') ?? action.href)
    } catch (e) { setError(e instanceof Error ? e.message : String(e)) }
  }
  return <Dialog open maxWidth="sm" fullWidth onClose={onClose}><DialogTitle>{action.title ?? action.name}</DialogTitle><DialogContent><Stack spacing={2} sx={{pt: 1}}>{error && <Alert severity="error">{error}</Alert>}{fields.filter(f => !f.name.includes('{')).map(field => field.type === 'checkbox' ? <FormControlLabel key={field.name} control={<Checkbox checked={Boolean(values[field.name])} onChange={e => setValues({...values, [field.name]: e.target.checked})}/>} label={field.title ?? field.name}/> : <TextField key={field.name} select={Boolean(field.options)} multiline={field.type === 'json'} minRows={field.type === 'json' ? 4 : undefined} type={field.type === 'number' ? 'number' : 'text'} required={field.required} label={field.title ?? field.name} helperText={field.description} value={String(values[field.name] ?? '')} onChange={e => setValues({...values, [field.name]: e.target.value})}>{field.options?.map(option => <MenuItem key={String(option.value)} value={String(option.value)}>{option.title}</MenuItem>)}</TextField>)}</Stack></DialogContent><DialogActions><Button onClick={onClose}>Cancel</Button><Button variant="contained" color={action.method === 'DELETE' ? 'error' : 'primary'} onClick={submit}>{action.method === 'DELETE' ? 'Delete' : 'Run'}</Button></DialogActions></Dialog>
}
