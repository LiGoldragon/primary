import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { deriveIdleObservation } from './flow-idleness.mjs';
import { createFlowIdlenessSubscription, readFlowRegistry } from './flow-idleness-registry.mjs';

const root = fs.mkdtempSync(path.join(os.tmpdir(), 'flow-idleness-registry-'));
const marker = (alias, harness, identity) => fs.writeFileSync(path.join(root, `.${alias}.flow-id`), `version=1\nharness=${harness}\nidentity=${identity}\nalias=${alias}\n`);
for (const alias of ['core', 'primary']) fs.mkdirSync(path.join(root, alias));
marker('core', 'codex', '01a0a7922d0e7a53ac0b9b3e43002941');
marker('primary', 'claude', '840e42bbb2cd42eba9ec7659a5b13ded');

const registry = readFlowRegistry({ flowsRoot: root });
assert.deepEqual(registry, [
  { flowId: 'core', harness: 'codex', identity: '01a0a7922d0e7a53ac0b9b3e43002941' },
  { flowId: 'primary', harness: 'claude', identity: '840e42bbb2cd42eba9ec7659a5b13ded' },
]);

const service = createFlowIdlenessSubscription(registry);
const events = [];
const unsubscribe = service.subscribe(event => events.push(event));
assert.equal(events[0].kind, 'snapshot');
assert.equal(events[0].flows[0].observation, null);
const idle = deriveIdleObservation({ threadId: '01a0a792-2d0e-7a53-ac0b-9b3e43002941', operationalState: 'idle', observedAtMs: 900_000, turn: { id: 'turn-7', status: 'completed', completedAt: 600 } });
assert.equal(service.publish({ flowId: 'core', harness: 'codex', identity: registry[0].identity, observation: { state: idle.state, idleMinutes: idle.idleMinutes, sourceEvent: { kind: idle.source, identifier: idle.turnId }, unknownReason: null } }), true);
assert.equal(events.at(-1).kind, 'idleness-changed');
assert.equal(events.at(-1).observation.idleMinutes, 5);
assert.equal(service.publish({ flowId: 'core', harness: 'codex', identity: registry[0].identity, observation: { state: idle.state, idleMinutes: idle.idleMinutes, sourceEvent: { kind: idle.source, identifier: idle.turnId }, unknownReason: null } }), false);
assert.throws(() => service.publish({ flowId: 'core', harness: 'claude', identity: registry[0].identity, observation: { state: 'unknown', idleMinutes: null, sourceEvent: null, unknownReason: 'wrong-harness' } }), /harness mismatch/);
assert.throws(() => service.publish({ flowId: 'core', harness: 'codex', identity: '01a0a7922d0e7a53ac0b9b3e43002942', observation: { state: 'unknown', idleMinutes: null, sourceEvent: null, unknownReason: 'stale-session' } }), /identity mismatch/);
assert.throws(() => service.publish({ flowId: 'absent', harness: 'codex', identity: registry[0].identity, observation: { state: 'unknown', idleMinutes: null, sourceEvent: null, unknownReason: 'unknown' } }), /unknown Flow/);
unsubscribe();
assert.equal(service.publish({ flowId: 'primary', harness: 'claude', identity: registry[1].identity, observation: { state: 'approval-wait', idleMinutes: null, sourceEvent: null, unknownReason: 'approval-pending' } }), true);
assert.equal(events.length, 2);

fs.mkdirSync(path.join(root, 'duplicate'));
marker('duplicate', 'codex', '01a0a7922d0e7a53ac0b9b3e43002941');
assert.throws(() => readFlowRegistry({ flowsRoot: root }), /duplicate Flow identity/);
fs.unlinkSync(path.join(root, '.duplicate.flow-id'));
marker('duplicate', 'codex', '01A0A7922D0E7A53AC0B9B3E43002941');
assert.throws(() => readFlowRegistry({ flowsRoot: root }), /invalid Flow marker/);
fs.rmSync(root, { recursive: true, force: true });
console.log('Flow registry/idleness subscription fixtures passed');
