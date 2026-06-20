/**
 * Hugo css.TailwindCSS must execute tailwindcss as a Node .mjs entry — not pnpm's shell shim.
 * See: https://github.com/gohugoio/hugo/issues/14852
 *
 * macOS/Linux: symlink to @tailwindcss/cli/dist/index.mjs
 * Windows: copy index.mjs when symlinks are unavailable (no Developer Mode / admin)
 */
const fs = require("fs");
const path = require("path");

const binPath = path.join(__dirname, "../node_modules/.bin/tailwindcss");
const cliMjs = path.join(
  __dirname,
  "../node_modules/@tailwindcss/cli/dist/index.mjs",
);
const symlinkTarget = "../@tailwindcss/cli/dist/index.mjs";

function isFixed() {
  if (!fs.existsSync(binPath)) return false;

  const stat = fs.lstatSync(binPath);
  if (stat.isSymbolicLink()) {
    const link = fs.readlinkSync(binPath);
    return link.replace(/\\/g, "/").endsWith("@tailwindcss/cli/dist/index.mjs");
  }

  // Windows fallback: index.mjs copied over the pnpm/npm shim
  if (!stat.isFile() || !fs.existsSync(cliMjs)) return false;
  return fs.statSync(binPath).size === fs.statSync(cliMjs).size;
}

function needsFix() {
  return fs.existsSync(binPath) && !isFixed();
}

function applyFix() {
  if (fs.existsSync(binPath)) fs.unlinkSync(binPath);

  try {
    fs.symlinkSync(symlinkTarget, binPath);
    return;
  } catch {
    // Windows often blocks symlinks without Developer Mode or elevated shell.
  }

  if (!fs.existsSync(cliMjs)) {
    console.warn("fix-tailwind-bin: @tailwindcss/cli not found; skipping.");
    return;
  }

  fs.copyFileSync(cliMjs, binPath);
}

try {
  if (!needsFix()) return;
  applyFix();
} catch (err) {
  console.warn("fix-tailwind-bin:", err.message);
}
