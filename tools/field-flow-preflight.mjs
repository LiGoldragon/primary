#!/usr/bin/env node
// Passive gate for a managed native seat before using the installed Flow CLI.
// This never registers a Flow, sends a message, or changes a route.
import fs from 'node:fs';
import crypto from 'node:crypto';
import { spawnSync } from 'node:child_process';

const args = process.argv.slice(2);
const value = flag => { const i = args.indexOf(flag); return i < 0 ? undefined : args[i + 1]; };
const flowId = value('--flow');
const receiptPath = value('--receipt');
const registryPath = value('--registry');
const flowBin = value('--flow-bin') ?? '/home/li/.local/bin/flow';
const nexusBin = value('--nexus-bin') ?? '/home/li/.local/bin/flow-nexus';
const nexusPid = value('--nexus-pid');
const bindingPath = value('--binding-evidence');
const attestationPath = value('--source-attestation');
if (!flowId || !/^[a-f0-9]{6}$/.test(flowId) || !receiptPath || !registryPath) {
  console.error('usage: field-flow-preflight.mjs --flow SIX_HEX --receipt FILE --registry FILE [--flow-bin FILE] [--nexus-bin FILE] [--nexus-pid PID] [--binding-evidence FILE] [--source-attestation FILE]');
  process.exit(2);
}

const readJson = file => {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch (error) { return { error: `${error.code ?? error.name}: ${error.message}` }; }
};
const digest = file => {
  try { return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'); }
  catch { return null; }
};
const receipt = readJson(receiptPath);
const registry = readJson(registryPath);
const binding = bindingPath ? readJson(bindingPath) : {};
const attestation = attestationPath ? readJson(attestationPath) : {};
const fresh = value => typeof value === 'string' && Number.isFinite(Date.parse(value)) &&
  Date.now() - Date.parse(value) >= 0 && Date.now() - Date.parse(value) <= 5 * 60 * 1000;
const installedNexusSha = digest(nexusBin);
const installedFlowSha = digest(flowBin);
const processNexusSha = nexusPid && /^[1-9][0-9]*$/.test(nexusPid)
  ? digest(`/proc/${nexusPid}/exe`) : null;
const nativeThread = typeof receipt.threadId === 'string' ? receipt.threadId : null;
const nativeMatch = receipt.status === 'verified' && nativeThread !== null &&
  registry.native_thread === nativeThread && registry.name === `flow-${flowId}`;

// The installed CLI is positional; the candidate CLI takes one typed Datom.
// Both forms here are read-only recipient queries. A failed legacy parse may
// be retried as a typed query; a successful answer is never silently retried.
let dialect = 'legacy';
let result = spawnSync(flowBin, ['resolve', flowId], { encoding: 'utf8', timeout: 5000 });
if (!result.error && result.status !== 0) {
  dialect = 'datom';
  result = spawnSync(flowBin, [`ResolveRecipient.${flowId}`], { encoding: 'utf8', timeout: 5000 });
}
const reply = (result.stdout ?? '').trim();
const escape = value => String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
const exactResolution = nativeThread && ['session', 'name', 'pane_id', 'terminal_id'].every(key => typeof registry[key] === 'string')
  ? new RegExp(`^RecipientResolved\\.\\{ ${escape(flowId)} ${escape(nativeThread)} (Codex|Claude) Available\\.\\{ [^{}]* Ready \\} Available\\.\\{ ${escape(registry.session)} ${escape(registry.name)} ${escape(registry.pane_id)} ${escape(registry.terminal_id)} \\} \\{ [^{}]* \\} Active \\}$`)
  : null;
const flowResolution = result.error ? 'error' : result.status !== 0 ? 'error' :
  reply === 'RecipientResolutionRejected.UnknownFlow' ? 'unknown-flow' :
  exactResolution?.test(reply)
    ? 'resolved' : reply.startsWith('RecipientResolved.') ? 'resolved-mismatch-or-unavailable' : 'unrecognized-reply';
const bindingMatches = binding.source === 'herdr-direct-read' && binding.flowId === flowId &&
  binding.nativeThreadId === nativeThread && binding.paneId === registry.pane_id &&
  binding.terminalId === registry.terminal_id && binding.session === registry.session &&
  binding.agent === registry.agent && binding.readiness === 'ready' && fresh(binding.observedAt);
const sourceMatches = /^[0-9a-f]{40}$/.test(attestation.sourceRevision ?? '') &&
  attestation.remoteCheck === 'passed' && fresh(attestation.observedAt) &&
  attestation.flowSha256 === installedFlowSha &&
  attestation.nexusSha256 === installedNexusSha &&
  attestation.runningNexusSha256 === processNexusSha;
const blockers = [];
if (!nativeMatch) blockers.push('native-hm-binding-mismatch-or-unverified-receipt');
if (flowResolution !== 'resolved') blockers.push(`flow-${flowResolution}`);
if (processNexusSha === null || processNexusSha !== installedNexusSha) blockers.push('running-nexus-unverified-or-different');
// External receipts remain operator evidence, not an identity authority. The
// controller must own their creation and review before invoking this gate.
if (!bindingMatches) blockers.push('current-herdr-binding-not-witnessed');
if (!sourceMatches) blockers.push('source-installed-parity-unproven');

console.log(JSON.stringify({
  flowId,
  native: {
    receiptStatus: receipt.status ?? null,
    receiptThread: nativeThread,
    registryThread: registry.native_thread ?? null,
    registryPane: registry.pane_id ?? null,
    registryTerminal: registry.terminal_id ?? null,
    receiptAndRegistryMatch: nativeMatch,
    currentHerdrBinding: bindingMatches ? 'evidence-matched' : 'unverified',
  },
  installed: {
    flowBin,
    flowSha256: installedFlowSha,
    nexusBin,
    nexusSha256: installedNexusSha,
    processNexusSha256: processNexusSha,
    processMatchesInstalled: processNexusSha === null ? null : processNexusSha === installedNexusSha,
    sourceRevisionParity: sourceMatches ? 'attested' : 'unproven',
    dialect,
    resolution: flowResolution,
    reply: reply.slice(0, 512),
    error: result.error?.message ?? (result.status === 0 ? null : (result.stderr ?? '').trim().slice(0, 512)),
  },
  readyForFlowLifecycle: blockers.length === 0,
  blockers,
}, null, 2));
