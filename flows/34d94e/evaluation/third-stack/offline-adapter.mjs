#!/usr/bin/env node
// Requires an explicitly supplied OpenCode executable; never discovers or installs one.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import http from 'node:http';
import {spawn} from 'node:child_process';

const arg=process.argv.indexOf('--opencode');
if(arg<0||!process.argv[arg+1]?.startsWith('/')) throw new Error('usage: offline-adapter.mjs --opencode /absolute/path/to/opencode');
const binary=process.argv[arg+1];
if(!fs.existsSync(binary)) { console.log(JSON.stringify({status:'adapter-witness-pending',reason:'explicit OpenCode binary is absent',binary})); process.exit(2); }
const requests=[];
const sse=(res,events)=>{res.writeHead(200,{'content-type':'text/event-stream','cache-control':'no-cache'}); for(const event of events) res.write(`data: ${JSON.stringify(event)}\n\n`); res.end();};
const server=http.createServer((req,res)=>{let body=''; req.on('data',c=>body+=c); req.on('end',()=>{if(req.url!=='/v1/chat/completions'){res.writeHead(404);return res.end();} const json=JSON.parse(body); requests.push(json); if(requests.length===1) return sse(res,[{choices:[{delta:{role:'assistant',reasoning_content:'fixture reasoning'}}]},{choices:[{delta:{tool_calls:[{index:0,id:'call_fixture',type:'function',function:{name:'read_fixture',arguments:'{"path":"fixture.txt"}'}}]}}]},{choices:[{finish_reason:'tool_calls',delta:{}}]},{choices:[]}]); return sse(res,[{choices:[{delta:{role:'assistant',content:'fixture stop'}}]},{choices:[{finish_reason:'stop',delta:{}}]}]);});});
const port=await new Promise(resolve=>server.listen(0,'127.0.0.1',()=>resolve(server.address().port)));
const dir=fs.mkdtempSync(path.join(os.tmpdir(),'third-stack-opencode-')); const config=path.join(dir,'opencode.json');
fs.writeFileSync(config,JSON.stringify({provider:{fixture:{npm:'@ai-sdk/openai-compatible',options:{baseURL:`http://127.0.0.1:${port}/v1`},models:{fixture:{name:'fixture',reasoning:true,tool_call:true,interleaved:{field:'reasoning_content'}}}}}}));
const child=spawn(binary,['run','--format','json','--model','fixture/fixture','read fixture.txt'],{env:{...process.env,XDG_CONFIG_HOME:dir,OPENCODE_CONFIG:config},stdio:['ignore','pipe','pipe']}); let stderr=''; child.stderr.on('data',d=>stderr+=d); const exit=await new Promise(resolve=>child.on('close',(code,signal)=>resolve({code,signal})));
server.close(); fs.rmSync(dir,{recursive:true,force:true});
if(exit.code!==0) throw new Error(`OpenCode exited ${JSON.stringify(exit)}: ${stderr.slice(0,500)}`);
if(requests.length<2) throw new Error(`expected assistant/tool continuation, received ${requests.length} requests`);
const first=JSON.stringify(requests[0]); const second=JSON.stringify(requests[1]);
if(!first.includes('reasoning_content')||!first.includes('call_fixture')||!second.includes('reasoning_content')||!second.includes('call_fixture')||!second.includes('fixture.txt')) throw new Error('assistant reasoning/tool-call or matching tool result was not preserved');
console.log(JSON.stringify({status:'adapter-replay-passed',requests:requests.length,provider_calls:0,model_downloads:0}));
