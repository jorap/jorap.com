#!/usr/bin/env node
/** ponytail: O(n) path check; upgrade = parse writing-samples.md automatically */
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const samplesMd = join(root, '.cursor/skills/ai-writing-system/writing-samples.md');
const text = readFileSync(samplesMd, 'utf8');
const paths = [...text.matchAll(/`(content\/english\/(?:blog|notes)\/[^`]+\.md)`/g)].map((m) =>
  join(root, m[1]),
);

const missing = paths.filter((p) => !existsSync(p));
if (missing.length) {
  console.error('Missing writing samples:');
  missing.forEach((p) => console.error(' ', p.replace(root + '/', '')));
  process.exit(1);
}

console.log(`OK: ${paths.length} writing sample paths resolve`);
process.exit(0);
