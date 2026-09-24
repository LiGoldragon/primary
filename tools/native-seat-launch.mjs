#!/usr/bin/env node
/* Native seat launcher: typed skills, fat source bundle, post-start receipt. */
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';
import { modelTitle, requireModelTitle } from './model-display-name.mjs';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const args = process.argv.slice(2);
const option = name => { const i = args.indexOf(name); return i < 0 ? undefined : args[i + 1]; };
const has = name => args.includes(name);
const seat = option('--seat');
const profileFile = option('--profile-file');
const requestedPredecessor = option('--predecessor');
const freshSeat = has('--fresh');
const cwd = path.resolve(option('--cwd') ?? ROOT);
const threadName = option('--name');
const verifyThread = option('--verify-thread');
const adoptHerdrThread = option('--adopt-herdr-thread');
const expectedRunnerSha256 = option('--expected-runner-sha256');
const receiptFile = option('--receipt');
const finalizeTitle = has('--finalize-title');
const claimedFlowId = option('--flow-id');
const herdrRollout = option('--herdr-rollout');
const activate = has('--activate');
const bindHerdr = has('--bind-herdr');
const disposableProbe = has('--disposable-probe');
const probeDirectory = option('--probe-directory');
// Main-flow mode: every seat this launcher starts is a main seat, so its Codex
// thread replaces the base instructions with the living's main-flow prompt
// (model_instructions_file).  --no-main-seat keeps the stock instructions.
const mainSeat = !has('--no-main-seat');
const mainFlowPromptFile = path.resolve(option('--main-flow-prompt') ?? path.join(ROOT, 'tools', 'main-flow-mode', 'system-prompt.md'));
const invokedDirectly = Boolean(process.argv[1]) && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname);
const roles = {
  // Current Field refreshes are explicit launch profiles, kept separate from
  // historical provenance profiles below.  Source bodies are sent only to the
  // native first-turn input; this profile persists locators, never copies.
  'field-astra-current': { model: 'gpt-6-astra', effort: 'medium', role: 'Field Astra', predecessor: null, ancestor: '1cb440', skills: ['spirit','main-flow','field','refresh','psyche','psyche-acquisition','behavior','correction','vocabulary','testing','subflow','edit-coordination','orchestrate','flow-evidence','prompt-crafting','codex-harness','herdr','messaging'], sourceManifest: ['Vision/flowNexus.md','Vision/nexus.md','Vision/modelRoles.md','vision-raw/roleDescriptions.md','vision-raw/flowNaming.md','vision-raw/flowDaemon.md','vision-raw/flowKnowledge.md','vision-raw/noctalia.md','flows/1f96fc/vision/fieldMaintenanceAndRefresh.md','flows/b05237/vision/operational-fableRestartWithRecoveredVision.md','flows/b05237/vision/operational-fatPromptAndCustomSystemPrompt.md','flows/b05237/vision/operational-skillsAreVisionRepropagated.md','flows/b05237/vision/operational-fieldMaintainsAndFixes.md','flows/b05237/vision/operational-whoTalksToWhom.md','flows/b05237/vision/operational-responseAnatomyAndPowerAllocation.md','flows/b05237/vision/operational-messagingToDeployment.md','flows/1cb440/reports/refresh-handoff.md'] },
  'field-sol-current': { model: 'gpt-6-sol', effort: 'medium', role: 'Field Sol', predecessor: null, ancestor: '1cb440', skills: ['spirit','main-flow','field','refresh','psyche','psyche-acquisition','behavior','correction','vocabulary','testing','subflow','edit-coordination','orchestrate','flow-evidence','prompt-crafting','codex-harness','herdr','messaging'], sourceManifest: ['flows/6db4fe/reports/field-sol-startup.md'] },
  // A named receipt-first successor preserves the accepted 395aed lineage
  // while retaining the 8565e8 handoff as its audited source material.
  'field-sol-of-395aed': { model: 'gpt-5.6-sol', effort: 'medium', role: 'Field Sol', predecessor: '395aed', ancestor: '395aed', skills: ['spirit','main-flow','field','refresh','psyche','psyche-acquisition','behavior','correction','vocabulary','testing','subflow','edit-coordination','orchestrate','flow-evidence','prompt-crafting','codex-harness','herdr','messaging'], sourceManifest: ['flows/8565e8/reports/refresh-handoff.md','flows/8565e8/reports/morning-2026-09-20.md','flows/8565e8/reports/lojix-schema-compatibility-addendum.md'] },
  // Mind succession remains receipt-first.  The incumbent is retained until
  // the separately witnessed identity, HM route, and acceptance gates pass.
  'mind-astra-of-0ab019': { model: 'gpt-6-astra', effort: 'medium', role: 'Mind Astra', predecessor: '0ab019', ancestor: '0ab019', skills: ['spirit','main-flow','psyche','behavior','correction','vocabulary','testing','subflow','edit-coordination','flow-evidence','prompt-crafting','codex-harness','refresh','herdr','messaging'], sourceManifest: ['flows/0ab019/reports/night-refresh-handoff.md','flows/1cb440/reports/mind-astra-clean-refresh-preparation.md','flows/0ab019/reports/night-2026-09-20.md','flows/893603/reports/astra-successor-handoff.md','flows/893603/reports/refresh-audit.md','flows/893603/reports/primary-next-mind-report.md','flows/893603/reports/primary-next-source-inventory.json','flows/893603/vision/claude-persistence.md','flows/893603/quarantine/e26a64.hacky-messenger.json','flows/9993b5/vision/mindMemory.md','flows/9993b5/vision/psycheVsMind.md','flows/9993b5/vision/transcriptOverFiles.md','flows/9993b5/vision/transcriptArchive.md','flows/9993b5/vision/transcriptIndex.md','flows/9993b5/vision/transcriptSelfReference.md','flows/9993b5/vision/flowAnatomy.md','flows/9993b5/vision/flowIdLayers.md','flows/9993b5/vision/structuredLog.md','flows/9993b5/vision/easyFlowDispatch.md','flows/9993b5/vision/powerLevels.md','flows/9993b5/vision/datomStructuralEditing.md','Vision/flowNexus.md','Vision/nexus.md','Vision/psyche.md','Vision/distillation.md','Intent/context.md','vision-raw/spirit.md','flows/cf3553/summary.md','flows/cf3553/vision/operational-mainFlowStartupCorrection.md'] },
  // The lean refresh intentionally carries only its published handoff and
  // PsycheHigh's night direction; no predecessor transcript or broad bundle.
  'mind-astra-of-98ac2e': { model: 'gpt-6-astra', effort: 'medium', role: 'Mind Astra', predecessor: '98ac2e', ancestor: '98ac2e', skills: ['spirit','main-flow','psyche','behavior','correction','vocabulary','testing','subflow','edit-coordination','flow-evidence','prompt-crafting','codex-harness','refresh','herdr','messaging'], sourceManifest: ['flows/98ac2e/reports/refresh-handoff.md','flows/f38926/vision/nightWork.md'] },
  'mind-astra-current': { model: 'gpt-6-astra', effort: 'medium', role: 'Mind Astra', predecessor: '9e7ea5', ancestor: '9e7ea5', skills: ['spirit','main-flow','psyche','behavior','correction','vocabulary','testing','subflow','edit-coordination','flow-evidence','prompt-crafting','codex-harness','refresh','herdr','messaging'], sourceManifest: ['flows/9e7ea5/reports/refresh-handoff.md','flows/98ac2e/reports/refresh-handoff.md','flows/f38926/vision/nightWork.md'] },
  astra: { model: 'gpt-6-astra', effort: 'medium', role: 'Field Astra', predecessor: 'cf7791', ancestor: 'cf3553', skills: ['spirit','main-flow','field','refresh','psyche','behavior','correction','vocabulary','testing','subflow','edit-coordination','orchestrate','flow-evidence','prompt-crafting','codex-harness','herdr','messaging'], sourceManifest: ['Vision/flowNexus.md','Vision/nexus.md','flows/33ba2b/handoff/field-astro-voice-source-manifest.md','flows/33ba2b/handoff/field-astro-voice-refresh.md','flows/33ba2b/vision/operational-fieldRefreshSuccession.md','flows/33ba2b/vision/psycheDataArchitecture.md','flows/cf3553/summary.md','flows/cf3553/vision/operational-mainFlowStartupCorrection.md','flows/cf3553/vision/operational-fieldWorkersAreReapers.md','flows/cf3553/vision/operational-fieldReapingJudgmentAndExecution.md','flows/cf3553/reports/field-opus46-updated-judgment.md','flows/cf3553/reports/reaping-execution-addendum.md','flows/cf3553/reports/oneac573-final-export-metadata.md','flows/cf3553/field-sol-of-3b1574-native-receipt.json','flows/c3e42e/reports/native-start-readiness.md','flows/cf3553/mind-astra-of-893603-native-receipt.json','flows/cf3553/reports/mind-astra-of-893603-readiness.md','flows/cf3553/reports/claude-mainflow-refresh-056f6d30.json','flows/cf3553/reports/codex-mainflow-refresh-3b1574.md','flows/cf3553/reports/claude-mainflow-refresh-b8156034.json','flows/cf3553/reports/claude-opus-review-af762b-9a79dc.json','flows/cf3553/reports/claude-parent-delegation-corrections.md'] },
  sol: { model: 'gpt-5.6-sol', effort: 'medium', role: 'Field Sol', predecessor: '3b1574', ancestor: '33ba2b', skills: ['spirit','main-flow','field','refresh','psyche','behavior','correction','vocabulary','testing','subflow','edit-coordination','flow-evidence','herdr','messaging','prompt-crafting'], sourceManifest: ['Vision/flowNexus.md','Vision/nexus.md','flows/cf3553/summary.md','flows/cf3553/vision/operational-mainFlowStartupCorrection.md','flows/33ba2b/handoff/field-astro-voice-source-manifest.md','flows/33ba2b/handoff/field-astro-voice-refresh.md','flows/33ba2b/vision/operational-fieldRefreshSuccession.md','flows/33ba2b/vision/psycheDataArchitecture.md'] },
  luna: { model: 'gpt-6-luna', effort: 'medium', role: 'low Codex seat', predecessor: null, skills: ['spirit','main-flow','psyche','behavior','vocabulary','subflow'], sourceManifest: ['Vision/flowNexus.md','Vision/nexus.md','flows/cf3553/summary.md','flows/cf3553/vision/operational-mainFlowStartupCorrection.md'] },
};
if (profileFile) {
  const file=path.resolve(profileFile), body=fs.readFileSync(file,'utf8'), profile=JSON.parse(body);
  if (!seat || roles[seat] || profile.name!==seat || !/^[a-z][a-z0-9-]{2,40}$/.test(seat)) throw new Error('external profile name must match a new --seat');
  const reservedMainRole = /^(Field|Mind) (Astra|Sol|High|Medium)$/.test(profile.role);
  const lowCostModel = !reservedMainRole && ['gpt-5.6-terra','gpt-5.6-luna','gpt-6-luna'].includes(profile.model) && ['low','medium'].includes(profile.effort);
  const authorizedMindSol = ['gpt-5.6-sol','gpt-6-sol'].includes(profile.model) && profile.effort === 'medium' && profile.role === 'Mind Medium' && freshSeat;
  const authorizedFreshFieldMain = freshSeat && (
    (seat === 'field-sol' && profile.role === 'Field Sol' && profile.model === 'gpt-6-sol' && profile.effort === 'medium') ||
    (seat === 'field-luna' && profile.role === 'Field Luna' && profile.model === 'gpt-6-luna' && profile.effort === 'medium')
  );
  const authorizedMindAstra = seat === 'mind-astra-of-4b0f60' && requestedPredecessor === '4b0f60' && profile.model === 'gpt-6-astra' && profile.effort === 'medium' && profile.role === 'Mind Astra' && !freshSeat;
  const authorizedFieldSol = (
    (seat === 'field-sol-of-7091ea' && requestedPredecessor === '7091ea') ||
    (seat === 'field-sol-of-753e69' && requestedPredecessor === '753e69')
  ) && profile.model === 'gpt-5.6-sol' && profile.effort === 'medium' && profile.role === 'Field Sol' && !freshSeat;
  const authorizedFieldAstra = (seat === 'field-astra-of-6db4fe' && requestedPredecessor === '6db4fe' || seat === 'field-astra-of-03e825' && requestedPredecessor === '03e825' || seat === 'field-astra-of-6fb948' && requestedPredecessor === '6fb948' || seat === 'field-astra-of-0ad137' && requestedPredecessor === '0ad137') && profile.model === 'gpt-6-astra' && profile.effort === 'medium' && profile.role === 'Field Astra' && !freshSeat;
  if (!lowCostModel && !authorizedMindSol && !authorizedFreshFieldMain && !authorizedMindAstra && !authorizedFieldSol && !authorizedFieldAstra) throw new Error('external profile requires an authorized Codex model, role, and effort');
  if ('nativeTitle' in profile) throw new Error('external profile cannot provide an arbitrary native title');
  if (typeof profile.role!=='string' || !profile.role.trim() || !Array.isArray(profile.skills) || !profile.skills.includes('spirit') || !profile.skills.includes('main-flow') || !profile.skills.includes('refresh') || !profile.skills.includes('psyche') || !profile.skills.includes('testing-flow-titles') || !Array.isArray(profile.sourceManifest) || !profile.sourceManifest.length) throw new Error('external profile requires role, core native skills including testing-flow-titles, and source manifest');
  if (profile.skills.some(x=>typeof x!=='string'||!/^[a-z][a-z0-9-]*$/.test(x)) || new Set(profile.skills).size!==profile.skills.length) throw new Error('external profile skills must be unique names');
  if (profile.sourceManifest.some(x=>typeof x!=='string'||path.isAbsolute(x)||path.relative(cwd,path.resolve(cwd,x)).startsWith('..')) || new Set(profile.sourceManifest).size!==profile.sourceManifest.length) throw new Error('external profile sources must be unique paths in cwd');
  const requiredStartupPrompt = seat === 'field-sol' ? 'flows/752e0f/field-launch/field-sol.md' : seat === 'field-luna' ? 'flows/752e0f/field-launch/field-luna.md' : null;
  if (authorizedFreshFieldMain && (profile.startupPromptFile !== requiredStartupPrompt || !profile.sourceManifest.includes(requiredStartupPrompt))) throw new Error('fresh GPT-6 Field main requires its exact audited startup prompt file');
  if ('startupPromptFile' in profile && (!requiredStartupPrompt || profile.startupPromptFile !== requiredStartupPrompt)) throw new Error('external profile startup prompt is not authorized for this seat');
  const canonicalFieldFlowRoot='/git/github.com/LiGoldragon/field';
  const relativeFlowRoot=typeof profile.flowRoot==='string'&&!path.isAbsolute(profile.flowRoot)&&!path.relative(cwd,path.resolve(cwd,profile.flowRoot)).startsWith('..');
  const authorizedCanonicalFieldFlowRoot=authorizedFieldAstra&&profile.flowRoot===canonicalFieldFlowRoot;
  if ('flowRoot' in profile && !relativeFlowRoot && !authorizedCanonicalFieldFlowRoot) throw new Error('external profile flow root must be a relative path in cwd or the authorized canonical Field root');
  if (!profile.sourceAudit || !/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z$/.test(profile.sourceAudit.reviewedAt??'') || !Array.isArray(profile.sourceAudit.newestApplicableVision) || !profile.sourceAudit.newestApplicableVision.length || profile.sourceAudit.newestApplicableVision.some(item=>!profile.sourceManifest.includes(item))) throw new Error('external profile requires an audited newest applicable Vision subset of its source manifest');
  if (freshSeat ? (requestedPredecessor || profile.predecessor!==null || profile.fresh!==true || profile.ancestor!==null) : (!requestedPredecessor || !/^[a-f0-9]{6}$/.test(requestedPredecessor) || profile.predecessor!==requestedPredecessor || typeof profile.ancestor!=='string' || !/^[a-f0-9]{6}$/.test(profile.ancestor))) throw new Error('external profile requires exact predecessor and ancestor Flow IDs, or explicit fresh seat with neither');
  roles[seat]={...profile,profileSha256:crypto.createHash('sha256').update(body).digest('hex')};
}
if (!roles[seat] && invokedDirectly) { console.error('usage: native-seat-launch.mjs --seat <field-astra-current|field-sol-current|astra|sol|luna> [--predecessor FLOW_ID] [--cwd DIR] [--plan|--prompt|--adopt-herdr-thread UUID --herdr-session SESSION --herdr-pane PANE --herdr-agent NAME --herdr-terminal TERMINAL --receipt FILE --expected-runner-sha256 HASH --acknowledge-live-launch|--verify-thread THREAD_ID --receipt FILE|--verify-rollout FILE --receipt FILE]'); process.exit(2); }
if (disposableProbe && !probeDirectory) { console.error('--disposable-probe requires --probe-directory'); process.exit(2); }
const role = roles[seat];
function canonicalRole(value) {
  const exact = /^(Psyche|Mind|Field) (High|Medium|Low|Ultra Low)$/.exec(value);
  if (exact) return { aspect: exact[1], power: exact[2] };
  const legacy = {
    'Field Astra': { aspect: 'Field', power: 'High' },
    'Field Sol': { aspect: 'Field', power: 'Medium' },
    'Field Luna': { aspect: 'Field', power: 'Low' },
    'Mind Astra': { aspect: 'Mind', power: 'High' },
    'Mind Sol': { aspect: 'Mind', power: 'Medium' },
  };
  return legacy[value] ?? null;
}
function endpointForModel(model,home=process.env.HOME) {
  if (!home || !path.isAbsolute(home)) throw new Error('absolute home required for Codex endpoint selection');
  const generation = ['gpt-6-sol','gpt-6-luna'].includes(model) ? '.codex-next' : '.codex';
  return path.join(home,generation,'app-server-control','app-server-control.sock');
}
function clientForModel(model,home=process.env.HOME) {
  const next=['gpt-6-sol','gpt-6-luna'].includes(model);
  return {command:next?'codex-next':'codex',expectedPath:path.join(home,'.nix-profile','bin',next?'codex-next':'codex'),
          endpoint:endpointForModel(model,home)};
}
function selectedSocket(model) {
  const expected=endpointForModel(model), supplied=option('--socket');
  if(['gpt-6-sol','gpt-6-luna'].includes(model) && supplied && path.resolve(supplied)!==expected) throw new Error(`endpoint refused for ${model}: expected ${expected}`);
  return supplied ? path.resolve(supplied) : expected;
}
function receiptSocket(receipt) {
  const expected=selectedSocket(receipt.model);
  if(receipt.endpoint && receipt.endpoint!==expected) throw new Error('receipt endpoint differs from model-owned endpoint');
  return expected;
}
function authorizedFreshFieldLowPower(seatName,profile,profileSupplied,isFresh) {
  return Boolean(profileSupplied && isFresh && profile?.effort==='medium' && (
    (seatName==='field-terra-recovery' && profile.role==='Field Low' && profile.model==='gpt-5.6-terra') ||
    (seatName==='field-luna-recovery' && profile.role==='Field Ultra Low' && profile.model==='gpt-6-luna')
  ));
}
const canonical = canonicalRole(role?.role);
const requiredSkills = role ? [...new Set([...role.skills, 'testing-flow-titles'])] : [];
const currentField = seat === 'field-astra-current' || seat === 'field-sol-current';
if (invokedDirectly && freshSeat && (!profileFile || currentField)) { console.error('--fresh requires an explicit external profile'); process.exit(2); }
if (invokedDirectly && currentField && (!requestedPredecessor || !/^[a-f0-9]{6}$/.test(requestedPredecessor))) { console.error('current Field profiles require --predecessor FLOW_ID (six lowercase hex digits)'); process.exit(2); }
const predecessor = freshSeat ? null : currentField || profileFile ? requestedPredecessor : role?.predecessor;
const digest = value => crypto.createHash('sha256').update(value).digest('hex');
function sources() { const missing=role.sourceManifest.filter(f=>!fs.existsSync(path.join(cwd,f))); if(missing.length) throw new Error(`preflight refused: audited ${seat} source manifest is missing: ${missing.join(', ')}`); return role.sourceManifest.map(file=>{const body=fs.readFileSync(path.join(cwd,file),'utf8');return {path:file,body,sha256:digest(body)};}); }
function buildPlan() {
  const manifest = sources();
  const claimRoot = role.flowRoot ?? 'flows';
  const probe = disposableProbe ? `\n\nThis is a disposable native context receipt probe. Its only identity directory is \`${probeDirectory}\`. Do not create a Flow directory or registration.` : '';
  const provenance = freshSeat ? `You are ${role.role}, a fresh seat with no predecessor or ancestor.` : `You are ${role.role}, refreshed from ${predecessor ?? 'the witnessed predecessor'}; that provenance does not retire, replace, or deregister any predecessor.`;
  const startupPrompt = role.startupPromptFile ? manifest.find(source=>source.path===role.startupPromptFile)?.body : null;
  if (role.startupPromptFile && typeof startupPrompt !== 'string') throw new Error('preflight refused: exact startup prompt body is absent from audited manifest');
  const firstPrompt = startupPrompt ?? `# Native main-flow refresh\n\n${provenance} Preserve your native model and effort.\n\nThe launcher sends these role-specific skills through the native structured interface: ${requiredSkills.join(', ')}. A written dollar token is not skill receipt.\n\nAll sources below are attached once with provenance. They are source material, not evidence of a deployment, migration, registration, or seat retirement.\n\n${manifest.map(s => `## Source: \`${s.path}\`\n\n${s.body.trim()}`).join('\n\n')}\n\nThe first turn is receipt-only. Do not use tools; do not claim or create a Flow identity; do not claim or delegate a task; do not launch, restart, retire, register, or mutate another seat. After the native-context receipt, claim any new Flow identity under \`${claimRoot}\`. Reply only with whether native context is present.${probe}`;
  const sourceRecords=manifest.map(({body,...rest})=>rest);
  const displayPower = requireModelTitle(role.model);
  return { version: 2, seat, cwd, claimRoot, provisionalTitle: canonical ? `${canonical.aspect} ${displayPower}` : null, canonicalRole: canonical, displayPower, model: role.model, effort: role.effort, client:clientForModel(role.model), launchGate:['gpt-6-sol','gpt-6-luna'].includes(role.model)?'coherent-flow-deployment-required':null, role: role.role, predecessor: predecessor, ancestor: role.ancestor ?? null, profileSha256:role.profileSha256??null, sourceAudit:role.sourceAudit??null, requiredSkillNames: requiredSkills, requiredMainFlow: { name: 'main-flow', path: path.join(cwd, '.agents/skills/main-flow/SKILL.md') }, sources: sourceRecords, sourceManifestSha256:digest(JSON.stringify(sourceRecords)), firstPrompt, firstPromptSha256: digest(firstPrompt), safety: { oneCompleteInitialInputBlock:true, receiptOnlyFirstTurn:true, activationAfterNativeContextReceiptOnly:true, noImplicitPredecessorRetirement: true, registrationAfterReadinessOnly: true, readyRequiresExpandedNativeMainFlow: true } };
}
function mainFlowMode(isMain=mainSeat, file=mainFlowPromptFile) {
  if (!isMain) return null;
  if (!fs.existsSync(file) || !fs.statSync(file).isFile() || !fs.readFileSync(file,'utf8').trim()) throw new Error(`launch refused: main-flow system prompt file missing or empty: ${file}`);
  return { modelInstructionsFile: file, sha256: digest(fs.readFileSync(file,'utf8')) };
}
function threadStartParams(mode, base) { return mode ? { ...base, config: { model_instructions_file: mode.modelInstructionsFile } } : base; }
function rejectTokenOnly(text) { if (/\$main-flow|\/main-flow/.test(text)) throw new Error('text token is not skill injection; use typed {type:"skill",name:"main-flow",path} input'); }
function structuredSkills(skills) { return skills.map(skill => ({ type: 'skill', name: skill.name, path: skill.path })); }
function containsMainFlow(value, expectedPath) { if (Array.isArray(value)) return value.some(v => containsMainFlow(v, expectedPath)); if (!value || typeof value !== 'object') return false; if (value.type === 'skill' && value.name === 'main-flow' && value.path === expectedPath) return true; return Object.values(value).some(v => containsMainFlow(v, expectedPath)); }
function resolveStartupSkills(available, plan) {
  const map=new Map(available.flatMap(item=>item.skills??[item.skill??item]).map(s=>[s.name,s]));
  return requiredSkills.map(name=>{
    // User-only startup skills are deliberately absent from the native
    // catalog. The protocol admits them only through an explicit typed item.
    const skillPath=name==='main-flow' ? plan.requiredMainFlow.path : map.get(name)?.path;
    if(!skillPath)throw new Error(`required native skill unavailable: ${name}`);
    const source=fs.readFileSync(skillPath,'utf8');
    return {name,path:skillPath,source,sha256:digest(source)};
  });
}
function runnerBytes() { const executed=path.resolve(process.argv[1] ?? ''); const self=path.resolve(new URL(import.meta.url).pathname); if(executed!==self) throw new Error(`preflight refused: executed runner is not this source (${executed})`); return fs.readFileSync(executed); }
function preflight(plan, requireRunnerHash=false) {
  if (seat === 'sol') {
    const requiredSources=['flows/33ba2b/handoff/field-astro-voice-source-manifest.md','flows/33ba2b/handoff/field-astro-voice-refresh.md','flows/33ba2b/vision/operational-fieldRefreshSuccession.md','flows/33ba2b/vision/psycheDataArchitecture.md'];
    if (plan.ancestor !== '33ba2b' || requiredSources.some(p=>!plan.sources.some(s=>s.path===p))) throw new Error('preflight refused: Field Sol ancestry or full source bundle is incomplete');
  }
  if (!plan.requiredSkillNames.includes('main-flow')) throw new Error('preflight refused: main-flow is required');
  if (!plan.requiredSkillNames.includes('testing-flow-titles') || !plan.canonicalRole) throw new Error('preflight refused: canonical role and testing-flow-titles are required');
  if (requireRunnerHash&&!expectedRunnerSha256) throw new Error('--launch requires --expected-runner-sha256');
  if (expectedRunnerSha256) {
    const actual=digest(runnerBytes());
    if (actual !== expectedRunnerSha256) throw new Error(`preflight refused: runner hash mismatch (expected ${expectedRunnerSha256}, got ${actual})`);
  }
}
function receiptPath() { return receiptFile ? path.resolve(receiptFile) : path.join(cwd,'.native-seat-receipts',`${seat}-${threadName??'unnamed'}.json`); }
function writeReceipt(receipt) { const file=receiptPath(); fs.mkdirSync(path.dirname(file),{recursive:true}); fs.writeFileSync(file,JSON.stringify(receipt,null,2)+'\n',{mode:0o600}); return file; }
function readReceipt() { if(!receiptFile) throw new Error('--verify-thread requires --receipt'); return JSON.parse(fs.readFileSync(path.resolve(receiptFile),'utf8')); }
function targetTurn(read, receipt) { const thread=read?.thread??read; if(thread?.id!==receipt.threadId) throw new Error('verification refused: returned thread ID differs from pending receipt'); const turns=thread?.turns??thread?.history?.turns??[]; const turn=turns.find(t=>(t.id??t.turnId)===receipt.turnId); if(!turn){if(turns.length)throw new Error('verification refused: thread/read contains only a prior or different turn');return null;} if(receipt.generationId&&(turn.generationId??turn.generation?.id)!==receipt.generationId)throw new Error('verification refused: returned generation differs from pending receipt'); return turn; }
function observedContext(turn) { return turn?.turn_context??turn?.turnContext??turn?.metadata?.turn_context??turn?.metadata?.turnContext??null; }
function receiptOnlyResponse(turn) { const value=turn?.output_text??turn?.output?.text??turn?.response?.text; if(typeof value!=='string'||/\b(tool|task|delegat|flow[- ]?id)\b/i.test(value)) throw new Error('verification refused: target first response is not an observed receipt-only response'); }
function verifyReceipt(read,receipt) { const thread=read?.thread??read; if(receipt.provisionalTitle && thread?.name!==(receipt.canonicalTitle??receipt.provisionalTitle)) throw new Error('verification refused: native title readback differs'); const turn=targetTurn(read,receipt); if(!turn)return {threadId:receipt.threadId,turnId:receipt.turnId,readiness:'pending'}; const context=observedContext(turn); if(!context)throw new Error('verification refused: target turn has no observed turn_context/metadata'); if(context.model!==receipt.model||context.effort!==receipt.effort)throw new Error(`verification refused: observed native model/effort mismatch (${context.model}/${context.effort})`); if(context.promptSha256!==receipt.firstPromptSha256&&digest(context.prompt??'')!==receipt.firstPromptSha256) throw new Error('verification refused: target turn prompt differs from pending receipt'); const records=context.skills??context.expanded_skills??context.expandedSkills; if(!Array.isArray(records)||records.length!==receipt.skillManifest.length) throw new Error('verification refused: target turn expanded skill count differs'); for(const want of receipt.skillManifest){const got=records.find(s=>s?.type==='skill'&&s.name===want.name);const source=got?.source??got?.body??got?.content;if(!got||got.path!==want.path||digest(source??'')!==want.sha256)throw new Error(`verification refused: expanded source mismatch for ${want.name}`);} if(context.sourceManifestSha256!==receipt.sourceManifestSha256)throw new Error('verification refused: target turn source manifest differs'); receiptOnlyResponse(turn); return {threadId:receipt.threadId,turnId:receipt.turnId,generationId:receipt.generationId??null,readiness:receipt.canonicalTitle?'native-ready':'native-context-verified-title-pending',firstPromptSha256:receipt.firstPromptSha256}; }
function verifyRolloutReceipt(file,receipt) {
  const body=fs.readFileSync(file,'utf8'), rows=body.trim().split('\n').filter(Boolean).map(JSON.parse);
  const session=rows.find(r=>r.type==='session_meta')?.payload;
  if(session?.id!==receipt.threadId)throw new Error('verification refused: rollout session ID differs');
  const context=rows.find(r=>r.type==='turn_context'&&r.payload?.turn_id===receipt.turnId)?.payload;
  if(!context||context.model!==receipt.model||context.effort!==receipt.effort)throw new Error('verification refused: rollout has no matching native model/effort context');
  const inputIndex=rows.findIndex(r=>r.type==='event_msg'&&r.payload?.thread_id===receipt.threadId&&r.payload?.turn_id===receipt.turnId&&r.payload?.item?.type==='UserMessage');
  const responseIndex=rows.findIndex((r,i)=>i>inputIndex&&r.type==='event_msg'&&r.payload?.thread_id===receipt.threadId&&r.payload?.turn_id===receipt.turnId&&r.payload?.item?.type==='AgentMessage');
  if(inputIndex<0||responseIndex<0)throw new Error('verification refused: rollout lacks target input or response');
  const input=rows[inputIndex].payload.item,records=input?.content?.filter(x=>x.type==='skill')??[],text=input?.content?.find(x=>x.type==='text')?.text;
  if(records.length!==receipt.skillManifest.length||digest(text??'')!==receipt.firstPromptSha256)throw new Error('verification refused: rollout target input differs from pending receipt');
  const expanded=rows.slice(inputIndex+1,responseIndex).filter(r=>r.type==='response_item'&&r.payload?.role==='user').flatMap(r=>r.payload?.content??[]).map(c=>c.text??'');
  for(const want of receipt.skillManifest){
    if(!records.some(got=>got.name===want.name&&got.path===want.path))throw new Error(`verification refused: rollout lacks typed skill ${want.name}`);
    const prefix=`<skill>\n<name>${want.name}</name>\n<path>${want.path}</path>\n`;
    if(!expanded.some(item=>item.startsWith(prefix)&&item.includes(want.source)&&item.trimEnd().endsWith('</skill>')))throw new Error(`verification refused: rollout lacks expanded skill source ${want.name}`);
  }
  receiptOnlyResponse({output_text:rows[responseIndex].payload.item.content?.map(x=>x.text??'').join('')});
  return {threadId:receipt.threadId,turnId:receipt.turnId,readiness:receipt.canonicalTitle?'native-ready':'native-context-verified-title-pending',rolloutSha256:digest(body)};
}
function rolloutRows(file) { return fs.readFileSync(file,'utf8').trim().split('\n').filter(Boolean).map(JSON.parse); }
function resolveHerdrRollout(target,threadId) {
  if(!target) throw new Error('adoption refused: Herdr rollout path or date directory is required');
  const file=path.resolve(target), root=path.join(process.env.HOME,'.codex','sessions');
  if(!file.startsWith(root+path.sep)) throw new Error('adoption refused: rollout must be under the local Codex sessions directory');
  if(fs.existsSync(file)&&fs.statSync(file).isDirectory()) {
    const matches=fs.readdirSync(file).filter(name=>name.startsWith('rollout-')&&name.endsWith(`-${threadId}.jsonl`));
    if(matches.length>1) throw new Error('adoption refused: multiple target rollouts exist');
    return matches.length?path.join(file,matches[0]):null;
  }
  if(!path.basename(file).startsWith('rollout-')||!path.basename(file).endsWith(`-${threadId}.jsonl`)) throw new Error('adoption refused: exact Herdr rollout path is required');
  return fs.existsSync(file)?file:null;
}
function emptyHerdrRollout(target,threadId) {
  const file=resolveHerdrRollout(target,threadId);
  if(!file) return;
  const rows=rolloutRows(file);
  if(rows.length!==1||rows[0].type!=='session_meta'||rows[0].payload?.id!==threadId||path.resolve(rows[0].payload?.cwd??'')!==cwd) throw new Error('adoption refused: Herdr rollout is not the untouched target native session');
}
function frame(payload, opcode = 1) { const body = Buffer.from(payload), mask = crypto.randomBytes(4); let header; if (body.length < 126) header = Buffer.from([128|opcode,128|body.length]); else if(body.length<=65535) { header = Buffer.alloc(4); header[0]=128|opcode; header[1]=254; header.writeUInt16BE(body.length,2); } else { header=Buffer.alloc(10); header[0]=128|opcode; header[1]=255; header.writeBigUInt64BE(BigInt(body.length),2); } const encrypted = Buffer.alloc(body.length); for(let i=0;i<body.length;i++) encrypted[i]=body[i]^mask[i%4]; return Buffer.concat([header,mask,encrypted]); }
async function withRpc(socketPath, fn) { return new Promise((resolve,reject) => { const socket=net.createConnection(socketPath); let buf=Buffer.alloc(0), upgraded=false, next=0, fragment=null; const pending=new Map(); const fail=e=>{socket.destroy();reject(e);}; const call=(method,params)=>new Promise((ok,no)=>{const id=++next;const timer=setTimeout(()=>{pending.delete(id);no(new Error(`RPC timeout: ${method}`));},15000);pending.set(id,{ok,no,timer});socket.write(frame(JSON.stringify({jsonrpc:'2.0',id,method,params})));}); const parse=()=>{while(buf.length>=2){const fin=!!(buf[0]&128),opcode=buf[0]&15;let n=buf[1]&127,offset=2;if(n===126){if(buf.length<4)return;n=buf.readUInt16BE(2);offset=4;}else if(n===127){if(buf.length<10)return;n=Number(buf.readBigUInt64BE(2));offset=10;}if(buf.length<offset+n)return;const body=buf.subarray(offset,offset+n);buf=buf.subarray(offset+n);if(opcode===9){socket.write(frame(body,10));continue;}if(opcode===1)fragment=body;else if(opcode===0&&fragment)fragment=Buffer.concat([fragment,body]);else continue;if(!fin)continue;const message=JSON.parse(fragment);fragment=null;const wait=pending.get(message.id);if(wait){pending.delete(message.id);clearTimeout(wait.timer);message.error?wait.no(new Error(JSON.stringify(message.error))):wait.ok(message.result);}}}; socket.on('error',fail);socket.on('connect',()=>socket.write('GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n'));socket.on('data',data=>{buf=Buffer.concat([buf,data]);if(!upgraded){const end=buf.indexOf('\r\n\r\n');if(end<0)return;if(!buf.subarray(0,end).toString().startsWith('HTTP/1.1 101'))return fail(new Error('websocket upgrade refused'));buf=buf.subarray(end+4);upgraded=true;void(async()=>{try{await call('initialize',{clientInfo:{name:'native-seat-launch',version:'1'}});socket.write(frame(JSON.stringify({jsonrpc:'2.0',method:'initialized',params:{}})));resolve(await fn(call));socket.end();}catch(e){fail(e);}})();}parse();});});}
async function readOrPending(call,threadId) { try{return await call('thread/read',{threadId,includeTurns:true});}catch(error){if(/rollout.*empty/i.test(String(error)))return null;throw error;} }
async function setAndReadNativeTitle(call, threadId, nativeTitle) {
  await call('thread/name/set',{threadId,name:nativeTitle});
  const read=await call('thread/read',{threadId,includeTurns:false});
  const thread=read?.thread??read;
  if(thread?.id!==threadId || thread?.name!==nativeTitle) throw new Error('native title setter readback differs');
  return thread;
}
function herdrJson(session, command, target) {
  const output=execFileSync('herdr',['--session',session,command,'get',target],{encoding:'utf8',timeout:10000});
  const parsed=JSON.parse(output);
  return parsed[command]??parsed.result?.[command]??parsed.result??parsed;
}
function nativeUuidFromFdTargets(targets, home=process.env.HOME) {
  const directory=path.join(home,'.codex','thread-writer-locks')+path.sep;
  const pattern=/^([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\.lock$/;
  const matches=[];
  for(const target of targets) {
    if(typeof target!=='string'||!target.startsWith(directory)) continue;
    const match=pattern.exec(target.slice(directory.length));
    if(match) matches.push({threadId:match[1],lockPath:target});
  }
  const unique=[...new Map(matches.map(item=>[item.threadId,item])).values()];
  if(unique.length!==1) throw new Error(`native UUID binding refused: foreground Codex holds ${unique.length} writer-lock UUIDs`);
  return unique[0];
}
function nativeUuidFromHerdrWriterLock(session,paneId,home=process.env.HOME) {
  const output=execFileSync('herdr',['--session',session,'pane','process-info','--pane',paneId],{encoding:'utf8',timeout:10000});
  const parsed=JSON.parse(output), info=parsed.process_info??parsed.result?.process_info??parsed.result??parsed;
  const processes=info.foreground_processes??[];
  const codex=processes.filter(process=>path.basename(process.argv?.[0]??'')==='codex'||process.name==='.codex-wrapped');
  if(info.pane_id!==paneId||codex.length!==1||!Number.isSafeInteger(codex[0].pid)) throw new Error('native UUID binding refused: target pane lacks one exact foreground Codex process');
  const fdDirectory=`/proc/${codex[0].pid}/fd`;
  const targets=fs.readdirSync(fdDirectory).flatMap(fd=>{try{return [fs.readlinkSync(path.join(fdDirectory,fd))];}catch{return [];}});
  return {...nativeUuidFromFdTargets(targets,home),pid:codex[0].pid,method:'foreground-codex-writer-lock'};
}
function nativeUuidFromRemoteResumeArgv(argv) {
  if(!Array.isArray(argv)||argv.length<5||path.basename(argv[0])!=='codex'||argv[1]!=='resume') return null;
  const threadId=argv[2], remoteIndex=argv.indexOf('--remote');
  if(!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(threadId)||remoteIndex<3||argv[remoteIndex+1]!==`unix://${process.env.HOME}/.codex/app-server-control/app-server-control.sock`) return null;
  return {threadId,method:'foreground-codex-remote-resume'};
}
function nativeUuidFromHerdrBinding(session,paneId,home=process.env.HOME) {
  const output=execFileSync('herdr',['--session',session,'pane','process-info','--pane',paneId],{encoding:'utf8',timeout:10000});
  const parsed=JSON.parse(output), info=parsed.process_info??parsed.result?.process_info??parsed.result??parsed;
  const processes=info.foreground_processes??[];
  const codex=processes.filter(process=>path.basename(process.argv?.[0]??'')==='codex'||process.name==='.codex-wrapped');
  if(info.pane_id!==paneId||codex.length!==1||!Number.isSafeInteger(codex[0].pid)) throw new Error('native UUID binding refused: target pane lacks one exact foreground Codex process');
  const resumed=nativeUuidFromRemoteResumeArgv(codex[0].argv);
  return resumed?{...resumed,pid:codex[0].pid}:nativeUuidFromHerdrWriterLock(session,paneId,home);
}
function verifyHerdrBinding(threadId) {
  const session=option('--herdr-session'), paneId=option('--herdr-pane'), agentName=option('--herdr-agent'), terminalId=option('--herdr-terminal');
  if(!session||!paneId||!agentName||!terminalId||!receiptFile) throw new Error('adoption refused: require --herdr-session, --herdr-pane, --herdr-agent, --herdr-terminal, and --receipt');
  if(!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(threadId)) throw new Error('adoption refused: thread ID is not an exact UUID');
  const agent=herdrJson(session,'agent',agentName), pane=herdrJson(session,'pane',paneId);
  if(agent.name!==agentName||agent.pane_id!==paneId||agent.terminal_id!==terminalId||agent.agent!=='codex'||agent.interactive_ready!==true||!['idle','done'].includes(agent.agent_status??agent.status)) throw new Error('adoption refused: Herdr agent is not the expected ready Codex in the target pane');
  if(pane.pane_id!==paneId||pane.terminal_id!==terminalId||pane.workspace_id!==agent.workspace_id||pane.agent!=='codex'||path.resolve(pane.cwd)!==cwd||path.resolve(agent.cwd)!==cwd) throw new Error('adoption refused: Herdr pane identity or cwd differs');
  const snapshot=execFileSync('herdr',['--session',session,'pane','read',paneId,'--source','recent','--lines','120','--format','text'],{encoding:'utf8',timeout:10000});
  const displayed=new RegExp(`\\bSession:\\s+${threadId}\\b`).test(snapshot);
  const binding=displayed?{threadId,method:'terminal-session-line'}:nativeUuidFromHerdrBinding(session,paneId);
  if(binding.threadId!==threadId) throw new Error('adoption refused: foreground Codex writer-lock UUID differs from target thread UUID');
  return {session,paneId,agentName,terminalId,workspaceId:pane.workspace_id,agentRevision:agent.revision,paneRevision:pane.revision,nativeBinding:binding};
}
async function adoptHerdr(plan) {
  preflight(plan,true);
  const herdr=verifyHerdrBinding(adoptHerdrThread);
  const socket=selectedSocket(role.model);
  const result=await withRpc(socket,async call=>{
    let read;
    try { read=await call('thread/read',{threadId:adoptHerdrThread,includeTurns:true}); }
    catch(error) { if(/rollout is empty/i.test(String(error))) { /* exact pane UUID is checked above */ } else if(/list_turns is not supported yet/i.test(String(error))) emptyHerdrRollout(herdrRollout,adoptHerdrThread); else throw error; }
    if(read) { const thread=read.thread??read; if(thread.id!==adoptHerdrThread||!Array.isArray(thread.turns)||thread.turns.length) throw new Error('adoption refused: target native thread is missing or already has a turn'); }
    const reply=await call('skills/list',{cwds:[cwd]});
    const available=reply.skills??reply.data?.skills??reply.data?.items??reply.data??reply.result?.skills??reply;
    if(!Array.isArray(available)) throw new Error('skills/list did not return an array');
    const skills=resolveStartupSkills(available,plan);
    await setAndReadNativeTitle(call,adoptHerdrThread,plan.provisionalTitle);
    let receipt={version:3,status:'adopting',seat,threadId:adoptHerdrThread,turnId:null,herdr,endpoint:socket,provisionalTitle:plan.provisionalTitle,canonicalRole:plan.canonicalRole,model:plan.model,effort:plan.effort,firstPromptSha256:plan.firstPromptSha256,sourceManifest:plan.sources,sourceManifestSha256:plan.sourceManifestSha256,skillManifest:skills,createdAt:new Date().toISOString()};
    const file=writeReceipt(receipt);
    let turn;
    try { turn=await call('turn/start',{threadId:adoptHerdrThread,effort:role.effort,input:[...structuredSkills(skills),{type:'text',text:plan.firstPrompt}]}); }
    catch(error){writeReceipt({...receipt,status:'failed',failedAt:new Date().toISOString(),failure:String(error)});throw error;}
    const turnId=turn.turn?.id??turn.id;
    if(!turnId){writeReceipt({...receipt,status:'failed',failedAt:new Date().toISOString(),failure:'turn/start returned no id'});throw new Error('adoption refused: turn/start returned no id');}
    receipt={...receipt,status:'pending',turnId,generationId:turn.turn?.generationId??turn.generationId??turn.generation?.id??null,pendingAt:new Date().toISOString()};
    writeReceipt(receipt);
    let after, unsupportedRead=false;
    try { after=await readOrPending(call,adoptHerdrThread); }
    catch(error) { if(/list_turns is not supported yet/i.test(String(error))) unsupportedRead=true; else throw error; }
    let verified=after?verifyReceipt(after.thread??after,receipt):{threadId:adoptHerdrThread,turnId,readiness:'pending'};
    const observedRollout=unsupportedRead&&herdrRollout?resolveHerdrRollout(herdrRollout,adoptHerdrThread):null;
    if(observedRollout) {
      const rows=rolloutRows(observedRollout);
      if(rows.some(row=>row.payload?.turn_id===turnId&&row.payload?.item?.type==='AgentMessage')) verified=verifyRolloutReceipt(observedRollout,receipt);
    }
    if(verified.readiness!=='pending')writeReceipt({...receipt,status:'verified',verifiedAt:new Date().toISOString(),...(verified.rolloutSha256?{rolloutEvidence:{path:observedRollout,sha256:verified.rolloutSha256,verifiedAt:new Date().toISOString()}}:{})});
    return {...verified,receipt:file,herdr,registrationPerformed:false,predecessorRetired:false};
  });
  console.log(JSON.stringify(result));
}
async function launch(plan) {
  preflight(plan, true);
  const launchMindSol = profileFile && freshSeat && seat === 'mind-sol' && role.role === 'Mind Medium' && role.model === 'gpt-5.6-sol' && role.effort === 'medium';
  const launchMindAstra = profileFile && !freshSeat && seat === 'mind-astra-of-4b0f60' && predecessor === '4b0f60' && role.role === 'Mind Astra' && role.model === 'gpt-6-astra' && role.effort === 'medium';
  const launchFieldSol = profileFile && !freshSeat && (
    (seat === 'field-sol-of-7091ea' && predecessor === '7091ea') ||
    (seat === 'field-sol-of-753e69' && predecessor === '753e69')
  ) && role.role === 'Field Sol' && role.model === 'gpt-5.6-sol' && role.effort === 'medium';
  const launchFieldAstra = profileFile && !freshSeat && (seat === 'field-astra-of-6db4fe' && predecessor === '6db4fe' || seat === 'field-astra-of-03e825' && predecessor === '03e825' || seat === 'field-astra-of-6fb948' && predecessor === '6fb948' || seat === 'field-astra-of-0ad137' && predecessor === '0ad137') && role.role === 'Field Astra' && role.model === 'gpt-6-astra' && role.effort === 'medium';
  const launchFreshFieldLowPower = authorizedFreshFieldLowPower(seat,role,profileFile,freshSeat);
  const launchFreshFieldMain = Boolean(profileFile && freshSeat && (
    (seat === 'field-sol' && role.role === 'Field Sol' && role.model === 'gpt-6-sol' && role.effort === 'medium' && role.startupPromptFile === 'flows/752e0f/field-launch/field-sol.md') ||
    (seat === 'field-luna' && role.role === 'Field Luna' && role.model === 'gpt-6-luna' && role.effort === 'medium' && role.startupPromptFile === 'flows/752e0f/field-launch/field-luna.md')
  ));
  if (!launchMindSol && !launchMindAstra && !launchFieldSol && !launchFieldAstra && !launchFreshFieldLowPower && !launchFreshFieldMain) throw new Error('launch refused: profile is not authorized for receipt-first app-server startup');
  if (!receiptFile || fs.existsSync(receiptPath())) throw new Error('launch refused: require a new explicit receipt path');
  const mode=mainFlowMode();
  const socket=selectedSocket(role.model);
  const result=await withRpc(socket,async call=>{
    const reply=await call('skills/list',{cwds:[cwd]});
    const available=reply.skills??reply.data?.skills??reply.data?.items??reply.data??reply.result?.skills??reply;
    if(!Array.isArray(available)) throw new Error('skills/list did not return an array');
    const skills=resolveStartupSkills(available,plan);
    // Source material can accurately quote a slash command. Only the
    // launcher-authored instruction header is prohibited from substituting a
    // text token for the typed structured skill inputs below.
    rejectTokenOnly(plan.firstPrompt.split('\n\nAll sources below are attached once with provenance.')[0]);
    const started=await call('thread/start',threadStartParams(mode,{model:role.model,cwd,approvalPolicy:'never',sandbox:'danger-full-access'}));
    const threadId=started.thread?.id??started.id;
    if(!threadId)throw new Error('thread/start returned no id');
    await setAndReadNativeTitle(call,threadId,plan.provisionalTitle);
    const receipt={version:3,status:'created',seat,threadId,turnId:null,endpoint:socket,provisionalTitle:plan.provisionalTitle,canonicalRole:plan.canonicalRole,model:plan.model,effort:plan.effort,firstPromptSha256:plan.firstPromptSha256,sourceManifest:plan.sources,sourceManifestSha256:plan.sourceManifestSha256,skillManifest:skills,mainFlowMode:mode,createdAt:new Date().toISOString()};
    const file=writeReceipt(receipt);
    let turn;
    try {turn=await call('turn/start',{threadId,effort:role.effort,input:[...structuredSkills(skills),{type:'text',text:plan.firstPrompt,text_elements:[]}]});}
    catch(error){writeReceipt({...receipt,status:'failed',failedAt:new Date().toISOString(),failure:String(error)});throw error;}
    const turnId=turn.turn?.id??turn.id;
    if(!turnId){writeReceipt({...receipt,status:'failed',failedAt:new Date().toISOString(),failure:'turn/start returned no id'});throw new Error('launch refused: turn/start returned no id');}
    const pending={...receipt,status:'pending',turnId,generationId:turn.turn?.generationId??turn.generationId??turn.generation?.id??null,pendingAt:new Date().toISOString()};
    writeReceipt(pending);
    let after;
    try {after=await readOrPending(call,threadId);} catch(error) {if(!/list_turns is not supported yet/i.test(String(error)))throw error;}
    const verified=after?verifyReceipt(after.thread??after,pending):{threadId,turnId,readiness:'pending'};
    if(verified.readiness!=='pending')writeReceipt({...pending,status:'verified',verifiedAt:new Date().toISOString()});
    return {...verified,receipt:file,registrationPerformed:false,predecessorRetired:false};
  });
  console.log(JSON.stringify(result));
}
function activationPromptFor({claimRoot=path.resolve(cwd,role?.flowRoot ?? 'flows'),profilePath=profileFile?path.resolve(profileFile):null}={}) {
  const profile = profilePath ? ` Keep using launcher profile \`${profilePath}\` with \`--cwd ${cwd}\`.` : '';
  return `Native context receipt is verified. Claim your own Flow ID now by running \`flow-id codex --flows-root ${claimRoot}\` exactly. The claim marker must be under \`${claimRoot}\`, not another Flow root.${profile} Then finalize and read back the native title with this launcher and your exact claim receipt before reporting ready or binding HM. Obtain one harmless direct structured tool witness. Do not spawn a subagent for this receipt. Preserve this role, provenance, and inherited open work.`;
}
const activationPrompt = activationPromptFor();
async function activateReceipt() { const receipt=readReceipt(); if(receipt.status!=='verified'||!receipt.turnId) throw new Error('activation refused: receipt is not a verified first-turn receipt'); const socket=receiptSocket(receipt); const result=await withRpc(socket,async call=>{const read=await call('thread/read',{threadId:receipt.threadId,includeTurns:true});try{verifyReceipt(read.thread??read,receipt);}catch(error){if(!receipt.rolloutEvidence||verifyRolloutReceipt(receipt.rolloutEvidence.path,receipt).rolloutSha256!==receipt.rolloutEvidence.sha256)throw error;}const prompt=activationPromptFor({claimRoot:path.resolve(cwd,role.flowRoot ?? 'flows'),profilePath:profileFile?path.resolve(profileFile):null});const turn=await call('turn/start',{threadId:receipt.threadId,effort:receipt.effort,sandboxPolicy:{type:'dangerFullAccess'},input:[{type:'text',text:prompt}]});const turnId=turn.turn?.id??turn.id;if(!turnId)throw new Error('activation refused: turn/start returned no id');return {threadId:receipt.threadId,firstTurnId:receipt.turnId,activationTurnId:turnId,readiness:'activation-started'};});console.log(JSON.stringify(result)); }
async function bindHerdrReceipt() {
  const receipt=readReceipt();
  if(!['verified','ready'].includes(receipt.status)||!receipt.threadId||!receipt.turnId) throw new Error('Herdr binding refused: receipt lacks a verified first native turn');
  const herdr=verifyHerdrBinding(receipt.threadId);
  const socket=receiptSocket(receipt);
  await withRpc(socket,async call=>{
    const read=await call('thread/read',{threadId:receipt.threadId,includeTurns:false});
    const thread=read.thread??read;
    if(thread.id!==receipt.threadId||thread.name!==(receipt.canonicalTitle??receipt.provisionalTitle)) throw new Error('Herdr binding refused: app-server identity or title differs');
  });
  const bound={...receipt,herdr,boundAt:new Date().toISOString()};
  writeReceipt(bound);
  console.log(JSON.stringify({threadId:receipt.threadId,herdr,readiness:'herdr-bound'}));
}
function verifyClaimMarker(flowId, threadId, claimRoot=path.join(cwd,'flows')) {
  if (!/^[0-9a-f]{6}$/.test(flowId)) throw new Error('title finalization requires the own exact short Flow ID');
  const file=path.join(path.resolve(claimRoot),`.${flowId}.flow-id`);
  const metadata=fs.lstatSync(file);
  if (!metadata.isFile() || metadata.isSymbolicLink()) throw new Error('title finalization refused unsafe claim marker');
  const lines=fs.readFileSync(file,'utf8').trimEnd().split('\n');
  const expected=['version=1','harness=codex',`identity=${threadId.replaceAll('-','')}`,`alias=${flowId}`];
  if (lines.length!==expected.length || lines.some((line,index)=>line!==expected[index])) throw new Error('title finalization claim marker differs from exact native thread');
  return file;
}
async function finalizeNativeTitle() {
  const receipt=readReceipt();
  if (receipt.status!=='verified' || !receipt.turnId || receipt.seat!==seat || !canonical ||
      receipt.canonicalRole?.aspect!==canonical.aspect || receipt.canonicalRole?.power!==canonical.power ||
      receipt.model!==role.model || receipt.effort!==role.effort ||
      !receipt.skillManifest?.some(skill=>skill.name==='testing-flow-titles')) {
    throw new Error('title finalization requires matching verified native context, canonical role, and title skill');
  }
  verifyClaimMarker(claimedFlowId,receipt.threadId,path.resolve(cwd,role.flowRoot ?? 'flows'));
  const title=`${canonical.aspect} ${requireModelTitle(role.model)}`;
  const socket=receiptSocket(receipt);
  await withRpc(socket,async call=>{
    const read=await call('thread/read',{threadId:receipt.threadId,includeTurns:false});
    const thread=read?.thread??read;
    if(thread?.id!==receipt.threadId || ![receipt.provisionalTitle,title].includes(thread.name)) throw new Error('title finalization native thread or before-title changed');
    try { await setAndReadNativeTitle(call,receipt.threadId,title); }
    catch (error) {
      try { await setAndReadNativeTitle(call,receipt.threadId,receipt.provisionalTitle); }
      catch (rollbackError) { throw new Error(`title finalization failed and rollback failed: ${error}; ${rollbackError}`); }
      throw new Error(`title finalization failed; provisional title restored: ${error}`);
    }
  });
  const ready={...receipt,status:'ready',canonicalFlowId:claimedFlowId,canonicalTitle:title,titleVerifiedAt:new Date().toISOString()};
  writeReceipt(ready);
  console.log(JSON.stringify({threadId:receipt.threadId,flowId:claimedFlowId,title,readiness:'native-ready',receipt:receiptPath()}));
}
if (invokedDirectly) {
  if(finalizeTitle) await finalizeNativeTitle();
  else {
    const plan=buildPlan();
    if(has('--prompt')) console.log(plan.firstPrompt); else if(bindHerdr) await bindHerdrReceipt(); else if(activate) await activateReceipt(); else if(has('--verify-rollout')) { const receipt=readReceipt(), file=path.resolve(option('--verify-rollout')); const result=verifyRolloutReceipt(file,receipt), rolloutEvidence={path:file,sha256:result.rolloutSha256,verifiedAt:new Date().toISOString()}; writeReceipt({...receipt,status:'verified',verifiedAt:rolloutEvidence.verifiedAt,rolloutEvidence}); console.log(JSON.stringify(result)); } else if(verifyThread) { const receipt=readReceipt(); if(receipt.threadId!==verifyThread) throw new Error('--verify-thread does not match pending receipt'); const socket=receiptSocket(receipt); if(receipt.endpoint&&receipt.endpoint!==socket)throw new Error('receipt endpoint differs from model-owned endpoint'); const result=await withRpc(socket,async call=>{const read=await call('thread/read',{threadId:receipt.threadId,includeTurns:true});return verifyReceipt(read.thread??read,receipt);}); if(result.readiness!=='pending')writeReceipt({...receipt,status:'verified',verifiedAt:new Date().toISOString()}); console.log(JSON.stringify(result)); } else if(adoptHerdrThread) { if(!has('--acknowledge-live-launch')) { console.error('--adopt-herdr-thread requires --acknowledge-live-launch'); process.exit(2); } await adoptHerdr(plan); } else if(has('--launch')) { if(!has('--acknowledge-live-launch')) { console.error('--launch requires --acknowledge-live-launch'); process.exit(2); } await launch(plan); } else console.log(JSON.stringify({...plan,firstPrompt:undefined},null,2));
  }
}
export { rejectTokenOnly, structuredSkills, containsMainFlow, preflight, verifyReceipt, verifyRolloutReceipt, runnerBytes, activationPrompt, activationPromptFor, canonicalRole, modelTitle, verifyClaimMarker, nativeUuidFromFdTargets, nativeUuidFromHerdrWriterLock, nativeUuidFromRemoteResumeArgv, authorizedFreshFieldLowPower, endpointForModel, clientForModel, mainFlowMode, threadStartParams };
