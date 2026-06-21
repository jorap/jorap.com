/**
 * Resolve Hugo Extended at the pinned version. Uses PATH when correct,
 * otherwise downloads into .cache/hugo/<version>/ (Linux / Windows CI).
 */
import { chmodSync, existsSync, mkdirSync, readFileSync, rmSync } from "node:fs";
import { arch, platform } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { capture, projectRoot, run } from "./spawnUtil.mjs";

const __dirname = dirname(fileURLToPath(import.meta.url));

export function readPinnedHugoVersion() {
  return JSON.parse(
    readFileSync(join(__dirname, "deploy-versions.json"), "utf8"),
  ).hugo;
}

function parseHugoVersion(stdout) {
  const line = (stdout || "").trim();
  if (!/extended/i.test(line)) return null;
  const match = line.match(/v(\d+\.\d+\.\d+)/);
  return match ? match[1] : null;
}

/** Same major.minor (patch drift OK on local macOS). */
function sameMinor(a, b) {
  const pa = a.split(".").map(Number);
  const pb = b.split(".").map(Number);
  return pa[0] === pb[0] && pa[1] === pb[1];
}

function pathHugoVersion() {
  const result = capture("hugo", ["version"]);
  if (result.status !== 0 || !result.stdout) return null;
  return parseHugoVersion(result.stdout);
}

function cacheDir(version) {
  return join(projectRoot, ".cache", "hugo", version);
}

function cachedBinary(version) {
  const bin =
    platform() === "win32"
      ? join(cacheDir(version), "hugo.exe")
      : join(cacheDir(version), "hugo");
  return existsSync(bin) ? bin : null;
}

function assetForPlatform(version) {
  const p = platform();
  const a = arch();
  if (p === "linux") {
    if (a === "arm64") return `hugo_extended_${version}_linux-arm64.tar.gz`;
    return `hugo_extended_${version}_linux-amd64.tar.gz`;
  }
  if (p === "win32") {
    return `hugo_extended_${version}_windows-amd64.zip`;
  }
  return null;
}

function downloadUrl(version, asset) {
  return `https://github.com/gohugoio/hugo/releases/download/v${version}/${asset}`;
}

function installHugo(version) {
  const asset = assetForPlatform(version);
  if (!asset) {
    console.error(`[deploy] Hugo ${version} (extended) not found on PATH.`);
    console.error(
      `[deploy] Install it locally (e.g. mise use hugo-extended@${version}) or set HUGO_VERSION=${version} in CI.`,
    );
    process.exit(1);
  }

  const dir = cacheDir(version);
  mkdirSync(dir, { recursive: true });
  const archivePath = join(dir, asset);

  console.log(`[deploy] Installing Hugo Extended ${version} (${asset})...`);
  run("curl", ["-fsSL", "-o", archivePath, downloadUrl(version, asset)]);

  if (asset.endsWith(".tar.gz") || asset.endsWith(".zip")) {
    run("tar", ["-xf", archivePath, "-C", dir]);
  }

  rmSync(archivePath, { force: true });

  const bin = cachedBinary(version);
  if (!bin) {
    console.error(`[deploy] Hugo binary missing after extracting ${asset}.`);
    process.exit(1);
  }
  if (platform() !== "win32") {
    chmodSync(bin, 0o755);
  }

  const check = capture(bin, ["version"]);
  const got = parseHugoVersion(check.stdout);
  if (got !== version) {
    console.error(`[deploy] Expected Hugo ${version}, got ${check.stdout}`);
    process.exit(1);
  }
  console.log(`[deploy] Using cached Hugo: ${check.stdout.trim()}`);
  return bin;
}

/** @returns {string} Path to hugo binary (or "hugo" when PATH is correct). */
export function ensureHugo() {
  const pinned = readPinnedHugoVersion();
  const fromPath = pathHugoVersion();
  if (fromPath === pinned) {
    return "hugo";
  }

  // Homebrew/mise often differ by patch; macOS has no auto-download fallback.
  if (platform() === "darwin" && fromPath && sameMinor(fromPath, pinned)) {
    console.warn(
      `[deploy] Hugo ${fromPath} on PATH (pinned ${pinned}); using PATH on macOS.`,
    );
    return "hugo";
  }

  const cached = cachedBinary(pinned);
  if (cached) {
    const got = parseHugoVersion(capture(cached, ["version"]).stdout);
    if (got === pinned) {
      if (fromPath && fromPath !== pinned) {
        console.warn(
          `[deploy] Hugo ${fromPath} on PATH ignored; using pinned ${pinned} from .cache`,
        );
      }
      return cached;
    }
  }

  if (fromPath && fromPath !== pinned) {
    console.warn(
      `[deploy] Hugo ${fromPath} != pinned ${pinned}; installing pinned version...`,
    );
  } else if (!fromPath) {
    console.warn(`[deploy] Hugo not on PATH; installing pinned ${pinned}...`);
  }

  return installHugo(pinned);
}
