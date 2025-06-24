export async function onRequestGet(context) {
    return new Response(JSON.stringify({
        message: 'Cloudflare Pages function is working!',
        timestamp: new Date().toISOString(),
        environment: {
            hasGitHubClientId: !!context.env.GITHUB_CLIENT_ID,
            hasGitHubClientSecret: !!context.env.GITHUB_CLIENT_SECRET
        }
    }), {
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    });
} 