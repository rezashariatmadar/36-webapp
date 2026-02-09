import { readdirSync, statSync } from 'node:fs';
import { dirname, extname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const LIMITS = {
  entryJs: 150000,
  entryCss: 2000,
  maxChunkJs: 10000,
  totalChunkJs: 40000,
};

function formatBytes(value) {
  return `${value.toLocaleString()} B`;
}

function statSize(path) {
  return statSync(path).size;
}

const scriptDir = dirname(fileURLToPath(import.meta.url));
const staticJsDir = resolve(scriptDir, '..', '..', 'static', 'js');
const chunksDir = join(staticJsDir, 'chunks');

const entryJsPath = join(staticJsDir, 'spa-app.js');
const entryCssPath = join(staticJsDir, 'spa-app.css');

const chunkFiles = readdirSync(chunksDir)
  .filter((name) => extname(name) === '.js')
  .map((name) => ({
    name,
    size: statSize(join(chunksDir, name)),
  }));

const maxChunk = chunkFiles.reduce(
  (largest, current) => (current.size > largest.size ? current : largest),
  { name: '(none)', size: 0 },
);
const totalChunkJs = chunkFiles.reduce((sum, file) => sum + file.size, 0);

const metrics = {
  entryJs: statSize(entryJsPath),
  entryCss: statSize(entryCssPath),
  maxChunkJs: maxChunk.size,
  totalChunkJs,
};

const failures = [];

if (chunkFiles.length === 0) {
  failures.push('No JS chunks found in theme/static/js/chunks.');
}

for (const [key, limit] of Object.entries(LIMITS)) {
  if (metrics[key] > limit) {
    failures.push(
      `${key} exceeded: ${formatBytes(metrics[key])} > ${formatBytes(limit)}`,
    );
  }
}

console.log(`SPA Budget Report
- entryJs: ${formatBytes(metrics.entryJs)} (limit ${formatBytes(LIMITS.entryJs)})
- entryCss: ${formatBytes(metrics.entryCss)} (limit ${formatBytes(LIMITS.entryCss)})
- maxChunkJs: ${formatBytes(metrics.maxChunkJs)} (${maxChunk.name}) (limit ${formatBytes(LIMITS.maxChunkJs)})
- totalChunkJs: ${formatBytes(metrics.totalChunkJs)} (limit ${formatBytes(LIMITS.totalChunkJs)})`);

if (failures.length > 0) {
  console.error('\nBudget check failed:');
  failures.forEach((failure) => console.error(`- ${failure}`));
  process.exit(1);
}

console.log('\nBudget check passed.');
