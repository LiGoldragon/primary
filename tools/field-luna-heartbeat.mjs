#!/usr/bin/env node
/* Bounded Field Luna maintenance: marker-authorized archive and route cleanup. */
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';

const digest = file => crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const now = () => new Date().toISOString();
const run = (bin, args, options = {}) => spawnSync(bin, args, {encoding:'utf8', timeout:15_000, maxBuffer:1_048_576, ...options});
const text = result => result.status === 0 ? result.stdout : `${result.stdout}${result.stderr}`;

const validFlow = value => typeof value==='string'&&/^[-A-Za-z0-9_]{1,96}$/.test(value);
const routeFields = ['session','name','pane_id','terminal_id','agent'];
const validRoute = route => route&&routeFields.every(k=>typeof route[k]==='string'&&route[k]);

export function typedSnapshot(result) {
  if(result.status!==0) throw new Error('typed HM state unavailable');
  try {
    const value=JSON.parse(result.stdout);
    if(value.version!==1||!Array.isArray(value.routes)||!Array.isArray(value.retirements)) throw new Error('invalid typed HM state envelope');
    if(!value.routes.every(x=>x&&validFlow(x.flow)&&validRoute(x.route)&&typeof x.route.state==='string')) throw new Error('invalid typed HM route');
    return value;
  } catch(error) { throw new Error(`invalid typed HM state: ${error.message}`); }
}

export function markerCandidate(value, routes) {
  const record=value?.record;
  if(value?.version!==1||value.state!=='retired'||!validFlow(value.flow)||!validRoute(record)||
    typeof value.native_thread!=='string'||!value.evidence?.path||!value.evidence?.sha256||
    !path.isAbsolute(value.evidence.path)||!fs.existsSync(value.evidence.path)||digest(value.evidence.path)!==value.evidence.sha256) return null;
  const registration=routes.get(value.flow);
  if(!registration) return {flow:value.flow, state:'already-deregistered', record, native_thread:value.native_thread, evidence:value.evidence};
  if(!routeFields.every(k=>registration[k]===record[k])||registration.native_thread!==value.native_thread) return null;
  return {flow:value.flow,state:'candidate',record,native_thread:value.native_thread,evidence:value.evidence};
}

export function decide(candidate,{agent,locks,pane}) {
  if(candidate.state!=='candidate') return candidate.state;
  if(!agent||agent.agent_status!=='done') return 'hold-agent-not-done';
  if(locks.includes(candidate.flow)) return 'hold-active-lock';
  if(!pane||pane.pane_id!==candidate.record.pane_id||pane.terminal_id!==candidate.record.terminal_id) return 'hold-route-mismatch';
  return 'eligible';
}

export function deregisterInvocation(candidate) {
  return ['hm-deregister',[candidate.flow,'--name',candidate.record.name,'--session',candidate.record.session,'--pane-id',candidate.record.pane_id,'--terminal-id',candidate.record.terminal_id]];
}

function luna(summary) {
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'field-luna-')); const schema=path.join(dir,'schema.json'), out=path.join(dir,'out.json');
  try {
    fs.writeFileSync(schema,JSON.stringify({type:'object',additionalProperties:false,required:['status'],properties:{status:{enum:['clear','attention','unavailable']}}}));
    const prompt=`You are Field Luna, an ultra-low operational observer. Read only this metadata. Do not run commands, propose commands, or authorize cleanup. Return JSON only. ${JSON.stringify(summary)}`;
    const result=run('codex',['exec','--ephemeral','--model','gpt-5.6-luna','--sandbox','read-only','--skip-git-repo-check','--output-schema',schema,'--output-last-message',out,prompt],{stdio:'ignore',timeout:90_000});
    return result.status===0&&fs.existsSync(out)?JSON.parse(fs.readFileSync(out,'utf8')):{status:'unavailable'};
  } catch { return {status:'unavailable'}; } finally { fs.rmSync(dir,{recursive:true,force:true}); }
}

function main() {
  const [stateRoot,sourceRoot]=process.argv.slice(2); if(!stateRoot||!sourceRoot) throw new Error('usage: field-luna-heartbeat STATE_ROOT SOURCE_ROOT');
  const archive=path.join(stateRoot,'archive'); fs.mkdirSync(archive,{recursive:true,mode:0o700});
  const snapshot=typedSnapshot(run('hm-heartbeat-state',[]));
  const routes=new Map(snapshot.routes.map(({flow,route})=>[flow,route]));
  const locks=text(run('orchestrate',['Observe.Locks']));
  const scan=run(path.join(sourceRoot,'tools/reaper'),['--dry-run']);
  const rows=[];
  for(const retirement of snapshot.retirements) {
    const candidate=markerCandidate(retirement,routes); if(!candidate){rows.push({marker:retirement?.flow||'unknown',state:'hold-invalid-marker'});continue;}
    if(candidate.state==='already-deregistered'){rows.push(candidate);continue;}
    const agents=run('herdr',['--session',candidate.record.session,'agent','list']);
    const agent=agents.status===0?(JSON.parse(agents.stdout).result?.agents||[]).find(a=>a.name===candidate.record.name):null;
    const paneResult=run('herdr',['--session',candidate.record.session,'pane','get',candidate.record.pane_id]);
    const pane=paneResult.status===0?(JSON.parse(paneResult.stdout).result?.pane||null):null;
    const state=decide(candidate,{agent,locks,pane}); const row={...candidate,state};
    if(state==='eligible') {
      const receipt={at:now(),flow:candidate.flow,native_thread:candidate.native_thread,evidence:candidate.evidence,action:'archive-before-deregister'};
      fs.writeFileSync(path.join(archive,`${candidate.flow}.json`),JSON.stringify(receipt)+'\n',{mode:0o600});
      const d=run(...deregisterInvocation(candidate));
      if(d.status===0) { const close=run('herdr',['--session',candidate.record.session,'pane','close',candidate.record.pane_id]); row.state=close.status===0?'reaped':'deregistered-pane-close-held'; row.deregister=text(d).trim(); }
      else row.state='hold-deregister-refused';
    }
    rows.push(row);
  }
  for(const [flow,r] of routes) {
    const a=run('herdr',['--session',r.session,'agent','list']);
    const agent=a.status===0?(JSON.parse(a.stdout).result?.agents||[]).find(x=>x.name===r.name):null;
    if(agent?.agent_status==='done') rows.push({flow,state:'finished-needs-field-judgment',native_thread:r.native_thread});
  }
  const thin=rows.map(r=>({flow:r.flow||r.marker,state:r.state})); const fingerprint=crypto.createHash('sha256').update(JSON.stringify(thin)).digest('hex');
  const previous=fs.existsSync(path.join(stateRoot,'latest.json'))?JSON.parse(fs.readFileSync(path.join(stateRoot,'latest.json'),'utf8')):{};
  const result={at:now(),kind:'field-luna-heartbeat',reaper_scan:{status:scan.status===0?'observed':'unavailable',sha256:crypto.createHash('sha256').update(text(scan)).digest('hex')},luna:previous.fingerprint===fingerprint?{status:'unchanged-skip'}:luna(thin),fingerprint,rows};
  fs.writeFileSync(path.join(stateRoot,'latest.json'),JSON.stringify(result)+'\n',{mode:0o600}); console.log(JSON.stringify(result));
}
if(import.meta.url===`file://${process.argv[1]}`) main();
