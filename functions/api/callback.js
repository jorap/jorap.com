/** HTML that hands the OAuth token back to Sveltia CMS via postMessage. */
function sveltiaCallbackHtml({ provider = "github", token, error, errorCode }) {
  const state = error ? "error" : "success";
  const content = error
    ? { provider, error, errorCode }
    : { provider, token };
  const msg = `authorization:${provider}:${state}:${JSON.stringify(content)}`;

  return `<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>Authorization ${state}</title></head>
<body>
  <p>${error ? "Sign-in failed. You can close this window." : "Signed in. You can close this window."}</p>
  <script>
    (() => {
      const msg = ${JSON.stringify(msg)};
      window.addEventListener("message", ({ data, origin }) => {
        if (data === "authorizing:${provider}") {
          window.opener?.postMessage(msg, origin);
          window.close();
        }
      });
      window.opener?.postMessage("authorizing:${provider}", "*");
    })();
  </script>
</body>
</html>`;
}

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

  const code = url.searchParams.get("code");
  if (!code) {
    return new Response(
      sveltiaCallbackHtml({
        error: "Authorization code not found.",
        errorCode: "AUTH_CODE_REQUEST_FAILED",
      }),
      { headers: { "Content-Type": "text/html;charset=UTF-8" } },
    );
  }

  if (!env.GITHUB_CLIENT_ID || !env.GITHUB_CLIENT_SECRET) {
    return new Response(
      sveltiaCallbackHtml({
        error: "OAuth app client ID or secret is not configured.",
        errorCode: "MISCONFIGURED_CLIENT",
      }),
      { headers: { "Content-Type": "text/html;charset=UTF-8" } },
    );
  }

  const redirectUri = `${url.origin}/api/callback`;

  try {
    const tokenResponse = await fetch(
      "https://github.com/login/oauth/access_token",
      {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          client_id: env.GITHUB_CLIENT_ID,
          client_secret: env.GITHUB_CLIENT_SECRET,
          code,
          redirect_uri: redirectUri,
        }),
      },
    );

    const contentType = tokenResponse.headers.get("content-type") || "";
    if (!contentType.includes("application/json")) {
      const errorText = await tokenResponse.text();
      console.error("GitHub OAuth returned non-JSON response:", errorText);
      return new Response(
        sveltiaCallbackHtml({
          error: "GitHub returned an unexpected response format.",
          errorCode: "MALFORMED_RESPONSE",
        }),
        { headers: { "Content-Type": "text/html;charset=UTF-8" } },
      );
    }

    const tokenData = await tokenResponse.json();

    if (tokenData.error || !tokenData.access_token) {
      const message =
        tokenData.error_description || tokenData.error || "Token exchange failed.";
      console.error("GitHub OAuth token error:", message);
      return new Response(
        sveltiaCallbackHtml({
          error: message,
          errorCode: "TOKEN_REQUEST_FAILED",
        }),
        { headers: { "Content-Type": "text/html;charset=UTF-8" } },
      );
    }

    return new Response(
      sveltiaCallbackHtml({ token: tokenData.access_token }),
      { headers: { "Content-Type": "text/html;charset=UTF-8" } },
    );
  } catch (error) {
    console.error("OAuth callback error:", error);
    return new Response(
      sveltiaCallbackHtml({
        error: error.message || "Authentication error.",
        errorCode: "TOKEN_REQUEST_FAILED",
      }),
      { headers: { "Content-Type": "text/html;charset=UTF-8" } },
    );
  }
}
