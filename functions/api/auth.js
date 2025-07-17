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

    // GET request - redirect to GitHub OAuth
    if (request.method === 'GET') {
        const state = url.searchParams.get('state') || '';
        const scope = 'repo,user';

        const authUrl = `https://github.com/login/oauth/authorize?client_id=${env.GITHUB_CLIENT_ID}&redirect_uri=${encodeURIComponent(url.origin + '/api/callback')}&scope=${scope}&state=${state}`;

        return Response.redirect(authUrl, 302);
    }

    return new Response('Method not allowed', { status: 405 });
}