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
  if (seat==='field-sol-current') assert.deepEqual(current.sources.map(source=>source.path),['flows/8565e8/reports/refresh-handoff.md','flows/8565e8/reports/morning-2026-09-20.md','flows/8565e8/reports/lojix-schema-compatibility-addendum.md']);
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

// A valid launch request must fail before even connecting to app-server.
// This fixture would count a connection if any RPC, including thread/start,
// were attempted.
const socketPath=path.join(dir,'app-server.sock'); let connections=0;
const server=net.createServer(socket=>{connections++;socket.destroy();});
await new Promise(ok=>server.listen(socketPath,ok));
const runnerHash=crypto.createHash('sha256').update(fs.readFileSync(tool)).digest('hex');
const receipt=path.join(dir,'receipt.json');
const refused=await new Promise(resolve=>{const child=spawn(process.execPath,[tool,'--seat','luna','--name','fixture-native-seat','--cwd',dir,'--socket',socketPath,'--receipt',receipt,'--expected-runner-sha256',runnerHash,'--launch','--acknowledge-live-launch']);let out='',err='';child.stdout.on('data',d=>out+=d);child.stderr.on('data',d=>err+=d);child.on('exit',code=>resolve({code,out,err}));});
server.close();
assert.notEqual(refused.code,0);
assert.match(refused.err,/start Codex in a Herdr pane first/);
assert.equal(connections,0,'launch must not open app-server RPC');
assert.equal(fs.existsSync(receipt),false,'launch must not write a created-thread receipt');
// Adoption uses an already-running Herdr Codex pane and an existing empty
// native thread. The fake app-server fails the fixture if thread/start occurs.
const adoptedId='01a0bf90-41fd-72a1-ac8b-ee9c1dab9a41';
const bin=path.join(dir,'bin'); fs.mkdirSync(bin);
const fakeHerdr=path.join(bin,'herdr');
fs.writeFileSync(fakeHerdr,`#!/usr/bin/env node
const args=process.argv.slice(2);
if(args.includes('--json')) process.exit(8);
if(args.includes('agent')&&args.includes('get')) console.log(JSON.stringify({result:{agent:{name:'field-sol-of-8565e8',pane_id:'wN:p1',terminal_id:'term_fixture',workspace_id:'wN',cwd:${JSON.stringify(dir)},agent:'codex',interactive_ready:true,agent_status:'idle',revision:3}}}));
else if(args.includes('pane')&&args.includes('get')) console.log(JSON.stringify({result:{pane:{pane_id:'wN:p1',terminal_id:'term_fixture',workspace_id:'wN',cwd:${JSON.stringify(dir)},agent:'codex',revision:3}}}));
else if(args.includes('pane')&&args.includes('read')) console.log('Session: ${adoptedId}');
else process.exit(9);
`,{mode:0o755});
const adoptedSocket=path.join(dir,'adopt.sock'); let firstTurn,adoptedCalls=[];
const adoptedServer=net.createServer(socket=>{let raw=Buffer.alloc(0),upgraded=false;const reply=(id,result)=>socket.write(serverFrame(JSON.stringify({jsonrpc:'2.0',id,result})));socket.on('data',data=>{raw=Buffer.concat([raw,data]);if(!upgraded){const end=raw.indexOf('\r\n\r\n');if(end<0)return;raw=raw.subarray(end+4);upgraded=true;socket.write('HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n\r\n');}while(raw.length>=2){let n=raw[1]&127,o=2;if(n===126){if(raw.length<4)return;n=raw.readUInt16BE(2);o=4;}if(raw.length<o+4+n)return;const mask=raw.subarray(o,o+4),body=Buffer.alloc(n);for(let i=0;i<n;i++)body[i]=raw[o+4+i]^mask[i%4];raw=raw.subarray(o+4+n);const request=JSON.parse(body);if(!request.id)continue;adoptedCalls.push(request.method);if(request.method==='thread/start')throw new Error('app-server-only thread creation attempted');if(request.method==='thread/read'){if(!firstTurn)socket.write(serverFrame(JSON.stringify({jsonrpc:'2.0',id:request.id,error:{code:-32000,message:'rollout is empty'}})));else{const skills=plan.requiredSkillNames.map(name=>{const p=path.join(dir,'.agents/skills',name,'SKILL.md');return {type:'skill',name,path:p,source:fs.readFileSync(p,'utf8')};});reply(request.id,{thread:{id:adoptedId,turns:[{id:'first-turn',output_text:'Native context is present.',turn_context:{model:'gpt-5.6-luna',effort:'medium',prompt:firstTurn.params.input.at(-1).text,sourceManifestSha256:plan.sourceManifestSha256,skills}}]}});}}else if(request.method==='skills/list')reply(request.id,plan.requiredSkillNames.map(name=>({name,path:path.join(dir,'.agents/skills',name,'SKILL.md')})));else if(request.method==='turn/start'){firstTurn=request;reply(request.id,{turn:{id:'first-turn'}});}else reply(request.id,{});}});});
await new Promise(ok=>adoptedServer.listen(adoptedSocket,ok));
const adoptedReceipt=path.join(dir,'adopted-receipt.json');
const adopted=await new Promise(resolve=>{const child=spawn(process.execPath,[tool,'--seat','luna','--cwd',dir,'--socket',adoptedSocket,'--receipt',adoptedReceipt,'--expected-runner-sha256',runnerHash,'--adopt-herdr-thread',adoptedId,'--herdr-session','messaging-build','--herdr-pane','wN:p1','--herdr-agent','field-sol-of-8565e8','--herdr-terminal','term_fixture','--acknowledge-live-launch'],{env:{...process.env,PATH:`${bin}:${process.env.PATH}`}});let out='',err='';child.stdout.on('data',d=>out+=d);child.stderr.on('data',d=>err+=d);child.on('exit',code=>resolve({code,out,err}));});
adoptedServer.close();
assert.equal(adopted.code,0,adopted.err);
assert.deepEqual(adoptedCalls,['initialize','thread/read','skills/list','turn/start','thread/read']);
assert.ok(firstTurn.params.input.some(i=>i.type==='skill'&&i.name==='main-flow'));
assert.equal(JSON.parse(adopted.out).readiness,'native-full-bundle-expanded-witnessed');
assert.equal(JSON.parse(fs.readFileSync(adoptedReceipt,'utf8')).herdr.paneId,'wN:p1');
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
