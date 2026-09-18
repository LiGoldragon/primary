#!/usr/bin/env node
import assert from 'node:assert/strict';
import {execFileSync,spawn,spawnSync} from 'node:child_process';
import fs from 'node:fs'; import net from 'node:net'; import os from 'node:os'; import path from 'node:path';
const tool=path.join(import.meta.dirname,'native-seat-launch.mjs'); const dir=fs.mkdtempSync(path.join(os.tmpdir(),'native-seat-launch-'));
for(const file of ['Vision/flowNexus.md','Vision/nexus.md','flows/cf3553/vision/operational-mainFlowStartupCorrection.md','flows/da1e3f/vision/operational-launcher.md']) { fs.mkdirSync(path.dirname(path.join(dir,file)),{recursive:true});fs.writeFileSync(path.join(dir,file),'# fixture\n'); }
const plan=JSON.parse(execFileSync(process.execPath,[tool,'--seat','luna','--cwd',dir],{encoding:'utf8'})); const prompt=execFileSync(process.execPath,[tool,'--seat','luna','--cwd',dir,'--prompt'],{encoding:'utf8'}); assert.equal(plan.requiredMainFlow.name,'main-flow'); assert.ok(plan.sources.some(s=>s.path.includes('operational-mainFlowStartupCorrection'))); assert.doesNotMatch(prompt,/\$main-flow/);
const uri=new URL(`file://${tool}`).href; const old=spawnSync(process.execPath,['--input-type=module','--eval',`import {rejectTokenOnly} from ${JSON.stringify(uri)};rejectTokenOnly('$main-flow')`],{encoding:'utf8'});assert.notEqual(old.status,0);assert.match(old.stderr,/not skill injection/);
const accepted=spawnSync(process.execPath,['--input-type=module','--eval',`import {structuredSkills,containsMainFlow} from ${JSON.stringify(uri)};let p='/x/main-flow/SKILL.md';if(!containsMainFlow({items:structuredSkills([{name:'main-flow',path:p}])},p))process.exit(9)`],{encoding:'utf8'});assert.equal(accepted.status,0,accepted.stderr);
const safe=spawnSync(process.execPath,[tool,'--seat','luna','--cwd',dir,'--launch'],{encoding:'utf8'});assert.equal(safe.status,2);assert.match(safe.stderr,/acknowledge-live-launch/);

// Disposable app-server fixture: readiness is accepted only when the actual
// turn payload has a typed main-flow input and items/list echoes that item.
const socketPath=path.join(dir,'app-server.sock'); let turnStart;
const rolloutPath=path.join(dir,'fixture-thread-rollout.jsonl');
fs.writeFileSync(rolloutPath, `<skill>\n<name>main-flow</name>\n<path>${path.join(dir,'.agents/skills/main-flow/SKILL.md')}</path>\nbody\n</skill>`);
const server=net.createServer(socket=>{let raw=Buffer.alloc(0),upgraded=false; const reply=(id,result)=>socket.write(serverFrame(JSON.stringify({jsonrpc:'2.0',id,result}))); socket.on('data',data=>{raw=Buffer.concat([raw,data]);if(!upgraded){const end=raw.indexOf('\r\n\r\n');if(end<0)return;raw=raw.subarray(end+4);upgraded=true;socket.write('HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n\r\n');}while(raw.length>=2){let n=raw[1]&127,o=2;if(n===126){if(raw.length<4)return;n=raw.readUInt16BE(2);o=4;}if(raw.length<o+4+n)return;const mask=raw.subarray(o,o+4),body=Buffer.alloc(n);for(let i=0;i<n;i++)body[i]=raw[o+4+i]^mask[i%4];raw=raw.subarray(o+4+n);const request=JSON.parse(body);if(!request.id)continue;if(request.method==='skills/list')reply(request.id,[...plan.requiredSkillNames].map(name=>({name,path:path.join(dir,'.agents/skills',name,'SKILL.md')})));else if(request.method==='thread/start')reply(request.id,{thread:{id:'fixture-thread'}});else if(request.method==='turn/start'){turnStart=request;reply(request.id,{turn:{id:'fixture-turn'}});}else if(request.method==='thread/read')reply(request.id,{thread:{id:'fixture-thread',path:rolloutPath}});else reply(request.id,{});}});});
await new Promise(ok=>server.listen(socketPath,ok));
const launched=await new Promise(resolve=>{const child=spawn(process.execPath,[tool,'--seat','luna','--name','fixture-native-seat','--cwd',dir,'--socket',socketPath,'--launch','--acknowledge-live-launch']);let out='',err='';child.stdout.on('data',d=>out+=d);child.stderr.on('data',d=>err+=d);child.on('exit',code=>resolve({code,out,err}));}); server.close();
assert.equal(launched.code,0,launched.err); assert.ok(turnStart.params.input.some(i=>i.type==='skill'&&i.name==='main-flow')); assert.equal(JSON.parse(launched.out).readiness,'native-main-flow-expanded-witnessed');
assert.equal(JSON.parse(launched.out).threadName,'fixture-native-seat');
console.log('native-seat-launch fixtures passed');

function serverFrame(text){const body=Buffer.from(text);return body.length<126?Buffer.concat([Buffer.from([129,body.length]),body]):Buffer.concat([Buffer.from([129,126,body.length>>8,body.length&255]),body]);}
