# Native seat fixture interpreter correction

The adoption fixture in `tools/native-seat-launch.test.mjs` writes a fake `herdr` command into its disposable fixture `PATH`. Its previous `#!/usr/bin/env node` shebang required `/usr/bin/env`, which is absent in the reported Node/Python-only remote fixture closure. The child launcher then failed with `ENOENT` before the fake Herdr binding could be exercised. The test now writes `#!${process.execPath}`, selecting the exact Node executable already running the fixture. The fake Herdr command, app-server fixture, exact binding guards, and runtime launcher are unchanged.

Local focused verification: `node --test tools/native-seat-launch.test.mjs` passed (`1/1` test file). This is not a claim that the separately owned remote fixture build has rerun. Only this test file and this report are in the intended commit; unrelated shared working-tree edits remain with their owners.

The exact two-file change landed as Primary commit `6f64ae63881f413c04c0749a415141cbe40a2cdc`; `jj show --summary` listed only the test and this report, and the real GitHub `refs/heads/main` returned that commit after push. Orchestrate returned `Released.{ 4039 ... }` for the exact test path. This report-only receipt update leaves the test bytes unchanged.

## Sources

- `tools/native-seat-launch.test.mjs:114-132`: fake Herdr executable, its child `PATH`, adoption spawn, and `ENOENT` assertion site.
- `flake.nix:163-169`: remote fixture closure declares Node.js and Python, without a system `/usr/bin/env` dependency.
- Focused local `node --test tools/native-seat-launch.test.mjs` result: exit `0`, fixture passed.
- Orchestrate `Locked.{ 4039 ... }`: exact test-file write ownership for this change.
