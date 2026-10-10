import assert from 'node:assert/strict';
import {mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync, chmodSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {spawnSync} from 'node:child_process';
import test from 'node:test';

const guard = new URL('./claude-rc-guard.mjs', import.meta.url).pathname;
const target = {
  session: '836818cc-83ab-4657-8b8f-1414f887559c',
  agentName: 'fable-rc-target', paneId: 'wD:p9', terminalId: 'term_65c138019438357',
  pid: 3784555, startTicks: 102010340, cwd: '/home/li/primary',
  argv: ['claude', '--session-id', '836818cc-83ab-4657-8b8f-1414f887559c', '--model', 'claude-fable-5-1[1m]'],
};

function fixture({agentStatus = 'idle', promptExit = 0, before = 'Fable 5.1·medium  ctx 3%',
  after = 'Fable 5.1·medium  ctx 3%  /rc', pane = target.paneId, terminal = target.terminalId,
  session = target.session, processInfo = target} = {}) {
  const dir = mkdtempSync(join(tmpdir(), 'claude-rc-guard-'));
  const bin = join(dir, 'bin'); mkdirSync(bin);
  const state = join(dir, 'state.json'); const prompt = join(dir, 'prompt.txt');
  writeFileSync(state, JSON.stringify({agentStatus, promptExit, before, after, pane, terminal, session, process: processInfo}));
  const herdr = join(bin, 'herdr');
  writeFileSync(herdr, `#!/usr/bin/env node
const fs=require('fs'); const s=JSON.parse(fs.readFileSync(process.env.RC_FIXTURE_STATE,'utf8'));
const a=process.argv.slice(2); const ix=a.indexOf('--session'); const session=ix<0?null:a[ix+1];
const rest=ix<0?a:a.slice(ix+2); const out=v=>process.stdout.write(JSON.stringify({result:v})+'\\n');
if(session!==s.session) process.exit(23);
if(rest[0]==='pane'&&rest[1]==='get') { if(rest[2]!==s.pane) process.exit(24); out({pane:{pane_id:s.pane,terminal_id:s.terminal,agent:s.process.agentName}}); }
else if(rest[0]==='pane'&&rest[1]==='process-info') { out({process_info:{pid:s.process.pid,start_ticks:s.process.startTicks,cwd:s.process.cwd,foreground_processes:[{pid:s.process.pid,argv:s.process.argv}]}}); }
else if(rest[0]==='agent'&&rest[1]==='get') { if(rest[2]!==s.pane) process.exit(25); out({agent:{name:s.process.agentName,pane_id:s.pane,terminal_id:s.terminal,agent_status:s.agentStatus,interactive_ready:true}}); }
else if(rest[0]==='pane'&&rest[1]==='read') { process.stdout.write(fs.existsSync(process.env.RC_FIXTURE_PROMPT)?s.after:s.before); }
else if(rest[0]==='agent'&&rest[1]==='prompt') { if(rest[2]!==s.pane||rest[3]!=='/remote-control') process.exit(26); fs.writeFileSync(process.env.RC_FIXTURE_PROMPT,rest[3]); process.exit(s.promptExit); }
else process.exit(27);
`); chmodSync(herdr, 0o755);
  const spec = join(dir, 'spec.json'); const receipt = join(dir, 'receipt.json');
  writeFileSync(spec, JSON.stringify(target));
  const run = mode => spawnSync(process.execPath, [guard, mode, '--spec', spec, '--receipt', receipt, '--proc-root', dir], {
    encoding: 'utf8', env: {...process.env, PATH: `${bin}:${process.env.PATH}`, RC_FIXTURE_STATE: state, RC_FIXTURE_PROMPT: prompt}, timeout: 10_000});
  return {dir, prompt, receipt, run, close: () => rmSync(dir, {recursive: true, force: true})};
}

function assertNoPrompt(f) { assert.equal(f.run('apply').status, 1); assert.equal(Boolean(f.prompt && (() => { try { readFileSync(f.prompt); return true; } catch { return false; } })()), false); }

test('applies exactly one supported Herdr /remote-control prompt after all pins and observes /rc', () => {
  const f = fixture();
  try {
    const result = f.run('apply');
    assert.equal(result.status, 0, result.stderr);
    assert.equal(readFileSync(f.prompt, 'utf8'), '/remote-control');
    const receipt = JSON.parse(readFileSync(f.receipt, 'utf8'));
    assert.equal(receipt.status, 'applied');
    assert.equal(receipt.prompt, '/remote-control');
    assert.equal(receipt.postcondition.remoteControl.featureEnabled, true);
  } finally { f.close(); }
});

test('fails closed without input when a pinned identity differs', () => {
  const f = fixture({terminal: 'term_other'});
  try { assertNoPrompt(f); } finally { f.close(); }
});

test('fails closed without input while the target is busy', () => {
  const f = fixture({agentStatus: 'working'});
  try { assertNoPrompt(f); } finally { f.close(); }
});

test('nonzero Herdr prompt exit is a failure and leaves no success receipt', () => {
  const f = fixture({promptExit: 9});
  try {
    const result = f.run('apply');
    assert.equal(result.status, 1);
    assert.equal(readFileSync(f.prompt, 'utf8'), '/remote-control');
    assert.equal(Boolean(result.stdout.includes('applied')), false);
  } finally { f.close(); }
});

test('an ambiguous or missing post footer fails closed even after the single allowed input', () => {
  const f = fixture({after: 'Fable 5.1·medium ctx 3%\n❯ /rc\nremote-control help'});
  try {
    const result = f.run('apply');
    assert.equal(result.status, 1);
    assert.equal(readFileSync(f.prompt, 'utf8'), '/remote-control');
  } finally { f.close(); }
});

test('receipt and output redact pane content, authentication material, and pairing-shaped values', () => {
  const sentinel = 'PAIRING_CODE_SECRET_123456';
  const f = fixture({before: `${sentinel}\nFable 5.1·medium ctx 3%`, after: `${sentinel}\nFable 5.1·medium ctx 3% /rc`});
  try {
    const result = f.run('apply');
    assert.equal(result.status, 0, result.stderr);
    assert.equal(result.stdout.includes(sentinel), false);
    assert.equal(readFileSync(f.receipt, 'utf8').includes(sentinel), false);
  } finally { f.close(); }
});
