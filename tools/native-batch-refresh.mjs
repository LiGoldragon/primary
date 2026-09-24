#!/usr/bin/env node
// One-command, Herdr-first native refresh.  This controller never retires a seat.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import crypto from 'node:crypto';
import {spawn, execFileSync} from 'node:child_process';
import {canonicalRole,nativeUuidFromHerdrWriterLock} from './native-seat-launch.mjs';
import {requireModelTitle} from './model-display-name.mjs';

const root = path.resolve(import.meta.dirname, '..');
const launcher = path.join(import.meta.dirname, 'native-seat-launch.mjs');
const claudeHelper = path.join(import.meta.dirname, 'claude-native-seat-refresh.py');
const mainFlowPrompt = path.join(import.meta.dirname, 'main-flow-mode', 'system-prompt.md');
const mainFlowReminder = path.join(import.meta.dirname, 'main-flow-mode', 'reminder-hook.py');
const argv = process.argv.slice(2);
const action = argv[0];
const invokedDirectly = Boolean(process.argv[1]) && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname);
const value = flag => { const i=argv.indexOf(flag); return i<0 ? undefined : argv[i+1]; };
const now = () => new Date().toISOString();
const hash = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const flowId = /^[a-f0-9]{6}$/;
const namePattern = /^[a-z][a-z0-9_-]{0,31}$/;
const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;
const firstPrestartError='Unexpected end of JSON input';
const markerTimeoutError='herdr exited 1: {"error":{"code":"timeout","message":"timed out waiting for output match"},"id":"cli:pane:wait-output"}';
const shellQuote = value => `'${String(value).replaceAll("'", "'\\''")}'`;
function claudeJobDir(nativeThreadId, home=os.homedir()) {
  if(!uuid.test(nativeThreadId)) fail('Claude native UUID required for isolated job directory');
  return path.join(home,'.claude','jobs',`native-${nativeThreadId}`);
}
function claudeShellEnvironmentCommand(nativeThreadId, jobDir, nonce) {
  if(!uuid.test(nativeThreadId) || !path.isAbsolute(jobDir) || !/^[a-f0-9]{24}$/.test(nonce??'')) fail('Claude native environment identity invalid');
  // Herdr agent.start types into this exact pane's shell; its API has no env field.
  // Compose the marker at runtime so echoed shell input cannot satisfy wait-output.
  return `unset CLAUDE_CODE_CHILD_SESSION CLAUDE_CODE_SESSION_KIND CLAUDE_CODE_SESSION_ID && export CLAUDE_JOB_DIR=${shellQuote(jobDir)} && printf 'CLAUDE_ENV_READY_%s_%s\\n' ${shellQuote(nativeThreadId)} ${shellQuote(nonce)}`;
}
function claudeJobDirectoryReusable(jobDir) {
  const entries=fs.readdirSync(jobDir);
  return entries.length===0 || entries.length===1 && entries[0]==='main-flow-settings.json';
}
async function prepareClaudePaneEnvironment(session,paneId,nativeThreadId,retained=false,recordMarker=()=>{}) {
  const jobDir=claudeJobDir(nativeThreadId);
  fs.mkdirSync(path.dirname(jobDir),{recursive:true,mode:0o700});
  if(retained) {
    if(!fs.lstatSync(jobDir).isDirectory() || !claudeJobDirectoryReusable(jobDir)) fail('retained Claude job directory contains foreign state');
  } else fs.mkdirSync(jobDir,{mode:0o700}); // Exclusive: never adopt another session's job state.
  const nonce=crypto.randomBytes(12).toString('hex');
  const command=claudeShellEnvironmentCommand(nativeThreadId,jobDir,nonce);
  const marker=`CLAUDE_ENV_READY_${nativeThreadId}_${nonce}`;
  recordMarker(marker);
  // pane run is an action: success is its exit status, and it may emit no JSON.
  await run('herdr',['--session',session,'pane','run',paneId,command]);
  const observed=await herdr(session,'pane','wait-output',paneId,'--match',marker,'--source','visible','--lines','50','--timeout','5000');
  if(observed.pane_id!==paneId || observed.matched_line!==marker) fail('Claude pane environment preparation was not witnessed');
  return jobDir;
}
async function verifyClaudeProcessEnvironment(session,paneId,nativeThreadId,jobDir) {
  const observed=await herdr(session,'pane','process-info','--pane',paneId);
  const processes=observed.process_info?.foreground_processes??[];
  const matches=processes.filter(process=>{
    const args=process.argv??[]; const at=args.indexOf('--session-id');
    return at>=0 && args[at+1]===nativeThreadId && Number.isSafeInteger(process.pid);
  });
  if(matches.length!==1) fail('Claude native process identity is not unique in the target pane');
  const fields=Object.fromEntries(fs.readFileSync(`/proc/${matches[0].pid}/environ`).toString('utf8').split('\0').filter(Boolean).map(entry=>{
    const index=entry.indexOf('='); return [entry.slice(0,index),entry.slice(index+1)];
  }));
  if(fields.CLAUDE_JOB_DIR!==jobDir || (fields.CLAUDE_CODE_SESSION_ID && fields.CLAUDE_CODE_SESSION_ID!==nativeThreadId) ||
     'CLAUDE_CODE_CHILD_SESSION' in fields || 'CLAUDE_CODE_SESSION_KIND' in fields) fail('Claude native process inherited another session environment');
  return {pid:matches[0].pid,jobDir,nativeThreadId};
}
function fail(message) { throw new Error(message); }
function atomic(file, body) { fs.mkdirSync(path.dirname(file),{recursive:true}); const tmp=`${file}.${process.pid}.tmp`; fs.writeFileSync(tmp,JSON.stringify(body,null,2)+'\n',{mode:0o600}); fs.renameSync(tmp,file); }
function read(file) { return JSON.parse(fs.readFileSync(file,'utf8')); }
function requireMainFlowPrompt(file=mainFlowPrompt) {
  if(!fs.existsSync(file) || !fs.statSync(file).isFile() || !fs.readFileSync(file,'utf8').trim()) fail(`main-flow system prompt file missing or empty: ${file}`);
  return file;
}
function reminderCommand(promptFile,stateDir,every) {
  if(!Number.isSafeInteger(every) || every<1 || every>1000) fail('mainFlowReminderEvery must be an integer from 1 through 1000');
  return `python3 ${shellQuote(mainFlowReminder)} --prompt-file ${shellQuote(promptFile)} --state-dir ${shellQuote(stateDir)} --every ${every}`;
}
function mainSeatLaunchArgs({harness,model,effort,nativeThreadId=null,launchTitle=null,jobDir=null,stateDir,promptFile=mainFlowPrompt,reminderEvery=20,mainSeat=true}) {
  const base=harness==='claude'?['--session-id',nativeThreadId,'--model',model,'--effort',effort,'--name',launchTitle,'--remote-control']:['--model',model,'-c',`model_reasoning_effort=${effort}`];
  if(!mainSeat) return base;
  requireMainFlowPrompt(promptFile);
  if(!fs.existsSync(mainFlowReminder)) fail(`main-flow reminder hook missing: ${mainFlowReminder}`);
  const hookState=path.resolve(stateDir??path.join(jobDir??'', 'main-flow-hook-state'));
  const command=reminderCommand(promptFile,hookState,reminderEvery);
  if(harness==='claude') {
    if(!jobDir) fail('Claude main seat requires an isolated job directory');
    const settings=path.join(jobDir,'main-flow-settings.json');
    atomic(settings,{hooks:{UserPromptSubmit:[{hooks:[{type:'command',command,timeout:10}]}]}});
    return [...base,'--system-prompt-file',promptFile,'--settings',settings];
  }
  if(harness==='codex') {
    const hooks=`[{ hooks = [{ type = "command", command = ${JSON.stringify(command)}, timeout = 10 }] }]`;
    return [...base,'-c',`model_instructions_file=${JSON.stringify(promptFile)}`,'-c',`hooks.UserPromptSubmit=${hooks}`,'--dangerously-bypass-hook-trust'];
  }
  fail(`unsupported harness for main-flow mode: ${harness}`);
}
function claudeProfile(seat) {
  if(!seat.profileFile) fail(`Claude profile file required: ${seat.agent}`);
  seat.profileFile=path.resolve(seat.profileFile);
  if(!fs.existsSync(seat.profileFile)) fail(`Claude profile file missing: ${seat.agent}`);
  seat.profileSha256=hash(seat.profileFile);
  const profile=read(seat.profileFile);
  if(profile.name!==seat.profile || !/^claude-(sonnet|haiku|opus|fable)-[0-9][a-z0-9-]*(?:\[1m\])?$/.test(profile.model) ||
     !['low','medium','high'].includes(profile.effort) || !canonicalRole(profile.role) || 'nativeTitle' in profile) fail(`Claude profile identity and canonical role must be explicit and pinned: ${seat.agent}`);
  const canonical=canonicalRole(profile.role);
  const display=requireModelTitle(profile.model);
  if(profile.titlePlan?.aspect!==canonical.aspect || profile.titlePlan?.power!==canonical.power || profile.titlePlan?.model!==display || profile.titlePlan?.afterOwnVerifiedFlowId!==true || profile.titlePlan?.template!==`${canonical.aspect} ${display} <FLOW_ID>`) fail(`Claude profile title plan differs from canonical role and model: ${seat.agent}`);
  const family=profile.model.split('-')[1];
  if(!Array.isArray(profile.modelCatalog) || !profile.modelCatalog.some(x=>x?.id===profile.model && x.family===family)) fail(`Claude ${family} model absent from audited profile catalog: ${seat.agent}`);
  if(profile.predecessor!==seat.predecessor || (seat.fresh===true)!==(seat.predecessor===null)) fail(`Claude profile predecessor/fresh seat mismatch: ${seat.agent}`);
  if(!Array.isArray(profile.skills) || !profile.skills.includes('spirit') || !profile.skills.includes('main-flow') || !profile.skills.includes('refresh') || !profile.skills.includes('psyche') || !profile.skills.includes('testing-flow-titles') || new Set(profile.skills).size!==profile.skills.length || profile.skills.some(x=>!namePattern.test(x))) fail(`Claude profile native skills invalid: ${seat.agent}`);
  if(!Array.isArray(profile.sources) || !profile.sources.length) fail(`Claude profile source hashes required: ${seat.agent}`);
  for(const source of profile.sources) {
    if(!source?.path || path.isAbsolute(source.path) || path.relative(root,path.resolve(root,source.path)).startsWith('..') || !/^[a-f0-9]{64}$/.test(source.sha256) || hash(path.join(root,source.path))!==source.sha256) fail(`Claude audited source missing or changed: ${source?.path}`);
  }
  if(!profile.sourceAudit || !/^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z$/.test(profile.sourceAudit.reviewedAt??'') || !Array.isArray(profile.sourceAudit.newestApplicableVision) || !profile.sourceAudit.newestApplicableVision.length || profile.sourceAudit.newestApplicableVision.some(item=>!profile.sources.some(source=>source.path===item))) fail(`Claude profile requires an audited newest applicable Vision subset: ${seat.agent}`);
  for(const skill of profile.skills) if(!fs.existsSync(path.join(root,'.claude','skills',skill,'SKILL.md'))) fail(`Claude native skill missing: ${skill}`);
  if(seat.model && seat.model!==profile.model || seat.effort && seat.effort!==profile.effort) fail(`Claude model/effort differs from audited profile: ${seat.agent}`);
  seat.model=profile.model; seat.effort=profile.effort; seat.claudeProfile=profile;
}
function command(binary,args,opts={}) { return execFileSync(binary,args,{cwd:root,encoding:'utf8',timeout:opts.timeout??30000,maxBuffer:4*1024*1024}); }
async function herdr(session,...args) { const body=JSON.parse(await run('herdr',['--session',session,...args])); return body.result??body; }
function manifest(file) {
  const data=read(file);
  if(data.version!==1 || !Array.isArray(data.seats) || !data.seats.length) fail('manifest requires version 1 and a nonempty seats array');
  if(!data.session || !data.workspace) fail('manifest requires explicit Herdr session and workspace ID');
  if(!data.cwd || path.resolve(data.cwd)!==root) fail('manifest cwd must be this checkout');
  requireMainFlowPrompt();
  if('mainFlowReminderEvery' in data && (!Number.isSafeInteger(data.mainFlowReminderEvery) || data.mainFlowReminderEvery<1 || data.mainFlowReminderEvery>1000)) fail('mainFlowReminderEvery must be an integer from 1 through 1000');
  const seen=new Set();
  for(const seat of data.seats) {
    if(!seat.profile || !namePattern.test(seat.agent) || !seat.label || !(seat.predecessor===null && seat.fresh===true || flowId.test(seat.predecessor) && seat.fresh!==true)) fail('each seat requires profile, explicit fresh or six-hex predecessor, valid agent name, and tab label');
    if(!['codex','claude'].includes(seat.harness)) fail(`unsupported harness for ${seat.agent}`);
    if(seen.has(seat.agent)) fail(`duplicate agent name: ${seat.agent}`); seen.add(seat.agent);
    if(seat.harness==='claude') { claudeProfile(seat); continue; }
    const profileArgs=[];
    if(seat.profileFile) { seat.profileFile=path.resolve(seat.profileFile); if(!fs.existsSync(seat.profileFile)) fail(`missing profile file: ${seat.agent}`); seat.profileSha256=hash(seat.profileFile); profileArgs.push('--profile-file',seat.profileFile); }
    // Plan evaluation validates the audited source bundle and typed skill list.
    const plan=JSON.parse(command(process.execPath,[launcher,'--seat',seat.profile,...(seat.fresh?['--fresh']:['--predecessor',seat.predecessor]),'--cwd',root,...profileArgs]));
    if(plan.predecessor!==seat.predecessor || !plan.canonicalRole || !plan.requiredSkillNames.includes('main-flow') || !plan.requiredSkillNames.includes('testing-flow-titles')) fail(`profile ${seat.profile} does not bind predecessor, canonical role, and title skills`);
    if(plan.launchGate) fail(`profile ${seat.profile} ${plan.launchGate}; batch Herdr startup cannot select its owned client and endpoint`);
    if(seat.model && seat.model!==plan.model) fail(`model differs from audited profile: ${seat.agent}`);
    if(seat.effort && seat.effort!==plan.effort) fail(`effort differs from audited profile: ${seat.agent}`);
    seat.model=plan.model; seat.effort=plan.effort;
  }
  return data;
}
function publicState(state) { return {version:state.version,createdAt:state.createdAt,launchAttemptsSettled:state.seats.every(s=>['native-verified','native-pending','failed'].includes(s.phase)),allNativeVerified:state.seats.every(s=>s.phase==='native-verified'),acceptance:'unwitnessed',predecessorReaping:'disabled',seats:state.seats.map(({agent,profile,predecessor,phase,error})=>({agent,profile,predecessor,phase,...(error?{error}: {})}))}; }
function update(file,agent,patch) { const state=read(file), seat=state.seats.find(s=>s.agent===agent); if(!seat) fail(`unknown ledger seat ${agent}`); Object.assign(seat,patch,{updatedAt:now()}); atomic(file,state); }
async function run(bin,args,opts={}) { return new Promise((resolve,reject)=>{const child=spawn(bin,args,{cwd:root,env:process.env,stdio:['ignore','pipe','pipe']}); let out='',err=''; child.stdout.on('data',d=>out+=d);child.stderr.on('data',d=>err+=d);child.on('error',reject);child.on('close',code=>code===0?resolve(out):reject(new Error(`${path.basename(bin)} exited ${code}: ${err.trim()}`)));}); }
function retainedPrestartFailure(failed,expected) {
  const old=failed.seats?.[0];
  if(failed.version!==1 || failed.seats?.length!==1 || failed.manifest?.seats?.length!==1 ||
     old?.phase!=='failed' || old.receipt || old.paneId!==expected.paneId ||
     old.terminalId!==expected.terminalId || old.nativeThreadId!==expected.nativeThreadId) return false;
  if(old.error===firstPrestartError) return !old.retained;
  if(old.error!==markerTimeoutError || !old.retained) return false;
  const prior=old.retained;
  if(prior.paneId!==expected.paneId || prior.terminalId!==expected.terminalId ||
     prior.nativeThreadId!==expected.nativeThreadId || !prior.failedStatePath || !prior.failedStateSha256) return false;
  try {
    if(hash(prior.failedStatePath)!==prior.failedStateSha256) return false;
    const first=read(prior.failedStatePath), beginning=first.seats?.[0];
    return first.version===1 && first.seats?.length===1 && first.manifest?.seats?.length===1 &&
      beginning?.phase==='failed' && beginning.error===firstPrestartError && !beginning.retained && !beginning.receipt &&
      beginning.paneId===expected.paneId && beginning.terminalId===expected.terminalId && beginning.nativeThreadId===expected.nativeThreadId;
  } catch { return false; }
}
async function retainedPanePreflight(data,seat,retained) {
  const failed=read(retained.failedStatePath);
  if(hash(retained.failedStatePath)!==retained.failedStateSha256 || !retainedPrestartFailure(failed,retained)) fail('retained failed-state witness changed');
  const pane=await herdr(data.session,'pane','get',retained.paneId);
  if(pane.pane?.pane_id!==retained.paneId || pane.pane?.terminal_id!==retained.terminalId ||
     pane.pane?.workspace_id!==data.workspace || path.resolve(pane.pane?.cwd??'')!==root) fail('retained pane identity changed');
  const info=await herdr(data.session,'pane','process-info','--pane',retained.paneId);
  const processes=info.process_info?.foreground_processes??[];
  if(info.process_info?.pane_id!==retained.paneId || processes.length!==1 ||
     !/^(?:zsh|bash|sh)$/.test(processes[0].name??'') || !Number.isSafeInteger(processes[0].pid)) fail('retained pane is not an idle shell');
  const roster=await herdr(data.session,'agent','list');
  const agents=roster.agents??[];
  if(!Array.isArray(agents) || agents.some(a=>a.name===seat.agent || a.pane_id===retained.paneId || a.terminal_id===retained.terminalId)) fail('retained pane already has an agent');
  const native=JSON.parse(await run('claude',['agents','--json']));
  const nativeAgents=Array.isArray(native)?native:(native.agents??[]);
  if(!Array.isArray(nativeAgents) || nativeAgents.some(a=>a.sessionId===retained.nativeThreadId || a.session_id===retained.nativeThreadId)) fail('retained Claude session already exists');
  for(const pid of fs.readdirSync('/proc').filter(x=>/^\d+$/.test(x))) {
    let args;
    try { args=fs.readFileSync(`/proc/${pid}/cmdline`).toString('utf8').split('\0'); }
    catch { continue; }
    if(args.includes(retained.nativeThreadId) && args.some(x=>/(?:^|\/)claude(?:$|\s)/.test(x))) fail('retained Claude native process already exists');
  }
  const transcript=path.join(os.homedir(),'.claude','projects',root.replaceAll('/','-'),`${retained.nativeThreadId}.jsonl`);
  if(fs.existsSync(transcript)) fail('retained Claude transcript already exists');
  const jobDir=claudeJobDir(retained.nativeThreadId);
  if(!fs.existsSync(jobDir) || !fs.lstatSync(jobDir).isDirectory() || !claudeJobDirectoryReusable(jobDir)) fail('retained Claude job directory contains foreign state');
  if(fs.existsSync(path.join(path.dirname(retained.failedStatePath),'receipts'))) fail('failed attempt has a receipt directory');
}
async function launchSeat(file,data,seat,retained=null) {
  try {
    if(seat.profileFile && hash(seat.profileFile)!==seat.profileSha256) fail('profile changed after manifest validation');
    if(seat.harness==='claude') for(const source of seat.claudeProfile.sources) if(hash(path.join(root,source.path))!==source.sha256) fail(`Claude source changed after manifest validation: ${source.path}`);
    if(retained) await retainedPanePreflight(data,seat,retained);
    const tab=retained?null:await herdr(data.session,'tab','create','--workspace',data.workspace,'--cwd',root,'--label',seat.label,'--no-focus');
    const pane=retained?{pane_id:retained.paneId,terminal_id:retained.terminalId}:(tab.root_pane??tab.rootPane);
    if(!pane?.pane_id || !pane?.terminal_id) fail('Herdr tab creation lacked pane and terminal IDs');
    update(file,seat.agent,{phase:'pane-created',paneId:pane.pane_id,terminalId:pane.terminal_id});
    const nativeThreadId=seat.harness==='claude'?(retained?.nativeThreadId??crypto.randomUUID()):null;
    if(nativeThreadId) update(file,seat.agent,{phase:'native-id-reserved',nativeThreadId});
    const claudeJob=seat.harness==='claude'?await prepareClaudePaneEnvironment(data.session,pane.pane_id,nativeThreadId,!!retained,
      marker=>update(file,seat.agent,{environmentMarker:marker})):null;
    const canonical=seat.harness==='claude'?canonicalRole(seat.claudeProfile.role):null;
    const launchTitle=canonical?`${canonical.aspect} ${requireModelTitle(seat.model)} (claim pending)`:null;
    const nativeArgs=mainSeatLaunchArgs({harness:seat.harness,model:seat.model,effort:seat.effort,nativeThreadId,launchTitle,jobDir:claudeJob,stateDir:path.join(path.dirname(file),'main-flow-hook-state',seat.agent),reminderEvery:data.mainFlowReminderEvery??20,mainSeat:true});
    const start=await herdr(data.session,'agent','start',seat.agent,'--kind',seat.harness,'--pane',pane.pane_id,'--timeout','300000','--',...nativeArgs);
    const agent=start.agent??(await herdr(data.session,'agent','get',seat.agent)).agent;
    if(agent?.name!==seat.agent || agent?.pane_id!==pane.pane_id || agent?.terminal_id!==pane.terminal_id || agent?.agent!==seat.harness || agent?.interactive_ready!==true || path.resolve(agent?.cwd??'')!==root) fail('Herdr ready agent does not match new pane, harness, and cwd');
    if(seat.harness==='claude') await verifyClaudeProcessEnvironment(data.session,pane.pane_id,nativeThreadId,claudeJob);
    update(file,seat.agent,{phase:'herdr-ready'});
    const snapshot=await run('herdr',['--session',data.session,'pane','read',pane.pane_id,'--source','recent','--lines','120','--format','text']);
    let matches=seat.harness==='claude'?[nativeThreadId]:[...snapshot.matchAll(/\bSession:\s*([0-9a-f-]{36})\b/g)].map(m=>m[1]).filter(x=>uuid.test(x));
    let nativeBinding=matches.length===1?{threadId:matches[0],method:'terminal-session-line'}:null;
    if(seat.harness==='codex'&&matches.length===0) {
      nativeBinding=nativeUuidFromHerdrWriterLock(data.session,pane.pane_id);
      matches=[nativeBinding.threadId];
    }
    if(matches.length!==1 || (nativeThreadId && matches[0]!==nativeThreadId)) fail('target Herdr pane must identify exact native session UUID');
    const receipt=path.join(path.dirname(file),'receipts',`${seat.agent}.json`);
    update(file,seat.agent,{phase:'native-identified',nativeThreadId:matches[0],nativeBinding,receipt});
    if(seat.harness==='claude') {
      const bootstrap=path.join(path.dirname(file),'receipts',`${seat.agent}.manifest.json`);
      atomic(bootstrap,{session_id:nativeThreadId,model:seat.model,effort:seat.effort,role:seat.claudeProfile.role,titlePlan:seat.claudeProfile.titlePlan,predecessor:seat.predecessor,skills:seat.claudeProfile.skills,sources:seat.claudeProfile.sources,sourceAudit:seat.claudeProfile.sourceAudit});
      const result=JSON.parse(await run('python3',[claudeHelper,'--manifest',bootstrap,'--cwd',root,'--refresh','--acknowledge-live-refresh','--herdr-session',data.session,'--herdr-agent',seat.agent,'--herdr-pane',pane.pane_id,'--herdr-terminal',pane.terminal_id,'--timeout','300']));
      const canonical=canonicalRole(seat.claudeProfile.role);
      const display=requireModelTitle(seat.model);
      if(result.generation?.session_id!==nativeThreadId || result.generation?.skills?.length!==seat.claudeProfile.skills.length || result.generation?.skills?.some((r,i)=>r.skill!==seat.claudeProfile.skills[i]) || result.generation?.first_user_prompt?.accepted_user_prompts!==1 || result.generation?.first_user_prompt?.leading_skill!=='main-flow' || result.native_main_flow?.observed!==true || result.observed_identity?.model!==seat.model || result.observed_identity?.effort!==seat.effort || result.native_title?.value!==`${canonical.aspect} ${display} (claim pending)` || result.native_title?.session_id!==nativeThreadId || result.generation?.acknowledged!=='BOOTSTRAP_READY' || !result.generation?.source_payload_hash) fail('Claude single first prompt, title, transcript, or source acknowledgement incomplete');
      atomic(receipt,{...result,herdr:{session:data.session,agentName:seat.agent,paneId:pane.pane_id,terminalId:pane.terminal_id},profileSha256:seat.profileSha256});
      update(file,seat.agent,{phase:'native-pending',nativeReadiness:'native-context-verified-title-pending'});
      return;
    }
    const answer=JSON.parse(await run(process.execPath,[launcher,'--seat',seat.profile,...(seat.fresh?['--fresh']:['--predecessor',seat.predecessor]),'--cwd',root,...(seat.profileFile?['--profile-file',seat.profileFile]:[]),'--name',seat.agent,'--receipt',receipt,'--expected-runner-sha256',hash(launcher),'--adopt-herdr-thread',matches[0],'--herdr-session',data.session,'--herdr-pane',pane.pane_id,'--herdr-agent',seat.agent,'--herdr-terminal',pane.terminal_id,'--acknowledge-live-launch']));
    const receiptData=read(receipt);
    if(receiptData.threadId!==matches[0] || receiptData.herdr?.paneId!==pane.pane_id || receiptData.herdr?.agentName!==seat.agent) fail('native receipt target binding mismatch');
    update(file,seat.agent,{phase:receiptData.status==='ready' && answer.readiness==='native-ready'?'native-verified':'native-pending',nativeReadiness:answer.readiness});
  } catch(error) { update(file,seat.agent,{phase:'failed',error:String(error.message??error)}); }
}
async function worker(file) {
  const state=read(file); const data=state.manifest;
  if(process.env.HERDR_ENV!=='1') fail('Herdr-managed pane required for batch worker');
  if(!Array.isArray(state.seats) || state.seats.length!==data.seats.length || state.seats.some(s=>s.phase!=='queued' || s.paneId || s.nativeThreadId)) fail('worker requires a fresh queued state; failed states cannot be replayed');
  await Promise.all(data.seats.map(seat=>launchSeat(file,data,seat,state.seats.find(s=>s.agent===seat.agent)?.retained??null)));
}
function continueRetained(failedFile,manifestFile,stateFile,expectedCurrentModel) {
  if(process.env.HERDR_ENV!=='1') fail('Herdr-managed pane required for retained continuation');
  if(path.resolve(failedFile)===path.resolve(stateFile) || fs.existsSync(stateFile)) fail('continuation requires a new state path');
  const failed=read(failedFile), data=manifest(manifestFile), old=failed.seats?.[0], seat=data.seats?.[0];
  const original=failed.manifest?.seats?.[0];
  if(failed.version!==1 || failed.seats?.length!==1 || failed.manifest?.seats?.length!==1 || data.seats.length!==1 ||
     old?.phase!=='failed' || !retainedPrestartFailure(failed,old) ||
     !old.paneId || !old.terminalId || !uuid.test(old.nativeThreadId??'') || old.receipt ||
     seat.harness!=='claude' || original.harness!=='claude' ||
     data.session!==failed.manifest.session || data.workspace!==failed.manifest.workspace || data.cwd!==failed.manifest.cwd ||
     seat.agent!==original.agent || seat.profile!==original.profile || seat.model!==expectedCurrentModel ||
     seat.model!==seat.claudeProfile.model || original.model!==original.claudeProfile?.model ||
     seat.model.split('-')[1]!==original.model.split('-')[1] || seat.effort!==original.effort ||
     seat.claudeProfile.role!==original.claudeProfile?.role ||
     JSON.stringify(seat.claudeProfile.titlePlan)!==JSON.stringify(original.claudeProfile?.titlePlan) ||
     JSON.stringify(seat.claudeProfile.remember??null)!==JSON.stringify(original.claudeProfile?.remember??null) ||
     seat.predecessor!==original.predecessor || seat.fresh!==original.fresh) fail('failed attempt does not match a retained pre-start Claude seat');
  const retained={failedStatePath:path.resolve(failedFile),failedStateSha256:hash(failedFile),paneId:old.paneId,
    terminalId:old.terminalId,nativeThreadId:old.nativeThreadId,
    profileTransition:{priorSha256:original.profileSha256,currentSha256:seat.profileSha256,priorModel:original.model,currentModel:seat.model}};
  const state={version:1,createdAt:now(),manifest:data,seats:[{agent:seat.agent,profile:seat.profile,predecessor:seat.predecessor,
    phase:'queued',updatedAt:now(),retained}]};
  atomic(stateFile,state);
  const child=spawn(process.execPath,[new URL(import.meta.url).pathname,'worker','--state',stateFile],{cwd:root,env:process.env,detached:true,stdio:'ignore'});
  child.unref();
  console.log(JSON.stringify({state:stateFile,workerPid:child.pid,launch:'retained-continuation-initiated',seats:1}));
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
if(invokedDirectly) try {
  if(action==='start') { const source=value('--manifest'),state=value('--state'); if(!source||!state) fail('start requires --manifest and --state'); start(path.resolve(source),path.resolve(state)); }
  else if(action==='continue-retained') { const failed=value('--failed-state'),source=value('--manifest'),state=value('--state'),model=value('--expected-current-model'); if(!failed||!source||!state||!model) fail('continue-retained requires --failed-state, --manifest, --state, and --expected-current-model'); continueRetained(path.resolve(failed),path.resolve(source),path.resolve(state),model); }
  else if(action==='validate') { const source=value('--manifest'); if(!source) fail('validate requires --manifest'); const data=manifest(path.resolve(source)); console.log(JSON.stringify({valid:true,seats:data.seats.length,session:data.session,workspace:data.workspace})); }
  else if(action==='worker') { const state=value('--state'); if(!state) fail('worker requires --state'); await worker(path.resolve(state)); }
  else if(action==='status') { const state=value('--state'); if(!state) fail('status requires --state'); console.log(JSON.stringify(publicState(read(path.resolve(state))),null,2)); }
  else if(action==='environment-plan') { const native=value('--native-id'); const job=claudeJobDir(native),nonce=crypto.randomBytes(12).toString('hex'); console.log(JSON.stringify({nativeThreadId:native,jobDir:job,marker:`CLAUDE_ENV_READY_${native}_${nonce}`,shellCommand:claudeShellEnvironmentCommand(native,job,nonce)})); }
  else fail('usage: native-batch-refresh.mjs validate --manifest FILE | start --manifest FILE --state FILE | status --state FILE');
} catch(error) { console.error(String(error.message??error)); process.exitCode=1; }

export {manifest,publicState,claudeJobDir,claudeShellEnvironmentCommand,verifyClaudeProcessEnvironment,mainSeatLaunchArgs,requireMainFlowPrompt};
