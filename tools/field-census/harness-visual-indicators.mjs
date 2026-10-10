#!/usr/bin/env node
/* Bounded harness TUI indicator observation. Raw pane content is never emitted. */
import fs from 'node:fs';
import {execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const ANSI = /\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07]*(?:\x07|\x1b\\))/g;
const option = (args, name) => { const i = args.indexOf(name); return i < 0 ? null : args[i + 1]; };
const clean = value => String(value ?? '').replace(ANSI, '').replace(/\r/g, '');
const nullablePercent = value => Number.isFinite(value) && value >= 0 && value <= 100 ? value : null;

function footerLines(text, count = 10) {
  return clean(text).split('\n').map(line => line.trim()).filter(Boolean).slice(-count);
}

function remoteControlGlyph(lines) {
  return lines.find(line => !/^[❯>]/u.test(line) && /(?:^|\s)\/rc(?:\s|$)/i.test(line) &&
    /\b(?:ctx|wk|Fable|Opus|Sonnet|Haiku|Claude)\b/i.test(line)) ?? null;
}

function textModel(lines) {
  const joined = lines.join(' ');
  const claude = joined.match(/\b(Fable|Opus|Sonnet|Haiku)\s+([0-9]+(?:\.[0-9]+)?)(?:\s+\([^)]{1,40}\))?\s*[·•]\s*(low|medium|high)\b/i);
  if (claude) return {name: `${claude[1]} ${claude[2]}`, effort: claude[3].toLowerCase()};
  const codex = joined.match(/\b(gpt-[a-z0-9.-]+)\s+(low|medium|high|xhigh|max|ultra)\b/i);
  return codex ? {name: codex[1], effort: codex[2].toLowerCase()} : {name: null, effort: null};
}

function harnessKind(processInfo, lines) {
  const argv = JSON.stringify(processInfo ?? {}).toLowerCase();
  if (/claude/.test(argv)) return {kind: 'claude', grade: 'machine'};
  if (/codex/.test(argv)) return {kind: 'codex', grade: 'machine'};
  const text = lines.join(' ');
  if (/\b(Fable|Opus|Sonnet|Haiku)\b/i.test(text)) return {kind: 'claude', grade: 'text-pane'};
  if (/\bgpt-[a-z0-9.-]+\b/i.test(text)) return {kind: 'codex', grade: 'text-pane'};
  return {kind: 'unknown', grade: 'unknown'};
}

function visualRemoteControl(value) {
  if (!value || value.status !== 'observed' || value.fullScreen !== true ||
      value.fact !== 'remote-control-indicator' || typeof value.enabled !== 'boolean' ||
      !['high', 'medium'].includes(value.confidence) || typeof value.model !== 'string' || !value.model.trim()) return null;
  return {enabled: value.enabled, model: value.model, confidence: value.confidence};
}

export function analyzeHarnessVisualState({paneText = '', processInfo = null, pane = null,
  visualObservation = null, observedAt = new Date().toISOString()} = {}) {
  const lines = footerLines(paneText);
  const visual = visualRemoteControl(visualObservation);
  const harness = harnessKind(processInfo, lines);
  const glyph = harness.kind === 'claude' ? remoteControlGlyph(lines) : null;
  const model = textModel(lines);
  const text = lines.join(' ');
  const authFailed = /not logged in|login expired|oauth error|authentication (?:failed|required)/i.test(text);
  const context = text.match(/\bctx\s+(\d+(?:\.\d+)?)%/i);
  const featureEnabled = glyph ? true : visual?.enabled === true ? true : null;
  const featureEvidence = glyph ? {grade: 'text-pane', indicator: '/rc'} : visual?.enabled === true
    ? {grade: 'model-visual', indicator: '/rc', model: visual.model, confidence: visual.confidence} : null;
  return {
    version: 1,
    observedAt,
    harness,
    binding: {
      paneId: typeof pane?.pane_id === 'string' ? pane.pane_id : null,
      terminalId: typeof pane?.terminal_id === 'string' ? pane.terminal_id : null,
      agent: typeof pane?.agent === 'string' ? pane.agent : null,
    },
    indicators: {
      model: {value: model.name, evidenceGrade: model.name ? 'text-pane' : 'unknown'},
      effort: {value: model.effort, evidenceGrade: model.effort ? 'text-pane' : 'unknown'},
      contextPercent: {value: context ? nullablePercent(Number(context[1])) : null,
        evidenceGrade: context ? 'text-pane' : 'unknown'},
      accountAuthenticated: {value: authFailed ? false : null,
        evidenceGrade: authFailed ? 'text-pane' : 'unknown'},
      remoteControl: {
        featureEnabled,
        evidence: featureEvidence,
        accountAuthenticated: authFailed ? false : null,
        remoteUrlPresent: null,
        externalClientAttached: null,
      },
    },
    limitations: [
      'remote-control feature state does not establish account authentication',
      'remote-control feature state does not establish a reachable URL or external client attachment',
      ...(featureEnabled === null ? ['absence of an accepted indicator is preserved as unknown'] : []),
    ],
  };
}

function herdrJson(session, args) {
  const value = JSON.parse(execFileSync('herdr', ['--session', session, ...args], {encoding: 'utf8', timeout: 10000}));
  if (value.error) throw new Error(`${value.error.code}: ${value.error.message}`);
  return value.result;
}

export function collectHarnessVisualState({session, paneId, visualObservation = null} = {}) {
  if (!session || !paneId) throw new Error('session and paneId are required');
  const pane = herdrJson(session, ['pane', 'get', paneId])?.pane;
  const processInfo = herdrJson(session, ['pane', 'process-info', '--pane', paneId])?.process_info;
  const paneText = execFileSync('herdr', ['--session', session, 'pane', 'read', paneId,
    '--source', 'visible', '--lines', '200', '--format', 'text'], {encoding: 'utf8', timeout: 10000, maxBuffer: 1024 * 1024});
  return analyzeHarnessVisualState({paneText, processInfo, pane, visualObservation});
}

function readVisual(file) {
  if (!file) return null;
  const body = fs.readFileSync(file, 'utf8');
  if (body.length > 65536) throw new Error('visual observation exceeds byte limit');
  return JSON.parse(body);
}

const invokedDirectly = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];
if (invokedDirectly) {
  try {
    const args = process.argv.slice(2);
    const result = collectHarnessVisualState({session: option(args, '--session'), paneId: option(args, '--pane'),
      visualObservation: readVisual(option(args, '--visual-observation'))});
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  } catch (error) {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = 1;
  }
}
