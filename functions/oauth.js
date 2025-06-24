export async function onRequestGet(context) {
    const { request, env } = context;
    const url = new URL(request.url);
    const params = url.searchParams;

    const provider = params.get('provider');
    const site_id = params.get('site_id');

    if (provider === 'github') {
        // Redirect to GitHub OAuth
        const clientId = env.GITHUB_CLIENT_ID;
        const redirectUri = `${url.origin}/admin/oauth.html`;
        const scope = 'repo';

        const githubAuthUrl = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${scope}`;

        return Response.redirect(githubAuthUrl, 302);
    }

    return new Response('Invalid provider', { status: 400 });
}

export async function onRequestPost(context) {
    const { request, env } = context;

    try {
        // Add debugging for the incoming request
        const contentType = request.headers.get('content-type');
        const body = await request.text();
        
        // Try to parse the JSON
        let jsonData;
        try {
            jsonData = JSON.parse(body);
        } catch (parseError) {
            return new Response(JSON.stringify({ 
                error: 'JSON Parse Error',
                message: parseError.message,
                receivedBody: body,
                contentType: contentType
            }), {
                status: 400,
                headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
            });
        }
        
        const { code } = jsonData;

        if (!code) {
            return new Response(JSON.stringify({ 
                error: 'No code provided',
                receivedData: jsonData
            }), {
                status: 400,
                headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' }
            });
        }

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

        if (tokenData.access_token) {
            return new Response(JSON.stringify({
                token: tokenData.access_token
            }), {
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
            });
        } else {
            return new Response(JSON.stringify({
                error: 'Failed to get access token',
                details: tokenData
            }), {
                status: 400,
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                },
            });
        }
    } catch (error) {
        return new Response(JSON.stringify({
            error: 'Server error',
            message: error.message
        }), {
            status: 500,
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            },
        });
    }
} 