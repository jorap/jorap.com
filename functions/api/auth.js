export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  if (request.method === "OPTIONS") {
    return new Response(null, {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
      },
    });
  }

  if (request.method !== "GET") {
    return new Response("Method not allowed", { status: 405 });
  }

  if (!env.GITHUB_CLIENT_ID || !env.GITHUB_CLIENT_SECRET) {
    return new Response(
      "CMS OAuth is not configured. Set GITHUB_CLIENT_ID in wrangler.toml [vars] and GITHUB_CLIENT_SECRET as a Pages secret (dashboard or wrangler pages secret put). Redeploy after changes.",
      { status: 500, headers: { "Content-Type": "text/plain;charset=UTF-8" } },
    );
  }

  const state = url.searchParams.get("state") || "";
  const scope = url.searchParams.get("scope") || "repo,user";
  const redirectUri = `${url.origin}/api/callback`;
  const authUrl = new URL("https://github.com/login/oauth/authorize");
  authUrl.searchParams.set("client_id", env.GITHUB_CLIENT_ID);
  authUrl.searchParams.set("redirect_uri", redirectUri);
  authUrl.searchParams.set("scope", scope);
  authUrl.searchParams.set("state", state);

  return Response.redirect(authUrl.toString(), 302);
}
