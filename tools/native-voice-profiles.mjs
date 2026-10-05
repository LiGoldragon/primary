// Pure correspondence data. Only a configured row may select a native launch.
// Pending and unresolved rows retain provenance without supplying a fallback.
const rows = {
  'Psyche.Primary': {status: 'configured', harness: 'claude', model: 'claude-fable-5-1', effort: 'medium', source: 'existing chosen launch'},
  'Mind.Primary': {status: 'unresolved', reason: 'observed profile is not an authorized voice assignment'},
  'Field.Primary': {status: 'configured', harness: 'codex', model: 'gpt-6-astra', effort: 'medium', source: 'qualified Field Astra profile and user role assignment'},

  'Psyche.Secondary': {status: 'unresolved', reason: 'direct Claude Opus ruling and effort provenance required; launcher medium is only a source default'},
  'Mind.Secondary': {status: 'pending', harness: 'codex', effort: 'medium', reason: 'Curriculum latest Sol correspondence is adoption-pending; exact installed model must be qualified'},
  'Field.Secondary': {status: 'unresolved', reason: 'no Field Secondary correspondence'},

  'Psyche.Tertiary': {status: 'configured', harness: 'claude', model: 'claude-sonnet-5-5', effort: 'medium', source: 'living correspondence'},
  'Mind.Tertiary': {status: 'configured', harness: 'codex', model: 'gpt-6-luna', effort: 'medium', source: 'living correspondence'},
  'Field.Tertiary': {status: 'configured', harness: 'codex', model: 'gpt-6-luna', effort: 'medium', source: 'living correspondence'},

  'Psyche.Quaternary': {status: 'configured', harness: 'claude', model: 'claude-sonnet-5-5', effort: 'low', source: 'living correspondence'},
  'Mind.Quaternary': {status: 'configured', harness: 'codex', model: 'gpt-6-luna', effort: 'low', source: 'living correspondence'},
  'Field.Quaternary': {status: 'configured', harness: 'codex', model: 'gpt-6-luna', effort: 'low', source: 'living correspondence'},
};
export const VOICE_PROFILES = Object.freeze(Object.fromEntries(Object.entries(rows).map(([key, row]) => [key, Object.freeze(row)])));

export const voiceKey = ({aspect, layer}) => {
  if (!aspect || !layer) throw new Error('voice aspect and layer are required for native launch');
  return `${aspect}.${layer}`;
};

// Optional supplied values are assertions, never choices. The returned frozen
// row is the only source of harness, model, and effort for a native launch.
export function selectVoiceProfile({aspect, layer, harness, model, effort}) {
  const key = voiceKey({aspect, layer});
  const profile = VOICE_PROFILES[key];
  if (!profile) throw new Error(`no voice correspondence: ${key}`);
  if (profile.status !== 'configured') throw new Error(`voice correspondence is ${profile.status}: ${key}; ${profile.reason}`);
  if (harness !== undefined && harness !== profile.harness) throw new Error(`voice harness differs for ${key}: required ${profile.harness}, received ${harness}`);
  if (model !== undefined && model !== profile.model) throw new Error(`voice model differs for ${key}: required ${profile.model}, received ${model}`);
  if (effort !== undefined && effort !== profile.effort) throw new Error(`voice effort differs for ${key}: required ${profile.effort}, received ${effort}`);
  return profile;
}
export const requireVoiceProfile = selectVoiceProfile;
