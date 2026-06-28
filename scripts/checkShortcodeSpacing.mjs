#!/usr/bin/env node
/** Fail if markdown shortcodes are indented or preceded by inline space (Hugo needs column-0 {{<). */
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const root = join(import.meta.dirname, '..', 'content');
const bad = [];

const walk = (dir) => {
  for (const name of readdirSync(dir)) {
    const path = join(dir, name);
    if (statSync(path).isDirectory()) walk(path);
    else if (name.endsWith('.md')) check(path);
  }
};

const check = (path) => {
  const rel = path.replace(/^.*\/content\//, 'content/');
  const lines = readFileSync(path, 'utf8').split('\n');
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.includes('{{</*') || line.includes('{{%/*')) continue;
    if (/^\s+\{\{[%<]/.test(line)) {
      bad.push(`${rel}:${i + 1} indented shortcode`);
      continue;
    }
    if (/(?<=\S) \{\{[%<]/.test(line)) {
      bad.push(`${rel}:${i + 1} inline space before shortcode`);
    }
  }
};

walk(root);

if (bad.length) {
  console.error('Shortcode spacing issues:\n' + bad.map((x) => `  ${x}`).join('\n'));
  process.exit(1);
}

console.log('OK: no leading/inline spaces before shortcodes in content/');
