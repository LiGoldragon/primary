import test from 'node:test';
import assert from 'node:assert/strict';
import net from 'node:net';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {Restarter, checkLock, rpc, subscribe} from './restart.mjs';

const config = {flow: '127d95', name: 'field_quaternary_127d95', uuid: 'same-real-native-id', lock: {id: 19178, name: 'PrimaryPublish', owner: '127d95', paths: ['/primary/.PrimaryPublish.lock']}};
const old = {pane: 'w1:p1', terminal: 'term1', workspace: 'w1'};
const target = {pane: 'w1:p2', terminal: 'term2', workspace: 'w1'};
const event = {event: 'pane.exited', data: {pane_id: old.pane, workspace_id: old.workspace}};
function agent(b = old) { return {name: config.name, agent: 'codex', agent_session: {agent: 'codex', kind: 'id', value: config.uuid}, pane_id: b.pane, terminal_id: b.terminal, workspace_id: b.workspace, interactive_ready: true, launch_pending: false, agent_status: 'idle'}; }
function fixture(failAt) {
  const calls = []; let live = agent(); let phase = 'startup'; let oldRoute = true;
  const hit = name => { calls.push(name); if (name === failAt && phase !== 'startup') throw new Error(`refused ${name}`); };
  const io = {
    record: status => calls.push(status),
    guard: async () => hit('guard'),
    agent: async () => { hit('agent'); return live; },
    absent: async () => hit('absent'),
    create: async () => { hit('create'); return target; },
    resume: async () => { hit('resume'); live = agent(target); return live; },
    deregister: async b => { hit('deregister'); assert.deepEqual(b, old); oldRoute = false; },
    register: async () => { hit('register'); if (phase !== 'startup') assert.equal(oldRoute, false); },
  };
  const restarter = new Restarter(config, io);
  return {restarter, calls, begin: async () => { await restarter.start(); calls.length = 0; phase = 'event'; }, io};
}

test('one event burst makes one ready replacement with the same UUID, recipient and lock', async () => {
  const f = fixture(); await f.begin();
  await Promise.all([f.restarter.event(event), f.restarter.event(event), f.restarter.event({event: 'pane.exited', data: {pane_id: 'unrelated', workspace_id: 'w1'}})]);
  assert.equal(f.calls.filter(x => x === 'create').length, 1);
  assert.equal(f.calls.filter(x => x === 'resume').length, 1);
  assert.deepEqual(f.restarter.current, target);
  assert.equal(f.restarter.phase, 'watching');
  assert.ok(f.calls.indexOf('resume') < f.calls.indexOf('deregister'));
  assert.ok(f.calls.indexOf('deregister') < f.calls.lastIndexOf('register'));
  assert.equal(f.calls.at(-1), 'recovered');
});

test('guard, old-client, launch, native-identity and partial-registration refusals never retry or claim recovery', async () => {
  for (const step of ['absent', 'guard', 'create', 'resume', 'deregister', 'register']) {
    const f = fixture(step); await f.begin();
    await assert.rejects(f.restarter.event(event), /refused/);
    const count = f.calls.filter(x => x === 'resume').length;
    await assert.rejects(f.restarter.event(event));
    assert.equal(f.calls.filter(x => x === 'resume').length, count);
    assert.ok(!f.calls.includes('recovered'));
    assert.equal(f.restarter.phase, 'blocked');
    if (['absent', 'guard'].includes(step)) assert.ok(!f.calls.includes('create'));
  }
  for (const difference of [{agent_session: {agent: 'codex', kind: 'id', value: 'other'}}, {interactive_ready: false}, {terminal_id: 'different'}]) {
    const f = fixture(); await f.begin();
    f.io.resume = async () => ({...agent(target), ...difference});
    await assert.rejects(f.restarter.event(event), /identity|ready/);
    assert.ok(!f.calls.includes('deregister'));
  }
});

test('ownership parser rejects absent, changed, conflicting, malformed and reason-only owner evidence', () => {
  const row = '{ 19178 PrimaryPublish 127d95 [ /primary/.PrimaryPublish.lock ] «held» }';
  const wrap = rows => `Observed.Locks.[ ${rows} ]\n`;
  checkLock(wrap(row), config.lock);
  for (const text of [wrap(''), wrap(row.replace('127d95', 'other')), wrap(row + row), wrap(row + ' { 8 Other another [ /primary ] «conflict» }'), wrap('{ 1 Other another [ /elsewhere ] «19178 PrimaryPublish 127d95» }'), row, wrap(row) + 'garbage']) {
    assert.throws(() => checkLock(text, config.lock));
  }
});

test('public NDJSON adapter subscribes and carries errors without invoking any live endpoint', async () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'committer-api-'));
  const socketPath = path.join(dir, 'api.sock'); const sockets = new Set();
  const server = net.createServer(socket => {
    sockets.add(socket); socket.on('close', () => sockets.delete(socket));
    socket.once('data', bytes => {
      const request = JSON.parse(bytes.toString());
      if (request.method === 'events.subscribe') {
        assert.deepEqual(request.params.subscriptions, [{type: 'pane.exited'}]);
        socket.write(`${JSON.stringify({id: request.id, result: {type: 'subscription_started'}})}\n`);
        socket.write(`${JSON.stringify(event)}\n`);
      } else { socket.end(`${JSON.stringify({id: request.id, error: {code: 'pane_not_found', message: 'gone'}})}\n`); }
    });
  });
  await new Promise(resolve => server.listen(socketPath, resolve));
  try {
    let got; const received = new Promise(resolve => { got = resolve; });
    const subscription = await subscribe(socketPath, got, error => assert.fail(error));
    assert.deepEqual(await received, event);
    subscription.destroy();
    await assert.rejects(rpc(socketPath, 'pane.get', {pane_id: old.pane}), error => error.code === 'pane_not_found');
  } finally { for (const socket of sockets) socket.destroy(); await new Promise(resolve => server.close(resolve)); fs.rmSync(dir, {recursive: true}); }
});

test('event transport loss during a guard prevents subsequent shell creation', async () => {
  const f = fixture(); await f.begin();
  f.io.guard = async () => { f.restarter.cancel(new Error('stream disconnected')); };
  await assert.rejects(f.restarter.event(event), /disconnected/);
  assert.ok(!f.calls.includes('create'));
});

test('real local adapter preserves exact arguments and moves only the stale registration after readiness', async () => {
  const {adapter} = await import('./restart.mjs');
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'committer-adapter-'));
  const socketPath = path.join(dir, 'api.sock'); const sockets = new Set();
  const started = path.join(dir, 'started'); const log = path.join(dir, 'commands');
  const c = {...config, session: 'default', primary: dir, codexHome: dir, socket: socketPath, recoveryConfig: path.join(dir, 'config.json'), resumeExecutable: '/fixture/guarded-resume', resumeArgs: ['resume', config.uuid, '-m', 'gpt-6-luna']};
  const script = (name, body) => {
    const file = path.join(dir, name);
    fs.writeFileSync(file, `#!${process.execPath}\nconst fs=require('node:fs');const args=process.argv.slice(2);fs.appendFileSync(${JSON.stringify(log)},JSON.stringify({name:${JSON.stringify(name)},args})+'\\n');${body}\n`, {mode: 0o700});
    return file;
  };
  c.orchestrate = script('orchestrate', `console.log('Observed.Locks.[ { 19178 PrimaryPublish 127d95 [ /primary/.PrimaryPublish.lock ] «held» } ]')`);
  c.herdr = script('herdr', `fs.writeFileSync(${JSON.stringify(started)},'started');console.log(${JSON.stringify(JSON.stringify({result: {agent: agent(target)}}))});`);
  c.messenger = script('messenger', `console.log(args[0]==='register'?'Registered 127d95: field_quaternary_127d95 (default)':'Deregistered stale 127d95: field_quaternary_127d95 (default/w1:p1/term1)')`);
  let initial = true;
  const server = net.createServer(socket => {
    sockets.add(socket); socket.on('close', () => sockets.delete(socket));
    socket.once('data', bytes => {
      const request = JSON.parse(bytes); let result;
      if (request.method === 'agent.get') result = {agent: fs.existsSync(started) ? agent(target) : agent()};
      else if (request.method === 'agent.list') result = {agents: []};
      else if (request.method === 'pane.get') { socket.end(`${JSON.stringify({id: request.id, error: {code: 'pane_not_found', message: 'gone'}})}\n`); return; }
      else if (request.method === 'tab.create') {
        assert.equal(initial, false);
        assert.equal(request.params.focus, false);
        assert.equal(request.params.env.FLOW_ID, config.flow);
        assert.equal(request.params.env.PRIMARY_COMMITTER_RECOVERY_CONFIG, c.recoveryConfig);
        result = {root_pane: {pane_id: target.pane, terminal_id: target.terminal, workspace_id: target.workspace}};
      } else assert.fail(request.method);
      socket.end(`${JSON.stringify({id: request.id, result})}\n`);
    });
  });
  await new Promise(resolve => server.listen(socketPath, resolve));
  try {
    const io = adapter(c); io.record = () => {};
    const restarter = new Restarter(c, io);
    await restarter.start(); initial = false;
    await restarter.event(event);
    const calls = fs.readFileSync(log, 'utf8').trim().split('\n').map(JSON.parse);
    assert.equal(calls.filter(c => c.name === 'herdr').length, 1);
    assert.deepEqual(calls.find(c => c.name === 'herdr').args, ['--session', 'default', 'agent', 'start', config.name, '--kind', 'codex', '--pane', target.pane, '--executable', c.resumeExecutable, '--timeout', '60000', '--', ...c.resumeArgs]);
    assert.deepEqual(calls.filter(c => c.name === 'messenger').map(c => c.args), [
      ['register', config.flow, config.name, '--session', 'default', '--native-thread', config.uuid],
      ['deregister', config.flow, '--session', 'default', '--pane-id', old.pane, '--terminal-id', old.terminal, '--name', config.name],
      ['register', config.flow, config.name, '--session', 'default', '--native-thread', config.uuid],
    ]);
    assert.equal(restarter.phase, 'watching');
  } finally { for (const socket of sockets) socket.destroy(); await new Promise(resolve => server.close(resolve)); fs.rmSync(dir, {recursive: true}); }
});
