#!/usr/bin/env node
/* Persist a passive aspect checkup from the shared Field census snapshot. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {assess} from './field-checkup-shadow.mjs';

const census = process.env.FIELD_CENSUS_STATE || path.join(os.homedir(), '.local/state/field-census');
const roster = process.env.FIELD_CHECKUP_ROSTER || path.join(os.homedir(), '.config/field-checkup-shadow/roster.json');
const state = process.env.FIELD_CHECKUP_STATE || path.join(os.homedir(), '.local/state/field-checkup-shadow');
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
try {
  const result = assess(read(path.join(census, 'latest.json')), read(roster));
  fs.mkdirSync(state, {recursive:true, mode:0o700});
  const target = path.join(state, 'latest.json'), tmp = `${target}.${process.pid}.tmp`;
  fs.writeFileSync(tmp, `${JSON.stringify(result)}\n`, {mode:0o600});
  fs.renameSync(tmp, target);
  console.log(JSON.stringify({kind:result.kind, census_at:result.census_at, census_fresh:result.census_fresh,
    structure:{state:result.structure.structural_state, ...result.structure.findings},
    aspects:Object.fromEntries(Object.entries(result.aspects).map(([name, value]) => [name, {decision:value.decision, coverage:value.coverage}])),
    wake_attempts:result.wake_attempts, lifecycle_actions:result.lifecycle_actions}));
} catch (error) { console.error(error.stack || error); process.exitCode = 1; }
