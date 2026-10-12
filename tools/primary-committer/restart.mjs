#!/usr/bin/env node
// Our committer lifecycle, using unmodified Herdr's public JSON API and CLI.
import fs from 'node:fs';
import net from 'node:net';
import crypto from 'node:crypto';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const exec = promisify(execFile);
const requireFact = (ok, message) => { if (!ok) throw new Error(message); };
const digest = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');

export function checkLock(text, expected) {
  // Parse the complete typed snapshot, not an owner substring in another lock's reason.
  const match = /^\s*Observed\.Locks\.\s*\[([\s\S]*)\]\s*$/.exec(text);
  requireFact(match, 'unrecognized lock snapshot');
  const rows = [];
  let rest = match[1];
  const row = /^\s*\{\s*(\d+)\s+([^\s{}\[\]]+)\s+([^\s{}\[\]]+)\s+\[([^\[\]]*)\]\s+«[^«»]*»\s*\}/;
  while (rest.trim()) {
    const m = row.exec(rest);
    requireFact(m, 'unrecognized lock row');
    rows.push({id: Number(m[1]), name: m[2], owner: m[3], paths: m[4].trim().split(/\s+/).filter(Boolean)});
    rest = rest.slice(m[0].length);
  }
  const relevant = rows.filter(r => r.id === expected.id || r.name === expected.name || r.paths.some(p => expected.paths.some(q => p === q || q.startsWith(`${p}/`) || p.startsWith(`${q}/`))));
  requireFact(relevant.length === 1 && relevant[0].id === expected.id && relevant[0].name === expected.name && relevant[0].owner === expected.owner && JSON.stringify(relevant[0].paths) === JSON.stringify(expected.paths), 'lifetime lock absent, conflicting, ambiguous, or owned by someone else');
}

export function validateConfig(c) {
  requireFact(/^[a-f0-9]{6,64}$/.test(c.flow) && c.lock.owner === c.flow, 'invalid fixed owner');
  requireFact(c.lock.name === 'PrimaryPublish' && c.lock.paths.length === 1, 'invalid lifetime lock');
  requireFact(c.resumeArgs[0] === 'resume' && c.resumeArgs[1] === c.uuid, 'resume must name the same native UUID');
  requireFact(c.resumeArgs.includes('gpt-6-luna') && c.resumeArgs.includes('model_reasoning_effort="low"'), 'required Luna low profile missing');
  requireFact(c.resumeArgs.includes(`model_instructions_file=${JSON.stringify(c.systemPrompt)}`), 'SYSTEM closure is not the resume input');
  requireFact(!c.resumeArgs.includes('--last'), 'floating native session prohibited');
  for (const key of ['socket', 'primary', 'systemPrompt', 'herdr', 'messenger', 'orchestrate', 'resumeExecutable', 'nativeWrapper']) requireFact(path.isAbsolute(c[key] ?? ''), `absolute ${key} required`);
  const socket = fs.statSync(c.socket);
  requireFact(socket.isSocket() && socket.uid === process.getuid() && (socket.mode & 0o077) === 0, 'Herdr API socket ownership/permissions unqualified');
  requireFact(digest(c.systemPrompt) === c.systemSha256, 'SYSTEM bytes changed');
  requireFact(digest(c.nativeWrapper) === c.nativeWrapperSha256, 'native wrapper changed');
}

function nativeMatches(c, a) {
  return a?.name === c.name && a.agent === 'codex' && a.agent_session?.agent === 'codex' && a.agent_session.kind === 'id' && a.agent_session.value === c.uuid;
}
function binding(c, a) {
  requireFact(nativeMatches(c, a) && a.pane_id && a.terminal_id && a.workspace_id, 'native recipient binding mismatch');
  return {pane: a.pane_id, terminal: a.terminal_id, workspace: a.workspace_id};
}
function ready(c, a, target) {
  requireFact(nativeMatches(c, a) && a.pane_id === target.pane && a.terminal_id === target.terminal, 'replacement native identity changed');
  requireFact(a.interactive_ready === true && !a.launch_pending && ['idle', 'done'].includes(a.agent_status), 'replacement not interactively ready');
}

export class Restarter {
  constructor(config, io) { this.c = config; this.io = io; this.current = null; this.phase = 'initializing'; this.cancelled = null; this.tail = Promise.resolve(); }
  cancel(reason) { this.cancelled = reason; this.phase = 'blocked'; }
  async step(name, ...args) {
    if (this.cancelled) throw this.cancelled;
    const result = await this.io[name](...args);
    if (this.cancelled) throw this.cancelled;
    return result;
  }
  async start() {
    await this.step('guard');
    const a = await this.step('agent');
    this.current = binding(this.c, a);
    // Idempotent registration refuses any stale or conflicting route; never removes one at startup.
    await this.step('register');
    this.phase = 'watching';
    this.io.record('watching', this.current);
  }
  event(event) {
    this.tail = this.tail.then(async () => {
      if (this.phase === 'blocked') throw new Error('recovery blocked; no automatic retry');
      if (event.event !== 'pane.exited' || event.data?.pane_id !== this.current?.pane || event.data?.workspace_id !== this.current?.workspace) return;
      const old = this.current;
      try {
        this.phase = 'checking';
        await this.step('absent', old);
        await this.step('guard');
        this.phase = 'creating';
        const target = await this.step('create', old);
        requireFact(target.pane && target.terminal && target.pane !== old.pane && target.terminal !== old.terminal, 'replacement shell identity invalid');
        this.io.record('shell-created', target);
        // A second exact absence/ownership check closes the preparation interval; guard wrapper checks again at exec.
        await this.step('absent', old);
        await this.step('guard');
        this.phase = 'starting';
        ready(this.c, await this.step('resume', target), target);
        ready(this.c, await this.step('agent'), target);
        await this.step('guard');
        this.phase = 'registering';
        await this.step('deregister', old);
        await this.step('register');
        ready(this.c, await this.step('agent'), target);
        this.current = {...target};
        this.phase = 'watching';
        this.io.record('recovered', {flow: this.c.flow, uuid: this.c.uuid, lock: this.c.lock.id, ...target});
      } catch (error) {
        this.phase = 'blocked';
        this.io.record('blocked', {error: error.message, old});
        // Leave any replacement shell/client intact for exact operator disposition. Never spawn again or roll back a route.
        throw error;
      }
    });
    return this.tail;
  }
}

export function rpc(socketPath, method, params, timeout = 15000) {
  return new Promise((resolve, reject) => {
    const socket = net.createConnection(socketPath); socket.setEncoding('utf8'); let buffer = '';
    const timer = setTimeout(() => finish(new Error(`${method}: timeout; outcome unknown`)), timeout);
    function finish(error, result) { clearTimeout(timer); socket.destroy(); error ? reject(error) : resolve(result); }
    socket.on('error', error => finish(error));
    socket.on('connect', () => socket.write(`${JSON.stringify({id: 'committer-restarter', method, params})}\n`));
    socket.on('data', bytes => {
      buffer += bytes.toString('utf8');
      if (buffer.length > 1024 * 1024) return finish(new Error('oversized Herdr response'));
      const end = buffer.indexOf('\n'); if (end < 0) return;
      try {
        const response = JSON.parse(buffer.slice(0, end));
        requireFact(response.id === 'committer-restarter', 'response identity mismatch');
        if (response.error) return finish(Object.assign(new Error(response.error.message), {code: response.error.code}));
        requireFact(response.result, 'missing Herdr result'); finish(null, response.result);
      } catch (error) { finish(error); }
    });
    socket.on('end', () => finish(new Error(`${method}: closed without response`)));
  });
}

export async function subscribe(socketPath, onEvent, onFailure) {
  const socket = net.createConnection(socketPath); socket.setEncoding('utf8'); let buffer = ''; let started = false;
  await new Promise((resolve, reject) => {
    const timer = setTimeout(() => fail(new Error('event subscription timeout')), 15000);
    function fail(error) { clearTimeout(timer); socket.destroy(); started ? onFailure(error) : reject(error); }
    socket.on('error', fail);
    socket.on('end', () => fail(new Error('event stream ended; no blind reconnect or recovery')));
    socket.on('connect', () => socket.write(`${JSON.stringify({id: 'committer-events', method: 'events.subscribe', params: {subscriptions: [{type: 'pane.exited'}]}})}\n`));
    socket.on('data', bytes => {
      buffer += bytes.toString('utf8');
      if (buffer.length > 1024 * 1024) return fail(new Error('oversized event stream record'));
      let end;
      while ((end = buffer.indexOf('\n')) >= 0) {
        const line = buffer.slice(0, end); buffer = buffer.slice(end + 1);
        try {
          const message = JSON.parse(line);
          if (!started) {
            requireFact(message.id === 'committer-events' && message.result?.type === 'subscription_started', 'event subscription refused');
            started = true; clearTimeout(timer); resolve();
          } else { onEvent(message); }
        } catch (error) { fail(error); return; }
      }
    });
  });
  return socket;
}

export function adapter(c) {
  const env = {...process.env, FLOW_ID: c.flow, CODEX_HOME: c.codexHome};
  delete env.PRIMARY_COMMITTER_FLOW_ID; delete env.CODEX_THREAD_ID;
  const run = async (exe, args, timeout = 30000) => (await exec(exe, args, {env, timeout, maxBuffer: 1024 * 1024})).stdout;
  const call = (method, params) => rpc(c.socket, method, params);
  return {
    record: (status, facts) => console.log(JSON.stringify({at: new Date().toISOString(), status, ...facts})),
    guard: async () => checkLock(await run(c.orchestrate, ['Observe.Locks'], 10000), c.lock),
    agent: async () => (await call('agent.get', {target: c.name})).agent,
    absent: async old => {
      try { await call('pane.get', {pane_id: old.pane}); throw new Error('old pane still exists'); }
      catch (error) { if (error.code !== 'pane_not_found') throw error; }
      const {agents} = await call('agent.list', {});
      requireFact(Array.isArray(agents), 'missing session agent result');
      requireFact(!agents.some(a => a.name === c.name || a.terminal_id === old.terminal || a.agent_session?.value === c.uuid), 'live recipient/native session/terminal still exists');
    },
    create: async old => {
      const result = await call('tab.create', {workspace_id: old.workspace, cwd: c.primary, focus: false, label: 'Primary committer', env: {FLOW_ID: c.flow, FLOW_DIRECTORY: `${c.primary}/flows/${c.flow}`, CODEX_HOME: c.codexHome, PRIMARY_COMMITTER_RECOVERY_CONFIG: c.recoveryConfig}});
      const a = result.root_pane;
      requireFact(a?.workspace_id === old.workspace, 'replacement workspace mismatch');
      return {pane: a.pane_id, terminal: a.terminal_id, workspace: a.workspace_id};
    },
    resume: async target => {
      // Normal CLI provides its supported shell-initialization and agent-readiness wait.
      const result = JSON.parse(await run(c.herdr, ['--session', c.session, 'agent', 'start', c.name, '--kind', 'codex', '--pane', target.pane, '--executable', c.resumeExecutable, '--timeout', '60000', '--', ...c.resumeArgs], 75000));
      requireFact(!result.error && result.result?.agent, 'agent.start refused or returned no ready agent');
      return result.result.agent;
    },
    deregister: async old => {
      const output = await run(c.messenger, ['deregister', c.flow, '--session', c.session, '--pane-id', old.pane, '--terminal-id', old.terminal, '--name', c.name]);
      requireFact(output.trim() === `Deregistered stale ${c.flow}: ${c.name} (${c.session}/${old.pane}/${old.terminal})`, 'deregister outcome unqualified');
    },
    register: async () => {
      const output = await run(c.messenger, ['register', c.flow, c.name, '--session', c.session, '--native-thread', c.uuid]);
      requireFact(output.trim() === `Registered ${c.flow}: ${c.name} (${c.session})`, 'registration outcome unqualified');
    },
  };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  let stream;
  try {
    const [mode, configFile, ...resume] = process.argv.slice(2);
    requireFact(['--watch', '--guard'].includes(mode) && configFile, 'usage: restart.mjs --watch|--guard config.json');
    const config = JSON.parse(fs.readFileSync(configFile, 'utf8'));
    config.recoveryConfig = fs.realpathSync(configFile);
    validateConfig(config);
    const io = adapter(config);
    if (mode === '--guard') {
      requireFact(resume[0] === '--' && JSON.stringify(resume.slice(1)) === JSON.stringify(config.resumeArgs), 'resume argv differs from declared cohort');
      await io.guard();
    }
    else {
      const restarter = new Restarter(config, io);
      let events = []; let active = false;
      const fail = error => { restarter.cancel(error); console.error(JSON.stringify({status: 'blocked', error: error.message})); stream?.destroy(); process.exitCode = 1; };
      stream = await subscribe(config.socket, event => {
        if (!active) events.push(event);
        else restarter.event(event).catch(fail);
      }, fail);
      await restarter.start(); // Subscribe first so no death is missed between qualification and watch.
      active = true;
      for (const event of events) await restarter.event(event);
      events = [];
      const stop = () => { restarter.cancel(new Error('service stopped')); stream.destroy(); process.exitCode = 0; };
      process.once('SIGTERM', stop); process.once('SIGINT', stop);
    }
  } catch (error) {
    stream?.destroy(); console.error(JSON.stringify({status: 'blocked', error: error.message})); process.exitCode = 1;
  }
}
