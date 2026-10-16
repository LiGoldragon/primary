import assert from 'node:assert/strict';
import {parseArgs} from './claude-main-flow-launch.mjs';
const args=['--brief','/tmp/task','--aspect','Psyche','--layer','Secondary','--root','--metaflow','/tmp/definition','--topic','ethos'];
assert.equal(parseArgs(args).topic,'ethos');
assert.throws(()=>parseArgs([...args,'--system-prompt-file','/tmp/context']),/unsupported/);
assert.throws(()=>parseArgs([...args,'--herdr-workspace-label','old-direct-pane']),/unsupported/);
console.log('claude thin launcher arguments passed');
