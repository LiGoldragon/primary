import {defaultLaunchConfig, voiceFromConfig} from './main-flow-mode/launch-config.mjs';

// Native correspondence is declarative EDN. The reader validates every row
// before this table is exposed to either launcher.
const launchConfig = defaultLaunchConfig();
const rows = Object.fromEntries(['Psyche', 'Mind', 'Field'].flatMap(aspect =>
  ['Primary', 'Secondary', 'Tertiary', 'Quaternary'].map(layer =>
    [`${aspect}.${layer}`, voiceFromConfig(launchConfig, {aspect, layer})])));
export const VOICE_PROFILES = Object.freeze(Object.fromEntries(Object.entries(rows).map(([key, row]) => [key, Object.freeze(row)])));
export {launchConfig};

const stackRows = Object.fromEntries(['Psyche', 'Mind', 'Field'].map(aspect => [
  `${aspect}.Quaternary.Claude`,
  Object.freeze({status: 'configured', harness: 'claude', model: 'claude-haiku-5-5', effort: 'medium', source: 'living correspondence'}),
]));
export const STACK_PROFILES = Object.freeze(stackRows);

export const voiceKey = ({aspect, layer}) => {
  if (!aspect || !layer) throw new Error('voice aspect and layer are required for native launch');
  return `${aspect}.${layer}`;
};

// Optional supplied values are assertions, never choices. The returned frozen
// row is the only source of harness, model, and effort for a native launch.
export function selectVoiceProfile({aspect, layer, topic, harness, model, effort}) {
  const key = voiceKey({aspect, layer});
  const profile = topic === undefined ? VOICE_PROFILES[key] : voiceFromConfig(launchConfig, {aspect, layer, topic});
  if (!profile) throw new Error(`no voice correspondence: ${key}`);
  if (profile.status !== 'configured') throw new Error(`voice correspondence is ${profile.status}: ${key}; ${profile.reason}`);
  if (harness !== undefined && harness !== profile.harness) throw new Error(`voice harness differs for ${key}: required ${profile.harness}, received ${harness}`);
  if (model !== undefined && model !== profile.model) throw new Error(`voice model differs for ${key}: required ${profile.model}, received ${model}`);
  if (effort !== undefined && effort !== profile.effort) throw new Error(`voice effort differs for ${key}: required ${profile.effort}, received ${effort}`);
  return profile;
}

// A stack selection is explicit: it never changes a voice's native default.
export function selectStackProfile({aspect, layer, stack, harness, model, effort}) {
  const key = `${voiceKey({aspect, layer})}.${stack}`;
  const profile = STACK_PROFILES[key];
  if (!profile) throw new Error(`no stack correspondence: ${key}`);
  if (harness !== undefined && harness !== profile.harness) throw new Error(`stack harness differs for ${key}: required ${profile.harness}, received ${harness}`);
  if (model !== undefined && model !== profile.model) throw new Error(`stack model differs for ${key}: required ${profile.model}, received ${model}`);
  if (effort !== undefined && effort !== profile.effort) throw new Error(`stack effort differs for ${key}: required ${profile.effort}, received ${effort}`);
  return profile;
}
export const requireVoiceProfile = selectVoiceProfile;
