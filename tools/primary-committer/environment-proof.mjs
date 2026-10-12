#!/usr/bin/env node
// Only the private native fixture installs this SessionStart command hook.
import fs from 'node:fs';
import path from 'node:path';
import {spawnSync} from 'node:child_process';

const output = process.argv[2];
if (!path.isAbsolute(output ?? '')) throw new Error('absolute private proof output required');
const event = JSON.parse(fs.readFileSync(0, 'utf8'));
if (event.hook_event_name !== 'SessionStart' || typeof event.session_id !== 'string') throw new Error('actual native SessionStart required');
const flow = process.env.FLOW_ID;
if (!/^[a-f0-9]{6,64}$/.test(flow ?? '')) throw new Error('process did not inherit FLOW_ID');
const child = spawnSync(process.execPath, ['-e', 'process.stdout.write(process.env.FLOW_ID ?? "")'], {encoding: 'utf8'});
if (child.status !== 0 || child.stdout !== flow) throw new Error('hook child did not inherit the same FLOW_ID');
fs.writeFileSync(output, `${JSON.stringify({hook_event_name: event.hook_event_name, native_session_id: event.session_id, flow_id: flow, child_flow_id: child.stdout, child_exit: child.status})}\n`, {flag: 'wx', mode: 0o600});
