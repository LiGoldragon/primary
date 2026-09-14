import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import {spawn} from 'node:child_process';

const stateFile = new URL('./interactive-probe-state.json', import.meta.url);
const resume = process.argv.includes('--resume');
const state = resume ? JSON.parse(fs.readFileSync(stateFile, 'utf8')) : {
  work: fs.mkdtempSync(path.join(os.tmpdir(), 'claude-interactive-34d94e-')),
  session: crypto.randomUUID(),
};
const home = path.join(state.work, 'home');
fs.mkdirSync(home, {recursive: true});
const key = 'inert-local-interactive-probe-key';
// These are preferences for this throwaway home, not a fabricated transcript.
fs.writeFileSync(path.join(home, '.claude.json'), JSON.stringify({
  hasCompletedOnboarding: true, theme: 'dark',
  customApiKeyResponses: {approved: [key.slice(-20)], rejected: []},
}));
const observer = path.join(state.work, 'observer.mjs');
fs.writeFileSync(observer, `import fs from 'node:fs'; let s=''; for await(const b of process.stdin)s+=b; const j=JSON.parse(s); fs.appendFileSync(${JSON.stringify(path.join(state.work, 'hooks.jsonl'))},JSON.stringify({session_id:j.session_id,prompt_id:j.prompt_id,prompt:j.prompt,transcript_path:j.transcript_path})+'\\n');`);
const settings = path.join(state.work, 'settings.json');
fs.writeFileSync(settings, JSON.stringify({hooks: {UserPromptSubmit: [{hooks: [{type: 'command', command: `${process.execPath} ${observer}`}]}]}}));
let requests = 0;
// Hold locally to make queuing observable; never forward or return model text.
const server = http.createServer((request) => {requests++; request.resume();});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const env = {HOME:home, PATH:process.env.PATH, TERM:'xterm-256color', LANG:'C.UTF-8',
  XDG_CONFIG_HOME:path.join(home,'config'), XDG_DATA_HOME:path.join(home,'data'),
  XDG_STATE_HOME:path.join(home,'state'), XDG_CACHE_HOME:path.join(home,'cache'),
  ANTHROPIC_API_KEY:key, ANTHROPIC_BASE_URL:`http://127.0.0.1:${server.address().port}`};
const child = spawn('/home/li/.nix-profile/bin/claude', [
  resume ? '--resume' : '--session-id', state.session, '--settings', settings,
  '--model','haiku','--no-chrome','--strict-mcp-config','--mcp-config','{"mcpServers":{}}',
  '--setting-sources','','--tools','','--permission-mode','dontAsk',
], {cwd:state.work, env, stdio:'inherit'});
state.parent_pid=process.pid;state.child_pid=child.pid;state.phase=resume?'resume':'start';
fs.writeFileSync(stateFile, JSON.stringify(state,null,2)+'\n');
console.log(JSON.stringify(state));
let killTimer;
const stop=()=>{child.kill('SIGTERM');killTimer=setTimeout(()=>child.kill('SIGKILL'),2000);};
process.on('SIGTERM',stop);
const deadline=setTimeout(stop,60000);
const result=await new Promise(resolve=>child.on('close',(code,signal)=>resolve({code,signal})));
clearTimeout(deadline);clearTimeout(killTimer);
server.closeAllConnections();await new Promise(resolve=>server.close(resolve));
console.log(JSON.stringify({phase:state.phase,result,localhost_requests:requests}));
