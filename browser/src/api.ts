import Ketting from 'ketting'

export const KEY_NAME = 'modwire.apikey'
export const getKey = () => sessionStorage.getItem(KEY_NAME) ?? ''
export const setKey = (key: string) => key ? sessionStorage.setItem(KEY_NAME, key) : sessionStorage.removeItem(KEY_NAME)

export function createClient() {
  const client = new Ketting(new URL('/api/', window.location.origin).href)
  client.use(async (request, next) => {
    request.headers.set('Accept', 'application/vnd.siren+json')
    const key = getKey()
    if (key) request.headers.set('apikey', key)
    const response = await next(request)
    if (response.status === 401) setKey('')
    return response
  })
  return client
}
