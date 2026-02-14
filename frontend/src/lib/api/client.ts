export type ApiErrorPayload = { detail?: string; errors?: unknown }

const getCookie = (name: string): string => {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length !== 2) return ''
  return parts.pop()?.split(';').shift() ?? ''
}

const stringifyErrors = (errors: unknown): string => {
  if (typeof errors === 'string') return errors
  try {
    return JSON.stringify(errors)
  } catch {
    return 'Unknown error'
  }
}

export async function apiFetch<T>(url: string, init: RequestInit = {}): Promise<T> {
  const method = init.method ?? 'GET'
  const headers = new Headers(init.headers ?? {})
  headers.set('Accept', 'application/json')

  const isWrite = !['GET', 'HEAD', 'OPTIONS'].includes(method.toUpperCase())
  if (isWrite && !headers.has('X-CSRFToken')) headers.set('X-CSRFToken', getCookie('csrftoken'))

  const response = await fetch(url, {
    ...init,
    headers,
    credentials: 'include',
  })

  let payload: ApiErrorPayload | T | null = null
  try {
    payload = (await response.json()) as ApiErrorPayload | T
  } catch {
    payload = null
  }

  if (!response.ok) {
    const err = payload as ApiErrorPayload | null
    const message = err?.detail ?? stringifyErrors(err?.errors) ?? `HTTP ${response.status}`
    throw new Error(message)
  }

  return payload as T
}

