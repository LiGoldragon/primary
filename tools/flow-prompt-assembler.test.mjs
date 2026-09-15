import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { assemblePrimaryPrompts, assemblePrompts, writePrompts } from './flow-prompt-assembler-core.mjs';

const root = fs.mkdtempSync(path.join(os.tmpdir(), 'flow-prompt-assembler-'));
const lane = path.join(root, 'real-predecessor-lane');
const output = path.join(root, 'out');
for (const directory of ['spirit', 'intent', 'Vision', 'vision']) fs.mkdirSync(path.join(lane, directory), { recursive: true });
fs.writeFileSync(path.join(lane, 'lane.json'), JSON.stringify({ identity: 'predecessor-12', topic: 'flow-refresh', successor: { identity: 'successor-12', topic: 'flow-refresh-repair' }, transcript_provenance: [{ source_path: '/opaque/transcript.jsonl', source_message_id: 'message-12' }], skills: ['spirit', 'psyche', 'testing'] }));
fs.writeFileSync(path.join(lane, 'spirit', 'core.md'), 'Spirit preserves evidence.');
fs.writeFileSync(path.join(lane, 'intent', 'goal.md'), 'Intent continues the flow.');
fs.writeFileSync(path.join(lane, 'Vision', 'refresh.md'), 'Vision uses a fresh flow.');
fs.writeFileSync(path.join(lane, 'vision', 'raw.md'), 'Raw Vision stays verbatim.');
fs.writeFileSync(path.join(lane, 'log.md'), '- [ ] carry this open item');
const assembled = assemblePrompts({ lane });
assert.match(assembled.system, /System prompt for successor-12/);
assert.match(assembled.system, /Spirit preserves evidence/);
assert.match(assembled.system, /Intent continues the flow/);
assert.match(assembled.system, /Vision uses a fresh flow/);
assert.match(assembled.system, /- psyche/);
assert.match(assembled.user, /Predecessor identity: predecessor-12/);
assert.match(assembled.user, /source_message_id: message-12/);
assert.match(assembled.user, /carry this open item/);
assert.match(assembled.user, /Raw Vision stays verbatim/);
fs.mkdirSync(output);
const written = writePrompts({ lane, output });
assert.notEqual(written.systemPath, written.userPath);
assert.equal(fs.readFileSync(written.systemPath, 'utf8'), assembled.system);
assert.equal(fs.readFileSync(written.userPath, 'utf8'), assembled.user);
const missing = path.join(root, 'missing-provenance');
fs.cpSync(lane, missing, { recursive: true });
const missingMetadata = JSON.parse(fs.readFileSync(path.join(missing, 'lane.json'))); missingMetadata.transcript_provenance = [];
fs.writeFileSync(path.join(missing, 'lane.json'), JSON.stringify(missingMetadata));
assert.throws(() => assemblePrompts({ lane: missing }), /exactly one transcript provenance/);
const ambiguous = path.join(root, 'ambiguous-provenance');
fs.cpSync(lane, ambiguous, { recursive: true });
const ambiguousMetadata = JSON.parse(fs.readFileSync(path.join(ambiguous, 'lane.json'))); ambiguousMetadata.transcript_provenance.push({ source_path: '/opaque/other.jsonl', source_message_id: 'message-13' });
fs.writeFileSync(path.join(ambiguous, 'lane.json'), JSON.stringify(ambiguousMetadata));
assert.throws(() => assemblePrompts({ lane: ambiguous }), /exactly one transcript provenance/);

// The direct-input form accepts a real predecessor directory without requiring
// a synthetic lane.json or successor topic. It must still refuse to invent
// transcript provenance and must write two physical prompt files.
const minimalLane = path.join(root, 'flows', '692df8');
fs.mkdirSync(minimalLane, { recursive: true });
fs.writeFileSync(path.join(minimalLane, 'log.md'), 'predecessor handoff for fixture 692df8');
fs.mkdirSync(path.join(minimalLane, 'vision'));
fs.writeFileSync(path.join(minimalLane, 'vision', 'signal.md'), 'Signal source record');
const minimalOutput = path.join(root, 'minimal-out');
const cliOutput = execFileSync(process.execPath, [path.resolve('tools/flow-prompt-assembler'), 'assemble', '--predecessor', minimalLane, '--successor', '05c6048e', '--output', minimalOutput], { encoding: 'utf8' });
const cliResult = JSON.parse(cliOutput);
assert.equal(cliResult.kind, 'assembled-prompts');
assert.match(fs.readFileSync(path.join(minimalOutput, 'system-prompt.md'), 'utf8'), /Successor identity: 05c6048e/);
assert.match(fs.readFileSync(path.join(minimalOutput, 'user-prompt.md'), 'utf8'), /unavailable: no exact source path/);

// The primary profile is deliberately broader than the predecessor-only
// assembler. This fixture demonstrates the old omission first, then requires
// whole primary Vision/Intent contents, relevant raw records, all nine bodies,
// and a path/hash coverage manifest without invented transcript identifiers.
const primary = path.join(root, 'primary');
const primaryPredecessor = path.join(root, 'predecessor');
for (const directory of [
  'Vision/nested', 'Intent', 'flows/a/vision', 'flows/b/vision', 'flows/c/vision',
  '.claude/skills',
]) fs.mkdirSync(path.join(primary, directory), { recursive: true });
fs.writeFileSync(path.join(primary, 'Vision', 'one.md'), 'Primary Vision one: whole.');
fs.writeFileSync(path.join(primary, 'Vision/nested', 'two.md'), 'Primary Vision two: whole.');
fs.writeFileSync(path.join(primary, 'Intent', 'goal.md'), 'Primary Intent: whole.');
fs.writeFileSync(path.join(primary, 'flows/a/vision/network.md'), 'Raw network A.');
fs.writeFileSync(path.join(primary, 'flows/b/vision/network.md'), 'Raw network B.');
fs.writeFileSync(path.join(primary, 'flows/c/vision/unrelated.md'), 'Raw unrelated.');
for (const skill of ['spirit', 'psyche', 'behavior', 'correction', 'vocabulary', 'testing', 'psyche-interraction', 'main-flow', 'edit-coordination']) {
  fs.mkdirSync(path.join(primary, '.claude', 'skills', skill), { recursive: true });
  fs.writeFileSync(path.join(primary, '.claude', 'skills', skill, 'SKILL.md'), `whole ${skill} body`);
}
for (const directory of ['vision', 'notion']) fs.mkdirSync(path.join(primaryPredecessor, directory), { recursive: true });
fs.writeFileSync(path.join(primaryPredecessor, 'vision', 'network.md'), 'Predecessor network vision.');
fs.writeFileSync(path.join(primaryPredecessor, 'notion', 'adjacent.md'), 'Predecessor adjacent notion.');
fs.writeFileSync(path.join(primaryPredecessor, 'log.md'), 'Original predecessor log.');
fs.writeFileSync(path.join(primaryPredecessor, 'lane.json'), JSON.stringify({ identity: 'real-predecessor', topic: 'network', successor: { identity: 'real-successor', topic: 'network' }, transcript_provenance: [], skills: [] }));
fs.mkdirSync(path.join(primary, 'flows/d/vision'), { recursive: true });
fs.writeFileSync(path.join(primary, 'flows/d/vision/adjacent.md'), 'Raw adjacent selected from predecessor notion.');
const oldPrimaryAssembly = assemblePrompts({ lane: primaryPredecessor, minimal: true, successorIdentity: 'actual-successor', topic: 'network' });
assert.throws(() => assert.match(oldPrimaryAssembly.system, /Primary Vision one: whole\./));
const primaryAssembly = assemblePrimaryPrompts({ lane: primaryPredecessor, primaryRoot: primary, successorIdentity: 'actual-successor', topic: 'network' });
for (const expected of [
  'Primary Vision one: whole.', 'Primary Vision two: whole.', 'Primary Intent: whole.',
  'Raw network A.', 'Raw network B.', 'Raw adjacent selected from predecessor notion.',
  'Predecessor network vision.', 'Predecessor adjacent notion.', 'whole edit-coordination body',
]) assert.match(primaryAssembly.system, new RegExp(expected.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
assert.doesNotMatch(primaryAssembly.system, /Raw unrelated\./);
assert.match(primaryAssembly.user, /No exact transcript provenance record was supplied\. No identifier has been invented\./);
assert.match(primaryAssembly.user, /Original predecessor log\./);
assert.equal(primaryAssembly.metadata.sourceCoverage.length, 17);
assert(primaryAssembly.metadata.sourceCoverage.every(entry => entry.path.startsWith(primary) || entry.path.startsWith(primaryPredecessor)));
assert(primaryAssembly.metadata.sourceCoverage.every(entry => /^[a-f0-9]{64}$/.test(entry.sha256)));
const primaryOutput = path.join(root, 'primary-out'); fs.mkdirSync(primaryOutput);
writePrompts({ lane: primaryPredecessor, output: primaryOutput, profile: 'primary', primaryRoot: primary, successorIdentity: 'actual-successor', topic: 'network' });
assert.deepEqual(fs.readdirSync(primaryOutput).sort(), ['system-prompt.md', 'user-prompt.md']);
console.log('flow prompt assembler fixtures passed');
