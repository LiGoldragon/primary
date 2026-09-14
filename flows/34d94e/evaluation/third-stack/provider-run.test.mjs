#!/usr/bin/env node
// Offline-only runner tests. The CA enters main's test dependency, never TLS bypass settings.
import assert from 'node:assert/strict'; import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path';
import {main} from './provider-run.mjs';
const root=fs.mkdtempSync(path.join(os.tmpdir(),'provider-run-test-')); const out=path.join(root,'out');
const fake=path.join(root,'fake.mjs'); fs.writeFileSync(fake,`#!/usr/bin/env node
import fs from 'node:fs'; import http from 'node:http';
if(process.argv[2]==='--version'){process.stdout.write(process.env.FAKE_VERSION||'1.17.13');process.exit(0)}
const c=JSON.parse(fs.readFileSync(process.env.OPENCODE_CONFIG)); const u=new URL(c.provider.fixture.options.baseURL+'/chat/completions'); const q=http.request({host:u.hostname,port:u.port,path:u.pathname,method:'POST',headers:{authorization:'Bearer inert-loopback-key'}},r=>{r.resume();r.on('end',()=>process.exit(0))});q.end('{}');
`,{mode:0o755});
function descriptor(url, extra={}) { const f=path.join(root,`d${Math.random()}.json`); fs.writeFileSync(f,JSON.stringify({access_authorized:true,provider:'fixture',baseURL:url,model:'fixture-model',version:'fixture-version',expected_opencode_version:'1.17.13',...extra})); return f; }
function secret() { const f=path.join(root,`s${Math.random()}`); fs.writeFileSync(f,'top-secret'); return fs.openSync(f,'r'); }
let calls=0; const fixtureRequest=async (upstream, secret, body) => { calls++; assert.equal(upstream.href,'https://fixture.invalid/v1'); assert.equal(secret,'top-secret'); assert.equal(body.toString(),'{}'); return {status:200,type:'text/event-stream',body:Buffer.from('data: ok\n\n')}; };
try {
  const dry=await main(['--provider-descriptor',descriptor('https://127.0.0.1:1/v1'),'--secret-fd','3','--opencode',fake,'--output',out,'--dry-run']); assert.equal(dry.status,'dry'); const plan=JSON.parse(fs.readFileSync(path.join(out,'provider-run-dry.json'))); assert.equal(plan.cases.length,12); assert.ok(plan.cases.every(x=>x.sources.length>0&&!JSON.stringify(x).includes('expectation')));
  await assert.rejects(main(['--provider-descriptor',descriptor('https://127.0.0.1:1/v1',{access_authorized:false}),'--secret-fd','3','--opencode',fake,'--output',path.join(root,'denied')]),/access_authorized/);
  const bad=path.join(root,'wrong.mjs'); fs.writeFileSync(bad,'#!/usr/bin/env node\nconsole.log("0.0.0")',{mode:0o755}); const fd=secret(); await assert.rejects(main(['--provider-descriptor',descriptor('https://127.0.0.1:1/v1'),'--secret-fd',String(fd),'--opencode',bad,'--output',path.join(root,'wrong')]),/expected OpenCode/); fs.closeSync(fd);
  const good=secret(); const result=await main(['--provider-descriptor',descriptor('https://fixture.invalid/v1'),'--secret-fd',String(good),'--opencode',fake,'--output',path.join(root,'real')],{upstreamRequest:fixtureRequest}); fs.closeSync(good); assert.equal(result.status,'completed'); assert.equal(calls,12); const records=fs.readdirSync(path.join(root,'real')).filter(x=>/^C\d+\.json$/.test(x)); assert.equal(records.length,12); assert.ok(records.every(x=>!fs.readFileSync(path.join(root,'real',x),'utf8').includes('top-secret')));
  process.stdout.write('provider-run offline tests passed\n');
} finally { fs.rmSync(root,{recursive:true,force:true}); }
