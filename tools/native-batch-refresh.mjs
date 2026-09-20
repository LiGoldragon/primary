#!/usr/bin/env node
// One-command, Herdr-first native refresh.  This controller never retires a seat.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawn, execFileSync} from 'node:child_process';

const root = path.resolve(import.meta.dirname, '..');
const launcher = path.join(import.meta.dirname, 'native-seat-launch.mjs');
const argv = process.argv.slice(2);
const action = argv[0];
const value = flag => { const i=argv.indexOf(flag); return i<0 ? undefined : argv[i+1]; };
const now = () => new Date().toISOString();
const hash = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const flowId = /^[a-f0-9]{6}$/;
const namePattern = /^[a-z][a-z0-9_-]{0,31}$/;
const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
function fail(message) { throw new Error(message); }
function atomic(file, body) { fs.mkdirSync(path.dirname(file),{recursive:true}); const tmp=`${file}.${process.pid}.tmp`; fs.writeFileSync(tmp,JSON.stringify(body,null,2)+'\n',{mode:0o600}); fs.renameSync(tmp,file); }
function read(file) { return JSON.parse(fs.readFileSync(file,'utf8')); }
function command(binary,args,opts={}) { return execFileSync(binary,args,{cwd:root,encoding:'utf8',timeout:opts.timeout??30000,maxBuffer:4*1024*1024}); }
async function herdr(session,...args) { const body=JSON.parse(await run('herdr',['--session',session,...args])); return body.result??body; }
function manifest(file) {
  const data=read(file);
  if(data.version!==1 || !Array.isArray(data.seats) || !data.seats.length) fail('manifest requires version 1 and a nonempty seats array');
  if(!data.session || !data.workspace) fail('manifest requires explicit Herdr session and workspace ID');
  if(!data.cwd || path.resolve(data.cwd)!==root) fail('manifest cwd must be this checkout');
  const seen=new Set();
  for(const seat of data.seats) {
    if(!seat.profile || !seat.predecessor || !flowId.test(seat.predecessor) || !namePattern.test(seat.agent) || !seat.label) fail('each seat requires profile, six-hex predecessor, valid agent name, and tab label');
    if(seat.harness!=='codex') fail(`unsupported harness for ${seat.agent}; native Claude adapter is not implemented`);
    if(seen.has(seat.agent)) fail(`duplicate agent name: ${seat.agent}`); seen.add(seat.agent);
    const profileArgs=[];
    if(seat.profileFile) { seat.profileFile=path.resolve(seat.profileFile); if(!fs.existsSync(seat.profileFile)) fail(`missing profile file: ${seat.agent}`); seat.profileSha256=hash(seat.profileFile); profileArgs.push('--profile-file',seat.profileFile); }
    // Plan evaluation validates the audited source bundle and typed skill list.
    const plan=JSON.parse(command(process.execPath,[launcher,'--seat',seat.profile,'--predecessor',seat.predecessor,'--cwd',root,...profileArgs]));
    if(plan.predecessor!==seat.predecessor || !plan.requiredSkillNames.includes('main-flow')) fail(`profile ${seat.profile} does not bind predecessor and main-flow`);
    if(seat.model && seat.model!==plan.model) fail(`model differs from audited profile: ${seat.agent}`);
    if(seat.effort && seat.effort!==plan.effort) fail(`effort differs from audited profile: ${seat.agent}`);
    seat.model=plan.model; seat.effort=plan.effort;
  }
  return data;
}
function publicState(state) { return {version:state.version,createdAt:state.createdAt,launchAttemptsSettled:state.seats.every(s=>['native-verified','native-pending','failed'].includes(s.phase)),allNativeVerified:state.seats.every(s=>s.phase==='native-verified'),acceptance:'unwitnessed',predecessorReaping:'disabled',seats:state.seats.map(({agent,profile,predecessor,phase,error})=>({agent,profile,predecessor,phase,...(error?{error}: {})}))}; }
function update(file,agent,patch) { const state=read(file), seat=state.seats.find(s=>s.agent===agent); if(!seat) fail(`unknown ledger seat ${agent}`); Object.assign(seat,patch,{updatedAt:now()}); atomic(file,state); }
async function run(bin,args,opts={}) { return new Promise((resolve,reject)=>{const child=spawn(bin,args,{cwd:root,env:process.env,stdio:['ignore','pipe','pipe']}); let out='',err=''; child.stdout.on('data',d=>out+=d);child.stderr.on('data',d=>err+=d);child.on('error',reject);child.on('close',code=>code===0?resolve(out):reject(new Error(`${path.basename(bin)} exited ${code}: ${err.trim()}`)));}); }
async function launchSeat(file,data,seat) {
  try {
    if(seat.profileFile && hash(seat.profileFile)!==seat.profileSha256) fail('profile changed after manifest validation');
    const tab=await herdr(data.session,'tab','create','--workspace',data.workspace,'--cwd',root,'--label',seat.label,'--no-focus');
    const pane=tab.root_pane??tab.rootPane;
    if(!pane?.pane_id || !pane?.terminal_id) fail('Herdr tab creation lacked pane and terminal IDs');
    update(file,seat.agent,{phase:'pane-created',paneId:pane.pane_id,terminalId:pane.terminal_id});
    const start=await herdr(data.session,'agent','start',seat.agent,'--kind','codex','--pane',pane.pane_id,'--timeout','300000','--','--model',seat.model,'-c',`model_reasoning_effort=${seat.effort}`);
    const agent=start.agent??(await herdr(data.session,'agent','get',seat.agent)).agent;
    if(agent?.name!==seat.agent || agent?.pane_id!==pane.pane_id || agent?.terminal_id!==pane.terminal_id || agent?.interactive_ready!==true) fail('Herdr ready agent does not match new pane');
    update(file,seat.agent,{phase:'herdr-ready'});
    const snapshot=await run('herdr',['--session',data.session,'pane','read',pane.pane_id,'--source','recent','--lines','120','--format','text']);
    const matches=[...snapshot.matchAll(/\bSession:\s*([0-9a-f-]{36})\b/g)].map(m=>m[1]).filter(x=>uuid.test(x));
    if(matches.length!==1) fail('target Herdr pane must display exactly one native session UUID');
    const receipt=path.join(path.dirname(file),'receipts',`${seat.agent}.json`);
    update(file,seat.agent,{phase:'native-identified',nativeThreadId:matches[0],receipt});
    const answer=JSON.parse(await run(process.execPath,[launcher,'--seat',seat.profile,'--predecessor',seat.predecessor,'--cwd',root,...(seat.profileFile?['--profile-file',seat.profileFile]:[]),'--name',seat.agent,'--receipt',receipt,'--expected-runner-sha256',hash(launcher),'--adopt-herdr-thread',matches[0],'--herdr-session',data.session,'--herdr-pane',pane.pane_id,'--herdr-agent',seat.agent,'--herdr-terminal',pane.terminal_id,'--acknowledge-live-launch']));
    const receiptData=read(receipt);
    if(receiptData.threadId!==matches[0] || receiptData.herdr?.paneId!==pane.pane_id || receiptData.herdr?.agentName!==seat.agent) fail('native receipt target binding mismatch');
    update(file,seat.agent,{phase:receiptData.status==='verified' && answer.readiness!=='pending'?'native-verified':'native-pending',nativeReadiness:answer.readiness});
  } catch(error) { update(file,seat.agent,{phase:'failed',error:String(error.message??error)}); }
}
async function worker(file) {
  const state=read(file); const data=state.manifest;
  if(process.env.HERDR_ENV!=='1') fail('Herdr-managed pane required for batch worker');
  await Promise.all(data.seats.map(seat=>launchSeat(file,data,seat)));
}
function start(file,stateFile) {
  if(process.env.HERDR_ENV!=='1') fail('Herdr-managed pane required; start this command inside Herdr');
  const data=manifest(file);
  if(fs.existsSync(stateFile)) fail('state file already exists; choose a new path to prevent duplicate launches');
  const state={version:1,createdAt:now(),manifest:data,seats:data.seats.map(s=>({agent:s.agent,profile:s.profile,predecessor:s.predecessor,phase:'queued',updatedAt:now()}))};
  atomic(stateFile,state);
  const child=spawn(process.execPath,[new URL(import.meta.url).pathname,'worker','--state',stateFile],{cwd:root,env:process.env,detached:true,stdio:'ignore'});
  child.unref();
  console.log(JSON.stringify({state:stateFile,workerPid:child.pid,launch:'initiated',seats:state.seats.length}));
}
try {
  if(action==='start') { const source=value('--manifest'),state=value('--state'); if(!source||!state) fail('start requires --manifest and --state'); start(path.resolve(source),path.resolve(state)); }
  else if(action==='worker') { const state=value('--state'); if(!state) fail('worker requires --state'); await worker(path.resolve(state)); }
  else if(action==='status') { const state=value('--state'); if(!state) fail('status requires --state'); console.log(JSON.stringify(publicState(read(path.resolve(state))),null,2)); }
  else fail('usage: native-batch-refresh.mjs start --manifest FILE --state FILE | status --state FILE');
} catch(error) { console.error(String(error.message??error)); process.exitCode=1; }

export {manifest,publicState};
