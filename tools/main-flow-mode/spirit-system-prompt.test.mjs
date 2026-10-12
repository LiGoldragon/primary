import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spiritModules, mainSystemModules, composeSpiritSystemPrompt, codexModelSystemPrompt} from './spirit-system-prompt.mjs';
const root = fs.mkdtempSync(path.join(os.tmpdir(), 'spirit-system-'));
try {
  const skills = path.join(root, '.agents/skills');
  fs.mkdirSync(skills, {recursive: true});
  assert.throws(() => spiritModules(root), /spirit-core.*missing/);
  for (const [name, body] of [['spirit-core', 'The psyche is extended.'], ['spirit-future', 'Future module.'], ['knowledge-spirit', 'Not a spirit module.']]) {
    const dir = path.join(skills, name); fs.mkdirSync(dir);
    fs.writeFileSync(path.join(dir, 'SKILL.md'), `---\ndescription: fixture\n---\n\n${body}\n`);
  }
  const modules = spiritModules(root);
  assert.deepEqual(modules.map(module => module.name), ['spirit-core', 'spirit-future']);
  const prompt = composeSpiritSystemPrompt('Stock harness instructions.\n', modules);
  assert.equal(prompt, 'Stock harness instructions.\n\n# spirit-core\n\nThe psyche is extended.\n\n# spirit-future\n\nFuture module.\n');
  assert.throws(() => composeSpiritSystemPrompt('', modules), /missing or empty/);
  const home = path.join(root, 'client'); fs.mkdirSync(home);
  const client = {endpoint: path.join(home, 'app-server-control/control.sock')};
  const cache = {models: [{slug: 'fixture-model', model_messages: {instructions_template: 'Stock harness instructions.', instructions_variables: null}}]};
  fs.writeFileSync(path.join(home, 'models_cache.json'), JSON.stringify(cache));
  assert.equal(codexModelSystemPrompt(client, 'fixture-model', root, {aspect: 'Mind', layer: 'Tertiary'}), prompt);
  assert.throws(() => codexModelSystemPrompt(client, 'missing', root, {aspect: 'Mind', layer: 'Tertiary'}), /one installed model/);
  cache.models[0].model_messages.instructions_variables = {personality_default: 'unknown rendering'};
  fs.writeFileSync(path.join(home, 'models_cache.json'), JSON.stringify(cache));
  assert.throws(() => codexModelSystemPrompt(client, 'fixture-model', root, {aspect: 'Mind', layer: 'Tertiary'}), /literal installed model/);
  for (const name of ['vision-design', 'intent-psyche-interaction']) {
    fs.mkdirSync(path.join(skills, name));
    fs.writeFileSync(path.join(skills, name, 'SKILL.md'), `${name} body`);
  }
  assert.deepEqual(mainSystemModules(root, '.agents', {aspect: 'Psyche', layer: 'Tertiary'}).map(module => module.name), ['spirit-core', 'spirit-future', 'vision-design', 'intent-psyche-interaction']);
  assert.deepEqual(mainSystemModules(root, '.agents', {aspect: 'Field', layer: 'Primary'}).map(module => module.name), ['spirit-core', 'spirit-future', 'vision-design']);
  assert.deepEqual(mainSystemModules(root, '.agents', {aspect: 'Mind', layer: 'Tertiary'}).map(module => module.name), ['spirit-core', 'spirit-future']);
  assert.deepEqual(mainSystemModules(root, '.agents', {aspect: 'Mind', layer: 'Tertiary', metaflow: 'Owned continuation context'}).map(module => module.name), ['spirit-core', 'spirit-future', 'intent-psyche-interaction']);
  fs.mkdirSync(path.join(skills, 'spirit'));
  assert.throws(() => spiritModules(root), /legacy spirit/);
} finally { fs.rmSync(root, {recursive: true, force: true}); }
console.log('all spirit-* system composition fixtures passed');
