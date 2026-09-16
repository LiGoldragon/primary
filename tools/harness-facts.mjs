import fs from 'node:fs';
import { spawnSync } from 'node:child_process';
import { createUnixWebSocketTransport } from './codex-app-server-client.mjs';
import { readFlowIdleness } from './flow-idleness.mjs';
import { deriveClaudeFlowIdleness } from './claude-flow-idleness.mjs';

const bounded = observation => ({
  state: observation.state,
  idleMinutes: observation.idleMinutes,
  sourceEvent: observation.eligible ? { kind: observation.source, identifier: observation.turnId ?? observation.completionEventId ?? null } : null,
  unknownReason: observation.eligible ? null : observation.reason,
});
const unknown = reason => ({ state: 'unknown', idleMinutes: null, sourceEvent: null, unknownReason: reason });
const within = async (promise, timeoutMs) => {
  let timer;
  try {
    return await Promise.race([Promise.resolve(promise), new Promise(resolve => { timer = setTimeout(() => resolve({ __timeout: true }), timeoutMs); })]);
  } finally { clearTimeout(timer); }
};
const decodeRecords = text => text.split('\n').filter(Boolean).map(line => JSON.parse(line));

export const collectHarnessFacts = async ({
  codexTargets = [], claudeTargets = [],
  createTransport = socketPath => createUnixWebSocketTransport(socketPath),
  claudeAgents = () => {
    const result = spawnSync('claude', ['agents', '--json'], { encoding: 'utf8', timeout: 15_000, maxBuffer: 1_048_576, stdio: ['ignore', 'pipe', 'ignore'] });
    if (result.status !== 0) throw new Error('agents-unavailable');
    return JSON.parse(result.stdout);
  },
  readText = sourcePath => fs.readFileSync(sourcePath, 'utf8'),
  adapters = { readFlowIdleness, deriveClaudeFlowIdleness },
  now = () => Date.now(), timeoutMs = 15_000,
}) => {
  const facts = [];
  for (const target of codexTargets) {
    const base = { targetIdentifier: target.identifier, harness: 'codex', openWork: target.openWork === true };
    let transport;
    try {
      transport = createTransport(target.socketPath);
      const initialized = await within(transport.request('initialize', { clientInfo: { name: 'core-harness-facts', version: '1' } }), timeoutMs);
      if (initialized?.__timeout) { facts.push({ ...base, ...unknown('timeout') }); continue; }
      await within(transport.notify('initialized', {}), timeoutMs);
      const metadata = await within(transport.request('thread/read', { threadId: target.threadId, includeTurns: false }), timeoutMs);
      if (metadata?.__timeout) { facts.push({ ...base, ...unknown('timeout') }); continue; }
      const thread = metadata?.thread;
      if (thread?.id !== target.threadId) { facts.push({ ...base, ...unknown('thread-identity-mismatch') }); continue; }
      const operationalState = thread.status?.type === 'idle' ? 'idle' : thread.status?.type === 'active' ? 'busy' : 'unknown';
      const observation = await within(adapters.readFlowIdleness({ transport, threadId: target.threadId, operationalState, now }), timeoutMs);
      facts.push({ ...base, ...(observation?.__timeout ? unknown('timeout') : bounded(observation)) });
    } catch { facts.push({ ...base, ...unknown('collector-unavailable') }); }
    finally { transport?.close?.(); }
  }

  let agents;
  try { agents = await within(claudeAgents(), timeoutMs); } catch { agents = null; }
  for (const target of claudeTargets) {
    const base = { targetIdentifier: target.identifier, harness: 'claude', openWork: target.openWork === true };
    try {
      if (agents?.__timeout) { facts.push({ ...base, ...unknown('timeout') }); continue; }
      if (!Array.isArray(agents)) { facts.push({ ...base, ...unknown('collector-unavailable') }); continue; }
      const matches = agents.filter(agent => agent?.sessionId === target.sessionId);
      if (matches.length !== 1) { facts.push({ ...base, ...unknown('roster-session-ambiguous') }); continue; }
      if (typeof target.transcriptPath !== 'string' || target.transcriptPath.length === 0) { facts.push({ ...base, ...unknown('transcript-path-unavailable') }); continue; }
      const records = decodeRecords(readText(target.transcriptPath));
      const observation = adapters.deriveClaudeFlowIdleness({ sessionId: target.sessionId, records, rosterEntry: matches[0], observedAtMs: now() });
      facts.push({ ...base, ...bounded(observation) });
    } catch { facts.push({ ...base, ...unknown('collector-unavailable') }); }
  }
  return facts;
};
