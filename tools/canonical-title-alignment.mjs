#!/usr/bin/env node
// Align one exact Flow binding at a time. Dry-run is the default.
import { execFile as execFileCallback } from 'node:child_process';
import { readFile } from 'node:fs/promises';
import { promisify } from 'node:util';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { readCodexThreadMetadata, setCodexThreadName } from './field-census/codex-context.mjs';

const execFile = promisify(execFileCallback);
const here = path.dirname(fileURLToPath(import.meta.url));
const FLOW = /^[0-9a-f]{6}$/;
const UUID = /^[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}$/i;
const registryRoot = process.env.HM_REGISTRY || path.join(os.homedir(), '.local/state/hacky-messenger');

async function command(binary, args) {
  const { stdout } = await execFile(binary, args, { timeout: 4000, maxBuffer: 1024 * 1024 });
  return stdout.trim();
}
async function herdr(session, kind, action, ...args) {
  const raw = await command('herdr', ['--session', session, kind, action, ...args]);
  const envelope = JSON.parse(raw);
  if (envelope.error) throw new Error(`Herdr ${kind}/${action}: ${envelope.error.code}`);
  return envelope.result?.[kind] ?? envelope.result;
}
async function registration(flow) {
  if (!FLOW.test(flow)) throw new Error('Flow must be an exact six-character ID');
  const record = JSON.parse(await readFile(path.join(registryRoot, `${flow}.json`), 'utf8'));
  const fields = ['session', 'pane_id', 'terminal_id', 'name', 'agent', 'native_thread'];
  if (fields.some(key => typeof record[key] !== 'string' || !record[key]) || !UUID.test(record.native_thread)) {
    throw new Error('Registration lacks an exact native and route identity');
  }
  if (!['codex', 'claude'].includes(record.agent)) throw new Error('Unsupported harness');
  return record;
}
function sameRoute(a, b, { name = true } = {}) {
  return ['session', 'pane_id', 'terminal_id', 'agent', 'native_thread', ...(name ? ['name'] : [])]
    .every(key => a[key] === b[key]);
}
async function live(flow, expected = null) {
  const hm = await registration(flow);
  if (expected && !sameRoute(hm, expected)) throw new Error('HM registration changed');
  const agent = await herdr(hm.session, 'agent', 'get', hm.pane_id);
  const pane = await herdr(hm.session, 'pane', 'get', hm.pane_id);
  const tab = await herdr(hm.session, 'tab', 'get', pane.tab_id);
  for (const item of [agent, pane]) {
    if (item.pane_id !== hm.pane_id || item.terminal_id !== hm.terminal_id || item.agent !== hm.agent) {
      throw new Error('Herdr native route differs from HM registration');
    }
  }
  if (agent.name !== hm.name || pane.tab_id !== agent.tab_id || tab.tab_id !== pane.tab_id) {
    throw new Error('Herdr name or tab identity differs');
  }
  let native = null;
  if (hm.agent === 'codex') {
    native = await readCodexThreadMetadata(hm.native_thread);
    if (native?.id !== hm.native_thread || !native.path?.endsWith(`-${hm.native_thread}.jsonl`)) {
      throw new Error('Codex native thread identity mismatch');
    }
  }
  return { flow, hm, agent, pane, tab, native };
}

export function desired(flow, role) {
  if (!FLOW.test(flow)) throw new Error('Flow must be an exact six-character ID');
  if (role?.flow_id !== flow || !['Psyche', 'Mind', 'Field'].includes(role?.aspect) ||
      !['High', 'Medium', 'Low', 'Ultra Low'].includes(role?.power)) {
    throw new Error('Explicit canonical aspect, power, and matching seat Flow ID required');
  }
  return { title: `${role.aspect} ${role.power} ${flow}`, agentName: `flow-${flow}`, paneLabel: flow };
}
export function plan(snapshot, role) {
  if (role?.native_thread !== snapshot.hm.native_thread || role?.harness !== snapshot.hm.agent) {
    throw new Error('Role metadata does not match native thread and harness');
  }
  const target = desired(snapshot.flow, role);
  return {
    flow: snapshot.flow, harness: snapshot.hm.agent, nativeThreadId: snapshot.hm.native_thread,
    route: { session: snapshot.hm.session, paneId: snapshot.hm.pane_id,
      terminalId: snapshot.hm.terminal_id, tabId: snapshot.tab.tab_id,
      tabPaneCount: snapshot.tab.pane_count },
    before: { title: snapshot.native?.name ?? null, agentName: snapshot.agent.name,
      paneLabel: snapshot.pane.label ?? null, tabLabel: snapshot.tab.label ?? null },
    desired: target,
    operations: {
      codexTitle: snapshot.hm.agent === 'codex' && snapshot.native.name !== target.title,
      claudeTitle: snapshot.hm.agent === 'claude' ? 'pending-supported-interactive-rename' : null,
      agentName: snapshot.agent.name !== target.agentName,
      paneLabel: (snapshot.pane.label ?? null) !== target.paneLabel,
      hmRebind: snapshot.hm.name !== target.agentName,
      tabLabel: 'unchanged',
    },
  };
}

async function rebind(flow, oldName, newName, hm) {
  return command(path.join(here, 'hm-rebind'), [flow, newName, '--old-name', oldName,
    '--session', hm.session, '--pane-id', hm.pane_id, '--terminal-id', hm.terminal_id,
    '--agent', hm.agent, '--native-thread', hm.native_thread]);
}
async function verifyNative(s, operations) {
  if (s.hm.agent !== 'codex') return;
  const now = await operations.readCodexThreadMetadata(s.hm.native_thread);
  if (now?.id !== s.hm.native_thread || now.path !== s.native.path || now.name !== s.native.name) {
    throw new Error('Native thread changed before operation');
  }
}
async function assertBinding(s, name, label, operations) {
  const hm = await operations.registration(s.flow);
  if (!sameRoute(hm, { ...s.hm, name })) throw new Error('HM binding changed during alignment');
  const agent = await operations.herdr(s.hm.session, 'agent', 'get', s.hm.pane_id);
  const pane = await operations.herdr(s.hm.session, 'pane', 'get', s.hm.pane_id);
  if (agent.name !== name || agent.pane_id !== s.hm.pane_id || agent.terminal_id !== s.hm.terminal_id || agent.agent !== s.hm.agent ||
      pane.pane_id !== s.hm.pane_id || pane.terminal_id !== s.hm.terminal_id || pane.agent !== s.hm.agent ||
      (pane.label ?? null) !== label || pane.tab_id !== s.tab.tab_id) {
    throw new Error('Live route changed during alignment');
  }
}

export async function alignFlow(flow, { apply = false, titleOnly = false, role, io = null } = {}) {
  const operations = io ?? { live, registration, herdr, readCodexThreadMetadata, setCodexThreadName, rebind };
  const start = await operations.live(flow);
  const proposed = plan(start, role);
  if (titleOnly) {
    proposed.operations.agentName = false;
    proposed.operations.paneLabel = false;
    proposed.operations.hmRebind = false;
  }
  if (apply && start.hm.agent === 'claude') throw new Error('Claude apply requires a supported native rename and readback adapter');
  const receipt = { ...proposed, mode: apply ? (titleOnly ? 'apply-title-only' : 'apply') : 'dry-run',
    observedAt: new Date().toISOString(), steps: [], outcome: apply ? 'pending' : 'planned' };
  if (!apply) return receipt;
  const target = desired(flow, role);
  let currentName = start.hm.name;
  let currentLabel = start.pane.label ?? null;
  let currentTitle = start.native?.name ?? null;
  let agentRenamed = false;
  let paneRenamed = false;
  let hmRebound = false;
  let titleRenamed = false;
  try {
    await assertBinding(start, currentName, currentLabel, operations);
    await verifyNative(start, operations);
    if (proposed.operations.codexTitle) {
      titleRenamed = true;
      await operations.setCodexThreadName(start.hm.native_thread, target.title);
      currentTitle = (await operations.readCodexThreadMetadata(start.hm.native_thread))?.name;
      if (currentTitle !== target.title) throw new Error('Codex title readback mismatch');
      receipt.steps.push('codex-title');
    }
    if (proposed.operations.agentName) {
      await assertBinding(start, currentName, currentLabel, operations);
      agentRenamed = true;
      await operations.herdr(start.hm.session, 'agent', 'rename', start.hm.pane_id, target.agentName);
      const updated = await operations.herdr(start.hm.session, 'agent', 'get', start.hm.pane_id);
      if (updated.name !== target.agentName || updated.terminal_id !== start.hm.terminal_id) throw new Error('Agent name readback mismatch');
      receipt.steps.push('herdr-agent');
    }
    if (proposed.operations.paneLabel) {
      const before = await operations.herdr(start.hm.session, 'pane', 'get', start.hm.pane_id);
      if (before.terminal_id !== start.hm.terminal_id || (before.label ?? null) !== currentLabel) throw new Error('Pane changed before rename');
      paneRenamed = true;
      await operations.herdr(start.hm.session, 'pane', 'rename', start.hm.pane_id, target.paneLabel);
      currentLabel = (await operations.herdr(start.hm.session, 'pane', 'get', start.hm.pane_id)).label ?? null;
      if (currentLabel !== target.paneLabel) throw new Error('Pane label readback mismatch');
      receipt.steps.push('herdr-pane');
    }
    if (proposed.operations.hmRebind) {
      const before = await operations.registration(flow);
      if (!sameRoute(before, start.hm)) throw new Error('HM changed before rebind');
      hmRebound = true;
      await operations.rebind(flow, start.hm.name, target.agentName, start.hm);
      currentName = (await operations.registration(flow)).name;
      if (currentName !== target.agentName) throw new Error('HM rebind readback mismatch');
      receipt.steps.push('hm-rebind');
    }
    await assertBinding(start, titleOnly ? start.hm.name : target.agentName,
      titleOnly ? start.pane.label ?? null : target.paneLabel, operations);
    if (start.hm.agent === 'codex' && (await operations.readCodexThreadMetadata(start.hm.native_thread))?.name !== target.title) {
      throw new Error('Final Codex title mismatch');
    }
    receipt.outcome = 'verified';
  } catch (error) {
    receipt.outcome = 'failed'; receipt.error = String(error.message || error);
    receipt.rollback = [];
    // Roll back in reverse order, with exact same-target guards at every step.
    try {
      if (hmRebound) {
        const now = await operations.registration(flow);
        if (!sameRoute(now, { ...start.hm, name: target.agentName }) && !sameRoute(now, start.hm)) throw new Error('HM rollback guard failed');
        if (now.name === target.agentName) {
          await operations.rebind(flow, target.agentName, start.hm.name, start.hm);
          if (!sameRoute(await operations.registration(flow), start.hm)) throw new Error('HM rollback readback mismatch');
          receipt.rollback.push('hm-rebind');
        }
      }
      if (paneRenamed) {
        const now = await operations.herdr(start.hm.session, 'pane', 'get', start.hm.pane_id);
        if (now.pane_id !== start.hm.pane_id || now.terminal_id !== start.hm.terminal_id || now.agent !== start.hm.agent || now.tab_id !== start.tab.tab_id ||
            ![target.paneLabel, start.pane.label ?? null].includes(now.label ?? null)) throw new Error('Pane rollback guard failed');
        if ((now.label ?? null) === target.paneLabel) {
          await operations.herdr(start.hm.session, 'pane', 'rename', start.hm.pane_id, ...(start.pane.label ? [start.pane.label] : ['--clear']));
          if (((await operations.herdr(start.hm.session, 'pane', 'get', start.hm.pane_id)).label ?? null) !== (start.pane.label ?? null)) throw new Error('Pane rollback readback mismatch');
          receipt.rollback.push('herdr-pane');
        }
      }
      if (agentRenamed) {
        const now = await operations.herdr(start.hm.session, 'agent', 'get', start.hm.pane_id);
        if (now.pane_id !== start.hm.pane_id || now.terminal_id !== start.hm.terminal_id || now.agent !== start.hm.agent || now.tab_id !== start.tab.tab_id ||
            ![target.agentName, start.agent.name].includes(now.name)) throw new Error('Agent rollback guard failed');
        if (now.name === target.agentName) {
          await operations.herdr(start.hm.session, 'agent', 'rename', start.hm.pane_id, start.agent.name);
          if ((await operations.herdr(start.hm.session, 'agent', 'get', start.hm.pane_id)).name !== start.agent.name) throw new Error('Agent rollback readback mismatch');
          receipt.rollback.push('herdr-agent');
        }
      }
      if (titleRenamed) {
        const now = await operations.readCodexThreadMetadata(start.hm.native_thread);
        if (now?.id !== start.hm.native_thread || now.path !== start.native.path || ![target.title, start.native.name].includes(now.name)) throw new Error('Title rollback guard failed');
        if (now.name === target.title) {
          await operations.setCodexThreadName(start.hm.native_thread, start.native.name);
          if ((await operations.readCodexThreadMetadata(start.hm.native_thread))?.name !== start.native.name) throw new Error('Title rollback readback mismatch');
          receipt.rollback.push('codex-title');
        }
      }
    } catch (rollbackError) {
      receipt.rollbackError = String(rollbackError.message || rollbackError);
    }
  }
  receipt.finishedAt = new Date().toISOString();
  return receipt;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const apply = args.includes('--apply');
  const titleOnly = args.includes('--title-only');
  const roleAt = args.indexOf('--role-file');
  const roleFile = roleAt >= 0 ? args[roleAt + 1] : null;
  const flows = args.filter((arg, i) => arg !== '--apply' && arg !== '--title-only' && i !== roleAt && i !== roleAt + 1);
  if (flows.length !== 1 || !FLOW.test(flows[0]) || !roleFile) {
    console.error('Usage: node tools/canonical-title-alignment.mjs [--apply] [--title-only] --role-file ROLE_JSON FLOW_ID');
    process.exitCode = 2;
  } else {
    const output = [];
    let role;
    try { role = JSON.parse(await readFile(roleFile, 'utf8')); }
    catch (error) { console.error(`Role metadata unavailable: ${error.message}`); process.exit(2); }
    for (const flow of flows) {
      try { output.push(await alignFlow(flow, { apply, titleOnly, role })); }
      catch (error) { output.push({ flow, mode: apply ? 'apply' : 'dry-run', outcome: 'blocked', error: String(error.message || error) }); }
    }
    console.log(JSON.stringify(output, null, 2));
    if (output.some(row => ['failed', 'blocked'].includes(row.outcome))) process.exitCode = 1;
  }
}
