const BASE = import.meta.env.VITE_API_BASE || '';
export async function api(path, options = {}) {
  const response = await fetch(BASE + path, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
  });
  let data = {};
  try { data = await response.json(); } catch { /* show generic error */ }
  if (!response.ok) {
    const message = typeof data.detail === 'string'
      ? data.detail : JSON.stringify(data.detail || 'Request failed');
    throw new Error(message);
  }
  return data;
}
