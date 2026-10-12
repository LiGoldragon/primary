import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {execFileSync, spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {selectVoiceProfile} from './native-voice-profiles.mjs';

// Explicit Core declarations for already-running secretary seats. A stale
// record never proves life: require the exact actual native/pane binding.
export const DECLARED_SECONDARIES = Object.freeze([
  {aspect: 'Mind', topic: 'Core', layer: 'Secondary', flowId: '41fa34', name: 'mind_sol_41fa34', nativeId: '01a0fdcc-c1a1-7f43-8c23-06d41fa34438'},
  {aspect: 'Field', topic: 'Core', layer: 'Secondary', flowId: '42265e', name: 'field_sol_42265e', nativeId: '01a0fdcc-4e82-7353-af14-d6c42265e940'}
]);

// Canonical title + actual native binding, never model/name correspondence.
export function liveSeats(response) {
  const agents = response?.result?.agents ?? response?.agents;
  if (!Array.isArray(agents)) throw new Error('Herdr returned no agent vector');
  return agents.flatMap(agent => {
    const title = agent.terminal_title_stripped ?? '';
    const match = /\{ (Psyche|Mind|Field) (?:(\w+) )?(Primary|Secondary|Tertiary|Quaternary) ([0-9a-f]{6,}) \}/.exec(title);
    const declared = DECLARED_SECONDARIES.find(seat => seat.name === agent.name && seat.nativeId === agent.agent_session?.value);
    if ((!match && !declared) || !agent.pane_id || !agent.terminal_id || !agent.agent_session?.value || !['idle', 'working', 'done'].includes(agent.agent_status)) return [];
    if (declared) return [{...declared, pane: agent.pane_id, terminal: agent.terminal_id}];
    return [{aspect: match[1], topic: match[2] ?? 'Core', layer: match[3], flowId: match[4], nativeId: agent.agent_session.value, name: agent.name, pane: agent.pane_id, terminal: agent.terminal_id}];
  });
}
export function missingSecondaries(seats) {
  return seats.filter(seat => seat.layer === 'Primary' && !seats.some(other => other.aspect === seat.aspect && other.topic === seat.topic && other.layer === 'Secondary'));
}
export function ensureSecondary(seat, {observe, start}) {
  if (seat.layer !== 'Primary') return;
  const matching = () => liveSeats(observe()).filter(other => other.aspect === seat.aspect && other.topic === seat.topic && other.layer === 'Secondary');
  let found = matching();
  if (found.length > 1) throw new Error('ambiguous live Secondary bindings; Primary refused');
  if (found.length === 1) return found[0];
  start();
  found = matching();
  if (found.length !== 1) throw new Error('Secondary did not become live; Primary refused');
  return found[0];
}

// Serialize the same aspect/topic's Primary launch from dependency check to
// terminal registration. A held/stale reservation refuses; never steal it.
export function secondaryBeforePrimary(options, continuation) {
  if (options.layer !== 'Primary') return () => {};
  const topic = continuation.topic;
  const runtime = process.env.XDG_RUNTIME_DIR ?? `/run/user/${process.getuid()}`;
  const root = path.join(runtime, 'flow-launch-dependencies');
  fs.mkdirSync(root, {recursive: true, mode: 0o700});
  const reservation = path.join(root, `${options.aspect}-${topic}`);
  fs.mkdirSync(reservation, {mode: 0o700});
  fs.writeFileSync(path.join(reservation, 'owner.json'), JSON.stringify({pid: process.pid, aspect: options.aspect, topic}));
  const release = () => { fs.unlinkSync(path.join(reservation, 'owner.json')); fs.rmdirSync(reservation); };
  try {
    ensureSecondary({...options, topic}, {
      observe: () => JSON.parse(execFileSync('herdr', ['--session', options.herdrSession, 'agent', 'list'], {encoding: 'utf8', timeout: 15000})),
      start: () => {
        // An unqualified Secondary profile is a concrete refusal, never a
        // guessed model or a Primary launch without its secretary.
        const profile = selectVoiceProfile({aspect: options.aspect, layer: 'Secondary'});
        const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'secondary-first-'));
        const brief = path.join(dir, 'brief.md'), metaflow = path.join(dir, 'metaflow.md');
        fs.writeFileSync(brief, `You are the ${options.aspect} ${topic} Secondary. Give only your normal startup presentation. No additional task is assigned.\n`, {mode: 0o600});
        fs.writeFileSync(metaflow, continuation.metaflow, {mode: 0o600});
        const backend = path.join(path.dirname(fileURLToPath(import.meta.url)), `${profile.harness}-main-flow-launch.mjs`);
        const args = [backend, '--aspect', options.aspect, '--layer', 'Secondary', '--brief', brief, '--root', '--metaflow', metaflow, '--topic', topic, '--workspace', options.workspace, '--herdr-session', options.herdrSession];
        if (options.herdrWorkspaceLabel) args.push('--herdr-workspace-label', options.herdrWorkspaceLabel);
        const result = spawnSync(process.execPath, args, {stdio: 'inherit'});
        if (result.error || result.status !== 0) throw new Error('Secondary launch failed; Primary refused');
      }
    });
    return release;
  } catch (error) { release(); throw error; }
}
