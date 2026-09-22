#!/usr/bin/env node
import assert from 'node:assert/strict';
import {execFileSync,spawn,spawnSync} from 'node:child_process';
import crypto from 'node:crypto'; import fs from 'node:fs'; import net from 'node:net'; import os from 'node:os'; import path from 'node:path';
import {verifyReceipt,verifyRolloutReceipt,activationPrompt,canonicalRole} from './native-seat-launch.mjs';
assert.match(activationPrompt,/direct structured tool witness/);
assert.match(activationPrompt,/Do not spawn a subagent/);
assert.doesNotMatch(activationPrompt,/delegate one benign acknowledgement/);
const tool=path.join(import.meta.dirname,'native-seat-launch.mjs'); const dir=fs.mkdtempSync(path.join(os.tmpdir(),'native-seat-launch-'));
const audited=(source='Vision/flowNexus.md')=>({sourceAudit:{reviewedAt:'2026-09-21T00:00:00Z',newestApplicableVision:[source]}});
for(const file of ['Vision/flowNexus.md','Vision/nexus.md','flows/cf3553/summary.md','flows/cf3553/vision/operational-mainFlowStartupCorrection.md','flows/da1e3f/vision/operational-launcher.md']) { fs.mkdirSync(path.dirname(path.join(dir,file)),{recursive:true});fs.writeFileSync(path.join(dir,file),'# fixture\n'); }
const plan=JSON.parse(execFileSync(process.execPath,[tool,'--seat','luna','--cwd',dir],{encoding:'utf8'})); const prompt=execFileSync(process.execPath,[tool,'--seat','luna','--cwd',dir,'--prompt'],{encoding:'utf8'}); assert.equal(plan.requiredMainFlow.name,'main-flow'); assert.ok(plan.sources.some(s=>s.path.includes('operational-mainFlowStartupCorrection'))); assert.doesNotMatch(prompt,/\$main-flow/); assert.doesNotMatch(prompt,/SHA-256:|[a-f0-9]{64}/);
const freshProfile=path.join(dir,'fresh.json');
fs.writeFileSync(freshProfile,JSON.stringify({name:'fresh-luna',model:'gpt-5.6-luna',effort:'low',role:'Fresh Luna',fresh:true,predecessor:null,ancestor:null,skills:['spirit','main-flow','refresh','psyche','testing-flow-titles'],sourceManifest:['Vision/flowNexus.md'],...audited()}));
const fresh=JSON.parse(execFileSync(process.execPath,[tool,'--seat','fresh-luna','--profile-file',freshProfile,'--fresh','--cwd',dir],{encoding:'utf8'}));
assert.equal(fresh.predecessor,null);assert.equal(fresh.ancestor,null);
fs.writeFileSync(freshProfile,JSON.stringify({name:'fresh-luna',model:'gpt-5.6-luna',effort:'low',role:'Fresh Luna',fresh:true,predecessor:null,ancestor:null,skills:['spirit','main-flow','refresh','psyche','testing-flow-titles'],sourceManifest:['Vision/flowNexus.md']}));
const missingAudit=spawnSync(process.execPath,[tool,'--seat','fresh-luna','--profile-file',freshProfile,'--fresh','--cwd',dir],{encoding:'utf8'});
assert.notEqual(missingAudit.status,0);assert.match(missingAudit.stderr,/audited newest applicable Vision/);
fs.writeFileSync(freshProfile,JSON.stringify({name:'fresh-luna',model:'gpt-5.6-luna',effort:'low',role:'Fresh Luna',fresh:true,predecessor:null,ancestor:null,skills:['spirit','main-flow','refresh','psyche','testing-flow-titles'],sourceManifest:['Vision/flowNexus.md'],...audited()}));
assert.match(execFileSync(process.execPath,[tool,'--seat','fresh-luna','--profile-file',freshProfile,'--fresh','--cwd',dir,'--prompt'],{encoding:'utf8'}),/fresh seat with no predecessor or ancestor/);
const invented=spawnSync(process.execPath,[tool,'--seat','fresh-luna','--profile-file',freshProfile,'--predecessor','abcdef','--cwd',dir],{encoding:'utf8'});
assert.notEqual(invented.status,0);assert.match(invented.stderr,/exact predecessor and ancestor/);
const mindSolProfile=path.join(dir,'mind-sol.json');
fs.writeFileSync(mindSolProfile,JSON.stringify({name:'mind-sol',model:'gpt-5.6-sol',effort:'medium',role:'Mind Medium',fresh:true,predecessor:null,ancestor:null,skills:['spirit','main-flow','refresh','psyche','testing-flow-titles'],sourceManifest:['Vision/flowNexus.md'],...audited()}));
for(const name of ['refresh','psyche']) {const file=path.join(dir,'.agents/skills',name,'SKILL.md');fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,`# ${name}\n`);}
const mindSol=spawnSync(process.execPath,[tool,'--seat','mind-sol','--profile-file',mindSolProfile,'--fresh','--cwd',dir],{encoding:'utf8'});
assert.equal(mindSol.status,0,mindSol.stderr);
const mindSolPlan=JSON.parse(mindSol.stdout);
assert.equal(mindSolPlan.model,'gpt-5.6-sol');
assert.equal(mindSolPlan.role,'Mind Medium');
assert.equal(mindSolPlan.predecessor,null);
assert.ok(mindSolPlan.requiredSkillNames.includes('main-flow'));
fs.writeFileSync(mindSolProfile,JSON.stringify({name:'mind-sol',model:'gpt-5.6-sol',effort:'medium',role:'Other Sol',fresh:true,predecessor:null,ancestor:null,skills:['spirit','main-flow','refresh','psyche','testing-flow-titles'],sourceManifest:['Vision/flowNexus.md']}));
const wrongRole=spawnSync(process.execPath,[tool,'--seat','mind-sol','--profile-file',mindSolProfile,'--fresh','--cwd',dir],{encoding:'utf8'});
assert.notEqual(wrongRole.status,0);
const fieldSolProfile=path.join(dir,'field-sol-of-7091ea.json');
const fieldSolProfileValue={name:'field-sol-of-7091ea',model:'gpt-5.6-sol',effort:'medium',role:'Field Sol',fresh:false,predecessor:'7091ea',ancestor:'7091ea',skills:['spirit','main-flow','field','refresh','psyche','testing-flow-titles'],sourceManifest:['Vision/flowNexus.md'],...audited()};
fs.writeFileSync(fieldSolProfile,JSON.stringify(fieldSolProfileValue));
const fieldSolPlan=JSON.parse(execFileSync(process.execPath,[tool,'--seat','field-sol-of-7091ea','--profile-file',fieldSolProfile,'--predecessor','7091ea','--cwd',dir],{encoding:'utf8'}));
assert.equal(fieldSolPlan.role,'Field Sol');assert.equal(fieldSolPlan.predecessor,'7091ea');assert.equal(fieldSolPlan.model,'gpt-5.6-sol');
fs.writeFileSync(fieldSolProfile,JSON.stringify({...fieldSolProfileValue,role:'Other Field'}));
const rejectedFieldRole=spawnSync(process.execPath,[tool,'--seat','field-sol-of-7091ea','--profile-file',fieldSolProfile,'--predecessor','7091ea','--cwd',dir],{encoding:'utf8'});
assert.notEqual(rejectedFieldRole.status,0);
fs.writeFileSync(fieldSolProfile,JSON.stringify(fieldSolProfileValue));
const rejectedFieldPredecessor=spawnSync(process.execPath,[tool,'--seat','field-sol-of-7091ea','--profile-file',fieldSolProfile,'--predecessor','395aed','--cwd',dir],{encoding:'utf8'});
assert.notEqual(rejectedFieldPredecessor.status,0);
const fieldAstraProfile=path.join(dir,'field-astra-of-6db4fe.json');
const fieldAstraProfileValue={name:'field-astra-of-6db4fe',model:'gpt-6-astra',effort:'medium',role:'Field Astra',fresh:false,predecessor:'6db4fe',ancestor:'6db4fe',skills:['spirit','main-flow','field','refresh','psyche','testing-flow-titles'],sourceManifest:['Vision/flowNexus.md'],...audited()};
fs.writeFileSync(fieldAstraProfile,JSON.stringify(fieldAstraProfileValue));
const fieldAstraPlan=JSON.parse(execFileSync(process.execPath,[tool,'--seat','field-astra-of-6db4fe','--profile-file',fieldAstraProfile,'--predecessor','6db4fe','--cwd',dir],{encoding:'utf8'}));
assert.equal(fieldAstraPlan.role,'Field Astra');assert.equal(fieldAstraPlan.predecessor,'6db4fe');assert.equal(fieldAstraPlan.model,'gpt-6-astra');
fs.writeFileSync(fieldAstraProfile,JSON.stringify({...fieldAstraProfileValue,model:'gpt-5.6-sol'}));
const rejectedAstraModel=spawnSync(process.execPath,[tool,'--seat','field-astra-of-6db4fe','--profile-file',fieldAstraProfile,'--predecessor','6db4fe','--cwd',dir],{encoding:'utf8'});
assert.notEqual(rejectedAstraModel.status,0);
fs.writeFileSync(fieldAstraProfile,JSON.stringify(fieldAstraProfileValue));
const rejectedAstraPredecessor=spawnSync(process.execPath,[tool,'--seat','field-astra-of-6db4fe','--profile-file',fieldAstraProfile,'--predecessor','1cb440','--cwd',dir],{encoding:'utf8'});
assert.notEqual(rejectedAstraPredecessor.status,0);
const currentAstraProfile=path.join(dir,'field-astra-of-03e825.json');
const currentAstraValue={...fieldAstraProfileValue,name:'field-astra-of-03e825',predecessor:'03e825',ancestor:'03e825'};
fs.writeFileSync(currentAstraProfile,JSON.stringify(currentAstraValue));
const currentAstraPlan=JSON.parse(execFileSync(process.execPath,[tool,'--seat','field-astra-of-03e825','--profile-file',currentAstraProfile,'--predecessor','03e825','--cwd',dir],{encoding:'utf8'}));
assert.equal(currentAstraPlan.model,'gpt-6-astra');assert.equal(currentAstraPlan.effort,'medium');assert.equal(currentAstraPlan.predecessor,'03e825');
const wrongCurrentAstraPredecessor=spawnSync(process.execPath,[tool,'--seat','field-astra-of-03e825','--profile-file',currentAstraProfile,'--predecessor','6db4fe','--cwd',dir],{encoding:'utf8'});
assert.notEqual(wrongCurrentAstraPredecessor.status,0);
fs.writeFileSync(currentAstraProfile,JSON.stringify({...currentAstraValue,model:'gpt-5.6-terra'}));
const wrongCurrentAstraModel=spawnSync(process.execPath,[tool,'--seat','field-astra-of-03e825','--profile-file',currentAstraProfile,'--predecessor','03e825','--cwd',dir],{encoding:'utf8'});
assert.notEqual(wrongCurrentAstraModel.status,0);
fs.writeFileSync(currentAstraProfile,JSON.stringify(currentAstraValue));
for (const seat of ['field-sol-current','field-astra-current']) {
  const missing=spawnSync(process.execPath,[tool,'--seat',seat],{encoding:'utf8'});
  assert.equal(missing.status,2);
  assert.match(missing.stderr,/require --predecessor/);
  const current=JSON.parse(execFileSync(process.execPath,[tool,'--seat',seat,'--predecessor','8565e8'],{encoding:'utf8'}));
  assert.equal(current.predecessor,'8565e8');
  assert.equal(current.ancestor,'1cb440');
  if (seat==='field-sol-current') assert.deepEqual(current.sources.map(source=>source.path),['flows/6db4fe/reports/field-sol-startup.md']);
  const text=execFileSync(process.execPath,[tool,'--seat',seat,'--predecessor','8565e8','--prompt'],{encoding:'utf8'});
  assert.match(text,/refreshed from 8565e8/);
  if (seat==='field-sol-current') { assert.match(text,/Lojix, Horizon, and OpenCode/); assert.doesNotMatch(text,/SHA-256|sha256|\b[a-f0-9]{16,}\b/); }
}
const fieldSolSuccessor=JSON.parse(execFileSync(process.execPath,[tool,'--seat','field-sol-of-395aed'],{encoding:'utf8'}));
assert.equal(fieldSolSuccessor.model,'gpt-5.6-sol');assert.equal(fieldSolSuccessor.effort,'medium');
assert.equal(fieldSolSuccessor.predecessor,'395aed');assert.equal(fieldSolSuccessor.ancestor,'395aed');
assert.deepEqual(fieldSolSuccessor.requiredSkillNames,['spirit','main-flow','field','refresh','psyche','psyche-acquisition','behavior','correction','vocabulary','testing','subflow','edit-coordination','orchestrate','flow-evidence','prompt-crafting','codex-harness','herdr','messaging','testing-flow-titles']);
assert.deepEqual(fieldSolSuccessor.sources.map(source=>source.path),['flows/8565e8/reports/refresh-handoff.md','flows/8565e8/reports/morning-2026-09-20.md','flows/8565e8/reports/lojix-schema-compatibility-addendum.md']);
assert.match(execFileSync(process.execPath,[tool,'--seat','field-sol-of-395aed','--prompt'],{encoding:'utf8'}),/refreshed from 395aed/);
for(const name of new Set([...plan.requiredSkillNames,...fieldSolPlan.requiredSkillNames])){const file=path.join(dir,'.agents/skills',name,'SKILL.md');fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,`# ${name}\n`);}
const uri=new URL(`file://${tool}`).href; const old=spawnSync(process.execPath,['--input-type=module','--eval',`import {rejectTokenOnly} from ${JSON.stringify(uri)};rejectTokenOnly('$main-flow')`],{encoding:'utf8'});assert.notEqual(old.status,0);assert.match(old.stderr,/not skill injection/);
const accepted=spawnSync(process.execPath,['--input-type=module','--eval',`import {structuredSkills,containsMainFlow} from ${JSON.stringify(uri)};let p='/x/main-flow/SKILL.md';if(!containsMainFlow({items:structuredSkills([{name:'main-flow',path:p}])},p))process.exit(9)`],{encoding:'utf8'});assert.equal(accepted.status,0,accepted.stderr);
const safe=spawnSync(process.execPath,[tool,'--seat','luna','--cwd',dir,'--launch'],{encoding:'utf8'});assert.equal(safe.status,2);assert.match(safe.stderr,/acknowledge-live-launch/);
const validSeat=['--seat','field-sol-of-7091ea','--profile-file',fieldSolProfile,'--predecessor','7091ea','--cwd',dir];
const noHash=spawnSync(process.execPath,[tool,...validSeat,'--launch','--acknowledge-live-launch'],{encoding:'utf8'});assert.notEqual(noHash.status,0);assert.match(noHash.stderr,/expected-runner-sha256/);
const wrongHash=spawnSync(process.execPath,[tool,...validSeat,'--launch','--acknowledge-live-launch','--expected-runner-sha256','0'.repeat(64)],{encoding:'utf8'});assert.notEqual(wrongHash.status,0);assert.match(wrongHash.stderr,/runner hash mismatch/);
const noActivation=spawnSync(process.execPath,[tool,'--seat','luna','--cwd',dir,'--activate','--receipt',path.join(dir,'missing-receipt.json')],{encoding:'utf8'});assert.notEqual(noActivation.status,0);

// Only the authorized fresh Mind Sol profile may create a receipt-first thread.
const socketPath=path.join(dir,'app-server.sock'); let connections=0;
const server=net.createServer(socket=>{connections++;socket.destroy();});
await new Promise(ok=>server.listen(socketPath,ok));
const runnerHash=crypto.createHash('sha256').update(fs.readFileSync(tool)).digest('hex');
const receipt=path.join(dir,'receipt.json');
const refused=await new Promise(resolve=>{const child=spawn(process.execPath,[tool,'--seat','luna','--name','fixture-native-seat','--cwd',dir,'--socket',socketPath,'--receipt',receipt,'--expected-runner-sha256',runnerHash,'--launch','--acknowledge-live-launch']);let out='',err='';child.stdout.on('data',d=>out+=d);child.stderr.on('data',d=>err+=d);child.on('exit',code=>resolve({code,out,err}));});
server.close();
assert.notEqual(refused.code,0);
assert.match(refused.err,/canonical role and testing-flow-titles are required/);
assert.equal(connections,0,'launch must not open app-server RPC');
assert.equal(fs.existsSync(receipt),false,'launch must not write a created-thread receipt');
fs.writeFileSync(mindSolProfile,JSON.stringify({name:'mind-sol',model:'gpt-5.6-sol',effort:'medium',role:'Mind Medium',fresh:true,predecessor:null,ancestor:null,skills:['spirit','main-flow','refresh','psyche','testing-flow-titles'],sourceManifest:['Vision/flowNexus.md'],...audited()}));
const launchedId='01a0c48c-e857-7df3-b86c-6cc6d11d4c25', launchedReceipt=path.join(dir,'launched-receipt.json');
let launchCalls=[],receiptPrecededTurn=false,launchedTurn;
const launchSocket=path.join(dir,'launch.sock'); let launchedTitle;
const launchServer=net.createServer(socket=>{let raw=Buffer.alloc(0),upgraded=false;const reply=(id,result)=>socket.write(serverFrame(JSON.stringify({jsonrpc:'2.0',id,result})));socket.on('data',data=>{raw=Buffer.concat([raw,data]);if(!upgraded){const end=raw.indexOf('\r\n\r\n');if(end<0)return;raw=raw.subarray(end+4);upgraded=true;socket.write('HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n\r\n');}while(raw.length>=2){let n=raw[1]&127,o=2;if(n===126){if(raw.length<4)return;n=raw.readUInt16BE(2);o=4;}if(raw.length<o+4+n)return;const mask=raw.subarray(o,o+4),body=Buffer.alloc(n);for(let i=0;i<n;i++)body[i]=raw[o+4+i]^mask[i%4];raw=raw.subarray(o+4+n);const request=JSON.parse(body);if(!request.id)continue;launchCalls.push(request.method);if(request.method==='skills/list')reply(request.id,['spirit','main-flow','refresh','psyche','testing-flow-titles'].map(name=>({name,path:path.join(dir,'.agents/skills',name,'SKILL.md')})));else if(request.method==='thread/start')reply(request.id,{thread:{id:launchedId}});else if(request.method==='thread/name/set'){launchedTitle=request.params.name;reply(request.id,{});}else if(request.method==='turn/start'){receiptPrecededTurn=fs.existsSync(launchedReceipt)&&JSON.parse(fs.readFileSync(launchedReceipt,'utf8')).status==='created';launchedTurn=request;reply(request.id,{turn:{id:'first-turn'}});}else if(request.method==='thread/read'&&!request.params.includeTurns)reply(request.id,{thread:{id:launchedId,name:launchedTitle}});else if(request.method==='thread/read')socket.write(serverFrame(JSON.stringify({jsonrpc:'2.0',id:request.id,error:{code:-32601,message:'list_turns is not supported yet'}})));else reply(request.id,{});}});});
await new Promise(ok=>launchServer.listen(launchSocket,ok));
const launched=await new Promise(resolve=>{const child=spawn(process.execPath,[tool,'--seat','mind-sol','--profile-file',mindSolProfile,'--fresh','--cwd',dir,'--socket',launchSocket,'--receipt',launchedReceipt,'--expected-runner-sha256',runnerHash,'--launch','--acknowledge-live-launch']);let out='',err='';child.stdout.on('data',d=>out+=d);child.stderr.on('data',d=>err+=d);child.on('exit',code=>resolve({code,out,err}));});
launchServer.close();
assert.equal(launched.code,0,launched.err);
assert.deepEqual(launchCalls,['initialize','skills/list','thread/start','thread/name/set','thread/read','turn/start','thread/read']);
assert.equal(receiptPrecededTurn,true,'native receipt must exist before the first target turn');
assert.equal(JSON.parse(fs.readFileSync(launchedReceipt,'utf8')).threadId,launchedId);
assert.ok(launchedTurn.params.input.some(input=>input.type==='skill'&&input.name==='main-flow'));
assert.equal(JSON.parse(launched.out).readiness,'pending');
// Adoption uses an already-running Herdr Codex pane and an existing empty
// native thread. The fake app-server fails the fixture if thread/start occurs.
const adoptedId='01a0bf90-41fd-72a1-ac8b-ee9c1dab9a41';
const bin=path.join(dir,'bin'); fs.mkdirSync(bin);
const fakeHerdr=path.join(bin,'herdr');
fs.writeFileSync(fakeHerdr,`#!${process.execPath}
const args=process.argv.slice(2);
if(args.includes('--json')) process.exit(8);
if(args.includes('agent')&&args.includes('get')) console.log(JSON.stringify({result:{agent:{name:'field-sol-of-8565e8',pane_id:'wN:p1',terminal_id:'term_fixture',workspace_id:'wN',cwd:${JSON.stringify(dir)},agent:'codex',interactive_ready:true,agent_status:'idle',revision:3}}}));
else if(args.includes('pane')&&args.includes('get')) console.log(JSON.stringify({result:{pane:{pane_id:'wN:p1',terminal_id:'term_fixture',workspace_id:'wN',cwd:${JSON.stringify(dir)},agent:'codex',revision:3}}}));
else if(args.includes('pane')&&args.includes('read')) console.log('│  Session:              ${adoptedId} │');
else process.exit(9);
`,{mode:0o755});
const adoptedRollout=path.join(dir,'.codex','sessions','2026','09','20',`rollout-${adoptedId}.jsonl`);fs.mkdirSync(path.dirname(adoptedRollout),{recursive:true});
const adoptedSocket=path.join(dir,'adopt.sock'); let firstTurn,adoptedCalls=[],adoptedTitle;
const adoptedServer=net.createServer(socket=>{let raw=Buffer.alloc(0),upgraded=false;const reply=(id,result)=>socket.write(serverFrame(JSON.stringify({jsonrpc:'2.0',id,result})));socket.on('data',data=>{raw=Buffer.concat([raw,data]);if(!upgraded){const end=raw.indexOf('\r\n\r\n');if(end<0)return;raw=raw.subarray(end+4);upgraded=true;socket.write('HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n\r\n');}while(raw.length>=2){let n=raw[1]&127,o=2;if(n===126){if(raw.length<4)return;n=raw.readUInt16BE(2);o=4;}if(raw.length<o+4+n)return;const mask=raw.subarray(o,o+4),body=Buffer.alloc(n);for(let i=0;i<n;i++)body[i]=raw[o+4+i]^mask[i%4];raw=raw.subarray(o+4+n);const request=JSON.parse(body);if(!request.id)continue;adoptedCalls.push(request.method);if(request.method==='thread/start')throw new Error('app-server-only thread creation attempted');if(request.method==='thread/name/set'){adoptedTitle=request.params.name;reply(request.id,{});}else if(request.method==='thread/read'&&!request.params.includeTurns)reply(request.id,{thread:{id:adoptedId,name:adoptedTitle}});else if(request.method==='thread/read')socket.write(serverFrame(JSON.stringify({jsonrpc:'2.0',id:request.id,error:{code:-32601,message:'list_turns is not supported yet'}})));else if(request.method==='skills/list')reply(request.id,fieldSolPlan.requiredSkillNames.map(name=>({name,path:path.join(dir,'.agents/skills',name,'SKILL.md')})));else if(request.method==='turn/start'){firstTurn=request;const skills=fieldSolPlan.requiredSkillNames.map(name=>({type:'skill',name,path:path.join(dir,'.agents/skills',name,'SKILL.md')}));const expanded=skills.map(s=>({type:'response_item',payload:{role:'user',content:[{text:`<skill>\n<name>${s.name}</name>\n<path>${s.path}</path>\n# ${s.name}\n</skill>`}]}}));const rows=[{type:'turn_context',payload:{turn_id:'first-turn',model:'gpt-5.6-sol',effort:'medium'}},{type:'event_msg',payload:{thread_id:adoptedId,turn_id:'first-turn',item:{type:'UserMessage',content:[...skills,{type:'text',text:firstTurn.params.input.at(-1).text}]}}},...expanded,{type:'event_msg',payload:{thread_id:adoptedId,turn_id:'first-turn',item:{type:'AgentMessage',content:[{type:'Text',text:'Native context is present.'}]}}}];fs.writeFileSync(adoptedRollout,[JSON.stringify({type:'session_meta',payload:{id:adoptedId,cwd:dir}}),...rows.map(JSON.stringify)].join('\n')+'\n');reply(request.id,{turn:{id:'first-turn'}});}else reply(request.id,{});}});});
await new Promise(ok=>adoptedServer.listen(adoptedSocket,ok));
const adoptedReceipt=path.join(dir,'adopted-receipt.json');
const adopted=await new Promise(resolve=>{const child=spawn(process.execPath,[tool,...validSeat,'--socket',adoptedSocket,'--receipt',adoptedReceipt,'--herdr-rollout',adoptedRollout,'--expected-runner-sha256',runnerHash,'--adopt-herdr-thread',adoptedId,'--herdr-session','messaging-build','--herdr-pane','wN:p1','--herdr-agent','field-sol-of-8565e8','--herdr-terminal','term_fixture','--acknowledge-live-launch'],{env:{...process.env,HOME:dir,PATH:`${bin}:${process.env.PATH}`}});let out='',err='';child.stdout.on('data',d=>out+=d);child.stderr.on('data',d=>err+=d);child.on('exit',code=>resolve({code,out,err}));});
adoptedServer.close();
assert.equal(adopted.code,0,adopted.err);
assert.deepEqual(adoptedCalls,['initialize','thread/read','skills/list','thread/name/set','thread/read','turn/start','thread/read']);
assert.ok(firstTurn.params.input.some(i=>i.type==='skill'&&i.name==='main-flow'));
assert.equal(JSON.parse(adopted.out).readiness,'native-context-verified-title-pending');
assert.equal(JSON.parse(fs.readFileSync(adoptedReceipt,'utf8')).herdr.paneId,'wN:p1');
// Receipt verification never searches a prior turn, and each observed native
// field is a hard gate.  The payload also crosses the 64 KiB websocket frame.
const source='x'.repeat(70_000), hash=v=>crypto.createHash('sha256').update(v).digest('hex');
const receiptShape={threadId:'t',turnId:'u',generationId:'g',model:'m',effort:'e',firstPromptSha256:hash('p'),sourceManifestSha256:'manifest',skillManifest:[{name:'main-flow',path:'/s',source,sha256:hash(source)}]};
const good={thread:{id:'t',turns:[{id:'u',generationId:'g',output_text:'Native context is present.',turn_context:{model:'m',effort:'e',prompt:'p',sourceManifestSha256:'manifest',skills:[{type:'skill',name:'main-flow',path:'/s',source}]}}]}};
assert.equal(verifyReceipt({thread:{id:'t',turns:[]}},receiptShape).readiness,'pending');
for(const [label,mutate] of [['model',x=>x.thread.turns[0].turn_context.model='bad'],['effort',x=>x.thread.turns[0].turn_context.effort='bad'],['generation',x=>x.thread.turns[0].generationId='bad'],['manifest',x=>x.thread.turns[0].turn_context.sourceManifestSha256='bad'],['skill source',x=>x.thread.turns[0].turn_context.skills[0].source='bad'],['missing skill',x=>x.thread.turns[0].turn_context.skills=[]],['prior turn',x=>x.thread.turns[0].id='old']]) { const bad=structuredClone(good);mutate(bad);assert.throws(()=>verifyReceipt(bad,receiptShape),/verification refused/,label); }
assert.equal(verifyReceipt(good,receiptShape).readiness,'native-context-verified-title-pending');
const rollout=path.join(dir,'rollout.jsonl'), rolloutRows=[{type:'session_meta',payload:{id:'t'}},{type:'turn_context',payload:{turn_id:'u',model:'m',effort:'e'}},{type:'event_msg',payload:{thread_id:'t',turn_id:'u',item:{type:'UserMessage',content:[{type:'skill',name:'main-flow',path:'/s'},{type:'text',text:'p'}]}}},{type:'response_item',payload:{role:'user',content:[{text:`<skill>\n<name>main-flow</name>\n<path>/s</path>\n${source}\n</skill>`}]}},{type:'event_msg',payload:{thread_id:'t',turn_id:'u',item:{type:'AgentMessage',content:[{type:'Text',text:'Native context is present.'}]}}}];fs.writeFileSync(rollout,rolloutRows.map(JSON.stringify).join('\n')+'\n');
assert.equal(verifyRolloutReceipt(rollout,receiptShape).readiness,'native-context-verified-title-pending');rolloutRows[3].payload.content[0].text='<skill>missing expansion</skill>';fs.writeFileSync(rollout,rolloutRows.map(JSON.stringify).join('\n')+'\n');assert.throws(()=>verifyRolloutReceipt(rollout,receiptShape),/expanded skill source/);rolloutRows[1].payload.model='bad';fs.writeFileSync(rollout,rolloutRows.map(JSON.stringify).join('\n')+'\n');assert.throws(()=>verifyRolloutReceipt(rollout,receiptShape),/verification refused/);
assert.deepEqual(canonicalRole('Field Sol'),{aspect:'Field',power:'Medium'});
assert.deepEqual(canonicalRole('Psyche Ultra Low'),{aspect:'Psyche',power:'Ultra Low'});
assert.equal(canonicalRole('Field Astra Power'),null);
assert.equal(canonicalRole('Field Sol 753e69'),null);

// A verified context remains pending until the exact native claim marker and
// title set/readback succeed. A failed readback must leave the receipt pending.
const claimId='1d4c25';
const claimDir=path.join(dir,'flows');fs.mkdirSync(claimDir,{recursive:true});
const claimFile=path.join(claimDir,`.${claimId}.flow-id`);
const finalizeSocket=path.join(dir,'finalize.sock');
let finalTitle=JSON.parse(fs.readFileSync(launchedReceipt,'utf8')).provisionalTitle;
let failReadback=false, finalizeCalls=[], finalReadCount=0;
const finalizeServer=net.createServer(socket=>{let raw=Buffer.alloc(0),upgraded=false;const reply=(id,result)=>socket.write(serverFrame(JSON.stringify({jsonrpc:'2.0',id,result})));socket.on('data',data=>{raw=Buffer.concat([raw,data]);if(!upgraded){const end=raw.indexOf('\r\n\r\n');if(end<0)return;raw=raw.subarray(end+4);upgraded=true;socket.write('HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n\r\n');}while(raw.length>=2){let n=raw[1]&127,o=2;if(n===126){if(raw.length<4)return;n=raw.readUInt16BE(2);o=4;}if(raw.length<o+4+n)return;const mask=raw.subarray(o,o+4),body=Buffer.alloc(n);for(let i=0;i<n;i++)body[i]=raw[o+4+i]^mask[i%4];raw=raw.subarray(o+4+n);const request=JSON.parse(body);if(!request.id)continue;finalizeCalls.push(request.method);if(request.method==='thread/read')reply(request.id,{thread:{id:launchedId,name:failReadback && ++finalReadCount===2?'stale native title':finalTitle}});else if(request.method==='thread/name/set'){finalTitle=request.params.name;reply(request.id,{});}else reply(request.id,{});}});});
await new Promise(ok=>finalizeServer.listen(finalizeSocket,ok));
const finalizeArgs=[tool,'--seat','mind-sol','--profile-file',mindSolProfile,'--fresh','--cwd',dir,'--socket',finalizeSocket,'--receipt',launchedReceipt,'--finalize-title','--flow-id',claimId];
const finalizeRun=()=>new Promise(resolve=>{const child=spawn(process.execPath,finalizeArgs,{encoding:'utf8'});let out='',err='';child.stdout.on('data',d=>out+=d);child.stderr.on('data',d=>err+=d);child.on('exit',code=>resolve({code,out,err}));});
let pending=JSON.parse(fs.readFileSync(launchedReceipt,'utf8'));pending.status='verified';pending.turnId='first-turn';fs.writeFileSync(launchedReceipt,JSON.stringify(pending));
let attempt=await finalizeRun();assert.notEqual(attempt.code,0);assert.match(attempt.err,/ENOENT/);assert.equal(finalizeCalls.length,0);
fs.writeFileSync(claimFile,`version=1\nharness=codex\nidentity=${'0'.repeat(32)}\nalias=${claimId}\n`);
attempt=await finalizeRun();assert.notEqual(attempt.code,0);assert.match(attempt.err,/claim marker differs/);assert.equal(finalizeCalls.length,0);
fs.writeFileSync(claimFile,`version=1\nharness=codex\nidentity=${launchedId.replaceAll('-','')}\nalias=${claimId}\n`);
failReadback=true;finalReadCount=0;attempt=await finalizeRun();assert.notEqual(attempt.code,0);assert.match(attempt.err,/provisional title restored/);assert.equal(finalTitle,pending.provisionalTitle);assert.equal(JSON.parse(fs.readFileSync(launchedReceipt,'utf8')).status,'verified');
failReadback=false;attempt=await finalizeRun();assert.equal(attempt.code,0,attempt.err);assert.equal(JSON.parse(attempt.out).title,`Mind Medium ${claimId}`);assert.equal(JSON.parse(fs.readFileSync(launchedReceipt,'utf8')).status,'ready');assert.deepEqual(finalizeCalls.slice(-3),['thread/read','thread/name/set','thread/read']);
finalizeServer.close();
console.log('native-seat-launch fixtures passed');


function serverFrame(text){const body=Buffer.from(text);return body.length<126?Buffer.concat([Buffer.from([129,body.length]),body]):Buffer.concat([Buffer.from([129,126,body.length>>8,body.length&255]),body]);}
