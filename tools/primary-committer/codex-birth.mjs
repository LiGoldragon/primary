// Native birth precedes the first working turn. No fabricated session identity.
import path from 'node:path';

const flowPattern = /^[a-f0-9]{6,64}$/;
const threadPattern = /^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i;
const quote = value => `'${value.replaceAll("'", `'\\''`)}'`;

export function codexOwnerConfig(flowId, {workspace, committer, node = process.execPath}) {
  if (!flowPattern.test(flowId ?? '')) throw new Error('actual claimed FLOW_ID required');
  const config = {'shell_environment_policy.set.FLOW_ID': flowId};
  if (committer !== undefined) {
    if (!flowPattern.test(committer) || !path.isAbsolute(workspace) || !path.isAbsolute(node)) throw new Error('exact committer and absolute hook paths required');
    // A remote app-server does not inherit the TUI environment. Bind the same
    // actual identity explicitly for its hook process and shell subprocesses.
    const command = ['env', `FLOW_ID=${quote(flowId)}`, quote(node), quote(path.join(workspace, 'tools/primary-committer/turn-end.mjs')), '--primary', quote(workspace), '--committer', quote(committer)].join(' ');
    config['hooks.Stop'] = [{hooks: [{type: 'command', command, timeout: 20}]}];
    config['features.hooks'] = true;
    // Native hook trust remains in force. This does not approve an untrusted
    // hook or modify global hooks.json; Field must qualify the installed hook.
  }
  return config;
}

export async function prepareCodexBirth({call, claim, workspace, model, effort, systemPromptFile, committer}) {
  if (!path.isAbsolute(workspace) || !path.isAbsolute(systemPromptFile)) throw new Error('absolute workspace and system prompt required');
  const common = {model, cwd: workspace, approvalPolicy: 'never', sandbox: 'danger-full-access'};
  const config = {model_reasoning_effort: effort, model_instructions_file: systemPromptFile};
  const born = await call('thread/start', {...common, config, ephemeral: false});
  const thread = born?.thread;
  if (!threadPattern.test(thread?.id ?? '') || !Array.isArray(thread.turns) || thread.turns.length !== 0)
    throw new Error('native birth did not return one actual empty thread; no working turn sent');
  const threadId = thread.id;
  const flowId = await claim(threadId);
  const ownerConfig = codexOwnerConfig(flowId, {workspace, committer});
  // A new native thread has an allocated path but no resumable storage yet.
  // The paginated live-read API persists its empty history without a model
  // turn. Never fabricate a rollout or detach before this succeeds.
  if (thread.historyMode !== 'paginated') throw new Error('native birth is not paginated; zero-turn persistence is unqualified');
  const persisted = await call('thread/read', {threadId, includeTurns: true});
  if (persisted?.thread?.id !== threadId || persisted.thread.historyMode !== 'paginated' ||
      !Array.isArray(persisted.thread.turns) || persisted.thread.turns.length !== 0)
    throw new Error('native persistence did not return the same empty paginated thread; no detach or working turn sent');
  // The native server cold-resumes an idle thread with changed config only
  // after its subscribers detach. Never resume somebody else's active thread.
  const detached = await call('thread/unsubscribe', {threadId});
  if (detached?.status !== 'unsubscribed') throw new Error('new thread did not detach; no working turn sent');
  const resumed = await call('thread/resume', {...common, threadId, config: {...config, ...ownerConfig}});
  if (resumed?.thread?.id !== threadId || !Array.isArray(resumed.thread.turns) || resumed.thread.turns.length !== 0)
    throw new Error('native resume identity/history differs; no working turn sent');
  if (resumed.model !== model || resumed.cwd !== workspace)
    throw new Error('native resume model/workspace differs; no working turn sent');
  return {threadId, flowId, config: {...config, ...ownerConfig}, thread: resumed.thread};
}
