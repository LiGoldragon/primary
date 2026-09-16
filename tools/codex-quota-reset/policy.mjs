/* The policy file: one datom struct, positional.
   { <UseReset|Hold> <thresholdPercent> <minimumDaysLeft> } */
import fs from 'node:fs';
import * as datom from './datom.mjs';

export function readPolicy(path) {
  let text;
  try {
    text = fs.readFileSync(path, 'utf8');
  } catch {
    throw new Error('policy file is unreadable');
  }
  let value;
  try {
    value = datom.readDatom(text);
  } catch (error) {
    throw new Error(`policy is not datom text: ${error.message}`);
  }
  const body = value.head === undefined ? value : value.value;
  const [mode, threshold, minimumDays] = datom.positions(body, 3, 'policy');
  const modeName = datom.symbol(mode, 'policy mode');
  if (modeName !== 'UseReset' && modeName !== 'Hold') throw new Error('policy mode is neither UseReset nor Hold');
  const thresholdPercent = datom.integer(threshold, 'policy threshold');
  if (thresholdPercent < 0 || thresholdPercent > 100) throw new Error('policy threshold is not a percentage');
  const minimum = datom.integer(minimumDays, 'policy minimum days');
  if (minimum < 0) throw new Error('policy minimum days is negative');
  return { mode: modeName, thresholdPercent, minimumDaysLeft: minimum };
}
