import fs from 'node:fs';
import {startRequest, submitStart} from '/home/li/primary/tools/flow-start-adapter.mjs';
import {loadLaunchConfig, roleModulesFromConfig, voiceFromConfig} from '/home/li/primary/tools/main-flow-mode/launch-config.mjs';
const [which, mode] = process.argv.slice(2);
const config = loadLaunchConfig('/home/li/primary');
const spec = {
  flow:  {topic: 'flow',  Topic: 'Flow',  predecessor: 'da2038', model: 'gpt-6-astra', effort: 'medium', brief: 'flow-brief.md', leaveOuts: ['CodexAgentsMd','CodexSkillListing','CodexCollaborationMode','CodexEnvironmentContext','CodexPermissions','CodexDeveloperInstructions']},
  ethos: {topic: 'ethos', Topic: 'Ethos', predecessor: '65f93a', brief: 'ethos-brief.md'},
}[which];
const row = config.metaflow.metaflows.find(r => r.aspect === 'Psyche' && r.layer === 'Secondary' && r.topic === spec.Topic);
const voice = voiceFromConfig(config, {aspect: 'Psyche', layer: 'Secondary', topic: spec.Topic});
const profile = {
  requestId: `d68c82-${which}-secondary-20261017-03`,
  system: roleModulesFromConfig(config, row, 'system'),
  user: roleModulesFromConfig(config, row, 'user'),
  aspect: 'Psyche', topic: spec.topic, layer: 'Secondary',
  model: spec.model ?? voice.model, effort: spec.effort ?? voice.effort,
  predecessor: spec.predecessor, leaveOuts: spec.leaveOuts, remembered: [], session: 'default',
  brief: `Address.{ Psyche ${spec.topic} Secondary }\n\n` + fs.readFileSync(new URL(spec.brief, import.meta.url), "utf8").trimEnd(),
};
if (mode === 'compose') { console.log(JSON.stringify({system: profile.system.length, user: profile.user.length, model: profile.model})); console.log(startRequest(profile)); }
else { const r = submitStart(profile, {timeout: 900000}); console.log(JSON.stringify(r)); }
