/* Birth-time, private hook binding. Launcher code supplies every identity fact. */
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const FLOW = /^[a-z0-9]{6,}$/;
const harnesses = new Set(['claude', 'codex']);
const layers = new Set(['Primary', 'Secondary', 'Tertiary', 'Quaternary']);
const aspects = new Set(['Psyche', 'Mind', 'Field']);

export function makeContextRefreshBinding({baseConfig, nativeSessionId, flowId, aspect, topic, layer, harness, model,
  seatTarget}) {
  if (!UUID.test(nativeSessionId || '') || !FLOW.test(flowId || '') || !aspects.has(aspect) ||
      !layers.has(layer) || !harnesses.has(harness) || typeof topic !== 'string' || !topic ||
      typeof model !== 'string' || !model || seatTarget !== `${aspect} ${topic} ${layer}`) {
    throw new TypeError('binding requires exact native, flow, aspect, topic, layer, harness, model, and seat identity');
  }
  if (!baseConfig || baseConfig.version !== 1 || !(baseConfig.warningWindowFraction > 0 && baseConfig.warningWindowFraction <= 1) ||
      !Number.isSafeInteger(baseConfig.claude?.warningTokens) || baseConfig.claude.warningTokens <= 0 ||
      !baseConfig.codex?.models || Object.values(baseConfig.codex.models).some(value => !Number.isSafeInteger(value) || value <= 0) ||
      baseConfig.recipients?.field !== 'Field Core Secondary') throw new TypeError('invalid context threshold base configuration');
  return {...baseConfig, bindings: [{nativeSessionId, flowId, aspect, topic, layer, harness, model, seatTarget}]};
}

export const nativeStopCommand = Object.freeze({
  claude: Object.freeze({stdin: 'JSON Stop object', sessionField: 'session_id', transcriptField: 'transcript_path'}),
  codex: Object.freeze({stdin: 'JSON Stop object', sessionField: 'session_id', alternateSessionField: 'thread_id', transcriptField: 'transcript_path'})
});
