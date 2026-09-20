#!/usr/bin/env node
/* Read-only Field census. The JSON snapshot is evidence, never a lifecycle decision. */
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const exec = promisify(execFile);
const session = process.env.FIELD_HERDR_SESSION || 'messaging-build';
const registry = process.env.HM_REGISTRY || path.join(os.homedir(), '.local/state/hacky-messenger');
const cwd = process.cwd();
const at = () => new Date().toISOString();

async function command(bin, args, timeout = 5000) {
  try {
    const {stdout} = await exec(bin, args, {cwd, timeout, maxBuffer: 4_194_304});
    return {ok: true, value: stdout, observed_at: at()};
  } catch (error) {
    return {ok: false, error: String(error.message || error).slice(0, 500), observed_at: at()};
  }
}

function resultArray(raw, key) {
  if (!raw.ok) return [];
  try {
    const value = JSON.parse(raw.value);
    const rows = value.result?.[key] ?? value[key];
    if (!Array.isArray(rows)) throw new Error(`missing ${key}`);
    return rows;
  } catch (error) {
    raw.ok = false;
    raw.error = `invalid Herdr ${key}: ${error.message}`;
    return [];
  }
}

function registrations(dir = registry) {
  const rows = [], errors = [];
  try {
    for (const name of fs.readdirSync(dir).filter(x => x.endsWith('.json')).sort()) {
      try {
        const record = JSON.parse(fs.readFileSync(path.join(dir, name), 'utf8'));
        if (!['session', 'name', 'pane_id', 'terminal_id', 'agent'].every(k => typeof record[k] === 'string' && record[k])) {
          throw new Error('missing binding field');
        }
        rows.push({flow_id: name.slice(0, -5), ...record, native_thread: record.native_thread || null});
      } catch (error) { errors.push({file: name, error: String(error.message || error)}); }
    }
  } catch (error) { errors.push({directory: dir, error: String(error.message || error)}); }
  return {rows, errors, observed_at: at()};
}

function transcriptIndex() {
  const index = new Map();
  const root = path.join(os.homedir(), '.codex/sessions');
  try {
    for (const year of fs.readdirSync(root)) for (const month of fs.readdirSync(path.join(root, year)))
      for (const day of fs.readdirSync(path.join(root, year, month))) {
        const directory = path.join(root, year, month, day);
        for (const name of fs.readdirSync(directory)) {
          const match = name.match(/([0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12})\.jsonl$/);
          if (match) index.set(match[1], path.join(directory, name));
        }
      }
  } catch { /* Missing history is represented by a null transcript path. */ }
  return index;
}

function transcript(record, codexIndex) {
  if (!record?.native_thread) return null;
  const file = record.agent === 'claude'
    ? path.join(os.homedir(), '.claude/projects/-home-li-primary', `${record.native_thread}.jsonl`)
    : codexIndex.get(record.native_thread);
  return file && fs.existsSync(file) ? file : null;
}

function locksByFlow(raw) {
  const map = new Map();
  if (!raw.ok || !raw.value.startsWith('Observed.Locks.[')) return map;
  for (const match of raw.value.matchAll(/\{\s+(\d+)\s+(\S+)\s+([A-Za-z0-9_-]+)\s+\[/g)) {
    const rows = map.get(match[3]) ?? [];
    rows.push({id: Number(match[1]), name: match[2]});
    map.set(match[3], rows);
  }
  return map;
}

function metrics(screen) {
  const context = [...screen.matchAll(/Context\s+(\d+)%\s+used/g)].at(-1);
  const quota = [...screen.matchAll(/weekly\s+(\d+)%\s+left/gi)].at(-1);
  const statusLine = screen.split('\n').reverse().find(line => /Context\s+\d+%\s+used/.test(line) || /primary main@/.test(line)) ?? '';
  const codex = statusLine.match(/\b(gpt-[\w.-]+)\s+(low|medium|high|xhigh|ultra)\b/i);
  const claude = statusLine.match(/\b(Fable|Opus|Sonnet|Haiku)\s+([\d.]+)(?:\s*\([^)]*\))?\s*[· ]\s*(low|medium|high|xhigh|ultra)\b/i);
  return {
    context_pct: context ? Number(context[1]) : null, quota_pct: quota ? Number(quota[1]) : null,
    display_model: codex?.[1] ?? (claude ? `${claude[1]} ${claude[2]}` : null),
    display_effort: codex?.[2] ?? claude?.[3] ?? null,
    model_evidence: codex || claude ? 'terminal-status' : 'unavailable',
  };
}

async function screens(agents, limit = 6) {
  const result = new Map(); let next = 0;
  await Promise.all(Array.from({length: Math.min(limit, agents.length)}, async () => {
    while (next < agents.length) {
      const agent = agents[next++];
      result.set(agent.name, await command('herdr', ['--session', session, 'agent', 'read', agent.name, '--lines', '16', '--format', 'text'], 3500));
    }
  }));
  return result;
}

function hostHealth(daemon) {
  const memory = Object.fromEntries(fs.readFileSync('/proc/meminfo', 'utf8').split('\n').map(line => line.match(/^(\w+):\s+(\d+)/)).filter(Boolean).map(m => [m[1], Number(m[2])]));
  const disk = fs.statfsSync('/');
  const daemonFields = daemon.ok ? Object.fromEntries(daemon.value.trim().split('\n').map(line => line.split('=', 2))) : {};
  return {
    ram_available_gb: +(memory.MemAvailable / 1_048_576).toFixed(2),
    disk_avail_gb: +(disk.bavail * disk.bsize / 2 ** 30).toFixed(2),
    disk_pct: Math.ceil(100 * (disk.blocks - disk.bfree) / (disk.blocks - disk.bfree + disk.bavail)),
    uptime_days: +(os.uptime() / 86400).toFixed(2),
    load_1m: +os.loadavg()[0].toFixed(2),
    nix_daemon_status: daemon.ok ? `${daemonFields.ActiveState || 'unknown'}/${daemonFields.SubState || 'unknown'}` : 'unavailable',
    nix_daemon_pid: daemonFields.MainPID ? Number(daemonFields.MainPID) : null,
    process_count: fs.readdirSync('/proc').filter(x => /^\d+$/.test(x)).length,
  };
}

export function joinCensus({agents, panes, bindings, screens: screenMap, locks, codexIndex}) {
  const byTerminal = new Map(agents.map(a => [a.terminal_id, a]));
  const byBinding = new Map();
  for (const binding of bindings) {
    const key = `${binding.session}\0${binding.pane_id}\0${binding.terminal_id}\0${binding.name}\0${binding.agent}`;
    const rows = byBinding.get(key) ?? []; rows.push(binding); byBinding.set(key, rows);
  }
  const matched = new Set();
  const rows = panes.map(pane => {
    const agent = byTerminal.get(pane.terminal_id);
    const key = agent && `${session}\0${agent.pane_id}\0${agent.terminal_id}\0${agent.name}\0${agent.agent}`;
    const candidates = key ? byBinding.get(key) ?? [] : [];
    const binding = candidates.length === 1 ? candidates[0] : null;
    if (binding) matched.add(binding.flow_id);
    const screen = agent ? screenMap.get(agent.name) : null;
    const file = transcript(binding, codexIndex);
    const ownedLocks = binding ? locks.get(binding.flow_id) ?? [] : [];
    return {
      flow_id: binding?.flow_id ?? null,
      binding_state: candidates.length > 1 ? 'ambiguous' : binding ? 'exact' : 'unbound',
      provenance_gap: Boolean(binding && !binding.native_thread),
      native_thread: binding?.native_thread ?? null,
      herdr_session: session,
      workspace_id: agent?.workspace_id ?? pane.workspace_id ?? null,
      agent_name: agent?.name ?? null,
      harness: agent?.agent ?? pane.agent ?? null,
      status: agent?.agent_status ?? pane.agent_status ?? 'unknown',
      pane_id: pane.pane_id,
      terminal_id: pane.terminal_id,
      interactive_ready: agent?.interactive_ready ?? null,
      ...metrics(screen?.ok ? screen.value : ''),
      transcript_path: file,
      last_activity: file ? fs.statSync(file).mtime.toISOString() : null,
      lock_count: ownedLocks.length,
      locks: ownedLocks,
      screen_error: screen && !screen.ok ? screen.error : null,
    };
  });
  for (const binding of bindings.filter(b => !matched.has(b.flow_id))) rows.push({
    flow_id: binding.flow_id, binding_state: 'stale', agent_name: binding.name,
    provenance_gap: !binding.native_thread,
    native_thread: binding.native_thread, herdr_session: binding.session, workspace_id: null,
    harness: binding.agent, status: 'unreachable', pane_id: binding.pane_id,
    terminal_id: binding.terminal_id, interactive_ready: false,
    context_pct: null, quota_pct: null,
    display_model: null, display_effort: null, model_evidence: 'unavailable',
    transcript_path: transcript(binding, codexIndex), last_activity: null,
    lock_count: (locks.get(binding.flow_id) ?? []).length,
    locks: locks.get(binding.flow_id) ?? [], screen_error: null,
  });
  return rows;
}

export async function collect() {
  const started = Date.now();
  const [agentRaw, paneRaw, lockRaw, daemonRaw] = await Promise.all([
    command('herdr', ['--session', session, 'agent', 'list']),
    command('herdr', ['--session', session, 'pane', 'list']),
    command('orchestrate', ['Observe.Locks']),
    command('systemctl', ['show', 'nix-daemon', '--property=ActiveState,SubState,MainPID', '--no-pager']),
  ]);
  const agents = resultArray(agentRaw, 'agents');
  const panes = resultArray(paneRaw, 'panes');
  const binding = registrations();
  const screenMap = await screens(agents.filter(a => a.name));
  const locks = locksByFlow(lockRaw);
  const rows = joinCensus({agents, panes, bindings: binding.rows, screens: screenMap, locks, codexIndex: transcriptIndex()});
  const source = (raw, valid = true) => ({status: raw.ok && valid ? 'ok' : 'unavailable', observed_at: raw.observed_at, error: raw.ok && valid ? null : raw.error ?? 'unexpected response'});
  const screenFailures = [...screenMap.values()].filter(x => !x.ok).length;
  const sources = {
    herdr_agents: source(agentRaw), herdr_panes: source(paneRaw),
    hm_registry: {status: binding.errors.length ? 'partial' : 'ok', observed_at: binding.observed_at, errors: binding.errors},
    herdr_screens: {status: screenFailures ? 'partial' : 'ok', observed_at: at(), failed: screenFailures, total: screenMap.size},
    orchestrate_locks: source(lockRaw, lockRaw.value?.startsWith('Observed.Locks.[')),
    host: {status: 'ok', observed_at: at()}, nix_daemon: source(daemonRaw),
  };
  return {
    version: 1, observed_at: at(), duration_ms: Date.now() - started, session,
    complete: ['herdr_agents', 'herdr_panes', 'hm_registry', 'herdr_screens', 'orchestrate_locks', 'host', 'nix_daemon'].every(key => sources[key].status === 'ok'),
    sources,
    counts: {panes: panes.length, agents: agents.length, exact_flows: rows.filter(r => r.binding_state === 'exact').length, stale_registrations: rows.filter(r => r.binding_state === 'stale').length, unbound_panes: rows.filter(r => r.binding_state === 'unbound').length},
    rows, health: hostHealth(daemonRaw),
  };
}

if (process.argv[1] && path.resolve(process.argv[1]) === new URL(import.meta.url).pathname) {
  collect().then(snapshot => { process.stdout.write(`${JSON.stringify(snapshot)}\n`); if (!snapshot.complete) process.exitCode = 2; })
    .catch(error => { process.stderr.write(`${error.stack || error}\n`); process.exitCode = 1; });
}
