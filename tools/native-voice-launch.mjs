#!/usr/bin/env node
import {spawnSync} from 'node:child_process';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {selectVoiceProfile} from './native-voice-profiles.mjs';

export function parseArgs(argv) {
  const o = {root: false, predecessor: undefined, metaflow: undefined};
  for (let index = 0; index < argv.length; index++) {
    const arg = argv[index];
    if (arg === '--root') { o.root = true; continue; }
    if (!['--voice', '--brief', '--predecessor', '--metaflow'].includes(arg) || argv[index + 1] === undefined || argv[index + 1].startsWith('--'))
      throw new Error('usage: --voice Aspect.Layer --brief PATH (--root --metaflow FILE | --predecessor FLOW_ID)');
    o[arg.slice(2).replace(/-(\w)/g, (_, c) => c.toUpperCase())] = argv[++index];
  }
  if (!o.voice || !o.brief || o.root === Boolean(o.predecessor) || (o.root && !o.metaflow) || (!o.root && o.metaflow))
    throw new Error('usage: --voice Aspect.Layer --brief PATH (--root --metaflow FILE | --predecessor FLOW_ID)');
  const [aspect, layer, ...extra] = o.voice.split('.');
  if (extra.length || !aspect || !layer) throw new Error('voice must be Aspect.Layer');
  return {aspect, layer, brief: path.resolve(o.brief), root: o.root, predecessor: o.predecessor, metaflow: o.metaflow && path.resolve(o.metaflow)};
}
export function dispatchCommand({aspect, layer, brief, root, predecessor, metaflow}) {
  const profile = selectVoiceProfile({aspect, layer});
  const here = path.dirname(fileURLToPath(import.meta.url));
  const backend = profile.harness === 'codex' ? 'codex-main-flow-launch.mjs' : 'claude-main-flow-launch.mjs';
  const lineage = root ? ['--root', '--metaflow', metaflow] : ['--predecessor', predecessor];
  return {command: process.execPath, args: [path.join(here, backend), '--aspect', aspect, '--layer', layer, '--brief', brief, ...lineage]};
}
const direct = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (direct) {
  try {
    const command = dispatchCommand(parseArgs(process.argv.slice(2)));
    const child = spawnSync(command.command, command.args, {stdio: 'inherit'});
    process.exit(child.status ?? 1);
  } catch (error) { console.error(`voice: FAILED: ${error.message}`); process.exit(2); }
}
