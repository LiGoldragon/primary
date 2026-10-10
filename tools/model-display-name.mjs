import fs from 'node:fs';
import path from 'node:path';

const file = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..', 'config', 'model-display-names.json');
const document = JSON.parse(fs.readFileSync(file, 'utf8'));
if (document.version !== 1 || !document.models || Array.isArray(document.models)) {
  throw new Error('model display map has unsupported shape');
}

export function modelTitle(modelId) {
  const title = document.models[modelId];
  return typeof title === 'string' && title.length > 0 ? title : null;
}

export function requireModelTitle(modelId) {
  const title = modelTitle(modelId);
  if (!title) throw new Error(`unmapped exact native model identifier: ${modelId}`);
  return title;
}
