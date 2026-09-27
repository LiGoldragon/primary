SubflowReturn

- Immutable Flow revision: `bc464e5e1b94fcc179af73111f43b69db1f69fc5` (0.17.4)
- Pushed commit: `c1a237045378` to `origin/main` (remote ref verified)
- Changed: `flake.nix`, `flake.lock`, `lib/default.nix`, `lib/components/herdr.nix`, `packages/message-flow.nix`, `README.md`
- Evidence: Nix source parsing and `git diff --check` passed; workspace clean after commit.
- Grade: source-parsed/diff-checked only. No build, live scenario, Start execution, or credential access occurred.
- Gaps: full `nix flake check --no-build` could not complete because formatter/check processes stalled; no release-readiness implication. Direct Field Sol routing was attempted through intercom, Flow meta, and Message meta, but available routes rejected/unavailable.