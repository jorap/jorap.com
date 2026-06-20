#!/usr/bin/env node
/**
 * Serve the built `public/` folder locally with Cloudflare Pages parity
 * (_headers, Functions under functions/). Requires a prior `pnpm run deploy`.
 */
import { existsSync } from "node:fs";
import { resolve } from "node:path";
import {
  projectRoot,
  resolveLocalBin,
  run,
  runNpx,
} from "./spawnUtil.mjs";

const publicDir = resolve(projectRoot, "public");
const port = process.env.PORT || "8788";
const host = process.env.HOST || "127.0.0.1";

if (!existsSync(publicDir)) {
  console.error("[serve] public/ not found. Run `pnpm run deploy` first.");
  process.exit(1);
}

const wranglerArgs = [
  "pages",
  "dev",
  "public",
  "--port",
  port,
  "--ip",
  host,
];

console.log(`[serve] ${publicDir} → http://${host}:${port}/`);
console.log("[serve] Uses wrangler (headers + functions/). Ctrl+C to stop.");

const localWrangler = resolveLocalBin("wrangler");
if (localWrangler) {
  run(localWrangler, wranglerArgs);
} else {
  runNpx(["--yes", "wrangler@4", ...wranglerArgs]);
}
