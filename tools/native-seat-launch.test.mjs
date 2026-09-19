#!/usr/bin/env node
import assert from 'node:assert/strict';
import {execFileSync,spawn,spawnSync} from 'node:child_process';
import crypto from 'node:crypto'; import fs from 'node:fs'; import net from 'node:net'; import os from 'node:os'; import path from 'node:path';
import {verifyReceipt,verifyRolloutReceipt} from './native-seat-launch.mjs';
const tool=path.join(import.meta.dirname,'native-seat-launch.mjs'); const dir=fs.mkdtempSync(path.join(os.tmpdir(),'native-seat-launch-'));
for(const file of ['Vision/flowNexus.md','Vision/nexus.md','flows/cf3553/summary.md','flows/cf3553/vision/operational-mainFlowStartupCorrection.md','flows/da1e3f/vision/operational-launcher.md']) { fs.mkdirSync(path.dirname(path.join(dir,file)),{recursive:true});fs.writeFileSync(path.join(dir,file),'# fixture\n'); }
const plan=JSON.parse(execFileSync(process.execPath,[tool,'--seat','luna','--cwd',dir],{encoding:'utf8'})); const prompt=execFileSync(process.execPath,[tool,'--seat','luna','--cwd',dir,'--prompt'],{encoding:'utf8'}); assert.equal(plan.requiredMainFlow.name,'main-flow'); assert.ok(plan.sources.some(s=>s.path.includes('operational-mainFlowStartupCorrection'))); assert.doesNotMatch(prompt,/\$main-flow/);
for (const seat of ['field-sol-current','field-astra-current']) {
  const missing=spawnSync(process.execPath,[tool,'--seat',seat],{encoding:'utf8'});
  assert.equal(missing.status,2);
  assert.match(missing.stderr,/require --predecessor/);
  const current=JSON.parse(execFileSync(process.execPath,[tool,'--seat',seat,'--predecessor','8565e8'],{encoding:'utf8'}));
  assert.equal(current.predecessor,'8565e8');
  assert.equal(current.ancestor,'1cb440');
  const text=execFileSync(process.execPath,[tool,'--seat',seat,'--predecessor','8565e8','--prompt'],{encoding:'utf8'});
  assert.match(text,/refreshed from 8565e8/);
}
for(const name of plan.requiredSkillNames){const file=path.join(dir,'.agents/skills',name,'SKILL.md');fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,`# ${name}\n`);}
const uri=new URL(`file://${tool}`).href; const old=spawnSync(process.execPath,['--input-type=module','--eval',`import {rejectTokenOnly} from ${JSON.stringify(uri)};rejectTokenOnly('$main-flow')`],{encoding:'utf8'});assert.notEqual(old.status,0);assert.match(old.stderr,/not skill injection/);
const accepted=spawnSync(process.execPath,['--input-type=module','--eval',`import {structuredSkills,containsMainFlow} from ${JSON.stringify(uri)};let p='/x/main-flow/SKILL.md';if(!containsMainFlow({items:structuredSkills([{name:'main-flow',path:p}])},p))process.exit(9)`],{encoding:'utf8'});assert.equal(accepted.status,0,accepted.stderr);
const safe=spawnSync(process.execPath,[tool,'--seat','luna','--cwd',dir,'--launch'],{encoding:'utf8'});assert.equal(safe.status,2);assert.match(safe.stderr,/acknowledge-live-launch/);
const noHash=spawnSync(process.execPath,[tool,'--seat','luna','--cwd',dir,'--launch','--acknowledge-live-launch'],{encoding:'utf8'});assert.notEqual(noHash.status,0);assert.match(noHash.stderr,/expected-runner-sha256/);
const wrongHash=spawnSync(process.execPath,[tool,'--seat','luna','--cwd',dir,'--launch','--acknowledge-live-launch','--expected-runner-sha256','0'.repeat(64)],{encoding:'utf8'});assert.notEqual(wrongHash.status,0);assert.match(wrongHash.stderr,/runner hash mismatch/);
const noActivation=spawnSync(process.execPath,[tool,'--seat','luna','--cwd',dir,'--activate','--receipt',path.join(dir,'missing-receipt.json')],{encoding:'utf8'});assert.notEqual(noActivation.status,0);

// Disposable app-server fixture: readiness is accepted only when the actual
// turn payload has a typed main-flow input and items/list echoes that item.
const socketPath=path.join(dir,'app-server.sock'); let turnStart,firstTurnStart,threadRead;
const server=net.createServer(socket=>{let raw=Buffer.alloc(0),upgraded=false; const reply=(id,result)=>socket.write(serverFrame(JSON.stringify({jsonrpc:'2.0',id,result}))); socket.on('data',data=>{raw=Buffer.concat([raw,data]);if(!upgraded){const end=raw.indexOf('\r\n\r\n');if(end<0)return;raw=raw.subarray(end+4);upgraded=true;socket.write('HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n\r\n');}while(raw.length>=2){let n=raw[1]&127,o=2;if(n===126){if(raw.length<4)return;n=raw.readUInt16BE(2);o=4;}if(raw.length<o+4+n)return;const mask=raw.subarray(o,o+4),body=Buffer.alloc(n);for(let i=0;i<n;i++)body[i]=raw[o+4+i]^mask[i%4];raw=raw.subarray(o+4+n);const request=JSON.parse(body);if(!request.id)continue;if(request.method==='skills/list')reply(request.id,[...plan.requiredSkillNames].map(name=>({name,path:path.join(dir,'.agents/skills',name,'SKILL.md')})));else if(request.method==='thread/start')reply(request.id,{thread:{id:'fixture-thread'}});else if(request.method==='turn/start'){turnStart=request;firstTurnStart??=request;reply(request.id,{turn:{id:'fixture-turn'}});}else if(request.method==='thread/read'){threadRead=request;const skills=plan.requiredSkillNames.map(name=>{const p=path.join(dir,'.agents/skills',name,'SKILL.md');return {type:'skill',name,path:p,source:fs.readFileSync(p,'utf8')};});reply(request.id,{thread:{id:'fixture-thread',turns:[{id:'fixture-turn',output_text:'Native context is present.',turn_context:{model:'gpt-5.6-luna',effort:'medium',prompt:firstTurnStart.params.input.at(-1).text,sourceManifestSha256:plan.sourceManifestSha256,skills}}]}});}else reply(request.id,{});}});});
await new Promise(ok=>server.listen(socketPath,ok));
const runnerHash=crypto.createHash('sha256').update(fs.readFileSync(tool)).digest('hex'); const receipt=path.join(dir,'receipt.json');
const launched=await new Promise(resolve=>{const child=spawn(process.execPath,[tool,'--seat','luna','--name','fixture-native-seat','--cwd',dir,'--socket',socketPath,'--receipt',receipt,'--expected-runner-sha256',runnerHash,'--launch','--acknowledge-live-launch']);let out='',err='';child.stdout.on('data',d=>out+=d);child.stderr.on('data',d=>err+=d);child.on('exit',code=>resolve({code,out,err}));});
const activated=await new Promise(resolve=>{const child=spawn(process.execPath,[tool,'--seat','luna','--cwd',dir,'--socket',socketPath,'--receipt',receipt,'--activate']);let out='',err='';child.stdout.on('data',d=>out+=d);child.stderr.on('data',d=>err+=d);child.on('exit',code=>resolve({code,out,err}));}); server.close();
assert.equal(launched.code,0,launched.err); assert.ok(firstTurnStart.params.input.some(i=>i.type==='skill'&&i.name==='main-flow')); assert.equal(JSON.parse(launched.out).readiness,'native-full-bundle-expanded-witnessed');
assert.equal(JSON.parse(launched.out).threadName,'fixture-native-seat');
assert.equal(threadRead.params.includeTurns,true);assert.deepEqual(JSON.parse(fs.readFileSync(receipt,'utf8')).sourceManifest,plan.sources);
assert.equal(activated.code,0,activated.err);assert.equal(JSON.parse(activated.out).threadId,'fixture-thread');
// Receipt verification never searches a prior turn, and each observed native
// field is a hard gate.  The payload also crosses the 64 KiB websocket frame.
const source='x'.repeat(70_000), hash=v=>crypto.createHash('sha256').update(v).digest('hex');
const receiptShape={threadId:'t',turnId:'u',generationId:'g',model:'m',effort:'e',firstPromptSha256:hash('p'),sourceManifestSha256:'manifest',skillManifest:[{name:'main-flow',path:'/s',source,sha256:hash(source)}]};
const good={thread:{id:'t',turns:[{id:'u',generationId:'g',output_text:'Native context is present.',turn_context:{model:'m',effort:'e',prompt:'p',sourceManifestSha256:'manifest',skills:[{type:'skill',name:'main-flow',path:'/s',source}]}}]}};
assert.equal(verifyReceipt({thread:{id:'t',turns:[]}},receiptShape).readiness,'pending');
for(const [label,mutate] of [['model',x=>x.thread.turns[0].turn_context.model='bad'],['effort',x=>x.thread.turns[0].turn_context.effort='bad'],['generation',x=>x.thread.turns[0].generationId='bad'],['manifest',x=>x.thread.turns[0].turn_context.sourceManifestSha256='bad'],['skill source',x=>x.thread.turns[0].turn_context.skills[0].source='bad'],['missing skill',x=>x.thread.turns[0].turn_context.skills=[]],['prior turn',x=>x.thread.turns[0].id='old']]) { const bad=structuredClone(good);mutate(bad);assert.throws(()=>verifyReceipt(bad,receiptShape),/verification refused/,label); }
assert.equal(verifyReceipt(good,receiptShape).readiness,'native-full-bundle-expanded-witnessed');
const rollout=path.join(dir,'rollout.jsonl'), rolloutRows=[{type:'turn_context',payload:{turn_id:'u',model:'m',effort:'e'}},{type:'event_msg',payload:{thread_id:'t',turn_id:'u',item:{type:'UserMessage',content:[{type:'skill',name:'main-flow',path:'/s'},{type:'text',text:'p'}]}}},{type:'event_msg',payload:{thread_id:'t',turn_id:'u',item:{type:'AgentMessage',content:[{type:'Text',text:'Native context is present.'}]}}}];fs.writeFileSync(rollout,rolloutRows.map(JSON.stringify).join('\n')+'\n');
assert.equal(verifyRolloutReceipt(rollout,receiptShape).readiness,'native-full-bundle-rollout-witnessed');rolloutRows[0].payload.model='bad';fs.writeFileSync(rollout,rolloutRows.map(JSON.stringify).join('\n')+'\n');assert.throws(()=>verifyRolloutReceipt(rollout,receiptShape),/verification refused/);
console.log('native-seat-launch fixtures passed');

function serverFrame(text){const body=Buffer.from(text);return body.length<126?Buffer.concat([Buffer.from([129,body.length]),body]):Buffer.concat([Buffer.from([129,126,body.length>>8,body.length&255]),body]);}
