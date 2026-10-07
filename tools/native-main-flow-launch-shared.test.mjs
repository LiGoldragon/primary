import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import {canonicalTitleFor, clientForModel, continuationForLaunch, orderSkillsForPrompt, resolveSkillDependencies, writeContinuationRecord} from './native-main-flow-launch-shared.mjs';

test('Next follows installed wrapper endpoint and refuses mismatched or ambiguous tuples', () => {
  const home = fs.mkdtempSync(path.join(os.tmpdir(), 'native-launch-endpoint-'));
  try {
    const bin = path.join(home, '.nix-profile', 'bin'); fs.mkdirSync(bin, {recursive: true});
    const wrapper = path.join(bin, 'codex-next');
    const candidate = path.join(home, '.codex-next-candidate');
    const endpoint = path.join(candidate, 'app-server-control', 'app-server-control.sock');
    fs.writeFileSync(wrapper, `export CODEX_HOME=${candidate}; exec codex --remote unix://${endpoint} "$@"`);
    assert.equal(clientForModel('gpt-6-sol', home).endpoint, endpoint);
    assert.equal(clientForModel('gpt-6.1-sol', home).endpoint, endpoint);
    assert.equal(clientForModel('gpt-5.6-sol', home).endpoint, path.join(home, '.codex', 'app-server-control', 'app-server-control.sock'));
    fs.writeFileSync(wrapper, `export CODEX_HOME=${candidate}; exec codex --remote unix:///other/socket "$@"`);
    assert.throws(() => clientForModel('gpt-6-sol', home), /matching literal/);
    fs.writeFileSync(wrapper, `export CODEX_HOME=${candidate}; exec codex --remote unix://${endpoint} --remote unix://${endpoint} "$@"`);
    assert.throws(() => clientForModel('gpt-6-sol', home), /matching literal/);
  } finally { fs.rmSync(home, {recursive: true, force: true}); }
});

test('Curriculum returns the typed dependency closure and prompt callers keep operation-main-flow first', () => {
  let request;
  const closure = resolveSkillDependencies(['operation-main-flow', 'spirit'], value => {
    request = value;
    return 'ResolvedSkills.[ knowledge-vocabulary knowledge-psyche compensation-behavior compensation-correction operation-main-flow compensation-book-distillation spirit ]\n';
  });
  assert.equal(request, 'ResolveSkills.[ operation-main-flow spirit ]');
  assert.deepEqual(closure, ['knowledge-vocabulary', 'knowledge-psyche', 'compensation-behavior', 'compensation-correction', 'operation-main-flow', 'compensation-book-distillation', 'spirit']);
  assert.deepEqual(orderSkillsForPrompt(closure), ['operation-main-flow', 'knowledge-vocabulary', 'knowledge-psyche', 'compensation-behavior', 'compensation-correction', 'compensation-book-distillation', 'spirit']);
});

test('Curriculum closure failures stop composition with no partial names', () => {
  assert.throws(() => resolveSkillDependencies(['spirit'], () => 'ResolvedSkills.[ compensation-behavior ]'), /Curriculum omitted requested skill roots/);
  assert.throws(() => resolveSkillDependencies(['spirit'], () => 'ResolvedSkills.[ spirit spirit ]'), /duplicate resolved skills/);
  assert.throws(() => resolveSkillDependencies(['spirit'], () => 'not a typed reply'), /invalid ResolvedSkills/);
  assert.throws(() => resolveSkillDependencies(['spirit'], () => { throw new Error('registry unavailable'); }), /Curriculum ResolveSkills failed: registry unavailable/);
  assert.throws(() => resolveSkillDependencies(['spirit bad.name'], () => ''), /nonempty vector of Datom names/);
  assert.throws(() => orderSkillsForPrompt(['spirit', 'spirit']), /contains duplicates/);
});

test('continuation reads only an existing exact predecessor record and writes a readback record', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'native-continuation-'));
  try {
    const source = path.join(root, 'metaflow.datom');
    fs.writeFileSync(source, 'Voice.{ Field Tertiary }\n');
    const rootLineage = continuationForLaunch({flowsRoot: root, root: true, metaflowFile: source});
    assert.deepEqual(rootLineage, {predecessor: null, metaflow: 'Voice.{ Field Tertiary }\n'});
    fs.mkdirSync(path.join(root, 'abcdef'));
    const rootReceipt = writeContinuationRecord(root, 'abcdef', rootLineage);
    assert.equal(rootReceipt.record.predecessor, null);
    assert.equal(rootReceipt.record.metaflow, rootLineage.metaflow);
    const child = continuationForLaunch({flowsRoot: root, predecessor: 'abcdef'});
    assert.deepEqual(child, {predecessor: 'abcdef', metaflow: rootLineage.metaflow});
    fs.mkdirSync(path.join(root, '123abc'));
    const childReceipt = writeContinuationRecord(root, '123abc', child);
    assert.equal(childReceipt.record.predecessor, 'abcdef');
    assert.equal(childReceipt.record.metaflow, rootLineage.metaflow);
    assert.throws(() => continuationForLaunch({flowsRoot: root, root: true, predecessor: 'abcdef', metaflowFile: source}), /exactly one/);
    assert.throws(() => continuationForLaunch({flowsRoot: root, predecessor: 'unknown'}), /exact Flow ID/);
    assert.throws(() => continuationForLaunch({flowsRoot: root, predecessor: 'deadbe'}), /unavailable/);
    fs.mkdirSync(path.join(root, 'fedcba'));
    fs.writeFileSync(path.join(root, 'fedcba', 'continuation.json'), JSON.stringify({flowId: 'abcdef', predecessor: null, metaflow: 'wrong'}));
    assert.throws(() => continuationForLaunch({flowsRoot: root, predecessor: 'fedcba'}), /invalid/);
    assert.throws(() => continuationForLaunch({flowsRoot: root, root: true}), /--metaflow/);
  } finally { fs.rmSync(root, {recursive: true, force: true}); }
});

test('native voice title is model-free and always carries aspect layer and Flow ID', () => {
  assert.equal(canonicalTitleFor('Mind', 'gpt-6-luna', '918df4', 'Tertiary'), '{ Mind Tertiary 918df4 }');
  assert.equal(canonicalTitleFor('Field', 'gpt-6-astra', 'abcdef', 'Primary'), '{ Field Primary abcdef }');
  assert.throws(() => canonicalTitleFor('Field', 'gpt-6-luna', 'abcdef'), /exact layer/);
});
