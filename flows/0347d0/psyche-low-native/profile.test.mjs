#!/usr/bin/env node
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import crypto from 'node:crypto';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const root=path.resolve(import.meta.dirname,'../../..');
const directory=path.join(root,'flows/0347d0/psyche-low-native');
const profileFile=path.join(directory,'profile.json');
const profile=JSON.parse(fs.readFileSync(profileFile,'utf8'));
const required=['spirit','psyche','psyche-interraction','behavior','correction','vocabulary','subflow','messaging','datom','visual-report-from-md','main-flow','refresh'];

assert.equal(profile.name,'psyche-low');
assert.equal(profile.model,'claude-sonnet-5');
assert.equal(profile.effort,'medium');
assert.equal(profile.role,'Psyche Low');
assert.equal(profile.fresh,true);
assert.equal(profile.predecessor,null);
assert.equal(profile.ancestor,null);
assert.deepEqual(profile.skills,required);
assert.deepEqual(profile.modelCatalog,[{id:'claude-sonnet-5',family:'sonnet'}]);
assert.equal(profile.sources.length,1);
for (const source of profile.sources) {
  const body=fs.readFileSync(path.join(root,source.path));
  assert.equal(crypto.createHash('sha256').update(body).digest('hex'),source.sha256);
}
assert.doesNotMatch(JSON.stringify(profile),/0625c3|PsycheHigh/i);

const temp=fs.mkdtempSync(path.join(os.tmpdir(),'psyche-low-profile-'));
const manifest=path.join(temp,'launch.json');
fs.writeFileSync(manifest,JSON.stringify({
  version:1,
  session:'psyche-low-validation',
  workspace:'psyche-low-workspace',
  cwd:root,
  seats:[{
    harness:'claude',
    profile:'psyche-low',
    profileFile,
    fresh:true,
    predecessor:null,
    agent:'psyche-low',
    label:'Psyche Low · Sonnet',
    model:'claude-sonnet-5',
    effort:'medium'
  }]
}));
const result=spawnSync(process.execPath,[path.join(root,'tools/native-batch-refresh.mjs'),'validate','--manifest',manifest],{cwd:root,encoding:'utf8'});
assert.equal(result.status,0,result.stderr);
assert.deepEqual(JSON.parse(result.stdout),{valid:true,seats:1,session:'psyche-low-validation',workspace:'psyche-low-workspace'});
console.log('psyche-low native profile fixture passed');
