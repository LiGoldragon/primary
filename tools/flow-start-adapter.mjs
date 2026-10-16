import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {loadLaunchConfig, voiceFromConfig, roleModulesFromConfig} from './main-flow-mode/launch-config.mjs';

const ASPECTS = new Set(['Psyche', 'Mind', 'Field']);
const LAYERS = new Set(['Primary', 'Secondary', 'Tertiary', 'Quaternary']);
const LEAVE_OUTS = new Set('ClaudeAiConnectors ConfiguredMcpServers AgentTool ExplorePlanAgents FileTools WorkflowTool ScheduleWakeupTool ReportFindingsTool ListAgentsTool CronTools WebTools DeferredTools SkillTool BundledSkills ClaudeMd GitInstructions AttributionReminder UserSettings ToolSearch BashTool CodexSkillListing CodexAgentsMd CodexCollaborationMode CodexEnvironmentContext CodexPermissions CodexDeveloperInstructions'.split(' '));
const FLOW = /^[0-9a-f]{6,}$/;
export const quoteDatom = text => {
  if (typeof text !== 'string' || text.includes('\0')) throw new Error('Datom string must be text without NUL');
  return `«${text.replaceAll('\\', '\\\\').replaceAll('»', '\\»')}»`;
};
function ids(values, label) {
  if (!Array.isArray(values) || values.some(v => !/^[a-z][a-z0-9-]*$/.test(v)) || new Set(values).size !== values.length) throw new Error(`invalid ${label} module IDs`);
  return `[ ${values.join(' ')} ]`;
}
export function startRequest(p) {
  if (!ASPECTS.has(p.aspect) || !LAYERS.has(p.layer) || !/^[a-z][a-z0-9-]*$/.test(p.topic ?? '')) throw new Error('invalid metaflow address');
  if (!/^[A-Za-z0-9_-]+$/.test(p.requestId ?? '')) throw new Error('stable launch request ID required');
  if (!/^(claude-[a-z0-9-]+-\d[\d-]*|gpt-\d[\w.-]*)$/.test(p.model ?? '')) throw new Error('exact native model ID required');
  if (!['low', 'medium', 'high', 'xhigh', 'max', 'ultra'].includes(p.effort)) throw new Error('invalid effort');
  if (!p.session || !p.brief?.trim()) throw new Error('Herdr session and task required');
  if (p.predecessor != null && !FLOW.test(p.predecessor)) throw new Error('invalid predecessor');
  const remembered = p.remembered ?? [];
  if (!Array.isArray(remembered) || remembered.some(r => !FLOW.test(r.flowId ?? '') || !Number.isSafeInteger(r.depth) || r.depth < 0)) throw new Error('invalid remembered flows');
  let leave = 'None';
  if (p.leaveOuts !== undefined) {
    if (!Array.isArray(p.leaveOuts) || p.leaveOuts.some(v => !LEAVE_OUTS.has(v)) || new Set(p.leaveOuts).size !== p.leaveOuts.length) throw new Error('invalid leave-outs');
    // The Nexus owns harness-specific and indispensable-tool validation.
    leave = `Some.[ ${p.leaveOuts.join(' ')} ]`;
  }
  const system = ids(p.system, 'SYSTEM'), user = ids(p.user, 'USER');
  if (!p.system.some(id => id.startsWith('spirit-')) || !p.system.some(id => id.startsWith('intent-')) || p.user.some(id => /^(spirit|intent)-/.test(id)) || p.user.some(id => p.system.includes(id))) throw new Error('spirit/intent are SYSTEM-only; placements cannot overlap');
  return `Start.{ ${quoteDatom(p.requestId)} ${system} ${user} { ${p.aspect} ${p.topic} ${p.layer} } ${quoteDatom(p.model)} ${quoteDatom(p.effort)} ${p.predecessor == null ? 'None' : 'Some.' + quoteDatom(p.predecessor)} [ ${remembered.map(r => `{ ${quoteDatom(r.flowId)} ${r.depth} }`).join(' ')} ] ${quoteDatom(p.session)} ${leave} ${quoteDatom(p.brief)} }`;
}

// A bounded decoder for the frozen Started response, not a second wire service.
function lex(text) {
  const out = []; let i = 0;
  while (i < text.length) {
    if (/\s/.test(text[i])) { i++; continue; }
    if ('.{}[]'.includes(text[i])) { out.push(text[i++]); continue; }
    if (text[i] === '«') {
      i++; let value = '', closed = false;
      while (i < text.length) {
        if (text[i] === '»') { i++; closed = true; break; }
        if (text[i] === '\\' && ['\\', '»'].includes(text[i + 1])) i++;
        value += text[i++];
      }
      if (!closed) throw new Error('unterminated response string');
      out.push({value}); continue;
    }
    const match = /^[^\s.{}«»\[\]]+/.exec(text.slice(i));
    if (!match) throw new Error('invalid response token');
    out.push({value: match[0]}); i += match[0].length;
  }
  return out;
}
function responseTree(text) {
  if (Buffer.byteLength(text, 'utf8') > 1024 * 1024) throw new Error('Flow response exceeds limit');
  const t = lex(text); let i = 0;
  const read = (depth = 0) => {
    if (depth > 128) throw new Error('Flow response nesting exceeds limit');
    const token = t[i++];
    if (token === '{' || token === '[') {
      const closer = token === '{' ? '}' : ']'; const fields = [];
      while (i < t.length && t[i] !== closer) fields.push(read(depth + 1));
      if (t[i++] !== closer) throw new Error('unclosed Flow response structure');
      return token === '{' ? {fields} : {items:fields};
    }
    if (!token || typeof token.value !== 'string') throw new Error('invalid Flow response value');
    if (t[i] === '.') { i++; return {variant:token.value, value:read(depth + 1)}; }
    return {atom:token.value};
  };
  const tree = read(); if (i !== t.length) throw new Error('trailing Flow response data');
  return tree;
}
function wireString(node) {
  if (typeof node?.atom === 'string') return node.atom;
  // Datom may print a String containing single dots as a bare path.
  if (node?.variant && node.value && !node.value.fields && !node.value.items) return node.variant + '.' + wireString(node.value);
  throw new Error('expected Flow String');
}
export function decodeFlowResponse(text, expectedSession) {
  const wire = String(text).trim(), tree = responseTree(wire);
  if (tree.variant === 'StartRejected' || tree.variant === 'Refused') {
    const reason = tree.value;
    const name = reason?.variant ?? reason?.atom;
    const known = tree.variant === 'StartRejected'
      ? new Set('CompositionRefused LaunchRequestConflict LaunchPersistenceRefused NativeLaunchRefused BindingRefused RegistrationRefused IntentPersistenceRefused OriginUnavailable AddressAwake AddressEnded ContextRefused LeaveOutRefused'.split(' '))
      : new Set('Locked Held Awake Asleep Lapsed Unknown NoLayer NotConfigured Ended OffRoute NoneAbove NotMessage Taken Unidentified Store'.split(' '));
    if (!known.has(name)) throw new Error('unknown typed Flow refusal: ' + wire);
    return {kind:tree.variant, reason, wire};
  }
  if (tree.variant !== 'Started' || tree.value?.fields?.length !== 4) throw new Error('Flow did not return a complete Started response: ' + wire);
  const [flow, native, routeNode, originNode] = tree.value.fields;
  const flowId = wireString(flow), nativeSessionId = wireString(native);
  let route = null;
  if (routeNode?.atom !== 'Unavailable') {
    if (routeNode?.variant !== 'Available' || routeNode.value?.fields?.length !== 4) throw new Error('invalid Herdr route for started flow ' + flowId);
    const [session,name,pane,terminal] = routeNode.value.fields.map(wireString);
    if (session !== expectedSession) throw new Error('Herdr session differs for started flow ' + flowId);
    route = {session,name,pane,terminal};
  }
  let origin;
  if (originNode?.atom === 'Unbound') origin = null;
  else {
    if (originNode?.variant !== 'Flow' || originNode.value?.fields?.length !== 2) throw new Error('invalid Origin for started flow ' + flowId);
    const [originFlow,sessionId] = originNode.value.fields.map(wireString); origin = {flowId:originFlow,sessionId};
  }
  return {kind:'Started',flowId,nativeSessionId,route,origin,wire};
}
export function launchedResponse(text, expectedSession) {
  const result = decodeFlowResponse(text,expectedSession);
  if (result.kind !== 'Started') {
    const error = new Error('Flow refused: ' + result.wire); error.response = result; throw error;
  }
  const {kind,wire,...launched} = result; return launched;
}

export function submitStart(profile, {run = execFileSync, timeout = 900000} = {}) {
  const query = startRequest(profile);
  if (Buffer.byteLength(query, 'utf8') > 131071) throw new Error('inline Start exceeds the operating system argument limit; no launch attempted');
  // A transport failure can follow a successful launch. Preserve requestId and
  // inspect LaunchStatus; never retry here or launch a native harness instead.
  let raw;
  try { raw = run('flow', [query], {encoding: 'utf8', timeout, maxBuffer: 1024 * 1024}); }
  catch (cause) {
    if (cause.stdout && /^(StartRejected|Refused)\./.test(String(cause.stdout).trim())) raw = String(cause.stdout);
    else throw new Error(`Flow Start unresolved for ${profile.requestId}; inspect LaunchStatus before any further start`, {cause});
  }
  let launched;
  try { launched = launchedResponse(raw, profile.session); }
  catch (cause) {
    if (cause.response) throw cause;
    throw new Error(`Flow Start response for ${profile.requestId} could not be decoded: ${String(raw).trim()}; inspect LaunchStatus before another start`, {cause});
  }
  if (!launched.route) return launched;
  try {
    run('hm-register', [launched.flowId, launched.route.name, '--session', launched.route.session, '--native-thread', launched.nativeSessionId, '--aspect', profile.aspect, '--topic', profile.topic, '--layer', profile.layer], {encoding: 'utf8', timeout: 60000});
  } catch (cause) { throw new Error(`Flow ${launched.flowId} started; messenger registration failed. Repair this route without starting another flow`, {cause}); }
  return launched;
}

export function parseArgs(argv, harness) {
  const o = {workspace: '/home/li/primary', aspect: harness === 'claude' ? 'Psyche' : 'Field', herdrSession: 'default', root: false, composeOnly: false};
  const keys = new Set(['--brief','--aspect','--layer','--workspace','--herdr-session','--model','--effort','--predecessor','--metaflow','--topic','--launch-request-id','--leave-outs']);
  for (let i = 0; i < argv.length; i++) {
    const key = argv[i];
    if (key === '--root') { o.root = true; continue; }
    if (key === '--compose-only') { o.composeOnly = true; continue; }
    if (!keys.has(key) || argv[i + 1] === undefined || argv[i + 1].startsWith('--')) throw new Error(`unsupported or missing argument: ${key}`);
    o[key.slice(2).replace(/-(\w)/g, (_, c) => c.toUpperCase())] = argv[++i];
  }
  if (!o.brief || !LAYERS.has(o.layer) || !ASPECTS.has(o.aspect)) throw new Error('--brief, valid aspect and --layer required');
  if ((harness === 'claude' && o.aspect === 'Mind') || (harness === 'codex' && o.aspect === 'Psyche')) throw new Error('aspect does not use this launcher');
  if (o.root === Boolean(o.predecessor) || (o.root && !o.metaflow) || (!o.root && (o.metaflow || o.topic))) throw new Error('choose --root --metaflow or --predecessor');
  if (o.topic !== undefined && !/^[a-z][a-z0-9-]*$/i.test(o.topic)) throw new Error('invalid topic');
  if (o.predecessor && !FLOW.test(o.predecessor)) throw new Error('invalid predecessor');
  if (o.leaveOuts !== undefined) o.leaveOuts = JSON.parse(o.leaveOuts);
  o.workspace = path.resolve(o.workspace); o.brief = path.resolve(o.brief);
  if (o.metaflow) o.metaflow = path.resolve(o.metaflow);
  return o;
}

export function prepareLaunch(o, harness, config) {
  const flowsRoot = path.join(o.workspace, 'flows');
  let continuation;
  if (o.root) {
    // The declaration is retained as lineage work data, never prompt context.
    continuation = {predecessor: null, topic: (o.topic ?? 'core').toLowerCase(), metaflow: fs.readFileSync(o.metaflow, 'utf8')};
  } else {
    const prior = JSON.parse(fs.readFileSync(path.join(flowsRoot, o.predecessor, 'continuation.json'), 'utf8'));
    if (prior.flowId !== o.predecessor || typeof prior.metaflow !== 'string') throw new Error('invalid predecessor lineage');
    continuation = {predecessor: o.predecessor, topic: (prior.topic ?? 'core').toLowerCase(), metaflow: prior.metaflow};
  }
  const rows = config.metaflow.metaflows.filter(r => r.aspect === o.aspect && r.layer === o.layer && r.topic.toLowerCase() === continuation.topic);
  if (rows.length !== 1) throw new Error('metaflow configuration missing or ambiguous');
  const row = rows[0];
  const voice = voiceFromConfig(config, {aspect: o.aspect, layer: o.layer, topic: row.topic, harness, model: o.model, effort: o.effort});
  const system = roleModulesFromConfig(config, row, 'system');
  const user = roleModulesFromConfig(config, row, 'user');
  const brief = fs.readFileSync(o.brief, 'utf8');
  const profile = {requestId: o.launchRequestId ?? 'launch-' + crypto.randomUUID(), system, user, aspect: o.aspect, topic: continuation.topic, layer: o.layer, model: voice.model, effort: voice.effort, predecessor: continuation.predecessor, remembered: [], session: o.herdrSession, leaveOuts: o.leaveOuts ?? row['leave-outs'], brief: `Address.{ ${o.aspect} ${continuation.topic} ${o.layer} }\n\n${brief}`};
  startRequest(profile); return {profile, continuation, flowsRoot};
}

export function launchMain(o, harness, {run = execFileSync, config = loadLaunchConfig(o.workspace), log = console.log} = {}) {
  const {profile, continuation, flowsRoot} = prepareLaunch(o, harness, config);
  if (o.composeOnly) { log(startRequest(profile)); return; }
  const seconds = config.shared['first-response-timeout-seconds'];
  if (!Number.isSafeInteger(seconds) || seconds < 1) throw new Error('configured first-response-timeout-seconds required');
  const recordStarted = (result, lineage, requestId) => {
    const dir = path.join(flowsRoot, result.flowId);
    if (!fs.statSync(dir).isDirectory()) throw new Error('Started ' + result.flowId + '; Flow directory missing; repair without relaunch');
    const record = {flowId: result.flowId, ...lineage, launchRequestId: requestId, nativeSessionId: result.nativeSessionId, route: result.route};
    fs.writeFileSync(path.join(dir, 'continuation.json'), JSON.stringify(record) + '\n', {flag:'wx', mode:0o600});
  };
  if (o.layer === 'Primary') {
    const reply = JSON.parse(run('herdr', ['--session', o.herdrSession, 'agent', 'list'], {encoding:'utf8', timeout:15000}));
    const agents = reply.result?.agents;
    if (!Array.isArray(agents)) throw new Error('Herdr returned no agent list; Primary dependency unknown');
    const title = '{ ' + profile.aspect + ' ' + profile.topic + ' Secondary ';
    const matches = agents.filter(a => a.terminal_title_stripped?.startsWith(title) && a.agent_session?.value && a.pane_id && a.terminal_id && ['idle','working','done'].includes(a.agent_status));
    if (matches.length > 1) throw new Error('ambiguous live Secondary; Primary refused');
    if (!matches.length) {
      const rows = config.metaflow.metaflows.filter(r => r.aspect === profile.aspect && r.topic.toLowerCase() === profile.topic && r.layer === 'Secondary');
      if (rows.length !== 1) throw new Error('Secondary configuration missing or ambiguous; Primary refused');
      const row = rows[0];
      const voice = voiceFromConfig(config, {aspect: profile.aspect, topic:row.topic, layer:'Secondary'});
      const secondary = {...profile, requestId:profile.requestId + '-secondary', layer:'Secondary', model:voice.model, effort:voice.effort, predecessor:null,
        system:roleModulesFromConfig(config,row,'system'), user:roleModulesFromConfig(config,row,'user'),
        leaveOuts:row['leave-outs'], brief:profile.brief.replace('Address.{ ' + profile.aspect + ' ' + profile.topic + ' Primary }', 'Address.{ ' + profile.aspect + ' ' + profile.topic + ' Secondary }')};
      // The same supplied work order goes to its Secondary first. No new
      // bootstrap instructions or context text are manufactured here.
      log('Starting Secondary first; request ' + secondary.requestId);
      const result = submitStart(secondary,{run,timeout:seconds*1000});
      recordStarted(result,{...continuation,predecessor:null},secondary.requestId);
      if (!result.route) throw new Error('Secondary ' + result.flowId + ' started with route Unavailable; Primary not started');
    }
  }
  // Emit request identity before crossing the side-effect boundary.
  log(`Starting ${profile.aspect} ${profile.topic} ${profile.layer}; request ${profile.requestId}`);
  const result = submitStart(profile, {run, timeout: seconds * 1000});
  recordStarted(result,continuation,profile.requestId);
  log(`Started { ${profile.aspect} ${profile.topic} ${profile.layer} ${result.flowId} }; ${result.route ? 'registered ' + result.route.name : 'route Unavailable; not registered'}`);
  return result;
}
