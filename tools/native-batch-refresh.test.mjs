#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';

const dir=fs.mkdtempSync(path.join(os.tmpdir(),'native-batch-refresh-'));
const root=path.resolve(import.meta.dirname,'..');
const batch=path.join(import.meta.dirname,'native-batch-refresh.mjs');
const launcher=path.join(import.meta.dirname,'native-seat-launch.mjs');
const audited=(source='Vision/flowNexus.md')=>({nativeTitle:'Fixture native title',sourceAudit:{reviewedAt:'2026-09-21T00:00:00Z',newestApplicableVision:[source]}});
const call=(tool,args,env={})=>spawnSync(process.execPath,[tool,...args],{cwd:root,encoding:'utf8',env:{...process.env,...env}});
const profile=path.join(dir,'mind-terra.json');
fs.writeFileSync(profile,JSON.stringify({name:'mind-terra',model:'gpt-5.6-terra',effort:'low',role:'Mind Terra',predecessor:'0ab019',ancestor:'0ab019',skills:['spirit','main-flow','refresh','psyche'],sourceManifest:['Vision/flowNexus.md'],...audited()}));
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
const claude={name:'mind-sonnet',model:'claude-sonnet-5',effort:'medium',role:'Mind Sonnet',predecessor:'0ab019',skills:['spirit','main-flow','refresh','psyche'],sources:[{path:source,sha256:sha}],modelCatalog:[{id:'claude-sonnet-5',family:'sonnet'}],...audited(source)};
fs.writeFileSync(claudeProfile,JSON.stringify(claude));
data.seats=[{harness:'claude',profile:'mind-sonnet',profileFile:claudeProfile,predecessor:'0ab019',agent:'mind_sonnet',label:'Mind Sonnet'}];fs.writeFileSync(manifest,JSON.stringify(data));
result=call(batch,['start','--manifest',manifest,'--state',state],{HERDR_ENV:''});
assert.match(result.stderr,/Herdr-managed pane required/);
claude.model='claude-haiku-4-5-20251001';fs.writeFileSync(claudeProfile,JSON.stringify(claude));
result=call(batch,['start','--manifest',manifest,'--state',state],{HERDR_ENV:'1'});
assert.notEqual(result.status,0);assert.match(result.stderr,/haiku model absent/);
for (const [model,family] of [['claude-opus-4-6[1m]','opus'],['claude-fable-5-1[1m]','fable']]) {
  claude.model=model;
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
fs.writeFileSync(freshProfile,JSON.stringify({name:'fresh-luna',model:'gpt-5.6-luna',effort:'low',role:'Fresh Luna',fresh:true,predecessor:null,ancestor:null,skills:['spirit','main-flow','refresh','psyche'],sourceManifest:[source],...audited(source)}));
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
  *) exit 8;;
esac
`,{mode:0o755});
const parallel=path.join(dir,'parallel.json');
const seats=['alpha','beta'].map(agent=>({harness:'codex',profile:'mind-terra',predecessor:'0ab019',agent,label:agent==='alpha'?'Alpha':'Beta',model:'gpt-5.6-terra',effort:'low'}));
fs.writeFileSync(parallel,JSON.stringify({version:1,manifest:{version:1,session:'fixture',workspace:'w1',cwd:root,seats},seats:seats.map(s=>({agent:s.agent,profile:s.profile,predecessor:s.predecessor,phase:'queued'}))}));
result=call(batch,['worker','--state',parallel],{HERDR_ENV:'1',PATH:`${bin}:${process.env.PATH}`});
assert.equal(result.status,0,result.stderr);
assert.deepEqual(fs.readFileSync(arrivals,'utf8').trim().split('\n').sort(),['alpha','beta']);
assert.ok(JSON.parse(fs.readFileSync(parallel,'utf8')).seats.every(s=>s.phase==='failed'&&/Session|UUID/.test(s.error)), 'both agent starts cleared the barrier before native ID refusal');
console.log('native batch refresh fixtures passed');
