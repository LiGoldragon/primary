#!/usr/bin/env node
/* A stand-in for the real `claude` binary, driven entirely by environment variables, for the
   harness.mjs unit tests. It ignores its argv, exactly as the real one is only ever invoked
   with the one fixed argument list this tool always passes. */
import fs from 'node:fs';

const mode = process.env.FAKE_CLAUDE_MODE;

if (mode === 'success') {
  process.stdout.write(fs.readFileSync(process.env.FAKE_CLAUDE_FIXTURE));
  process.exit(0);
} else if (mode === 'exit-nonzero') {
  process.exit(Number(process.env.FAKE_CLAUDE_EXIT_CODE));
} else if (mode === 'hang') {
  /* Never exits on its own; if the marker file below appears, the harness's kill did not
     actually stop this process before its own delay ran. */
  setTimeout(() => {
    try {
      fs.writeFileSync(process.env.FAKE_CLAUDE_MARKER, 'ran past the kill');
    } catch {}
  }, 1000);
  setInterval(() => {}, 1000);
} else {
  process.exit(9);
}
