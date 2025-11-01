const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

async function request(path, { method = 'GET', body, headers = {} } = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    method,
    headers: {
      ...headers,
    },
    body,
    credentials: 'include', // include cookies
  });
  const text = await res.text();
  let data;
  try { data = text ? JSON.parse(text) : {}; } catch { data = { raw: text }; }
  if (!res.ok) {
    const msg = data?.detail || data?.message || res.statusText;
    throw new Error(msg);
  }
  return data;
}

export async function register(username, password) {
  return request('/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });
}

export async function login(username, password) {
  const params = new URLSearchParams();
  params.set('username', username);
  params.set('password', password);
  // OAuth2 password flow requires form-encoded
  return request('/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: params,
  });
}

export async function me() {
  return request('/me');
}

export async function logout() {
  return request('/logout', { method: 'POST' });
}
