import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {loadLaunchConfig, validateLaunchConfig, voiceFromConfig, firstPromptFromConfig} from './launch-config.mjs';
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

const topic = {aspect: 'Psyche', topic: 'Flow', layer: 'Primary', 'raw-psyche-paths': ['raw/flow.md']};
const templateConfig = {shared: {'first-prompt-template': '{{modules}}\n{{handover}}\n{{raw-psyche}}\n{{metaflow}}'}};
assert.equal(firstPromptFromConfig(templateConfig, topic, {modules: '/context', handover: 'judgment'}), '/context\njudgment\nraw/flow.md\nPsyche Flow Primary\n');
assert.throws(() => firstPromptFromConfig(templateConfig, {...topic, 'raw-psyche-paths': []}, {modules: '', handover: 'judgment'}), /raw-psyche-paths/);
assert.throws(() => firstPromptFromConfig({shared: {}}, topic, {modules: '', handover: 'judgment'}), /first-prompt-template/);
assert.throws(() => firstPromptFromConfig({shared: {'first-prompt-template': '{{modules}}{{handover}}{{raw-psyche}}{{invented}}'}}, topic, {modules: '', handover: 'judgment'}), /unknown first-prompt field/);

for (const [topic, layer, model] of [['Publisher', 'Quaternary', 'claude-haiku-5-5'], ['Illustrator', 'Tertiary', 'claude-sonnet-5-5']]) {
  assert.deepEqual(voiceFromConfig(config, {aspect: 'Field', topic, layer}), {status: 'configured', harness: 'claude', model, effort: 'medium'});
  assert.throws(() => voiceFromConfig(config, {aspect: 'Field', topic, layer, harness: 'codex'}), /harness differs/);
}
assert.equal(voiceFromConfig(config, {aspect: 'Field', layer: 'Quaternary'}).harness, 'codex');
assert.equal(voiceFromConfig(config, {aspect: 'Field', topic: 'Publisher', layer: 'Tertiary'}).harness, 'codex');
const badVoice = voice => ({...config, metaflow: {metaflows: [{aspect: 'Field', topic: 'Example', layer: 'Quaternary', voice}]}});
assert.throws(() => validateLaunchConfig(badVoice({harness: 'claude', model: 'gpt-6-luna', effort: 'medium'})), /must match its harness/);
assert.throws(() => validateLaunchConfig(badVoice({harness: 'claude', model: 'claude-haiku-5-5'})), /effort is unsupported/);
assert.throws(() => validateLaunchConfig({...config, metaflow: {metaflows: [...config.metaflow.metaflows, config.metaflow.metaflows[0]]}}), /duplicate/);
