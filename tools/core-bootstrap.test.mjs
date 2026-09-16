import assert from 'node:assert/strict';
import test from 'node:test';
import { bootstrapPhasePlan } from './core-bootstrap.mjs';

test('future bootstrap claims and registers the Flow before its readiness turn', () => {
  assert.deepEqual(bootstrapPhasePlan(), ['thread/start', 'flow-id claim', 'lane creation', 'index registration', 'turn/start readiness']);
});
