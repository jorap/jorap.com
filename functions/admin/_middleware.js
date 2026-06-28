// Cloudflare Pages merges _headers from `/*` and `/admin/*`, so the browser
// gets two Content-Security-Policy values and must satisfy both. The site-wide
// CSP blocks unpkg.com and runtime inline scripts, which leaves Sveltia CMS blank.
// Replace every CSP on /admin/* with the admin-only policy from static/_headers.
const ADMIN_CSP =
  "default-src 'self'; base-uri 'self'; form-action 'self' https://github.com; frame-ancestors 'self'; img-src 'self' data: blob: https://*.githubusercontent.com https://avatars.githubusercontent.com https://raw.githubusercontent.com https://www.gravatar.com https:; font-src 'self' data:; style-src 'self' 'unsafe-inline'; style-src-attr 'unsafe-inline'; script-src 'self' 'unsafe-inline' https://unpkg.com https://static.cloudflareinsights.com; script-src-elem 'self' 'unsafe-inline' https://unpkg.com https://static.cloudflareinsights.com; connect-src 'self' https://api.github.com https://github.com https://raw.githubusercontent.com https://*.githubusercontent.com https://unpkg.com https://cloudflareinsights.com; frame-src 'self' https://github.com; worker-src 'self' blob:; object-src 'none'; manifest-src 'self'; upgrade-insecure-requests";

export async function onRequest(context) {
  const response = await context.next();
  const headers = new Headers(response.headers);
  headers.delete("Content-Security-Policy");
  headers.set("Content-Security-Policy", ADMIN_CSP);
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
}
