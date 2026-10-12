import test from 'node:test';
import assert from 'node:assert/strict';
import {nativeAgentName, canonicalTitleFor} from './native-main-flow-launch-shared.mjs';
test('long topic keeps exact identity within the actual Herdr name contract', () => {
 const name = nativeAgentName('Field', 'Quaternary', 'PrimaryCommitting', '89fbc1');
 assert.match(name, /^[a-z][a-z0-9_-]{0,31}$/);
 assert.ok(name.endsWith('_89fbc1'));
 assert.notEqual(name, nativeAgentName('Field', 'Quaternary', 'PrimaryCommitting', 'abcdef'));
 assert.equal(canonicalTitleFor('Field', undefined, '89fbc1', 'Quaternary', 'PrimaryCommitting'), '{ Field PrimaryCommitting Quaternary 89fbc1 }');
});
test('short core names stay stable and impossible identity lengths refuse', () => {
 assert.equal(nativeAgentName('Field', 'Quaternary', 'Core', '89fbc1'), 'field_quaternary_89fbc1');
 assert.throws(() => nativeAgentName('Field','Quaternary','Core','a'.repeat(32)), /binding name/);
});
