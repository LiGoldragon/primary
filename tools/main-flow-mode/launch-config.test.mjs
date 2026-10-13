import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {loadLaunchConfig, validateLaunchConfig, voiceFromConfig} from './launch-config.mjs';
import {mainSystemModules} from './spirit-system-prompt.mjs';

const config = loadLaunchConfig(path.resolve(import.meta.dirname, '../..'));
assert.equal(config.aspects.length, 3);
const frozenModules = mainSystemModules('/tmp/does-not-matter', '.agents', {aspect: 'Psyche', layer: 'Secondary', launchConfig: config, metaflowConfig: {modules: ['spirit-core', 'intent-main-flow', 'vision-book', 'compensation-book-crystallization']}});
assert.match(frozenModules.find(module => module.name === 'vision-book').body, /book/i);
assert.deepEqual(voiceFromConfig(config, {aspect: 'Mind', layer: 'Primary'}), {status: 'configured', harness: 'codex', model: 'gpt-6-astra', effort: 'medium'});
assert.throws(() => voiceFromConfig(config, {aspect: 'Mind', layer: 'Primary', model: 'gpt-6-luna'}), /voice model differs/);
assert.throws(() => validateLaunchConfig({shared: config.shared, aspects: [{...config.aspects[0], voices: [...config.aspects[0].voices, config.aspects[0].voices[0]]}, ...config.aspects.slice(1)], metaflow: config.metaflow}), /duplicate voice/);
assert.throws(() => validateLaunchConfig({shared: {...config.shared, repositories: {...config.shared.repositories, psyche: {...config.shared.repositories.psyche, ref: 'latest'}}}, aspects: config.aspects, metaflow: config.metaflow}), /40-hex ref/);
const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'launch-config-'));
try {
  const dir = path.join(fixture, 'config/main-flow'); fs.mkdirSync(dir, {recursive: true});
  for (const name of ['shared', 'psyche', 'mind', 'field']) fs.copyFileSync(path.resolve(import.meta.dirname, `../../config/main-flow/${name}.edn`), path.join(dir, `${name}.edn`));
  fs.mkdirSync(path.join(dir, 'metaflow'));
  for (const name of ['Psyche-Core-Primary', 'Mind-Core-Primary', 'Field-Core-Primary']) fs.copyFileSync(path.resolve(import.meta.dirname, `../../config/main-flow/metaflow/${name}.edn`), path.join(dir, 'metaflow', `${name}.edn`));
  const text = fs.readFileSync(path.join(dir, 'mind.edn'), 'utf8').replace(':medium}', ':bogus}'); fs.writeFileSync(path.join(dir, 'mind.edn'), text);
  assert.throws(() => loadLaunchConfig(fixture), /unsupported: bogus/);
} finally { fs.rmSync(fixture, {recursive: true, force: true}); }
console.log('launch-config tests passed');
