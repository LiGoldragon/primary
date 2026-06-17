# Nix Remote-Only Override Discipline

## Trigger

The psyche explicitly forbade the local path override pattern:
`--override-input name path:/git/...` is not allowed, and Nix code should not
use local path flake inputs.

## What Changed

- `tools/nix-local-stack` no longer creates filtered local snapshots and no
  longer emits `path:` overrides.
- The helper rejects local flake refs passed as the target or as extra Nix
  arguments: `path:`, `git+file:`, relative paths, and absolute paths.
- The helper now emits remote source overrides:
  `--override-input <repo>-source github:LiGoldragon/<repo>?ref=<ref>`.
- Historical layout inputs such as `*-previous-source` and
  `*-layout3-source` are skipped rather than mapped to fake sibling repos.
- `skills/nix-discipline.md` now says flake inputs and overrides use remote
  refs only. It removes the previous local-path inner-loop exception.
- `skills/testing.md` now describes multi-repo tests as remote-ref override
  tests: commit and push each repo first, then run the central Nix gate.
- The active `.pi/continue` note had stale cloud-operator path-override
  guidance; it now marks those results as historical diagnosis only, not a
  reusable testing pattern.

## Verification

- `bash -n tools/nix-local-stack`
- `tools/nix-local-stack build --target github:LiGoldragon/spirit#cli --flake-dir /git/github.com/LiGoldragon/spirit --print-command`
  prints only `github:LiGoldragon/<repo>?ref=main` overrides.
- Passing a local target like `path:/git/github.com/LiGoldragon/spirit#cli`
  is rejected.
- Passing an extra local override like
  `--override-input schema-next-source path:/git/...` is rejected.
- A scan of the helper and Nix/testing skills found no remaining
  `path:/git`, filtered-snapshot, raw-checkout, or fake-layout override
  pattern.
- Removed leftover `/tmp/nix-local-stack.*` scratch directories from the
  earlier local-snapshot helper.

## Environment Finding

`tools/orchestrate claim` failed before taking the claim because
`orchestrate-cli` cannot fetch stale `nota-codec` revision
`f761421c383121a04df761a444a3778d1c0b137d`. That is a separate primary tooling
blocker; it prevented a formal claim but did not affect this patch's local
checks.

## Intent Capture

Spirit rejected an additive record because existing record `po6y` explicitly
preferred local checkout overrides for central integration tests. That older
record is now superseded by `ttbt`, which records the remote-only Nix override
constraint.
