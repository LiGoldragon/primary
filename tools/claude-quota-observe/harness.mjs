/* Running the real harness: claude -p --output-format stream-json, from a fresh empty
   temporary directory, stdin detached, bounded to 90 seconds. This is the one place that
   touches a live process; Observe.{ Fixture.«path» } bypasses it entirely. */
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const TIMEOUT_MS = 90_000;
const ARGS = ['-p', '--output-format', 'stream-json', '--verbose', '--tools', '', '--no-session-persistence', '--', 'Reply OK.'];

export class Timeout extends Error {}
export class HarnessFailed extends Error {
  constructor(exitCode) {
    super(`claude exited ${exitCode}`);
    this.exitCode = exitCode;
  }
}

/* Resolves with the captured stdout text. Rejects with Timeout when the bound is hit before
   the process exits, or HarnessFailed with its exit code when it exits nonzero. `command` and
   `args` both default to the real invocation (claude with the fixed argument list above); a
   test overrides them (typically to `process.execPath` running a fake claude script, never
   relying on that script's own shebang, which a build sandbox need not honor) along with a
   short `timeoutMs`, to exercise Timeout and HarnessFailed without a live account or a
   90-second wait. */
export function runHarness({ command = 'claude', args = ARGS, timeoutMs = TIMEOUT_MS, env = process.env } = {}) {
  return new Promise((resolve, reject) => {
    const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'claude-quota-observe-'));
    const cleanup = () => fs.rmSync(directory, { recursive: true, force: true });
    const child = spawn(command, args, { cwd: directory, stdio: ['ignore', 'pipe', 'ignore'], env });
    let stdout = '';
    let settled = false;
    const timer = setTimeout(() => {
      if (settled) return;
      settled = true;
      const error = new Timeout();
      error.pid = child.pid;
      child.kill('SIGKILL');
      cleanup();
      reject(error);
    }, timeoutMs);
    child.stdout.on('data', chunk => {
      stdout += chunk;
    });
    child.on('error', error => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      cleanup();
      reject(error);
    });
    child.on('exit', code => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      cleanup();
      if (code !== 0) reject(new HarnessFailed(code));
      else resolve(stdout);
    });
  });
}
