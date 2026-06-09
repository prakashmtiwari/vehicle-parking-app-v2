export const API_HOST = import.meta.env.VITE_API_BASE_URL || ''

export function buildApiUrl(path) {
  if (!path.startsWith('/')) {
    path = `/${path}`
  }
  return `${API_HOST}${path}`
}
