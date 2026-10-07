import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import {clientForModel, orderSkillsForPrompt, resolveSkillDependencies} from './native-main-flow-launch-shared.mjs';

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
