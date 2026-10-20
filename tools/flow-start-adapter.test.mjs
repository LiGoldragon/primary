import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {startRequest, launchedResponse, decodeFlowResponse, submitStart, launchMain, parseArgs} from './flow-start-adapter.mjs';
const uuid = '4201a3e4-964c-403e-824c-6f8908023e6f';
const profile = {requestId:'proof-1',system:['spirit-core','intent-psyche'],user:['compensation-correction'],aspect:'Psyche',topic:'core',layer:'Tertiary',model:'claude-sonnet-5-5',effort:'medium',session:'default',brief:'Run once: «quoted» \\path\n$(never)'};
const success = 'Started.{ 4201a3 '+uuid+' Available.{ default child w1:p4E term_123 } Flow.{ 42265e caller-session } }';
const q = startRequest(profile);
assert.equal(q, 'Start.{ «proof-1» [ spirit-core intent-psyche ] [ compensation-correction ] { Psyche core Tertiary } «claude-sonnet-5-5» «medium» None [  ] «default» None «Run once: «quoted\\» \\\\path\n$(never)» }');
assert.match(startRequest({...profile,leaveOuts:[]}),/Some\.\[  \]/);
assert.match(startRequest({...profile,predecessor:'7c89aa',remembered:[{flowId:'abcdef',depth:2}]}),/Some\.«7c89aa» \[ \{ «abcdef» 2 \} \]/);
for (const invalid of [{system:['/tmp/context']},{user:['intent-psyche']},{system:['spirit-core']},{model:'sonnet'},{leaveOuts:['Unknown']},{remembered:[{flowId:'abcdef',depth:-1}]},{topic:'core } injected'}]) assert.throws(()=>startRequest({...profile,...invalid}));
assert.deepEqual(launchedResponse(success,'default'),{flowId:'4201a3',nativeSessionId:uuid,route:{session:'default',name:'child',pane:'w1:p4E',terminal:'term_123'},origin:{flowId:'42265e',sessionId:'caller-session'}});
assert.equal(launchedResponse(success.replace('Flow.{ 42265e caller-session }','Unbound'),'default').origin,null);
for (const wrong of [success.replace('Started','Launched'),success+' extra',success.replace('default','foreign'),'StartAmbiguous.{ ignored }','StartRejected.NativeLaunchRefused',success.slice(0,-1)]) assert.throws(()=>launchedResponse(wrong,'default'));
assert.equal(launchedResponse(success.replace(uuid,'native.session'),'default').nativeSessionId,'native.session');
assert.equal(launchedResponse(success.replace('w1:p4E','pane-anywhere'),'default').route.pane,'pane-anywhere');
const unavailable=success.replace('Available.{ default child w1:p4E term_123 }','Unavailable');
assert.equal(launchedResponse(unavailable,'default').flowId,'4201a3');
assert.equal(launchedResponse(unavailable,'default').route,null);
assert.equal(launchedResponse(success.replace(uuid,'«»'),'default').nativeSessionId,'');
const rejectionUnits='CompositionRefused LaunchRequestConflict LaunchPersistenceRefused NativeLaunchRefused RegistrationRefused IntentPersistenceRefused OriginUnavailable AddressAwake AddressEnded'.split(' ');
for(const reason of rejectionUnits) {
 const decoded=decodeFlowResponse('StartRejected.'+reason,'default');
 assert.equal(decoded.kind,'StartRejected');assert.equal(decoded.reason.atom,reason);
}
for(const [head,reasons] of Object.entries({ContextRefused:['ComposerUnavailable','ComposerRejected','MetaflowMismatch','PayloadMismatch','ModuleMissing','SystemTooLarge','ModuleTooLarge'],BindingRefused:['PaneMismatch','TerminalMismatch','HarnessMismatch','NotReady','ReservedIdentityMismatch','ClaimUnavailable','ObservationRefused','TransportRefused','Unclassified'],LeaveOutRefused:['Indispensable.ToolSearch','NeedsWorkflowLeftOut.SkillTool','NotForHarness.CodexAgentsMd']})) {
 for(const reason of reasons) {
  const text='StartRejected.'+head+'.'+reason;const decoded=decodeFlowResponse(text,'default');
  assert.equal(decoded.reason.variant,head);assert.equal(decoded.wire,text);
 }
}
const spawnRefusals = [
 'StartRejected.HarnessSpawnRefused.{ ControlCharacter None }',
 'StartRejected.HarnessSpawnRefused.{ CommandTooLong None }',
 'StartRejected.HarnessSpawnRefused.{ Herdr.{ Some.invalid_agent_argument «agent arguments cannot be encoded safely for the target shell» } Some.{ native-thread Answered Archived } }',
 'StartRejected.HarnessSpawnRefused.{ Herdr.{ None «agent wait timed out» } Some.{ native-thread InProgress ArchiveRefused } }'
];
for (const wire of spawnRefusals) {
 const decoded=decodeFlowResponse(wire,'default');
 assert.equal(decoded.kind,'StartRejected');assert.equal(decoded.reason.variant,'HarnessSpawnRefused');assert.equal(decoded.wire,wire);
 let submissions=0;
 assert.throws(()=>submitStart(profile,{run:()=>{submissions++;const e=Error('refused');e.stdout=wire;throw e;}}),error=>error.response?.wire===wire);
 assert.equal(submissions,1,'spawn refusal must not retry or register');
}
assert.deepEqual(decodeFlowResponse('Refused.Locked','default').reason,{atom:'Locked'});
let calls=[];
const present = JSON.stringify({result:{agent:{pane_id:'w1:p4E',terminal_id:'term_123'}}});
const gone = JSON.stringify({error:{code:'agent_not_found',message:'target not found'}});
const run=(bin,args,opts)=>{calls.push({bin,args,opts});return bin==='flow'?success:bin==='herdr'?present:'Registered';};
assert.equal(submitStart(profile,{run}).flowId,'4201a3');
assert.equal(calls.length,3);assert.equal(calls[0].bin,'flow');assert.deepEqual(calls[0].args,[q]);assert.deepEqual(calls[2].args,['Psyche core Tertiary','child','--session','default','--native-thread',uuid]);
assert.equal(calls[2].opts.env.HM_REGISTRATION_FLOW_ID,'4201a3');
const previousIdentity=process.env.HM_REGISTRATION_FLOW_ID;
process.env.HM_REGISTRATION_FLOW_ID='foreign-parent-identity';calls=[];submitStart(profile,{run});
assert.equal(calls[2].opts.env.HM_REGISTRATION_FLOW_ID,'4201a3');
assert.equal(process.env.HM_REGISTRATION_FLOW_ID,'foreign-parent-identity');
if(previousIdentity===undefined)delete process.env.HM_REGISTRATION_FLOW_ID;else process.env.HM_REGISTRATION_FLOW_ID=previousIdentity;
calls=[];const noRoute=submitStart(profile,{run:bin=>{calls.push(bin);return unavailable;}});assert.equal(noRoute.flowId,'4201a3');assert.equal(noRoute.route,null);assert.deepEqual(calls,['flow']);
calls=[];assert.throws(()=>submitStart(profile,{run:bin=>{calls.push(bin);const error=Error('exit1');error.stdout='StartRejected.ContextRefused.SystemTooLarge';throw error;}}),/StartRejected.ContextRefused.SystemTooLarge/);assert.deepEqual(calls,['flow']);
for (const reply of ['LaunchPending.{ unknown }','StartRejected.AddressAwake','StartAmbiguous.{ unknown }']) {calls=[];assert.throws(()=>submitStart(profile,{run:(bin,args)=>{calls.push(bin);return reply;}}));assert.deepEqual(calls,['flow']);}
calls=[];assert.throws(()=>submitStart(profile,{run:bin=>{calls.push(bin);throw Error('transport failed');}}),/inspect LaunchStatus/);assert.deepEqual(calls,['flow']);
calls=[];assert.throws(()=>submitStart(profile,{run:bin=>{calls.push(bin);if(bin==='flow')return success;if(bin==='herdr')return present;throw Error('register failed');}}),/without starting another flow/);assert.deepEqual(calls,['flow','herdr','hm-register','herdr']);

for (const throws of [false,true]) {
 calls=[];
 const result=submitStart(profile,{run:bin=>{calls.push(bin);if(bin==='flow')return success;if(bin==='herdr'){if(!throws)return gone;const e=Error('missing');e.stdout=gone;throw e;}throw Error('dead pane must not register');}});
 assert.equal(result.flowId,'4201a3');assert.equal(result.route,null);assert.equal(result.reachability,'flow-queue-only');assert.equal(result.registered,false);assert.equal(result.historicalRoute.pane,'w1:p4E');assert.deepEqual(calls,['flow','herdr']);
}
calls=[];let inspections=0;
const raced=submitStart(profile,{run:bin=>{calls.push(bin);if(bin==='flow')return success;if(bin==='herdr')return ++inspections===1?present:gone;throw Error('pane closed during registration');}});
assert.equal(raced.reachability,'flow-queue-only');assert.deepEqual(calls,['flow','herdr','hm-register','herdr']);
for (const response of ['not JSON',JSON.stringify({error:{code:'transport_error'}}),JSON.stringify({result:{agent:{pane_id:'other',terminal_id:'term_123'}}}),JSON.stringify({result:{agent:{pane_id:'w1:p4E',terminal_id:'reused'}}})]) {
 calls=[];assert.throws(()=>submitStart(profile,{run:bin=>{calls.push(bin);return bin==='flow'?success:response;}}),/without starting another flow/);assert.equal(calls.filter(x=>x==='flow').length,1);assert(!calls.includes('hm-register'));
}

const workspace=fs.mkdtempSync(path.join(os.tmpdir(),'flow-adapter-'));try {
 fs.mkdirSync(path.join(workspace,'flows','4201a3'),{recursive:true});
 const brief=path.join(workspace,'task.txt'),meta=path.join(workspace,'declaration.edn');fs.writeFileSync(brief,'READ THIS TASK ONCE');fs.writeFileSync(meta,'{:aspect :Psyche :topic :core :layer :Tertiary}');
 const config={shared:{'first-response-timeout-seconds':900,'first-prompt-template':'OUTSIDE CONTEXT MUST NOT BE USED'},aspects:[{aspect:'Psyche',harness:'claude',voices:[{layer:'Tertiary',model:'claude-sonnet-5-5',effort:'medium'}],modules:{system:['spirit-core','intent-psyche'],user:['compensation-correction']}}],metaflow:{metaflows:[{aspect:'Psyche',topic:'Core',layer:'Tertiary',modules:[], 'user-modules':['compensation-correction'],'topic-context':'OUTSIDE CONTEXT MUST NOT BE USED'}]}};
 const o=parseArgs(['--brief',brief,'--layer','Tertiary','--root','--metaflow',meta,'--workspace',workspace,'--topic','core','--launch-request-id','proof-1'],'claude');calls=[];
 launchMain(o,'claude',{config,run:(bin,args)=>{calls.push({bin,args});return bin==='flow'?success:bin==='herdr'?present:'registered';},log:()=>{}});
 assert.equal(calls.length,3);assert.equal(calls[0].bin,'flow');assert.match(calls[0].args[0],/Address\.\{ Psyche core Tertiary \}/);assert.match(calls[0].args[0],/READ THIS TASK ONCE/);assert.doesNotMatch(calls[0].args[0],/OUTSIDE CONTEXT/);
 const continuation=JSON.parse(fs.readFileSync(path.join(workspace,'flows','4201a3','continuation.json')));assert.equal(continuation.topic,'core');assert.equal(continuation.nativeSessionId,uuid);
 fs.unlinkSync(path.join(workspace,'flows','4201a3','continuation.json'));
 fs.mkdirSync(path.join(workspace,'flows','abcdef'));
 config.aspects[0].voices.push({layer:'Primary',model:'claude-fable-5-1',effort:'medium'},{layer:'Secondary',model:'claude-opus-5-5',effort:'medium'});
 config.metaflow.metaflows.push({aspect:'Psyche',topic:'Core',layer:'Primary',modules:[]},{aspect:'Psyche',topic:'Core',layer:'Secondary',modules:[]});
 calls=[];
 launchMain({...o,layer:'Primary'},'claude',{config,run:(bin,args)=>{
   calls.push({bin,args});
   if(bin==='herdr')return args.includes('list')?JSON.stringify({result:{agents:[]}}):present;
   if(bin==='flow')return args[0].includes('core Secondary')?success.replace('4201a3 '+uuid,'abcdef '+uuid):success;
   return 'registered';
 },log:()=>{}});
 assert.deepEqual(calls.map(c=>c.bin),['herdr','flow','herdr','hm-register','flow','herdr','hm-register']);
 assert.match(calls[1].args[0],/proof-1-secondary/);
 assert.match(calls[1].args[0],/core Secondary/);
 assert.match(calls[4].args[0],/core Primary/);
 assert.doesNotMatch(calls[1].args[0],/OUTSIDE CONTEXT/);
 assert.throws(()=>parseArgs(['--brief',brief,'--layer','Tertiary','--root','--metaflow',meta,'--system-prompt-file',brief],'claude'),/unsupported/);
} finally {fs.rmSync(workspace,{recursive:true,force:true});}
console.log('Flow Start adapter request, identity, registration and failure checks passed');
