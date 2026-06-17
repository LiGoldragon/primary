# Synthesis

## Fixed

The bad pattern that jammed disk is now blocked in the main workspace helper and
removed from the obvious scripts/docs:

- `tools/nix-local-stack` rejects local `path:` / `git+file:` / absolute /
  relative Nix refs and emits remote `github:` overrides.
- Spirit's local schema stack script now uses remote refs.
- Lore and primary report examples no longer teach local path overrides.
- `CriomOS-test-cluster` no longer generates local-path flake inputs for its
  synthetic deploy flake.

The focused scan over the edited deploy files is clean for:

- `path:/git`
- `git+file://`
- `--override-input ... path:`
- `inputs.<name>.url = "path:..."`
- stale `path:${...}` deploy-input construction in the edited deploy files

## Verified

For `CriomOS-test-cluster`:

- `nix fmt -- --check lib/deploy-flake.nix lib/mkDeployTest.nix` passed.
- `nix build --no-write-lock-file --no-link --print-out-paths .#checks.x86_64-linux.cluster-contracts` passed.
- `nix build --dry-run --no-write-lock-file --no-link --print-out-paths .#checks.x86_64-linux.lojix-deploy-smoke` passed evaluation and listed the generated deploy flake derivation normally.

Earlier in the same session, the full deploy smoke reached the VM behavior
phase and timed out waiting on the existing Tailscale/network path; it was not
blocked by generated source/lock evaluation. I stopped duplicate broad VM runs
that lacked `--no-write-lock-file` because they were dirtying `flake.lock` and
burning disk.

## Remaining Questions

Two cases are still not solved by a mechanical sweep:

1. `lojix-cli` tests contain hard-coded `path:/home/li/git/CriomOS` inputs.
   That is the next concrete code target if the literal rule is "no local flake
   refs in tests either."
2. Hermetic VM deploy tests still need a way to hand a synthetic deploy flake to
   the daemon without network access. In `CriomOS-test-cluster`, the bad local
   path inputs are gone, but the test concept still involves a generated store
   source as deploy payload. That does not copy `/git`, but it is not the same
   thing as deploying a pushed remote repo. If the rule is absolute, this needs
   a design change to the test harness or deploy protocol, not a grep rewrite.

