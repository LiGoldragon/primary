#!/usr/bin/env node
// Exercise the packaged OpenCode client against a local, fixed refusal. No
// descriptor, credential, or remote address is accepted by this command.
import fs from 'node:fs';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import {spawn} from 'node:child_process';

const VERSION = '1.17.13';
const TIMEOUT = 8_000;
const arg = name => { const i = process.argv.indexOf(name); return i < 0 ? undefined : process.argv[i + 1]; };
const binary = arg('--opencode');
if (!binary || !path.isAbsolute(binary) || !fs.existsSync(binary)) throw new Error('usage: refusal-dry-run.mjs --opencode /absolute/path/to/opencode');

function collect(child) { return new Promise(resolve => { let stdout='', stderr='', done=false; const finish=result=>{if(done)return;done=true;clearTimeout(timer);resolve({...result,stdout,stderr});}; child.stdout.on('data',b=>stdout=(stdout+b).slice(-131072)); child.stderr.on('data',b=>stderr=(stderr+b).slice(-131072)); child.once('error',error=>finish({error})); child.once('close',(code,signal)=>finish({code,signal})); const timer=setTimeout(()=>{try{process.kill(-child.pid,'SIGTERM')}catch{};setTimeout(()=>{try{process.kill(-child.pid,'SIGKILL')}catch{}},750).unref();},TIMEOUT); }); }
function env(home, config) { return {HOME:home, PATH:process.env.PATH||'/usr/bin:/bin', LANG:'C.UTF-8', LC_ALL:'C.UTF-8', XDG_CONFIG_HOME:path.join(home,'config'), XDG_DATA_HOME:path.join(home,'data'), XDG_STATE_HOME:path.join(home,'state'), XDG_CACHE_HOME:path.join(home,'cache'), OPENCODE_CONFIG:config, OPENAI_API_KEY:'inert-loopback-key'}; }
const root=fs.mkdtempSync(path.join(os.tmpdir(),'third-seat-refusal-'));
let server, child;
const sockets = new Set();
try {
  const home=path.join(root,'home'); fs.mkdirSync(path.join(home,'config'),{recursive:true});
  const version=await collect(spawn(binary,['--version'],{env:env(home,path.join(home,'config','opencode.json')),stdio:['ignore','pipe','pipe'],detached:true}));
  if (version.code !== 0 || !(`${version.stdout}\n${version.stderr}`).match(new RegExp(`\\b${VERSION.replaceAll('.','\\.')}\\b`))) throw new Error(`expected OpenCode ${VERSION}`);
  let requests=0, rejected=0;
  server=http.createServer((req,res)=>{ requests++; let body=''; req.on('data',b=>body+=b); req.on('end',()=>{ if(req.method==='POST'&&req.url==='/v1/chat/completions'&&body) rejected++; res.writeHead(503,{'content-type':'application/json'}); res.end(JSON.stringify({error:{message:'local fixture refusal'}})); }); });
  server.on('connection', socket => { sockets.add(socket); socket.once('close', () => sockets.delete(socket)); });
  await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve)});
  const base=`http://127.0.0.1:${server.address().port}/v1`;
  const config=path.join(home,'config','opencode.json'); const id='fixture/kimi-k3-refusal';
  fs.writeFileSync(config,JSON.stringify({autoupdate:false,plugin:[],provider:{fixture:{npm:'@ai-sdk/openai-compatible',options:{baseURL:base,apiKey:'inert-loopback-key'},models:{'kimi-k3-refusal':{name:'kimi-k3-refusal',reasoning:true,tool_call:true}}}},permission:{'*':'deny'}}));
  child=spawn(binary,['run','--format','json','--model',id,'Return exactly one word.'],{cwd:root,env:env(home,config),stdio:['ignore','pipe','pipe'],detached:true});
  const result=await collect(child); child=undefined;
  if (!requests || !rejected) throw new Error('OpenCode did not reach the local refusal endpoint');
  if (result.code === 0) throw new Error('OpenCode accepted the fixed refusal');
  const output=`${result.stdout}\n${result.stderr}`;
  if (output.includes('inert-local-secret')) throw new Error('local secret escaped');
  process.stdout.write(JSON.stringify({status:'localhost-refusal-passed',opencode_version:VERSION,requests,rejected,external_connections:0,provider_calls:0})+'\n');
} finally {
  if (child?.pid) { try { process.kill(-child.pid,'SIGKILL'); } catch {} }
  if (server) { for (const socket of sockets) socket.destroy(); await Promise.race([new Promise(resolve=>server.close(()=>resolve())),new Promise(resolve=>setTimeout(resolve,1_000))]); }
  fs.rmSync(root,{recursive:true,force:true});
}
