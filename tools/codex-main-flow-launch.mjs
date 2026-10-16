#!/usr/bin/env node
// Legacy command name; Flow owns context composition, native launch and receipts.
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {parseArgs as parse, launchMain} from './flow-start-adapter.mjs';
export const parseArgs = argv => parse(argv, 'codex');
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { launchMain(parseArgs(process.argv.slice(2)), 'codex'); }
  catch (error) { console.error(`launch failed: ${error.message}`); process.exitCode = 1; }
}
