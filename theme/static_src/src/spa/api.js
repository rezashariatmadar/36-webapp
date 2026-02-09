let csrfTokenCache = '';

const getCookie = (name) => {
  const cookie = `; ${document.cookie}`;
  const chunks = cookie.split(`; ${name}=`);
  if (chunks.length !== 2) return '';
  return chunks.pop().split(';').shift() || '';
};

export const setCsrfToken = (token) => {
  if (!token) return;
  csrfTokenCache = token;
};

export const apiFetch = async (path, options = {}) => {
  const method = options.method || 'GET';
  const headers = new Headers(options.headers || {});
  headers.set('Accept', 'application/json');
  const isWrite = !['GET', 'HEAD', 'OPTIONS'].includes(method.toUpperCase());

  if (isWrite && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json');
  }
  if (isWrite && !headers.has('X-CSRFToken')) {
    headers.set('X-CSRFToken', csrfTokenCache || getCookie('csrftoken'));
  }

  const response = await fetch(path, {
    ...options,
    method,
    headers,
    credentials: 'same-origin',
  });

  let payload = null;
  try {
    payload = await response.json();
  } catch {
    payload = null;
  }

  if (!response.ok) {
    const detail = payload?.detail || payload?.errors || `HTTP ${response.status}`;
    throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail));
  }
  return payload;
};
