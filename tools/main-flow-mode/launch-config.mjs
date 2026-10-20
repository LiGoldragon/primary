import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {execFileSync} from 'node:child_process';

const ASPECTS = ['Psyche', 'Mind', 'Field'];
const LAYERS = ['Primary', 'Secondary', 'Tertiary', 'Quaternary'];
const EFFORTS = ['low', 'medium', 'high', 'xhigh', 'max'];
const PLACEMENTS = ['system', 'user'];
const MODELS = new Set(['claude-fable-5-1', 'claude-opus-5-5', 'claude-sonnet-5-5', 'claude-haiku-5-5', 'gpt-6-astra', 'gpt-6.1-sol', 'gpt-6-luna']);
const HARNESS = new Set(['claude', 'codex']);
const BB = `(require '[clojure.edn :as edn] '[cheshire.core :as json])
(defn plain [x] (cond (keyword? x) (name x) (map? x) (into {} (map (fn [[k v]] [(plain k) (plain v)]) x)) (coll? x) (mapv plain x) :else x))
(print (json/generate-string (plain (edn/read-string (slurp (first *command-line-args*))))))`;

function readEdn(file) {
  if (!path.isAbsolute(file)) throw new Error(`EDN source must be absolute: ${file}`);
  if (!fs.statSync(file).isFile()) throw new Error(`EDN source is missing: ${file}`);
  try { return JSON.parse(execFileSync('bb', ['-e', BB, file], {encoding: 'utf8'})); }
  catch (error) { throw new Error(`invalid EDN source ${file}: ${error.message}`); }
}

function list(value, name) { if (!Array.isArray(value)) throw new Error(`${name} must be a vector`); return value; }
function exact(value, allowed, name) { if (!allowed.has(value)) throw new Error(`${name} is unsupported: ${value}`); }
function unique(values, name) { const seen = new Set(); for (const value of values) { if (seen.has(value)) throw new Error(`${name} contains duplicate: ${value}`); seen.add(value); } }

export function validateLaunchConfig({shared, aspects, metaflow}) {
  if (shared?.schema !== 'main-flow-launch/1') throw new Error('unsupported or missing launch config schema');
  for (const [name, tools] of Object.entries(shared.tools ?? {})) { list(tools, `tools.${name}`); unique(tools, `tools.${name}`); }
  const found = new Set();
  for (const config of aspects) {
    exact(config.aspect, new Set(ASPECTS), 'aspect'); exact(config.harness, HARNESS, `harness for ${config.aspect}`);
    for (const voice of list(config.voices, `${config.aspect}.voices`)) {
      exact(voice.layer, new Set(LAYERS), 'layer'); exact(voice.effort, new Set(EFFORTS), 'effort');
      if (!MODELS.has(voice.model)) throw new Error(`unsupported model: ${voice.model}`);
      const key = `${config.aspect}.${voice.layer}`; if (found.has(key)) throw new Error(`duplicate voice: ${key}`); found.add(key);
    }
    for (const placement of PLACEMENTS) { list(config.modules?.[placement], `${config.aspect}.modules.${placement}`); unique(config.modules[placement].map(module => module.name ?? module), `${config.aspect}.modules.${placement}`); }
  }
  if (found.size !== ASPECTS.length * LAYERS.length) throw new Error('every aspect and layer needs exactly one voice');
  for (const row of list(metaflow?.metaflows, 'metaflows')) {
    exact(row.aspect, new Set(ASPECTS), 'metaflow aspect');
    exact(row.layer, new Set(LAYERS), 'metaflow layer');
    if (!row.topic) throw new Error('metaflow topic is required');
    unique(row.modules ?? [], `metaflow ${row.aspect}.${row.layer}.modules`);
    const userModules = list(row['user-modules'], `metaflow ${row.aspect}.${row.topic}.${row.layer}.user-modules`);
    const userModuleNames = userModules.map(module => module.name ?? module);
    unique(userModuleNames, `metaflow ${row.aspect}.${row.topic}.${row.layer}.user-modules`);
    if (userModuleNames.filter(name => name === 'compensation-correction').length !== 1)
      throw new Error(`metaflow ${row.aspect}.${row.topic}.${row.layer}.user-modules must include compensation-correction exactly once`);
    if (row.voice !== undefined) {
      exact(row.voice.harness, HARNESS, 'metaflow voice harness');
      exact(row.voice.effort, new Set(EFFORTS), 'metaflow voice effort');
      if (!MODELS.has(row.voice.model) || (row.voice.harness === 'claude') !== row.voice.model.startsWith('claude-')) throw new Error('metaflow voice model must match its harness');
    }
  }
  unique(metaflow.metaflows.map(row => `${row.aspect}.${row.topic}.${row.layer}`), 'metaflow identities');
  return true;
}

export function loadLaunchConfig(root = process.cwd()) {
  const dir = path.join(root, 'config', 'main-flow');
  const shared = readEdn(path.join(dir, 'shared.edn'));
  const aspects = ASPECTS.map(aspect => readEdn(path.join(dir, `${aspect.toLowerCase()}.edn`)));
  // Module text comes from the installed skills of the one pinned context
  // cohort; the configuration names modules only.
  for (const config of aspects)
    for (const placement of ['system', 'user']) config.modules[placement] = config.modules[placement].map(name => ({name, placement}));
  const metaflow = {metaflows: fs.readdirSync(path.join(dir, 'metaflow'), {withFileTypes: true}).filter(entry => entry.isFile() && entry.name.endsWith('.edn')).map(entry => readEdn(path.join(dir, 'metaflow', entry.name)))};
  validateLaunchConfig({shared, aspects, metaflow});
  return Object.freeze({shared, aspects, metaflow});
}

export function voiceFromConfig(config, {aspect, layer, topic, harness, model, effort}) {
  const override = config.metaflow.metaflows.find(item => item.aspect === aspect && item.layer === layer && item.topic === topic)?.voice;
  const row = override ?? config.aspects.find(item => item.aspect === aspect)?.voices.find(item => item.layer === layer);
  if (!row) throw new Error(`no configured voice: ${aspect}.${layer}`);
  const expectedHarness = override?.harness ?? config.aspects.find(item => item.aspect === aspect).harness;
  if (harness !== undefined && harness !== expectedHarness) throw new Error(`voice harness differs for ${aspect}.${layer}: required ${expectedHarness}, received ${harness}`);
  if (model !== undefined && model !== row.model) throw new Error(`voice model differs for ${aspect}.${layer}: required ${row.model}, received ${model}`);
  if (effort !== undefined && effort !== row.effort) throw new Error(`voice effort differs for ${aspect}.${layer}: required ${row.effort}, received ${effort}`);
  return Object.freeze({status: 'configured', harness: expectedHarness, model: row.model, effort: row.effort, ...(row.source ? {source: row.source} : {})});
}

export function modulesFromConfig(config, aspect, placement) {
  const names = config.aspects.find(item => item.aspect === aspect)?.modules?.[placement];
  if (!names) throw new Error(`no configured ${placement} modules for ${aspect}`);
  return names.map(module => module.name ?? module);
}

// A role extends its aspect context; it cannot remove the standing defaults.
export function roleModulesFromConfig(config, metaflow, placement) {
  if (!['system', 'user'].includes(placement)) throw new Error('unsupported role module placement');
  const defaults = modulesFromConfig(config, metaflow.aspect, placement);
  const additions = placement === 'system' ? metaflow.modules ?? [] : metaflow['user-modules'] ?? [];
  return [...new Set([...defaults, ...additions.map(module => module.name ?? module)])];
}

export function metaflowFor(config, {aspect, topic = 'Core', layer}) {
  const row = config.metaflow.metaflows.find(item => item.aspect === aspect && item.topic === topic && item.layer === layer);
  if (!row) throw new Error(`no configured metaflow: ${aspect}.${topic}.${layer}`);
  return row;
}

export function birthSkillsFromConfig(config, aspect = 'Psyche') {
  const names = modulesFromConfig(config, aspect, 'user');
  if (!names.includes('compensation-main-flow')) throw new Error(`configured ${aspect} user modules omit compensation-main-flow`);
  return [...names];
}

export function firstPromptFromConfig(config, metaflow, {modules, handover, rawPsychePaths}) {
  const template = metaflow?.['first-prompt-template'] ?? config.shared['first-prompt-template'];
  if (typeof template !== 'string' || !template.trim()) throw new Error('EDN first-prompt-template is required');
  const sources = rawPsychePaths ?? metaflow?.['raw-psyche-paths'];
  if (!Array.isArray(sources) || !sources.length || sources.some(source => typeof source !== 'string' || !source.trim())) throw new Error('EDN raw-psyche-paths are required');
  if (!handover?.trim()) throw new Error('first prompt handover or topic context is required');
  const values = {modules, handover, 'raw-psyche': sources.join('\n'), 'topic-context': metaflow['topic-context'] ?? '', metaflow: `${metaflow.aspect} ${metaflow.topic} ${metaflow.layer}`};
  const prompt = template.replace(/\{\{([^}]+)\}\}/g, (_, key) => {
    if (!(key in values)) throw new Error(`unknown first-prompt field: ${key}`);
    return values[key];
  });
  if (!template.includes('{{handover}}') || !template.includes('{{raw-psyche}}') || !template.includes('{{modules}}')) throw new Error('EDN first prompt must carry modules, handover and raw psyche');
  return `${prompt.trim()}\n`;
}

export const defaultLaunchConfig = () => loadLaunchConfig(path.resolve(new URL('../..', import.meta.url).pathname));
