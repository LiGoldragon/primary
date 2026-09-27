#!/usr/bin/env node
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const root=path.resolve(import.meta.dirname,'..');
const tool=path.join(root,'tools','native-seat-launch.mjs');
const profilePath='flows/56ae53/mind-sol-successor/mind-sol-of-56ae53.profile.json';
const profile=JSON.parse(fs.readFileSync(path.join(root,profilePath),'utf8'));
const digest=file=>fs.existsSync(file)?crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'):null;
const tree=rootPath=>{
  if(!fs.existsSync(rootPath))return [];
  return fs.readdirSync(rootPath,{recursive:true}).filter(name=>{
    const file=path.join(rootPath,name);return fs.statSync(file).isFile();
  }).sort().map(name=>[name,digest(path.join(rootPath,name))]);
};
const markers=()=>fs.readdirSync(path.join(root,'flows')).filter(name=>/^\.[a-f0-9]{6}\.flow-id$/.test(name)).sort().map(name=>[name,digest(path.join(root,'flows',name))]);
const routeFile=path.join(process.env.HOME??'', '.local/state/hacky-messenger/56ae53.json');
const snapshot=()=>({
  flowMarkers:markers(),
  callerSession:process.env.CODEX_SESSION_ID??null,
  callerClaudeSession:process.env.CLAUDE_CODE_SESSION_ID??null,
  routeState:digest(routeFile),
  successorFiles:tree(path.join(root,'flows/56ae53/mind-sol-successor')),
  receiptFiles:tree(path.join(root,'.native-seat-receipts')),
});
const before=snapshot();
const plan=JSON.parse(execFileSync(process.execPath,[tool,'--seat','mind-sol-of-56ae53','--profile-file',profilePath,'--predecessor','56ae53','--cwd',root],{encoding:'utf8'}));
const after=snapshot();
assert.deepEqual(after,before,'plan-only evaluation changed an ID, caller session, route state, successor file, or receipt');
assert.equal(plan.model,'gpt-6-sol');assert.equal(plan.effort,'medium');assert.equal(plan.predecessor,'56ae53');assert.equal(plan.ancestor,'00f95a');
assert.equal(plan.canonicalFlowId,undefined);assert.equal(plan.canonicalTitle,undefined);
assert.deepEqual(plan.requiredSkillNames,profile.skills);
assert.equal(plan.requiredSkillNames.length,26);
assert.ok(plan.sources.some(source=>source.path==='Vision/psyche.md'));
assert.ok(plan.sources.some(source=>source.path==='flows/56ae53/mind-sol-successor/successor-handoff.md'));
assert.ok(plan.sources.every(source=>/^[a-f0-9]{64}$/.test(source.sha256)));
console.log('actual Mind Sol 56ae53 profile plan-only check passed');
