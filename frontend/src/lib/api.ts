let csrfTokenCache = '';
let csrfBootstrapPromise: Promise<void> | null = null;

const SAFE_METHODS = new Set(['GET', 'HEAD', 'OPTIONS']);

function getCookie(name: string): string {
  const cookie = `; ${document.cookie}`;
  const chunks = cookie.split(`; ${name}=`);
  if (chunks.length !== 2) return '';
  return chunks.pop()?.split(';').shift() || '';
}

export function setCsrfToken(token: string | undefined): void {
  if (!token) return;
  csrfTokenCache = token;
}

export async function ensureCsrfCookie(): Promise<void> {
  if (csrfBootstrapPromise) {
    return csrfBootstrapPromise;
  }

  csrfBootstrapPromise = fetch('/api/auth/csrf/', {
    method: 'GET',
    credentials: 'include',
    headers: {
      Accept: 'application/json',
    },
  }).then(async (response) => {
    if (!response.ok) {
      throw new Error(`Unable to initialize CSRF cookie (HTTP ${response.status})`);
    }
    try {
      const payload = (await response.json()) as { csrf_token?: string };
      if (payload?.csrf_token) {
        setCsrfToken(payload.csrf_token);
      }
    } catch {
      // Ignore empty payloads, cookie is still set by ensure_csrf_cookie.
    }
  });

  return csrfBootstrapPromise;
}

type ApiFetchOptions = RequestInit & { skipCsrfBootstrap?: boolean };

export async function apiFetch<T>(path: string, options: ApiFetchOptions = {}): Promise<T> {
  const method = (options.method || 'GET').toUpperCase();
  const isWrite = !SAFE_METHODS.has(method);
  const headers = new Headers(options.headers || {});

  headers.set('Accept', 'application/json');

  if (isWrite && !options.skipCsrfBootstrap && !csrfTokenCache && !getCookie('csrftoken')) {
    await ensureCsrfCookie();
  }

  if (isWrite && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }

  if (isWrite && !headers.has('X-CSRFToken')) {
    const csrfToken = csrfTokenCache || getCookie('csrftoken');
    if (csrfToken) {
      headers.set('X-CSRFToken', csrfToken);
    }
  }

  const response = await fetch(path, {
    ...options,
    method,
    headers,
    credentials: 'include',
  });

  let payload: unknown = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (payload && typeof payload === 'object' && 'csrf_token' in (payload as Record<string, unknown>)) {
    const csrfToken = (payload as { csrf_token?: string }).csrf_token;
    setCsrfToken(csrfToken);
  }

  if (!response.ok) {
    const errorPayload = payload as { detail?: unknown; errors?: unknown } | null;
    const detail = errorPayload?.detail || errorPayload?.errors || `HTTP ${response.status}`;
    throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail));
  }

  return payload as T;
}

