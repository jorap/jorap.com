/**
 * Hugo css.TailwindCSS must execute tailwindcss as a Node .mjs entry — not pnpm's shell shim.
 * See: https://github.com/gohugoio/hugo/issues/14852
 */
const fs = require("fs");
const path = require("path");

const binPath = path.join(__dirname, "../node_modules/.bin/tailwindcss");
const target = "../@tailwindcss/cli/dist/index.mjs";

function needsFix() {
  if (!fs.existsSync(binPath)) return false;
  const stat = fs.lstatSync(binPath);
  if (!stat.isSymbolicLink()) return true;
  const link = fs.readlinkSync(binPath);
  return !link.replace(/\\/g, "/").endsWith("@tailwindcss/cli/dist/index.mjs");
}

try {
  if (!needsFix()) return;
  if (fs.existsSync(binPath)) fs.unlinkSync(binPath);
  fs.symlinkSync(target, binPath);
} catch (err) {
  console.warn("fix-tailwind-bin:", err.message);
}
