#!/usr/bin/env node
import {spawnSync} from 'node:child_process';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {selectVoiceProfile} from './native-voice-profiles.mjs';

export function parseArgs(argv) {
  if (argv.length !== 4 || argv[0] !== '--voice' || argv[2] !== '--brief' || !argv[1] || !argv[3])
    throw new Error('usage: --voice Aspect.Layer --brief PATH');
  const [aspect, layer, ...extra] = argv[1].split('.');
  if (extra.length || !aspect || !layer) throw new Error('voice must be Aspect.Layer');
  return {aspect, layer, brief: path.resolve(argv[3])};
}
export function dispatchCommand({aspect, layer, brief}) {
  const profile = selectVoiceProfile({aspect, layer});
  const here = path.dirname(fileURLToPath(import.meta.url));
  const backend = profile.harness === 'codex' ? 'codex-main-flow-launch.mjs' : 'claude-main-flow-launch.mjs';
  return {command: process.execPath, args: [path.join(here, backend), '--aspect', aspect, '--layer', layer, '--brief', brief]};
}
const direct = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (direct) {
  try {
    const command = dispatchCommand(parseArgs(process.argv.slice(2)));
    const child = spawnSync(command.command, command.args, {stdio: 'inherit'});
    process.exit(child.status ?? 1);
  } catch (error) { console.error(`voice: FAILED: ${error.message}`); process.exit(2); }
}
