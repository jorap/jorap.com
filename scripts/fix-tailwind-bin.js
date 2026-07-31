/**
 * Hugo css.TailwindCSS must execute tailwindcss as a Node .mjs entry - not pnpm's shell shim.
 * See: https://github.com/gohugoio/hugo/issues/14852
 *
 * Writes a tiny Node shim to node_modules/.bin/tailwindcss (no symlinks).
 * On Windows also overwrites tailwindcss.cmd / tailwindcss.ps1 so pnpm wrappers
 * do not win when Hugo or the shell resolves the binary.
 */
const fs = require("fs");
const path = require("path");

const SHIM_MARKER = "fix-tailwind-bin-shim";
const binDir = path.join(__dirname, "../node_modules/.bin");
const binPath = path.join(binDir, "tailwindcss");
const shimMjsPath = path.join(binDir, "tailwindcss-shim.mjs");
const isWin = process.platform === "win32";

const shimMjsSource = `// ${SHIM_MARKER}
import { createRequire } from "node:module";
import { pathToFileURL } from "node:url";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(
  join(dirname(fileURLToPath(import.meta.url)), "../../package.json"),
);
const cliEntry = join(
  dirname(require.resolve("@tailwindcss/cli/package.json")),
  "dist/index.mjs",
);
await import(pathToFileURL(cliEntry).href);
`;

const unixLauncherSource = `#!/usr/bin/env node
// ${SHIM_MARKER}
import "./tailwindcss-shim.mjs";
`;

// cmd.exe expects CRLF; LF-only batch files can misparse at 512-byte boundaries.
const winCmdSource = [
  "@ECHO off",
  `REM ${SHIM_MARKER}`,
  'node "%~dp0tailwindcss-shim.mjs" %*',
].join("\r\n") + "\r\n";

const winPs1Source = `#!/usr/bin/env pwsh
# ${SHIM_MARKER}
$basedir = Split-Path $MyInvocation.MyCommand.Definition -Parent
& node (Join-Path $basedir "tailwindcss-shim.mjs") @args
exit $LASTEXITCODE
`;

function readText(filePath) {
  if (!fs.existsSync(filePath)) return "";
  return fs.readFileSync(filePath, "utf8");
}

function isFixed() {
  if (!readText(shimMjsPath).includes(SHIM_MARKER)) return false;
  if (!readText(binPath).includes(SHIM_MARKER)) return false;
  if (isWin) {
    if (!readText(path.join(binDir, "tailwindcss.cmd")).includes(SHIM_MARKER)) {
      return false;
    }
    if (!readText(path.join(binDir, "tailwindcss.ps1")).includes(SHIM_MARKER)) {
      return false;
    }
  }
  if (fs.existsSync(binPath) && fs.lstatSync(binPath).isSymbolicLink()) return false;
  return true;
}

function writeExecutable(filePath, content) {
  // Unlink first: pnpm on macOS/Linux often symlinks .bin entries; writing
  // through a symlink would corrupt the real @tailwindcss/cli package.
  if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
  fs.writeFileSync(filePath, content, { encoding: "utf8", mode: 0o755 });
}

function applyFix() {
  if (!fs.existsSync(path.join(__dirname, "../node_modules/@tailwindcss/cli"))) {
    console.warn("fix-tailwind-bin: @tailwindcss/cli not found; skipping.");
    return;
  }

  if (!fs.existsSync(binDir)) fs.mkdirSync(binDir, { recursive: true });

  writeExecutable(shimMjsPath, shimMjsSource);
  writeExecutable(binPath, unixLauncherSource);

  if (isWin) {
    writeExecutable(path.join(binDir, "tailwindcss.cmd"), winCmdSource);
    writeExecutable(path.join(binDir, "tailwindcss.ps1"), winPs1Source);
  }
}

function selfCheck() {
  const failures = [];
  const posixBinDir = "/Users/dev/proj/node_modules/.bin";
  const posixPkg = path.posix.normalize(
    path.posix.join(posixBinDir, "..", "..", "package.json"),
  );
  if (posixPkg !== "/Users/dev/proj/package.json") {
    failures.push(`posix package.json path: got ${posixPkg}`);
  }

  const winBinDir = "C:\\proj\\node_modules\\.bin";
  const winPkg = path.win32.normalize(
    path.win32.join(winBinDir, "..", "..", "package.json"),
  );
  if (winPkg !== "C:\\proj\\package.json") {
    failures.push(`win32 package.json path: got ${winPkg}`);
  }

  for (const [name, source] of [
    ["shimMjsSource", shimMjsSource],
    ["unixLauncherSource", unixLauncherSource],
    ["winCmdSource", winCmdSource],
    ["winPs1Source", winPs1Source],
  ]) {
    if (!source.includes(SHIM_MARKER)) failures.push(`${name} missing marker`);
  }

  if (!shimMjsSource.includes("pathToFileURL(cliEntry)")) {
    failures.push("shim must import CLI via file URL");
  }
  if (!winCmdSource.includes("\r\n")) {
    failures.push("winCmdSource must use CRLF line endings");
  }

  if (failures.length) {
    console.error("fix-tailwind-bin self-check failed:");
    for (const msg of failures) console.error(`  - ${msg}`);
    process.exit(1);
  }
  console.log("fix-tailwind-bin self-check OK");
}

if (process.argv.includes("--self-check")) {
  selfCheck();
} else {
  try {
    if (!isFixed()) applyFix();
  } catch (err) {
    console.warn("fix-tailwind-bin:", err.message);
  }
}
