import assert from 'node:assert/strict';
import { renderLauncherPlan, validatePostflight } from './flow-launcher-dry-run.mjs';

const sessionId = 'fd0f9762-d293-432b-a425-4f590fe9c8d5';
const name = 'primary-claude-fd0f97';
const plan = renderLauncherPlan({
  cwd: '/home/li/primary', flowId: 'fd0f97', sessionId, name,
  systemPromptFile: '/review/system-prompt.md', userPromptFile: '/review/user-prompt.md',
  userEnvironment: { HOME: '/home/li', PATH: '/run/current-system/sw/bin', DISPLAY: ':0', WAYLAND_DISPLAY: 'wayland-1', NO_COLOR: '1', CODEX_CI: '1', CODEX_THREAD_ID: 'wrong', SECRET: 'unread' },
});
assert.equal(plan.launches, false);
assert.deepEqual(plan.scope, { manager: 'user', unit: 'flow-fd0f97.scope', kind: 'scope', owns: ['ghostty', 'claude'] });
assert.deepEqual(plan.preservedEnvironment, { HOME: '/home/li', PATH: '/run/current-system/sw/bin', DISPLAY: ':0', WAYLAND_DISPLAY: 'wayland-1' });
assert.deepEqual(plan.cleanEnvironment.removed, ['NO_COLOR', 'CODEX_CI', 'CODEX_*']);
assert.deepEqual(plan.argv.slice(0, 6), ['systemd-run', '--user', '--scope', '--unit=flow-fd0f97.scope', '--collect', 'env']);
assert.ok(plan.argv.includes('ghostty'));
assert.equal(plan.promptDelivery.userPromptArguments, 1);
assert.match(plan.argv[plan.argv.indexOf('bash') + 2], /--dangerously-skip-permissions/);
assert.match(plan.argv[plan.argv.indexOf('bash') + 2], /--remote-control/);
const sessionRecord = { sessionId, bridgeSessionId: 'bridge-91' };
const remoteRecord = { entries: [{ bridgeSessionId: 'bridge-91', name }] };
assert.deepEqual(validatePostflight({ sessionRecord, remoteRecord, expectedSessionId: sessionId, expectedName: name }), { sessionId, bridgeSessionId: 'bridge-91', name });
// Prior-bug witness: a visible window cannot substitute for a bridge record.
assert.throws(() => validatePostflight({ sessionRecord: { sessionId, windowExists: true }, remoteRecord, expectedSessionId: sessionId, expectedName: name }), /bridgeSessionId/);
assert.throws(() => validatePostflight({ sessionRecord, remoteRecord: { entries: [{ bridgeSessionId: 'bridge-91', name: 'auto-renamed' }] }, expectedSessionId: sessionId, expectedName: name }), /matches both/);
assert.throws(() => validatePostflight({ sessionRecord: { sessionId: '11111111-1111-4111-8111-111111111111', bridgeSessionId: 'bridge-91', windowExists: true }, remoteRecord, expectedSessionId: sessionId, expectedName: name }), /UUID/);
assert.throws(() => renderLauncherPlan({ cwd: '/x', flowId: 'f', sessionId: 'not-a-uuid', name: 'n', systemPromptFile: '/s', userPromptFile: '/u', userEnvironment: { HOME: '/h', PATH: '/p' } }), /exact UUID/);
console.log('flow-launcher-dry-run fixtures passed');
