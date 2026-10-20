import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {loadLaunchConfig, validateLaunchConfig, voiceFromConfig, firstPromptFromConfig, roleModulesFromConfig} from './launch-config.mjs';
import {mainSystemModules} from './spirit-system-prompt.mjs';

const config = loadLaunchConfig(path.resolve(import.meta.dirname, '../..'));
assert.equal(config.aspects.length, 3);
const installed = fs.mkdtempSync(path.join(os.tmpdir(), 'installed-skills-'));
try {
  const seat = {aspect: 'Psyche', layer: 'Secondary', launchConfig: config, metaflowConfig: {modules: ['spirit-core', 'intent-main-flow', 'vision-book', 'compensation-book-crystallization']}};
  assert.throws(() => mainSystemModules(installed, '.agents', seat), /not installed/);
  for (const name of roleModulesFromConfig(config, {...seat.metaflowConfig, aspect: 'Psyche'}, 'system')) {
    fs.mkdirSync(path.join(installed, '.agents/skills', name), {recursive: true});
    fs.writeFileSync(path.join(installed, '.agents/skills', name, 'SKILL.md'), `---\ndescription: fixture\n---\n\n${name} installed body\n`);
  }
  const installedModules = mainSystemModules(installed, '.agents', seat);
  assert.equal(installedModules.find(module => module.name === 'vision-book').body, 'vision-book installed body');
} finally { fs.rmSync(installed, {recursive: true, force: true}); }
assert.equal(config.shared.repositories, undefined, 'module revisions are pinned once, in the CriomOS-home cohort');
assert.deepEqual(voiceFromConfig(config, {aspect: 'Mind', layer: 'Primary'}), {status: 'configured', harness: 'codex', model: 'gpt-6-astra', effort: 'medium'});
assert.throws(() => voiceFromConfig(config, {aspect: 'Mind', layer: 'Primary', model: 'gpt-6-luna'}), /voice model differs/);
assert.throws(() => validateLaunchConfig({shared: config.shared, aspects: [{...config.aspects[0], voices: [...config.aspects[0].voices, config.aspects[0].voices[0]]}, ...config.aspects.slice(1)], metaflow: config.metaflow}), /duplicate voice/);
const fixture = fs.mkdtempSync(path.join(os.tmpdir(), 'launch-config-'));
try {
  const dir = path.join(fixture, 'config/main-flow'); fs.mkdirSync(dir, {recursive: true});
  for (const name of ['shared', 'psyche', 'mind', 'field']) fs.writeFileSync(path.join(dir, `${name}.edn`), fs.readFileSync(path.resolve(import.meta.dirname, `../../config/main-flow/${name}.edn`)));
  fs.mkdirSync(path.join(dir, 'metaflow'));
  for (const name of ['Psyche-Core-Primary', 'Mind-Core-Primary', 'Field-Core-Primary']) fs.writeFileSync(path.join(dir, 'metaflow', `${name}.edn`), fs.readFileSync(path.resolve(import.meta.dirname, `../../config/main-flow/metaflow/${name}.edn`)));
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

for (const metaflow of config.metaflow.metaflows.filter(row => row.aspect === 'Psyche')) {
  const inherited = config.aspects.find(row => row.aspect === 'Psyche').modules.user.map(row => row.name);
  assert.ok(inherited.every(name => roleModulesFromConfig(config, metaflow, 'user').includes(name)));
  assert.equal(metaflow['user-modules'], undefined, `${metaflow.topic}.${metaflow.layer} must inherit its aspect roots`);
}
const extraRole = {aspect: 'Field', 'user-modules': ['compensation-main-flow', 'compensation-book']};
const completeRoots = roleModulesFromConfig(config, extraRole, 'user');
assert.equal(completeRoots.filter(name => name === 'compensation-main-flow').length, 1);
assert.ok(completeRoots.includes('compensation-truth'));
assert.ok(completeRoots.includes('compensation-book'));
assert.ok(roleModulesFromConfig(config, {aspect: 'Psyche', modules: ['vision-nexus']}, 'system').includes('intent-psyche'));
