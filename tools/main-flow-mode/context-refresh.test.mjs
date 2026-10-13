import test from 'node:test';
import assert from 'node:assert/strict';
import {makeContextRefreshBinding, nativeStopCommand} from './context-refresh.mjs';

test('birth binding preserves supplied identity and stable Stop contracts', () => {
  const baseConfig = {version: 1, warningWindowFraction: 0.37, claude: {warningTokens: 123456}, codex: {models: {'gpt-6.1-sol': 373000}}, recipients: {field: 'Field Core Secondary'}};
  const binding = makeContextRefreshBinding({nativeSessionId: '33752bfb-ebba-4e2d-ba66-be84b318e939', flowId: '33752b',
    aspect: 'Psyche', topic: 'Core', layer: 'Primary', harness: 'claude', model: 'claude-opus', seatTarget: 'Psyche Core Primary',
    baseConfig});
  assert.equal(binding.bindings[0].nativeSessionId, '33752bfb-ebba-4e2d-ba66-be84b318e939');
  assert.equal(binding.warningWindowFraction, 0.37);
  assert.equal(binding.claude.warningTokens, 123456);
  assert.equal(nativeStopCommand.codex.sessionField, 'session_id');
  assert.equal(nativeStopCommand.codex.alternateSessionField, 'thread_id');
});

test('birth binding refuses inferred or malformed identity', () => {
  const baseConfig = {version: 1, warningWindowFraction: 0.5, claude: {warningTokens: 200000}, codex: {models: {x: 1}}, recipients: {field: 'Field Core Secondary'}};
  assert.throws(() => makeContextRefreshBinding({baseConfig, nativeSessionId: 'short', flowId: '33752b', aspect: 'Psyche', topic: 'Core', layer: 'Primary', harness: 'claude', model: 'x', seatTarget: 'Psyche Core Primary'}));
  assert.throws(() => makeContextRefreshBinding({baseConfig, nativeSessionId: '33752bfb-ebba-4e2d-ba66-be84b318e939', flowId: '33752b', aspect: 'Psyche', topic: 'Core', layer: 'Primary', harness: 'claude', model: 'x', seatTarget: 'Wrong'}));
});
