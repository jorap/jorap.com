export async function onRequest(context) {
    const { request, env } = context;
    const url = new URL(request.url);

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
        return new Response(null, {
            headers: {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            },
        });
    }

    if (request.method === 'GET') {
        const code = url.searchParams.get('code');
        const state = url.searchParams.get('state');

        if (!code) {
            return new Response('Authorization code not found', { status: 400 });
        }

        try {
            // Exchange code for access token
            const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    client_id: env.GITHUB_CLIENT_ID,
                    client_secret: env.GITHUB_CLIENT_SECRET,
                    code: code,
                }),
            });

            const tokenData = await tokenResponse.json();

            if (tokenData.error) {
                return new Response(`GitHub OAuth error: ${tokenData.error_description}`, { status: 400 });
            }

            const { access_token, token_type } = tokenData;

            // Get user info
            const userResponse = await fetch('https://api.github.com/user', {
                headers: {
                    'Authorization': `${token_type} ${access_token}`,
                },
            });

            const userData = await userResponse.json();

            // Create response with token and user info
            const responseData = {
                token: access_token,
                provider: 'github',
                user: {
                    id: userData.id,
                    login: userData.login,
                    email: userData.email,
                    name: userData.name,
                    avatar_url: userData.avatar_url,
                },
            };

            // Return HTML that posts message to parent window (for CMS)
            const html = `
        <!DOCTYPE html>
        <html>
        <head>
          <title>Authorization Success</title>
        </head>
        <body>
          <h1>Authorization successful!</h1>
          <p>You can close this window.</p>
          <script>
            // Post message to parent window with the auth data
            if (window.opener) {
              window.opener.postMessage({
                type: 'authorization_code',
                provider: 'github',
                token: '${access_token}',
                user: ${JSON.stringify(responseData.user)}
              }, '*');
              window.close();
            }
          </script>
        </body>
        </html>
      `;

            return new Response(html, {
                headers: {
                    'Content-Type': 'text/html',
                    'Access-Control-Allow-Origin': '*',
                },
            });

        } catch (error) {
            console.error('OAuth callback error:', error);
            return new Response(`Authentication error: ${error.message}`, { status: 500 });
        }
    }

    return new Response('Method not allowed', { status: 405 });
}