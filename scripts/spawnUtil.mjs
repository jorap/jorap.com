/**
 * Cross-platform process helpers for deploy/build scripts (macOS, Linux, Windows).
 */
import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
export const projectRoot = resolve(__dirname, "..");
const isWin = process.platform === "win32";

/** Node binary running these scripts — reliable even when `node` is not on PATH. */
export const nodeBin = process.execPath;

/**
 * Resolve an npm/pnpm binary under node_modules/.bin (handles .cmd on Windows).
 */
export function resolveLocalBin(name) {
  const binDir = join(projectRoot, "node_modules", ".bin");
  const candidates = isWin ? [`${name}.cmd`, `${name}.ps1`, name] : [name];
  for (const file of candidates) {
    const full = join(binDir, file);
    if (existsSync(full)) return full;
  }
  return null;
}

function needsShell(cmd) {
  return isWin && /\.(cmd|bat|ps1)$/i.test(cmd);
}

/**
 * Run a command; throws nothing — exits the process on failure.
 */
export function run(cmd, args = [], opts = {}) {
  const cwd = opts.cwd ?? projectRoot;
  const shell = opts.shell ?? needsShell(cmd);

  const result = spawnSync(cmd, args, {
    stdio: "inherit",
    cwd,
    shell,
    env: opts.env ?? process.env,
  });

  if (result.error) {
    console.error(`[run] Failed to start ${cmd}:`, result.error.message);
    process.exit(1);
  }
  if (result.status !== 0) {
    process.exit(result.status ?? 1);
  }
}

export function runNodeScript(scriptPath, args = []) {
  run(nodeBin, [scriptPath, ...args]);
}

export function runNpx(args) {
  const npx = resolveLocalBin("npx");
  if (npx) {
    run(npx, args);
    return;
  }
  run(isWin ? "npx.cmd" : "npx", args, { shell: isWin });
}

export function capture(cmd, args = []) {
  return spawnSync(cmd, args, {
    encoding: "utf8",
    cwd: projectRoot,
    shell: needsShell(cmd),
  });
}
