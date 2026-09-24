#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {mainSeatLaunchArgs} from './native-batch-refresh.mjs';

const dir=fs.mkdtempSync(path.join(os.tmpdir(),'native-batch-refresh-'));
const root=path.resolve(import.meta.dirname,'..');
const batch=path.join(import.meta.dirname,'native-batch-refresh.mjs');
const launcher=path.join(import.meta.dirname,'native-seat-launch.mjs');
const systemPrompt=path.join(import.meta.dirname,'main-flow-mode','system-prompt.md');
const audited=(source='Vision/flowNexus.md')=>({sourceAudit:{reviewedAt:'2026-09-21T00:00:00Z',newestApplicableVision:[source]}});
const call=(tool,args,env={})=>spawnSync(process.execPath,[tool,...args],{cwd:root,encoding:'utf8',env:{...process.env,...env}});
const helperDir=path.join(dir,'launch-args');fs.mkdirSync(helperDir);
const claudeMain=mainSeatLaunchArgs({harness:'claude',model:'claude-haiku-4-5-20251001',effort:'medium',nativeThreadId:'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee',launchTitle:'Psyche Haiku 4.5 (claim pending)',jobDir:helperDir,mainSeat:true,reminderEvery:4});
assert.ok(claudeMain.includes('--system-prompt-file'));
assert.ok(claudeMain.includes('--dangerously-skip-permissions'));
assert.equal(claudeMain[claudeMain.indexOf('--system-prompt-file')+1],systemPrompt);
assert.ok(!claudeMain.includes('--append-system-prompt-file'));
assert.ok(!claudeMain.includes('--append-system-prompt'));
const claudeSettings=JSON.parse(fs.readFileSync(claudeMain[claudeMain.indexOf('--settings')+1],'utf8'));
const reminderHandler=claudeSettings.hooks.UserPromptSubmit[0].hooks[0];
const reminderRuns=[1,2,3,4].map(()=>spawnSync('sh',['-c',reminderHandler.command],{input:JSON.stringify({hook_event_name:'UserPromptSubmit',session_id:'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee'}),encoding:'utf8'}));
assert.deepEqual(reminderRuns.map(run=>run.status),[0,0,0,0],reminderRuns.map(run=>run.stderr).join(''));
assert.deepEqual(reminderRuns.map(run=>Boolean(run.stdout.trim())),[false,false,false,true],'main seat reminder fires on the configured prompt count');
assert.match(JSON.parse(reminderRuns[3].stdout).hookSpecificOutput.additionalContext,/^You are a main flow/);
const defaultCadence=mainSeatLaunchArgs({harness:'claude',model:'claude-haiku-4-5-20251001',effort:'medium',nativeThreadId:'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee',launchTitle:'Psyche Haiku 4.5 (claim pending)',jobDir:path.join(helperDir,'default'),mainSeat:true});
assert.match(JSON.parse(fs.readFileSync(defaultCadence[defaultCadence.indexOf('--settings')+1],'utf8')).hooks.UserPromptSubmit[0].hooks[0].command,/--every 20$/);
const claudeWorker=mainSeatLaunchArgs({harness:'claude',model:'claude-haiku-4-5-20251001',effort:'medium',nativeThreadId:'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee',launchTitle:'worker',mainSeat:false});
assert.ok(!claudeWorker.includes('--system-prompt-file'),'subagent launch keeps the stock Claude prompt');
assert.throws(()=>mainSeatLaunchArgs({harness:'codex',model:'gpt-5.6-terra',effort:'low',stateDir:path.join(helperDir,'codex'),mainSeat:true,reminderEvery:4}),/Codex main launch requires native-seat-launch startup block/);
const codexWorker=mainSeatLaunchArgs({harness:'codex',model:'gpt-5.6-terra',effort:'low',mainSeat:false});
assert.ok(!codexWorker.some(value=>value.startsWith('model_instructions_file=')),'subagent launch keeps the stock Codex prompt');
assert.throws(()=>mainSeatLaunchArgs({harness:'codex',model:'gpt-5.6-terra',effort:'low',stateDir:helperDir,mainSeat:true,promptFile:path.join(dir,'missing.md')}),/Codex main launch requires native-seat-launch startup block/);
const nativeId='aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee';
let environmentPlan=call(batch,['environment-plan','--native-id',nativeId]);
assert.equal(environmentPlan.status,0,environmentPlan.stderr);
const isolation=JSON.parse(environmentPlan.stdout);
assert.equal(isolation.nativeThreadId,nativeId);
assert.ok(isolation.jobDir.endsWith(`/native-${nativeId}`));
assert.match(isolation.marker,new RegExp(`^CLAUDE_ENV_READY_${nativeId}_[a-f0-9]{24}$`));
assert.ok(!isolation.shellCommand.includes(isolation.marker),'echoed shell input must not contain the complete marker');
const contaminated={...process.env,CLAUDE_JOB_DIR:'/tmp/another-claude-job',
  CLAUDE_CODE_SESSION_ID:'108ab020-3394-4fe2-8ae3-304ea1d20843',
  CLAUDE_CODE_SESSION_KIND:'bg',CLAUDE_CODE_CHILD_SESSION:'1'};
// The command is POSIX shell syntax; the repository Nix fixture closure has sh.
// A separate focused remote derivation also executes this through zsh.
const shell=spawnSync('sh',['-c',`${isolation.shellCommand} && printf 'JOB=%s\\nSESSION=%s\\nKIND=%s\\nCHILD=%s\\n' "$CLAUDE_JOB_DIR" "\${CLAUDE_CODE_SESSION_ID-unset}" "\${CLAUDE_CODE_SESSION_KIND-unset}" "\${CLAUDE_CODE_CHILD_SESSION-unset}"`],{encoding:'utf8',env:contaminated});
assert.equal(shell.status,0,shell.stderr);
assert.ok(shell.stdout.includes(isolation.marker));
assert.match(shell.stdout,new RegExp(`JOB=${isolation.jobDir.replaceAll('/','\\/')}`));
assert.match(shell.stdout,/SESSION=unset/);
assert.match(shell.stdout,/KIND=unset/);
assert.match(shell.stdout,/CHILD=unset/);
const profile=path.join(dir,'mind-terra.json');
fs.writeFileSync(profile,JSON.stringify({name:'mind-terra',model:'gpt-5.6-terra',effort:'low',role:'Mind Low',predecessor:'0ab019',ancestor:'0ab019',skills:['spirit','main-flow','refresh','psyche','testing-flow-titles'],sourceManifest:['Vision/flowNexus.md'],...audited()}));
let result=call(launcher,['--seat','mind-terra','--profile-file',profile,'--predecessor','0ab019']);
assert.equal(result.status,0,result.stderr);
const plan=JSON.parse(result.stdout);
assert.equal(plan.model,'gpt-5.6-terra'); assert.equal(plan.effort,'low'); assert.equal(plan.predecessor,'0ab019'); assert.ok(plan.profileSha256);
result=call(launcher,['--seat','mind-terra','--profile-file',profile,'--predecessor','98ac2e']);
assert.notEqual(result.status,0); assert.match(result.stderr,/exact predecessor/);
const manifest=path.join(dir,'manifest.json'), state=path.join(dir,'state.json');
const data={version:1,session:'fixture',workspace:'w1',cwd:root,seats:[{harness:'codex',profile:'mind-terra',profileFile:profile,predecessor:'0ab019',agent:'mind_terra_0ab019',label:'Mind Terra'}]};
fs.writeFileSync(manifest,JSON.stringify(data));
result=call(batch,['validate','--manifest',manifest],{HERDR_ENV:''});
assert.equal(result.status,0,result.stderr);
assert.equal(JSON.parse(result.stdout).seats,1);
result=call(batch,['start','--manifest',manifest,'--state',state],{HERDR_ENV:''});
assert.notEqual(result.status,0); assert.match(result.stderr,/Herdr-managed pane required/); assert.equal(fs.existsSync(state),false);
data.seats.push({...data.seats[0],agent:'mind_terra_0ab019'});fs.writeFileSync(manifest,JSON.stringify(data));
result=call(batch,['start','--manifest',manifest,'--state',state],{HERDR_ENV:'1'});
assert.notEqual(result.status,0); assert.match(result.stderr,/duplicate agent/); assert.equal(fs.existsSync(state),false);
data.seats=[{...data.seats[0],harness:'claude'}];fs.writeFileSync(manifest,JSON.stringify(data));
result=call(batch,['start','--manifest',manifest,'--state',state],{HERDR_ENV:'1'});
assert.notEqual(result.status,0); assert.match(result.stderr,/Claude profile identity/); assert.equal(fs.existsSync(state),false);
const source='Vision/flowNexus.md';
const sha=(await import('node:crypto')).createHash('sha256').update(fs.readFileSync(path.join(root,source))).digest('hex');
const claudeProfile=path.join(dir,'claude.json');
const claude={name:'mind-sonnet',model:'claude-sonnet-5',effort:'medium',role:'Mind Medium',titlePlan:{aspect:'Mind',power:'Medium',model:'Sonnet 5',afterOwnVerifiedFlowId:true,template:'Mind Sonnet 5 <FLOW_ID>'},predecessor:'0ab019',skills:['spirit','main-flow','refresh','psyche','testing-flow-titles'],sources:[{path:source,sha256:sha}],modelCatalog:[{id:'claude-sonnet-5',family:'sonnet'}],...audited(source)};
fs.writeFileSync(claudeProfile,JSON.stringify(claude));
data.seats=[{harness:'claude',profile:'mind-sonnet',profileFile:claudeProfile,predecessor:'0ab019',agent:'mind_sonnet',label:'Mind Sonnet'}];fs.writeFileSync(manifest,JSON.stringify(data));
result=call(batch,['start','--manifest',manifest,'--state',state],{HERDR_ENV:''});
assert.match(result.stderr,/Herdr-managed pane required/);
claude.model='claude-haiku-4-5-20251001';claude.titlePlan={aspect:'Mind',power:'Medium',model:'Haiku 4.5',afterOwnVerifiedFlowId:true,template:'Mind Haiku 4.5 <FLOW_ID>'};fs.writeFileSync(claudeProfile,JSON.stringify(claude));
result=call(batch,['start','--manifest',manifest,'--state',state],{HERDR_ENV:'1'});
assert.notEqual(result.status,0);assert.match(result.stderr,/haiku model absent/);
for (const [model,family] of [['claude-opus-4-6[1m]','opus'],['claude-fable-5-1[1m]','fable']]) {
  claude.model=model;
  const display=model.includes('opus')?'OldOpus 4.6 1m':'Fable';
  claude.titlePlan={aspect:'Mind',power:'Medium',model:display,afterOwnVerifiedFlowId:true,template:`Mind ${display} <FLOW_ID>`};
  claude.modelCatalog=[{id:model,family}];
  fs.writeFileSync(claudeProfile,JSON.stringify(claude));
  result=call(batch,['start','--manifest',manifest,'--state',state],{HERDR_ENV:''});
  assert.notEqual(result.status,0);
  assert.match(result.stderr,/Herdr-managed pane required/);
  assert.equal(fs.existsSync(state),false);
}
claude.modelCatalog=[{id:'claude-fable-5-1[1m]',family:'opus'}];
fs.writeFileSync(claudeProfile,JSON.stringify(claude));
result=call(batch,['start','--manifest',manifest,'--state',state],{HERDR_ENV:'1'});
assert.notEqual(result.status,0);assert.match(result.stderr,/fable model absent/);
const freshProfile=path.join(dir,'fresh-luna.json');
fs.writeFileSync(freshProfile,JSON.stringify({name:'fresh-luna',model:'gpt-5.6-luna',effort:'low',role:'Psyche Low',fresh:true,predecessor:null,ancestor:null,skills:['spirit','main-flow','refresh','psyche','testing-flow-titles'],sourceManifest:[source],...audited(source)}));
data.seats=[{harness:'codex',profile:'fresh-luna',profileFile:freshProfile,fresh:true,predecessor:null,agent:'fresh_luna',label:'Fresh Luna'}];fs.writeFileSync(manifest,JSON.stringify(data));
result=call(batch,['start','--manifest',manifest,'--state',state],{HERDR_ENV:''});
assert.match(result.stderr,/Herdr-managed pane required/);
fs.writeFileSync(state,JSON.stringify({version:1,createdAt:'fixture',seats:[{agent:'mind_terra_0ab019',profile:'mind-terra',predecessor:'0ab019',phase:'native-pending',nativeThreadId:'01a0bf90-41fd-72a1-ac8b-ee9c1dab9a41'}]}));
result=call(batch,['status','--state',state]); assert.equal(result.status,0,result.stderr);
const status=JSON.parse(result.stdout);assert.equal(status.allNativeVerified,false);assert.equal(status.acceptance,'unwitnessed');assert.equal(status.predecessorReaping,'disabled');assert.equal(status.seats[0].phase,'native-pending');assert.doesNotMatch(result.stdout,/01a0bf90-41fd/);
// Both Herdr starts must be in flight together. Each fake start waits for the
// other; a serialized worker would time out on the first seat.
const bin=path.join(dir,'bin');fs.mkdirSync(bin);
const arrivals=path.join(dir,'arrivals');
fs.writeFileSync(path.join(bin,'herdr'),`#!/bin/sh
case " $* " in
  *" tab create "*)
    case " $* " in *" Alpha "*) p=a;; *) p=b;; esac
    printf '{"result":{"root_pane":{"pane_id":"w1:p%s","terminal_id":"term_%s"}}}\\n' "$p" "$p";;
  *" agent start "*)
    case " $* " in *" alpha "*) n=alpha;p=a;; *) n=beta;p=b;; esac
    printf '%s\\n' "$n" >> ${JSON.stringify(arrivals)}
    i=0; while [ "$(wc -l < ${JSON.stringify(arrivals)})" -lt 2 ] && [ "$i" -lt 30 ]; do sleep 0.1; i=$((i+1)); done
    if [ "$i" -ge 30 ]; then exit 9; fi
    printf '{"result":{"agent":{"name":"%s","pane_id":"w1:p%s","terminal_id":"term_%s","agent":"codex","cwd":"${root}","interactive_ready":true}}}\\n' "$n" "$p" "$p";;
  *" pane read "*) printf 'no session yet\\n';;
  *" pane process-info "*)
    case " $* " in *" w1:pa "*) p=a;; *) p=b;; esac
    printf '{"result":{"process_info":{"pane_id":"w1:p%s","foreground_processes":[]}}}\\n' "$p";;
  *) exit 8;;
esac
`,{mode:0o755});
const parallel=path.join(dir,'parallel.json');
const seats=['alpha','beta'].map(agent=>({harness:'codex',profile:'mind-terra',predecessor:'0ab019',agent,label:agent==='alpha'?'Alpha':'Beta',model:'gpt-5.6-terra',effort:'low'}));
fs.writeFileSync(parallel,JSON.stringify({version:1,manifest:{version:1,session:'fixture',workspace:'w1',cwd:root,seats},seats:seats.map(s=>({agent:s.agent,profile:s.profile,predecessor:s.predecessor,phase:'queued'}))}));
result=call(batch,['worker','--state',parallel],{HERDR_ENV:'1',PATH:`${bin}:${process.env.PATH}`});
assert.equal(result.status,0,result.stderr);
assert.equal(fs.existsSync(arrivals),false,'the batch controller must not start a Codex main without a verified startup-block injector');
assert.ok(JSON.parse(fs.readFileSync(parallel,'utf8')).seats.every(s=>s.phase==='failed'&&/Codex main launch requires native-seat-launch startup block/.test(s.error)), 'every Codex main is rejected before a Herdr agent start');
// pane run is an action that can succeed with empty stdout. The structured
// wait-output witness, not JSON from pane run, proves environment preparation.
const claudeBin=path.join(dir,'claude-bin');fs.mkdirSync(claudeBin);
const calls=path.join(dir,'claude-calls');
fs.writeFileSync(path.join(claudeBin,'herdr'),`#!/bin/sh
printf '%s\n' "$*" >> ${JSON.stringify(calls)}
case " $* " in
  *" tab create "*) printf '{"result":{"root_pane":{"pane_id":"w1:p8","terminal_id":"term_fixture"}}}\n';;
  *" pane run "*) exit 0;;
  *" pane wait-output "*) case " $* " in *" --source visible "*) ;; *) exit 25;; esac
    while [ "$#" -gt 0 ]; do if [ "$1" = --match ]; then shift; marker="$1"; break; fi; shift; done
    if [ -n "$HERDR_STALE_MARKER" ]; then marker="\${marker%_*}"; fi
    printf '{"result":{"pane_id":"w1:p8","matched_line":"%s"}}\n' "$marker";;
  *" agent start "*) exit 23;;
  *) exit 24;;
esac
`,{mode:0o755});
const clProfile=path.join(dir,'valid-claude.json');
const cl={name:'fresh-claude',model:'claude-haiku-4-5-20251001',effort:'medium',role:'Psyche Ultra Low',
  titlePlan:{aspect:'Psyche',power:'Ultra Low',model:'Haiku 4.5',afterOwnVerifiedFlowId:true,template:'Psyche Haiku 4.5 <FLOW_ID>'},
  fresh:true,predecessor:null,skills:['spirit','main-flow','refresh','psyche','testing-flow-titles'],
  sources:[{path:source,sha256:sha}],modelCatalog:[{id:'claude-haiku-4-5-20251001',family:'haiku'}],...audited(source)};
fs.writeFileSync(clProfile,JSON.stringify(cl));
const clSeat={harness:'claude',profile:'fresh-claude',profileFile:clProfile,profileSha256:(await import('node:crypto')).createHash('sha256').update(fs.readFileSync(clProfile)).digest('hex'),
  claudeProfile:cl,fresh:true,predecessor:null,agent:'fresh_claude',label:'Psyche Ultra Low',model:cl.model,effort:cl.effort};
const clData={version:1,session:'fixture',workspace:'w1',cwd:root,seats:[clSeat]};
const clState=path.join(dir,'claude-state.json');
fs.writeFileSync(clState,JSON.stringify({version:1,manifest:clData,seats:[{agent:clSeat.agent,profile:clSeat.profile,predecessor:null,phase:'queued'}]}));
result=call(batch,['worker','--state',clState],{HERDR_ENV:'1',HOME:dir,PATH:`${claudeBin}:${process.env.PATH}`});
assert.equal(result.status,0,result.stderr);
const prepared=JSON.parse(fs.readFileSync(clState,'utf8')).seats[0];
assert.equal(prepared.phase,'failed'); assert.match(prepared.error,/herdr exited 23/);
assert.match(prepared.environmentMarker,new RegExp(`^CLAUDE_ENV_READY_${prepared.nativeThreadId}_[a-f0-9]{24}$`));
assert.ok(fs.readFileSync(calls,'utf8').includes('pane run w1:p8'));
const paneRunCall=fs.readFileSync(calls,'utf8').split('\n').find(line=>line.includes('pane run w1:p8'));
assert.ok(!paneRunCall.includes(prepared.environmentMarker),'echoed pane command cannot contain complete expected marker');
assert.ok(fs.readFileSync(calls,'utf8').includes('pane wait-output w1:p8'));
const agentStartCall=fs.readFileSync(calls,'utf8').split('\n').find(line=>line.includes('agent start fresh_claude'));
assert.match(agentStartCall,/--effort medium --name Psyche Haiku 4.5 \(claim pending\) --remote-control --dangerously-skip-permissions --system-prompt-file .*main-flow-mode\/system-prompt\.md --settings .*main-flow-settings\.json$/,
  'Claude native start must establish its provisional title and enable Remote Control in the original launch');
const staleState=path.join(dir,'stale-marker.json');
fs.writeFileSync(staleState,JSON.stringify({version:1,manifest:clData,seats:[{agent:clSeat.agent,profile:clSeat.profile,predecessor:null,phase:'queued'}]}));
const staleBefore=fs.readFileSync(calls,'utf8');
result=call(batch,['worker','--state',staleState],{HERDR_ENV:'1',HOME:dir,PATH:`${claudeBin}:${process.env.PATH}`,HERDR_STALE_MARKER:'1'});
assert.equal(result.status,0,result.stderr);
assert.match(JSON.parse(fs.readFileSync(staleState,'utf8')).seats[0].error,/environment preparation was not witnessed/);
assert.doesNotMatch(fs.readFileSync(calls,'utf8').slice(staleBefore.length),/agent start/);
const beforeCalls=fs.readFileSync(calls,'utf8');
result=call(batch,['worker','--state',clState],{HERDR_ENV:'1',HOME:dir,PATH:`${claudeBin}:${process.env.PATH}`});
assert.notEqual(result.status,0);assert.match(result.stderr,/fresh queued state/);
assert.equal(fs.readFileSync(calls,'utf8'),beforeCalls,'failed worker cannot create another tab or UUID');
// A continuation is a new ledger referencing the immutable failed pre-start
// attempt. It must reuse its pane and UUID; it never calls tab create.
const failedFile=path.join(dir,'failed-pre-start.json');
const originalData=structuredClone(clData);
originalData.seats[0].model='claude-haiku-4-5';
originalData.seats[0].claudeProfile.model='claude-haiku-4-5';
const failed={version:1,manifest:originalData,seats:[{agent:clSeat.agent,profile:clSeat.profile,predecessor:null,
  phase:'failed',paneId:'w1:p8',terminalId:'term_fixture',nativeThreadId:prepared.nativeThreadId,
  error:'Unexpected end of JSON input'}]};
fs.writeFileSync(failedFile,JSON.stringify(failed));
const clManifest=path.join(dir,'claude-manifest.json');fs.writeFileSync(clManifest,JSON.stringify(clData));
fs.writeFileSync(path.join(claudeBin,'claude'),`#!/bin/sh
[ "$1 $2" = "agents --json" ] || exit 1
if [ -n "$CLAUDE_AGENTS_EXISTING" ]; then printf '{"agents":[{"sessionId":"%s"}]}\n' "$CLAUDE_AGENTS_EXISTING"; else printf '[]\n'; fi
`,{mode:0o755});
fs.writeFileSync(path.join(claudeBin,'herdr'),`#!/bin/sh
printf '%s\n' "$*" >> ${JSON.stringify(calls)}
case " $* " in
  *" pane get w1:p8 "*) printf '{"result":{"pane":{"pane_id":"w1:p8","terminal_id":"term_fixture","workspace_id":"w1","cwd":"${root}"}}}\n';;
  *" pane process-info --pane w1:p8 "*) printf '{"result":{"process_info":{"pane_id":"w1:p8","foreground_processes":[{"name":"zsh","pid":1234}]}}}\n';;
  *" agent list "*) printf '{"result":{"agents":[]}}\n';;
  *" pane run w1:p8 "*) exit 0;;
  *" pane wait-output "*) case " $* " in *" --source visible "*) ;; *) exit 25;; esac
    while [ "$#" -gt 0 ]; do if [ "$1" = --match ]; then shift; marker="$1"; break; fi; shift; done
    printf '{"result":{"pane_id":"w1:p8","matched_line":"%s"}}\n' "$marker";;
  *" agent start "*) exit 23;;
  *) exit 24;;
esac
`,{mode:0o755});
const continuation=path.join(dir,'continuation','state.json');
const runEnv={HERDR_ENV:'1',HOME:dir,PATH:`${claudeBin}:${process.env.PATH}`};
result=call(batch,['continue-retained','--failed-state',failedFile,'--manifest',clManifest,'--state',continuation,'--expected-current-model',cl.model],runEnv);
assert.equal(result.status,0,result.stderr);
let continued;
for(let i=0;i<100;i++) {
  continued=JSON.parse(fs.readFileSync(continuation,'utf8')).seats[0];
  if(continued.phase==='failed') break;
  await new Promise(resolve=>setTimeout(resolve,20));
}
assert.equal(continued.phase,'failed');assert.match(continued.error,/herdr exited 23/);
assert.equal(continued.paneId,'w1:p8');assert.equal(continued.nativeThreadId,prepared.nativeThreadId);
assert.deepEqual(continued.retained.profileTransition.priorModel,'claude-haiku-4-5');
assert.deepEqual(continued.retained.profileTransition.currentModel,'claude-haiku-4-5-20251001');
const afterCalls=fs.readFileSync(calls,'utf8').slice(beforeCalls.length);
assert.doesNotMatch(afterCalls,/tab create/);
assert.match(afterCalls,/pane get w1:p8/);
const digest=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const timeoutFile=path.join(dir,'failed-marker-timeout.json');
const timeoutFailure={version:1,manifest:clData,seats:[{agent:clSeat.agent,profile:clSeat.profile,predecessor:null,
  phase:'failed',paneId:'w1:p8',terminalId:'term_fixture',nativeThreadId:prepared.nativeThreadId,
  error:'herdr exited 1: {"error":{"code":"timeout","message":"timed out waiting for output match"},"id":"cli:pane:wait-output"}',
  retained:{failedStatePath:failedFile,failedStateSha256:digest(fs.readFileSync(failedFile)),paneId:'w1:p8',
    terminalId:'term_fixture',nativeThreadId:prepared.nativeThreadId}}]};
fs.writeFileSync(timeoutFile,JSON.stringify(timeoutFailure));
const afterTimeout=path.join(dir,'after-timeout','state.json');
result=call(batch,['continue-retained','--failed-state',timeoutFile,'--manifest',clManifest,'--state',afterTimeout,'--expected-current-model',cl.model],runEnv);
assert.equal(result.status,0,result.stderr);
let afterTimeoutSeat;
for(let i=0;i<100;i++) {
  afterTimeoutSeat=JSON.parse(fs.readFileSync(afterTimeout,'utf8')).seats[0];
  if(afterTimeoutSeat.phase==='failed') break;
  await new Promise(resolve=>setTimeout(resolve,20));
}
assert.equal(afterTimeoutSeat.phase,'failed');assert.match(afterTimeoutSeat.error,/herdr exited 23/);
assert.equal(afterTimeoutSeat.nativeThreadId,prepared.nativeThreadId);
const collision=path.join(dir,'collision','state.json');
const collisionBefore=fs.readFileSync(calls,'utf8');
result=call(batch,['continue-retained','--failed-state',failedFile,'--manifest',clManifest,'--state',collision,'--expected-current-model',cl.model],
  {...runEnv,CLAUDE_AGENTS_EXISTING:prepared.nativeThreadId});
assert.equal(result.status,0,result.stderr);
let collisionSeat;
for(let i=0;i<100;i++) {
  collisionSeat=JSON.parse(fs.readFileSync(collision,'utf8')).seats[0];
  if(collisionSeat.phase==='failed') break;
  await new Promise(resolve=>setTimeout(resolve,20));
}
assert.equal(collisionSeat.phase,'failed');assert.match(collisionSeat.error,/Claude session already exists/);
assert.doesNotMatch(fs.readFileSync(calls,'utf8').slice(collisionBefore.length),/pane run|agent start/);
const refused=path.join(dir,'refused','state.json');
failed.seats[0].error='different failure';fs.writeFileSync(failedFile,JSON.stringify(failed));
result=call(batch,['continue-retained','--failed-state',failedFile,'--manifest',clManifest,'--state',refused,'--expected-current-model',cl.model],runEnv);
assert.notEqual(result.status,0);assert.equal(fs.existsSync(refused),false);
console.log('native batch refresh fixtures passed');
