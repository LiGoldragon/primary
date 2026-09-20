import assert from 'node:assert/strict';
import {test} from 'node:test';
import {due} from './field-census-cycle.mjs';

test('notification cadence holds uncertain attempts and avoids immediate repeats', () => {
  const time = Date.parse('2026-09-20T23:00:00Z');
  assert.equal(due({}, time, 1800), true);
  assert.equal(due({last_completed_at:'2026-09-20T22:45:00Z'}, time, 1800), false);
  assert.equal(due({last_completed_at:'2026-09-20T22:30:00Z'}, time, 1800), true);
  assert.equal(due({last_completed_at:'2026-09-20T21:00:00Z', hold:{status:'uncertain'}}, time, 1800), false);
});
