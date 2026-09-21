#!/usr/bin/env node
/* Periodic Field observation and bounded HM summaries. No wake or lifecycle action. */
import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {collect} from './field-census.mjs';

const stateDir = process.env.FIELD_CENSUS_STATE || path.join(os.homedir(), '.local/state/field-census');
const configFile = process.env.FIELD_CENSUS_CONFIG || path.join(os.homedir(), '.config/field-census/recipients.json');
const dryRun = process.argv.includes('--dry-run');
const observeOnly = process.argv.includes('--observe-only');
const now = () => new Date().toISOString();

function atomic(file, value) {
  fs.mkdirSync(path.dirname(file), {recursive:true, mode:0o700});
  const tmp = `${file}.${process.pid}.tmp`;
  fs.writeFileSync(tmp, `${JSON.stringify(value)}\n`, {mode:0o600});
  fs.renameSync(tmp, file);
}
function read(file, fallback) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch (error) { if (error.code === 'ENOENT') return fallback; throw error; }
}
function config(file) {
  const value = read(file, null);
  if (!value || !/^[a-f0-9]{6}$/.test(value.sender_flow_id) ||
      !/^[a-f0-9]{6}$/.test(value.field_low_flow_id) ||
      !/^[a-f0-9]{6}$/.test(value.field_ultra_flow_id) ||
      !Number.isInteger(value.notify_seconds) || value.notify_seconds < 300) {
    throw new Error('census recipients config requires exact sender/low/ultra Flow IDs and notify_seconds >= 300');
  }
  return value;
}
export function due(state, time, seconds) {
  if (state?.hold) return false;
  if (!state?.last_completed_at) return true;
  return time - Date.parse(state.last_completed_at) >= seconds * 1000;
}
function message(snapshot, file) {
  const c = snapshot.counts;
  return `Field census ${snapshot.observed_at}: ${snapshot.complete ? 'complete' : 'partial'}; ${c.panes} panes, ${c.agents} named agents, ${c.exact_flows} exact HM bindings, ${c.stale_registrations} stale registrations, ${c.unbound_panes} unbound panes. Full source/status/health JSON: ${file}. These are observations, not ready-main or closure claims. No wake or lifecycle action was taken.`;
}

export async function runCycle({
  collectSnapshot = collect,
  submit = (flow, text, sender) => execFileSync('hm-send', [flow, text], {
    env:{...process.env, FLOW_ID:sender}, encoding:'utf8', timeout:15_000, maxBuffer:8192,
  }),
  stateDirectory = stateDir,
  configPath = configFile,
  passive = observeOnly,
  preview = dryRun,
} = {}) {
  fs.mkdirSync(stateDirectory, {recursive:true, mode:0o700});
  const lock = path.join(stateDirectory, 'cycle.lock');
  let fd;
  try { fd = fs.openSync(lock, 'wx', 0o600); fs.writeSync(fd, `${process.pid} ${now()}\n`); }
  catch (error) { if (error.code === 'EEXIST') { console.log(JSON.stringify({status:'held-overlapping-or-stale-lock',lock})); return; } throw error; }
  try {
    const snapshot = await collectSnapshot();
    const latest = path.join(stateDirectory, 'latest.json');
    if (!preview) atomic(latest, snapshot);
    if (passive) {
      console.log(JSON.stringify({status:'observed-only',snapshot:latest,counts:snapshot.counts,
        complete:snapshot.complete,notification_due:false}));
      return;
    }
    const settings = config(configPath);
    const stateFile = path.join(stateDirectory, 'notification-state.json');
    const state = read(stateFile, {});
    const planned = due(state, Date.now(), settings.notify_seconds);
    if (preview || !planned) {
      console.log(JSON.stringify({status:preview?'dry-run':'observed',snapshot:latest,counts:snapshot.counts,complete:snapshot.complete,notification_due:planned}));
      return;
    }
    const recipients = [settings.field_low_flow_id, settings.field_ultra_flow_id];
    if (new Set(recipients).size !== recipients.length) throw new Error('low and ultra recipients must be distinct');
    const text = message(snapshot, latest);
    const attempt = {at:now(), recipients, status:'attempting', snapshot_at:snapshot.observed_at};
    atomic(stateFile, {...state, hold:attempt});
    const submitted = [];
    for (const flow of recipients) {
      try {
        const output = submit(flow, text, settings.sender_flow_id);
        if (!output.includes(`Submitted to ${flow} via Herdr (not a read receipt)`)) throw new Error('HM returned unexpected submission result');
        submitted.push({flow, state:'submitted-not-read'});
        atomic(stateFile, {...state, hold:{...attempt, submitted}});
      } catch (error) {
        const hold = {...attempt, status:'uncertain', submitted, failed_flow:flow, error:String(error.message || error).slice(0, 500)};
        atomic(stateFile, {...state, hold});
        console.log(JSON.stringify({status:'delivery-uncertain',snapshot:latest,hold}));
        process.exitCode = 3;
        return;
      }
    }
    atomic(stateFile, {last_completed_at:now(), last_snapshot_at:snapshot.observed_at, last_submitted:submitted});
    console.log(JSON.stringify({status:'submitted-not-read',snapshot:latest,counts:snapshot.counts,recipients}));
  } finally { fs.closeSync(fd); fs.unlinkSync(lock); }
}

if (process.argv[1] && path.resolve(process.argv[1]) === new URL(import.meta.url).pathname) {
  runCycle().catch(error => { console.error(error.stack || error); process.exitCode = 1; });
}
