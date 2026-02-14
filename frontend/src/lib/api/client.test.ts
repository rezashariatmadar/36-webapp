import { afterEach, describe, expect, it, vi } from 'vitest'
import { apiFetch } from './client'

describe('apiFetch', () => {
  afterEach(() => {
    vi.restoreAllMocks()
    document.cookie = 'csrftoken=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/'
  })

  it('sends csrf header for write requests and returns parsed payload', async () => {
    document.cookie = 'csrftoken=test-csrf-token'
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ ok: true }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }),
    )

    const data = await apiFetch<{ ok: boolean }>('/api/x/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({}),
    })

    expect(data.ok).toBe(true)
    const [url, init] = fetchMock.mock.calls[0]
    expect(url).toBe('/api/x/')
    const headers = init?.headers as Headers
    expect(headers.get('X-CSRFToken')).toBe('test-csrf-token')
  })

  it('normalizes detail response errors', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ detail: 'denied' }), {
        status: 403,
        headers: { 'Content-Type': 'application/json' },
      }),
    )

    await expect(apiFetch('/api/x/')).rejects.toThrow('denied')
  })

  it('normalizes errors response object', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(JSON.stringify({ errors: { phone_number: ['required'] } }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      }),
    )

    await expect(apiFetch('/api/x/')).rejects.toThrow('phone_number')
  })
})

