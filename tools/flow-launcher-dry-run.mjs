#!/usr/bin/env node
// Pure proposal renderer. This module never starts a process or reads prompt files.

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const FLOW_ID = /^[a-z0-9][a-z0-9-]*$/;
const preservedKeys = ['HOME', 'PATH', 'DISPLAY', 'WAYLAND_DISPLAY', 'XDG_CURRENT_DESKTOP', 'XDG_SESSION_TYPE', 'XDG_RUNTIME_DIR'];

function requiredString(value, name) {
  if (typeof value !== 'string' || value.length === 0) throw new Error(`missing ${name}`);
  return value;
}
function requiredUuid(value, name) {
  requiredString(value, name);
  if (!UUID.test(value)) throw new Error(`${name} must be an exact UUID`);
  return value;
}
function shellProgram() {
  // $1 is the append-system-prompt file; $2 becomes Claude's one user argument.
  // The renderer does not read either file.
  return 'user_prompt=$(<"$2"); exec claude --session-id "$3" --name "$4" --remote-control "$4" --effort medium --dangerously-skip-permissions --append-system-prompt-file "$1" "$user_prompt"';
}

export function validateUserEnvironment(userEnvironment = {}) {
  if (userEnvironment === null || Array.isArray(userEnvironment) || typeof userEnvironment !== 'object') throw new Error('userEnvironment must be a supplied environment object');
  const preserved = {};
  for (const key of preservedKeys) if (userEnvironment[key] !== undefined) preserved[key] = requiredString(userEnvironment[key], `userEnvironment.${key}`);
  for (const key of ['HOME', 'PATH']) if (!(key in preserved)) throw new Error(`missing userEnvironment.${key}`);
  return preserved;
}

export function renderLauncherPlan({ cwd, flowId, sessionId, name, systemPromptFile, userPromptFile, userEnvironment }) {
  requiredString(cwd, 'cwd');
  requiredString(flowId, 'flowId');
  if (!FLOW_ID.test(flowId)) throw new Error('flowId must be a safe unit-name segment');
  requiredUuid(sessionId, 'sessionId');
  requiredString(name, 'name');
  requiredString(systemPromptFile, 'systemPromptFile');
  requiredString(userPromptFile, 'userPromptFile');
  const preservedEnvironment = validateUserEnvironment(userEnvironment);
  const unit = `flow-${flowId}.scope`;
  const envAssignments = Object.entries(preservedEnvironment).map(([key, value]) => `${key}=${value}`);
  // env -i is inside the transient user scope. Ghostty and Claude therefore
  // receive only explicit interactive values even if the manager has Codex vars.
  const argv = [
    'systemd-run', '--user', '--scope', `--unit=${unit}`, '--collect',
    'env', '-i', ...envAssignments,
    'ghostty', '--window-inherit-working-directory=false', '--working-directory', cwd,
    '--title', `Claude ${name}`, '-e', 'bash', '-lc', shellProgram(),
    'flow-launcher', systemPromptFile, userPromptFile, sessionId, name,
  ];
  return {
    argv,
    scope: { manager: 'user', unit, kind: 'scope', owns: ['ghostty', 'claude'] },
    preservedEnvironment,
    cleanEnvironment: { method: 'env -i inside the transient scope', preservedKeys, removed: ['NO_COLOR', 'CODEX_CI', 'CODEX_*'] },
    promptDelivery: { systemPromptFile, userPromptFile, userPromptArguments: 1, claudeFlag: '--append-system-prompt-file' },
    postflight: 'validatePostflight(sessionRecord, remoteRecord, expected)',
    launches: false,
  };
}

export function validatePostflight({ sessionRecord, remoteRecord, expectedSessionId, expectedName }) {
  requiredUuid(expectedSessionId, 'expectedSessionId');
  requiredString(expectedName, 'expectedName');
  if (sessionRecord === null || typeof sessionRecord !== 'object') throw new Error('missing session record');
  if (sessionRecord.sessionId !== expectedSessionId) throw new Error('session record UUID does not match the planned UUID');
  requiredUuid(sessionRecord.sessionId, 'session record UUID');
  const bridgeSessionId = requiredString(sessionRecord.bridgeSessionId, 'session record bridgeSessionId');
  const entries = Array.isArray(remoteRecord) ? remoteRecord : remoteRecord?.entries;
  if (!Array.isArray(entries)) throw new Error('missing remote record entries');
  if (!entries.some((entry) => entry?.bridgeSessionId === bridgeSessionId && entry?.name === expectedName)) throw new Error('no remote entry matches both bridgeSessionId and planned name');
  return { sessionId: expectedSessionId, bridgeSessionId, name: expectedName };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  console.error('dry-run library only; import renderLauncherPlan or validatePostflight; no process is spawned');
  process.exit(2);
}
