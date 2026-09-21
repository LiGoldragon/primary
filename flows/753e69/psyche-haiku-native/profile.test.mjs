#!/usr/bin/env node
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const root=path.resolve(import.meta.dirname,'../../..');
const directory=path.join(root,'flows/753e69/psyche-haiku-native');
const profileFile=path.join(directory,'profile.json');
const profile=JSON.parse(fs.readFileSync(profileFile,'utf8'));
const required=['spirit','psyche','psyche-interraction','behavior','correction','vocabulary','subflow','messaging','datom','visual-report-from-md','main-flow','refresh'];

assert.equal(profile.name,'psyche-haiku-of-b80e55');
assert.equal(profile.model,'claude-haiku-4-5');
assert.equal(profile.effort,'medium');
assert.equal(profile.role,'Psyche Ultra Low');
assert.equal(profile.fresh,true);
assert.equal(profile.predecessor,null);
assert.equal(profile.ancestor,null);
assert.deepEqual(profile.remember,{flow:'b80e55',depth:1});
assert.equal(profile.nativeTitle,'Psyche Ultra Low');
assert.deepEqual(profile.sourceAudit,{reviewedAt:'2026-09-21T16:09:44Z',newestApplicableVision:['flows/b80e55/vision/haikuForPsycheUltraLow.md','flows/b80e55/vision/flashbookResponsiveDesign.md','flows/1b8ac0/vision/flashbooks.md']});
assert.deepEqual(profile.skills,required);
assert.deepEqual(profile.modelCatalog,[{id:'claude-haiku-4-5',family:'haiku'}]);
assert.ok(profile.sources.length>=6);
for (const source of profile.sources) {
  const body=fs.readFileSync(path.join(root,source.path));
  assert.equal(crypto.createHash('sha256').update(body).digest('hex'),source.sha256,source.path);
}

const temp=fs.mkdtempSync(path.join(os.tmpdir(),'psyche-haiku-profile-'));
const manifest=path.join(temp,'launch.json');
fs.writeFileSync(manifest,JSON.stringify({version:1,session:'psyche-haiku-validation',workspace:'psyche-haiku-workspace',cwd:root,seats:[{harness:'claude',profile:'psyche-haiku-of-b80e55',profileFile,fresh:true,predecessor:null,agent:'psyche-haiku-of-b80e55',label:'Psyche Ultra Low',model:'claude-haiku-4-5',effort:'medium'}]}));
const result=spawnSync(process.execPath,[path.join(root,'tools/native-batch-refresh.mjs'),'validate','--manifest',manifest],{cwd:root,encoding:'utf8'});
assert.equal(result.status,0,result.stderr);
assert.deepEqual(JSON.parse(result.stdout),{valid:true,seats:1,session:'psyche-haiku-validation',workspace:'psyche-haiku-workspace'});
console.log('psyche-haiku native profile fixture passed');
