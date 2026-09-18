#!/usr/bin/env node
/* Native seat launcher: typed skills, fat source bundle, post-start receipt. */
import crypto from 'node:crypto';
import fs from 'node:fs';
import net from 'node:net';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const args = process.argv.slice(2);
const option = name => { const i = args.indexOf(name); return i < 0 ? undefined : args[i + 1]; };
const has = name => args.includes(name);
const seat = option('--seat');
const cwd = path.resolve(option('--cwd') ?? ROOT);
const disposableProbe = has('--disposable-probe');
const probeDirectory = option('--probe-directory');
const invokedDirectly = Boolean(process.argv[1]) && path.resolve(process.argv[1]) === path.resolve(new URL(import.meta.url).pathname);
const roles = {
  astra: { model: 'gpt-6-astra', effort: 'medium', role: 'Field Astra', predecessor: 'cf3553', skills: ['spirit','main-flow','psyche','behavior','correction','vocabulary','testing','subflow','edit-coordination','orchestrate','flow-evidence','prompt-crafting','codex-harness'] },
  sol: { model: 'gpt-5.6-sol', effort: 'medium', role: 'Field Sol', predecessor: '3b1574', skills: ['spirit','main-flow','psyche','behavior','correction','vocabulary','subflow','edit-coordination'] },
  luna: { model: 'gpt-5.6-luna', effort: 'medium', role: 'low Codex seat', predecessor: null, skills: ['spirit','main-flow','psyche','behavior','vocabulary','subflow'] },
};
if (!roles[seat] && invokedDirectly) { console.error('usage: native-seat-launch.mjs --seat <astra|sol|luna> [--cwd DIR] [--plan|--prompt|--launch --acknowledge-live-launch]'); process.exit(2); }
if (disposableProbe && !probeDirectory) { console.error('--disposable-probe requires --probe-directory'); process.exit(2); }
const role = roles[seat];
const digest = value => crypto.createHash('sha256').update(value).digest('hex');
function sources() {
  const fixed = ['Vision/flowNexus.md','Vision/nexus.md','flows/cf3553/vision/operational-mainFlowStartupCorrection.md'];
  const old = path.join(cwd, 'flows/da1e3f/vision');
  if (fs.existsSync(old)) fixed.push(...fs.readdirSync(old).filter(f => /^operational.*\.md$/.test(f)).sort().map(f => `flows/da1e3f/vision/${f}`));
  return fixed.filter(f => fs.existsSync(path.join(cwd, f))).map(file => ({ path: file, body: fs.readFileSync(path.join(cwd, file), 'utf8'), sha256: digest(fs.readFileSync(path.join(cwd, file), 'utf8')) }));
}
function buildPlan() {
  const manifest = sources();
  const probe = disposableProbe ? `\n\nThis is a disposable native receipt probe. Its only identity directory is \`${probeDirectory}\`. Before reporting, delegate one harmless task that must not run commands, read files, or mutate anything: have the disposable helper restate this startup boundary. Then report the delegation receipt and your native main-flow acknowledgement. Do not create a Flow directory or registration.` : '';
  const firstPrompt = `# Native main-flow refresh\n\nYou are ${role.role}, refreshed from ${role.predecessor ?? 'the witnessed predecessor'}; that provenance does not retire, replace, or deregister any predecessor. Preserve your native model and effort. Claim the actual Flow identity after startup.\n\nThe launcher sends these role-specific skills through the native structured interface: ${role.skills.join(', ')}. A written dollar token is not skill receipt.\n\nAll sources below are attached once with provenance. They are source material, not evidence of a deployment, migration, registration, or seat retirement.\n\n${manifest.map(s => `## Source: \`${s.path}\`\n\nSHA-256: \`${s.sha256}\`\n\n${s.body.trim()}`).join('\n\n')}\n\nFirst state your actual identity and whether native main-flow context is present. The only authorized readiness activity is a harmless no-command probe. Do not launch, restart, retire, register, or mutate another seat.${probe}`;
  return { version: 1, seat, cwd, model: role.model, effort: role.effort, role: role.role, predecessor: role.predecessor, requiredSkillNames: role.skills, requiredMainFlow: { name: 'main-flow', path: path.join(cwd, '.agents/skills/main-flow/SKILL.md') }, sources: manifest.map(({body,...rest}) => rest), firstPrompt, firstPromptSha256: digest(firstPrompt), safety: { noImplicitPredecessorRetirement: true, registrationAfterReadinessOnly: true, readyRequiresExpandedNativeMainFlow: true } };
}
function rejectTokenOnly(text) { if (/\$main-flow|\/main-flow/.test(text)) throw new Error('text token is not skill injection; use typed {type:"skill",name:"main-flow",path} input'); }
function structuredSkills(skills) { return skills.map(skill => ({ type: 'skill', name: skill.name, path: skill.path })); }
function containsMainFlow(value, expectedPath) { if (Array.isArray(value)) return value.some(v => containsMainFlow(v, expectedPath)); if (!value || typeof value !== 'object') return false; if (value.type === 'skill' && value.name === 'main-flow' && value.path === expectedPath) return true; return Object.values(value).some(v => containsMainFlow(v, expectedPath)); }
function frame(payload, opcode = 1) { const body = Buffer.from(payload), mask = crypto.randomBytes(4); let header; if (body.length < 126) header = Buffer.from([128|opcode,128|body.length]); else { header = Buffer.alloc(4); header[0]=128|opcode; header[1]=254; header.writeUInt16BE(body.length,2); } const encrypted = Buffer.alloc(body.length); for(let i=0;i<body.length;i++) encrypted[i]=body[i]^mask[i%4]; return Buffer.concat([header,mask,encrypted]); }
async function withRpc(socketPath, fn) { return new Promise((resolve,reject) => { const socket=net.createConnection(socketPath); let buf=Buffer.alloc(0), upgraded=false, next=0, fragment=null; const pending=new Map(); const fail=e=>{socket.destroy();reject(e);}; const call=(method,params)=>new Promise((ok,no)=>{const id=++next;const timer=setTimeout(()=>{pending.delete(id);no(new Error(`RPC timeout: ${method}`));},15000);pending.set(id,{ok,no,timer});socket.write(frame(JSON.stringify({jsonrpc:'2.0',id,method,params})));}); const parse=()=>{while(buf.length>=2){const fin=!!(buf[0]&128),opcode=buf[0]&15;let n=buf[1]&127,offset=2;if(n===126){if(buf.length<4)return;n=buf.readUInt16BE(2);offset=4;}if(buf.length<offset+n)return;const body=buf.subarray(offset,offset+n);buf=buf.subarray(offset+n);if(opcode===9){socket.write(frame(body,10));continue;}if(opcode===1)fragment=body;else if(opcode===0&&fragment)fragment=Buffer.concat([fragment,body]);else continue;if(!fin)continue;const message=JSON.parse(fragment);fragment=null;const wait=pending.get(message.id);if(wait){pending.delete(message.id);clearTimeout(wait.timer);message.error?wait.no(new Error(JSON.stringify(message.error))):wait.ok(message.result);}}}; socket.on('error',fail);socket.on('connect',()=>socket.write('GET / HTTP/1.1\r\nHost: localhost\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\n\r\n'));socket.on('data',data=>{buf=Buffer.concat([buf,data]);if(!upgraded){const end=buf.indexOf('\r\n\r\n');if(end<0)return;if(!buf.subarray(0,end).toString().startsWith('HTTP/1.1 101'))return fail(new Error('websocket upgrade refused'));buf=buf.subarray(end+4);upgraded=true;void(async()=>{try{await call('initialize',{clientInfo:{name:'native-seat-launch',version:'1'}});socket.write(frame(JSON.stringify({jsonrpc:'2.0',method:'initialized',params:{}})));resolve(await fn(call));socket.end();}catch(e){fail(e);}})();}parse();});});}
async function launch(plan) { const socket=option('--socket') ?? `${process.env.HOME}/.codex/app-server-control/app-server-control.sock`; const result=await withRpc(socket,async call=>{const reply=await call('skills/list',{cwds:[cwd]});const available=reply.skills??reply;if(!Array.isArray(available))throw new Error('skills/list did not return an array');const map=new Map(available.map(s=>[s.name,s]));const skills=role.skills.map(name=>{const found=map.get(name);if(!found?.path)throw new Error(`required native skill unavailable: ${name}`);return {name,path:found.path};});const main=skills.find(s=>s.name==='main-flow');rejectTokenOnly(plan.firstPrompt);const started=await call('thread/start',{model:role.model,cwd,approvalPolicy:'never',sandbox:'danger-full-access'});const threadId=started.thread?.id??started.id;if(!threadId)throw new Error('thread/start returned no id');const turn=await call('turn/start',{threadId,effort:role.effort,input:[...structuredSkills(skills),{type:'text',text:plan.firstPrompt}]});const items=await call('thread/items/list',{threadId});if(!containsMainFlow(items,main.path))throw new Error('launch refused: thread/items/list lacks expanded native main-flow item');return {threadId,turnId:turn.turn?.id??turn.id??null,nativeMainFlowPath:main.path,readiness:'native-main-flow-witnessed',registrationPerformed:false,predecessorRetired:false};});console.log(JSON.stringify(result)); }
if (invokedDirectly) {
  const plan=buildPlan();
  if(has('--prompt')) console.log(plan.firstPrompt); else if(has('--launch')) { if(!has('--acknowledge-live-launch')) { console.error('--launch requires --acknowledge-live-launch'); process.exit(2); } await launch(plan); } else console.log(JSON.stringify({...plan,firstPrompt:undefined},null,2));
}
export { rejectTokenOnly, structuredSkills, containsMainFlow };
