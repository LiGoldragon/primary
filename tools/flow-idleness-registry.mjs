import fs from 'node:fs';
import path from 'node:path';

const MARKER = /^\.([a-z0-9][a-z0-9-]*)\.flow-id$/;
const IDENTITY = /^[0-9a-f]{32}$/;
const harnesses = new Set(['claude', 'codex']);
const states = new Set(['idle', 'busy', 'approval-wait', 'unknown']);

const parseMarker = text => {
  const fields = new Map();
  for (const line of text.split('\n').filter(Boolean)) {
    const at = line.indexOf('=');
    if (at <= 0) throw new Error('invalid Flow marker line');
    const key = line.slice(0, at);
    if (fields.has(key)) throw new Error(`duplicate Flow marker field ${key}`);
    fields.set(key, line.slice(at + 1));
  }
  return Object.fromEntries(fields);
};

// The Flow directory and its flow-id claim marker are the only registry input.
// This reader never writes markers, lifecycle facts, or an auxiliary registry.
export const readFlowRegistry = ({ flowsRoot, readDirectory = fs.readdirSync, read = fs.readFileSync, stat = fs.statSync }) => {
  if (typeof flowsRoot !== 'string' || !flowsRoot) throw new Error('flowsRoot is required');
  const records = [];
  const identities = new Set();
  for (const entry of readDirectory(flowsRoot, { withFileTypes: true })) {
    if (!entry.isFile()) continue;
    const match = MARKER.exec(entry.name);
    if (!match) continue;
    const flowId = match[1];
    const marker = parseMarker(read(path.join(flowsRoot, entry.name), 'utf8'));
    if (marker.version !== '1' || marker.alias !== flowId || !harnesses.has(marker.harness) || !IDENTITY.test(marker.identity)) throw new Error(`invalid Flow marker for ${flowId}`);
    let directory;
    try { directory = stat(path.join(flowsRoot, flowId)); }
    catch { throw new Error(`missing Flow directory for ${flowId}`); }
    if (!directory.isDirectory()) throw new Error(`Flow path is not a directory for ${flowId}`);
    if (identities.has(marker.identity)) throw new Error(`duplicate Flow identity ${marker.identity}`);
    identities.add(marker.identity);
    records.push(Object.freeze({ flowId, harness: marker.harness, identity: marker.identity }));
  }
  return Object.freeze(records.sort((left, right) => left.flowId.localeCompare(right.flowId)));
};

const copyObservation = input => {
  if (!input || typeof input !== 'object' || !states.has(input.state)) throw new Error('invalid idleness state');
  if (input.state === 'idle' && (!Number.isSafeInteger(input.idleMinutes) || input.idleMinutes < 0)) throw new Error('idle observation requires idleMinutes');
  if (input.state !== 'idle' && input.idleMinutes !== null) throw new Error('non-idle observation cannot claim idleMinutes');
  const sourceEvent = input.sourceEvent;
  if (sourceEvent !== null && (!sourceEvent || typeof sourceEvent.kind !== 'string' || (sourceEvent.identifier !== null && typeof sourceEvent.identifier !== 'string'))) throw new Error('invalid idleness source event');
  if (input.unknownReason !== null && typeof input.unknownReason !== 'string') throw new Error('invalid idleness reason');
  return Object.freeze({ state: input.state, idleMinutes: input.idleMinutes, sourceEvent: sourceEvent === null ? null : Object.freeze({ kind: sourceEvent.kind, identifier: sourceEvent.identifier }), unknownReason: input.unknownReason });
};

export const createFlowIdlenessSubscription = registry => {
  if (!Array.isArray(registry)) throw new Error('Flow registry is required');
  const records = new Map(registry.map(record => [record.flowId, record]));
  if (records.size !== registry.length) throw new Error('duplicate Flow id');
  const observations = new Map();
  const subscribers = new Set();
  const snapshot = () => Object.freeze([...records.values()].map(record => Object.freeze({ ...record, observation: observations.get(record.flowId) ?? null })));
  return Object.freeze({
    query: flowId => records.has(flowId) ? Object.freeze({ ...records.get(flowId), observation: observations.get(flowId) ?? null }) : null,
    subscribe: listener => {
      if (typeof listener !== 'function') throw new Error('subscription listener is required');
      subscribers.add(listener);
      listener(Object.freeze({ kind: 'snapshot', flows: snapshot() }));
      return () => subscribers.delete(listener);
    },
    publish: ({ flowId, harness, identity, observation }) => {
      const record = records.get(flowId);
      if (!record) throw new Error('unknown Flow');
      if (record.harness !== harness) throw new Error('Flow harness mismatch');
      if (record.identity !== identity) throw new Error('Flow identity mismatch');
      const next = copyObservation(observation);
      const previous = observations.get(flowId);
      if (JSON.stringify(previous) === JSON.stringify(next)) return false;
      observations.set(flowId, next);
      const event = Object.freeze({ kind: 'idleness-changed', flow: record, observation: next });
      for (const subscriber of subscribers) subscriber(event);
      return true;
    },
  });
};
