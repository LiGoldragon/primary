#!/usr/bin/env node
import assert from 'node:assert/strict';
import {VOICE_PROFILES, selectVoiceProfile, voiceKey} from './native-voice-profiles.mjs';

assert.equal(voiceKey({aspect: 'Field', layer: 'Primary'}), 'Field.Primary');
assert.throws(() => voiceKey({aspect: 'Field'}), /aspect and layer are required/);
assert.ok(Object.isFrozen(VOICE_PROFILES));
for (const [key, profile] of Object.entries(VOICE_PROFILES)) {
  assert.ok(Object.isFrozen(profile), key);
  if (profile.status !== 'configured') continue;
  const [aspect, layer] = key.split('.');
  assert.strictEqual(selectVoiceProfile({aspect, layer}), profile, key);
  assert.strictEqual(selectVoiceProfile({aspect, layer, harness: profile.harness, model: profile.model, effort: profile.effort}), profile, key);
}
assert.throws(() => { VOICE_PROFILES['Field.Primary'].model = 'gpt-6-luna'; }, TypeError);
assert.throws(() => selectVoiceProfile({aspect: 'Field', layer: 'Primary', harness: 'claude'}), /harness differs/);
assert.throws(() => selectVoiceProfile({aspect: 'Field', layer: 'Primary', model: 'gpt-6-luna'}), /model differs/);
assert.throws(() => selectVoiceProfile({aspect: 'Field', layer: 'Primary', effort: 'low'}), /effort differs/);
assert.throws(() => selectVoiceProfile({aspect: 'Mind', layer: 'Secondary'}), /correspondence is pending/);
assert.throws(() => selectVoiceProfile({aspect: 'Mind', layer: undefined}), /aspect and layer are required/);
console.log('native-voice-profiles tests passed');
