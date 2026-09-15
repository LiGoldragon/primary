#!/usr/bin/env node
const preserved = ['DISPLAY','WAYLAND_DISPLAY','XDG_CURRENT_DESKTOP','XDG_SESSION_TYPE','XDG_RUNTIME_DIR'];
export function renderLauncherPlan({ cwd, flowId, sessionId, name, env = {}, remoteControl = false }) {
  for (const [key, value] of Object.entries({ cwd, flowId, sessionId, name })) if (typeof value !== 'string' || !value) throw new Error(`missing ${key}`);
  const clean = Object.fromEntries(Object.entries(env).filter(([key]) => preserved.includes(key)));
  const argv = ['ghostty', '--window-inherit-working-directory=false', '--working-directory', cwd, '--title', `Claude ${name}`, '-e', 'bash', '-lc', `cd ${shell(cwd)} && exec claude --session-id ${shell(sessionId)} --name ${shell(name)} --effort medium${remoteControl ? ' --remote-control' : ''}`];
  return { argv, preservedEnvironment: clean, unsetPrefixes: ['CODEX_', 'NO_COLOR', 'TERM'], postflight: ['session record exists', 'bridge id matches session record', 'remote-list name matches planned name'], launches: false };
}
function shell(value) { return `'${value.replaceAll("'", "'\\''")}'`; }
if (import.meta.url === `file://${process.argv[1]}`) { console.error('dry-run library only; import renderLauncherPlan; no process is spawned'); process.exit(2); }
