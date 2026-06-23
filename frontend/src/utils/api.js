export const API = import.meta.env.DEV ? 'http://localhost:8000/api' : '/_/backend/api';

/**
 * Helper to safely handle fetch responses and parse error messages.
 * Catches HTML error responses and parses JSON responses safely.
 */
export const handleResponse = async (res, defaultMessage) => {
  const contentType = res.headers.get('content-type');
  const isJson = contentType && contentType.includes('application/json');

  if (res.ok) {
    if (isJson) {
      try {
        return await res.json();
      } catch (err) {
        throw new Error('Failed to parse successful response as JSON: ' + err.message);
      }
    } else {
      const text = await res.text();
      return text;
    }
  }

  let errorMessage = defaultMessage;
  try {
    if (isJson) {
      const err = await res.json();
      errorMessage = err.detail || errorMessage;
    } else {
      const text = await res.text();
      // If the response is HTML, don't show the raw HTML tags
      if (text && (text.trim().startsWith('<') || text.includes('<html>') || text.includes('<!DOCTYPE'))) {
        errorMessage = `Server Error ${res.status}: ${res.statusText}`;
      } else {
        errorMessage = text || `Error ${res.status}: ${res.statusText}`;
      }
    }
  } catch (e) {
    errorMessage = `Error ${res.status}: ${res.statusText}`;
  }
  throw new Error(errorMessage);
};
