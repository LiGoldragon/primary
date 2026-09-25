#!/usr/bin/env node
import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, renameSync, writeFileSync, existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import path from 'node:path';

const root = '/home/li/primary';
const own = path.join(root, 'flows/98eb43/monitor');
const stateDirectory = '/home/li/.local/state/field-monitor-98eb43';
const table = path.join(stateDirectory, 'status.edn');
const alertState = path.join(stateDirectory, 'alert-state.json');
const herdr = '/home/li/.nix-profile/bin/herdr';
const hmList = '/home/li/.local/bin/hm-list';
const hmSend = '/home/li/.local/bin/hm-send';
const jj = '/home/li/.nix-profile/bin/jj';
const session = 'messaging-build';
mkdirSync(own, { recursive: true });
mkdirSync(stateDirectory, { recursive: true });

function run(command, args, options = {}) {
  const result = spawnSync(command, args, { cwd: root, encoding: 'utf8', timeout: 10_000, maxBuffer: 256 * 1024, ...options });
  return { ok: result.status === 0 && !result.error, stdout: result.stdout ?? '', stderr: result.stderr ?? '', status: result.status, error: result.error?.message ?? null };
}
function hash(value) { return createHash('sha256').update(value).digest('hex'); }
function ednString(value) { return JSON.stringify(String(value)); }
function edn(value) {
  if (value === null) return 'nil';
  if (value === true || value === false) return String(value);
  if (Array.isArray(value)) return `[${value.map(edn).join(' ')}]`;
  if (typeof value === 'object') return `{${Object.entries(value).map(([key, item]) => `:${key} ${edn(item)}`).join(' ')}}`;
  return ednString(value);
}
function atomically(file, body) {
  const temp = `${file}.${process.pid}.tmp`;
  writeFileSync(temp, body);
  renameSync(temp, file);
}
function parseHm(value) {
  return value.split('\n').slice(1).map(line => line.trim().split(/\s+/)).filter(parts => parts.length >= 4).map(([flow, agent, hmSession, state]) => ({ flow, agent, session: hmSession, state }));
}
function recentCommit(flow) {
  if (!/^[a-f0-9]{6,}$/.test(flow) || !existsSync(path.join(root, 'flows', flow))) return 'unknown';
  const result = run(jj, ['log', '-r', '@', '--no-graph', '-T', 'change_id.short() ++ " " ++ description.first_line() ++ "\\n"', '--', `flows/${flow}`]);
  return result.ok && result.stdout.trim() ? result.stdout.trim().split('\n')[0] : 'unknown';
}

const observedAt = new Date().toISOString();
const herdrResult = run(herdr, ['--session', session, 'agent', 'list']);
let agents = [];
let herdrUnknown = null;
try { agents = JSON.parse(herdrResult.stdout).result?.agents ?? []; } catch { herdrUnknown = 'agent-list-unparseable'; }
if (!herdrResult.ok) herdrUnknown = `agent-list-failed:${herdrResult.status ?? 'unknown'}`;
const hmResult = run(hmList, []);
const hmRows = hmResult.ok ? parseHm(hmResult.stdout) : [];
const hmUnknown = hmResult.ok ? null : `hm-list-failed:${hmResult.status ?? 'unknown'}`;

const rows = agents.map(agent => {
  const tail = run(herdr, ['--session', session, 'agent', 'read', agent.name, '--source', 'recent', '--lines', '24', '--format', 'text']);
  const route = hmRows.find(row => row.agent === agent.name) ?? null;
  return {
    who: route?.flow && route.flow !== '-' ? route.flow : agent.name,
    doing: 'unknown',
    last_finished: agent.agent_status === 'done' ? 'observed-done; details-unknown' : 'unknown',
    blockers: agent.interactive_ready === false ? 'interactive-readiness-false' : 'unknown',
    observed_time: observedAt,
    provenance: `herdr:${session}:${agent.pane_id}; hm-list:${route?.flow ?? 'unregistered'}; pane-tail:24-lines-sha256:${hash(tail.stdout)}`,
    unknowns: `task-content, order-holder-status, blocker-cause; pane-tail-read:${tail.ok ? 'bounded-not-persisted' : 'failed'}`,
    flow: route?.flow ?? '-',
    agent: agent.name,
    pane: agent.pane_id,
    status: agent.agent_status ?? 'unknown',
    recent_commit: route?.flow ? recentCommit(route.flow) : 'unknown'
  };
});

const observedAlerts = hmRows.filter(row => row.state === 'STALE' && row.flow !== '-').map(row => `dead-pane:${row.flow}`).sort();
let previous = null;
try { previous = JSON.parse(readFileSync(alertState, 'utf8')); } catch { /* First census establishes the baseline. */ }
const previousAlerts = new Set(previous?.observedAlerts ?? []);
const newAlerts = previous ? observedAlerts.filter(item => !previousAlerts.has(item)) : [];
const deliveries = [];
if (newAlerts.length) {
  const body = `Field Monitor 98eb43 changed census: ${newAlerts.join(', ')}; observed ${observedAt}; provenance hm-list/herdr; task/blocker cause unknown.`;
  for (const recipient of ['e51411', '38de5b']) {
    const result = run(hmSend, [recipient, body, '--hold-seconds', '0'], { env: { ...process.env, FLOW_ID: '98eb43' } });
    deliveries.push({ recipient, status: result.ok ? 'transport-submitted' : 'unknown-or-held', result: (result.stdout || result.stderr).trim().slice(0, 240) });
  }
}
atomically(alertState, JSON.stringify({ observedAt, observedAlerts }, null, 2) + '\n');
atomically(table, edn({
  monitor: '98eb43', observed_time: observedAt, provenance: `herdr-agent-list:${session}; hm-list; bounded-pane-tails:24; jj-per-flow`,
  unknowns: [herdrUnknown, hmUnknown, 'no-transcript-content-persisted', 'no-secret-inspection'].filter(Boolean),
  rows, alert_baseline_or_changes: newAlerts, alert_delivery: deliveries
}) + '\n');
console.log(JSON.stringify({ table, observedAt, agents: rows.length, hmRows: hmRows.length, newAlerts, deliveries }));
