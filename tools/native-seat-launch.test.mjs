#!/usr/bin/env node
import assert from 'node:assert/strict';
import {execFileSync,spawnSync} from 'node:child_process';
import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path';
const tool=path.join(import.meta.dirname,'native-seat-launch.mjs'); const dir=fs.mkdtempSync(path.join(os.tmpdir(),'native-seat-launch-'));
for(const file of ['Vision/flowNexus.md','Vision/nexus.md','flows/cf3553/vision/operational-mainFlowStartupCorrection.md','flows/da1e3f/vision/operational-launcher.md']) { fs.mkdirSync(path.dirname(path.join(dir,file)),{recursive:true});fs.writeFileSync(path.join(dir,file),'# fixture\n'); }
const plan=JSON.parse(execFileSync(process.execPath,[tool,'--seat','luna','--cwd',dir],{encoding:'utf8'})); const prompt=execFileSync(process.execPath,[tool,'--seat','luna','--cwd',dir,'--prompt'],{encoding:'utf8'}); assert.equal(plan.requiredMainFlow.name,'main-flow'); assert.ok(plan.sources.some(s=>s.path.includes('operational-mainFlowStartupCorrection'))); assert.doesNotMatch(prompt,/\$main-flow/);
const uri=new URL(`file://${tool}`).href; const old=spawnSync(process.execPath,['--input-type=module','--eval',`import {rejectTokenOnly} from ${JSON.stringify(uri)};rejectTokenOnly('$main-flow')`],{encoding:'utf8'});assert.notEqual(old.status,0);assert.match(old.stderr,/not skill injection/);
const accepted=spawnSync(process.execPath,['--input-type=module','--eval',`import {structuredSkills,containsMainFlow} from ${JSON.stringify(uri)};let p='/x/main-flow/SKILL.md';if(!containsMainFlow({items:structuredSkills([{name:'main-flow',path:p}])},p))process.exit(9)`],{encoding:'utf8'});assert.equal(accepted.status,0,accepted.stderr);
const safe=spawnSync(process.execPath,[tool,'--seat','luna','--cwd',dir,'--launch'],{encoding:'utf8'});assert.equal(safe.status,2);assert.match(safe.stderr,/acknowledge-live-launch/); console.log('native-seat-launch fixtures passed');
