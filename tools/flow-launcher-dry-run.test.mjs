import assert from 'node:assert/strict';
import { renderLauncherPlan } from './flow-launcher-dry-run.mjs';
const p = renderLauncherPlan({ cwd:'/home/li/primary', flowId:'fd0f97', sessionId:'fd0f9762-d293-432b-a425-4f590fe9c8d5', name:'primary-claude-fd0f97', env:{DISPLAY:':0',WAYLAND_DISPLAY:'wayland-1',CODEX_CI:'1',NO_COLOR:'1',SECRET:'x'} });
assert.equal(p.launches,false); assert.match(p.argv.join(' '), /ghostty/); assert.match(p.argv.join(' '), /--window-inherit-working-directory=false/); assert.match(p.argv.join(' '), /--session-id .fd0f9762/); assert.deepEqual(p.preservedEnvironment,{DISPLAY:':0',WAYLAND_DISPLAY:'wayland-1'}); assert.deepEqual(p.unsetPrefixes,['CODEX_','NO_COLOR','TERM']); assert.match(p.postflight.join(','),/bridge id/);
const q=renderLauncherPlan({cwd:'/x',flowId:'f',sessionId:'s',name:'n',env:{},remoteControl:true}); assert.match(q.argv.join(' '),/--remote-control/);
console.log('flow-launcher-dry-run fixtures passed');
