// news-image-20261126 entry (Node 22, standard library only).
// The image is drawn at build time by render_news.py into entry.png
// beside this file; the program copies it to /output/entry.png.
// The gate takes a whole PNG or JPEG of at most 1 MiB and 1024x1024;
// the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const src = new URL('./entry.png', import.meta.url);
if (!existsSync(src)) {
  throw new Error('entry.png missing beside main.ts');
}
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(src, dest);
const bytes = statSync(dest).size;
if (bytes > 1048576) {
  throw new Error(`entry.png is ${bytes} bytes, over the 1 MiB gate`);
}
console.log(`wrote ${dest} (${bytes} bytes)`);
