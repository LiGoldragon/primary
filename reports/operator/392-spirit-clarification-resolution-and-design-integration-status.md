# 392 — Spirit clarification resolution and design integration status

## Frame

The psyche asked to keep working, integrate good design, aim high, and test hard. I treated
that as an operator integration pass across the schema stack and Spirit, with two bars:

- code-repo `main` only moves when the branch is green against the current main basis;
- a branch can be pushed as merge-ready-but-gated when Cargo/clippy pass and the remaining
  blocker is an external Nix/deploy gate.

## Integrated on main

The schema compiler stack is already on code-repo main:

- `schema-next` main includes schema-cc as a co-located workspace member and generates the
  live parenthesis-reference dispatch from `schemas/reference-grammar.nota`.
- `schema-next` main also includes the pipe-generic applied-root expansion and the
  architecture/intent constraints from Designer's `next/pipe-delimiter-design`; I integrated
  only the current docs from that branch because the branch also carried stale code history.
- `schema-rust-next` main emits applied generic frame roots as concrete enums.
- `signal-spirit` and `meta-signal-spirit` main are repinned to the landed schema compiler
  stack.
- `nota-next` main carries the pipe-delimiter architecture constraints from Designer's
  `next/pipe-delimiter-design`.

That part is no longer waiting on Designer branches.

## Spirit branch pushed

Spirit is not landed on main yet. I pushed:

- repo: `/git/github.com/LiGoldragon/spirit`
- bookmark: `operator/resolve-clarification-main-basis`
- commit: `2a0e7d36` — "spirit: resolve clarifications into target edits"
- basis: latest fetched Spirit main `4fce1c5f` — "spirit: migrate mixed schema ten
  production stores"

The branch keeps the latest main design for guarded effects and adds the stricter
clarification fold behavior:

- `ResolveClarification` routes through the Nexus effect plane and the existing guardian
  guard path.
- Store resolution is atomic at the operation level: it preflights the standalone
  clarification, preflights every target, rejects duplicate targets, rejects using the
  standalone clarification as a target, archives the standalone clarification plus every
  pre-edit target, mutates each target description, and removes the standalone
  clarification.
- Process and runtime tests cover the real user-facing path: clarification becomes target
  edit(s), the standalone clarification disappears, and archive history contains both the
  removed standalone clarification and target preimage.
- Nix integration tests now default to canonical `/git/github.com/LiGoldragon/...`
  checkouts instead of silently preferring stale `~/wt/.../structural-forms-integration`
  worktrees, and the override set includes the schema, signal, agent, and
  version-projection repos needed by the stack.

## Tests

Green on the Spirit branch:

- `SPIRIT_UPDATE_SCHEMA_ARTIFACTS=1 cargo test --all-features`
- `cargo fmt`
- `cargo clippy --all-targets --all-features -- -D warnings`

The all-features suite included:

- production migration tests for schema version ten / layout three to current layout;
- process-boundary daemon tests, including
  `cli_and_daemon_resolve_clarification_edits_target_and_removes_standalone`;
- runtime triad tests, including
  `signal_resolve_clarification_folds_standalone_clarification_into_targets`;
- versioned-store tests proving durable write log coverage;
- generated signal-plane and schema-source witnesses.

Nix gate status:

- command:
  `timeout 900 cargo test --features nota-text --test nix_integration nix_build_default_package_emits_both_binaries -- --ignored --test-threads=1`
- result: timeout exit `124`
- observed state: the test reached `nix build` with the corrected `/git` overrides, then
  blocked in the Nix daemon path for the full fifteen-minute bound.

I did not move Spirit main because the ignored Nix gate did not complete.

## Designer 660 prototype

Designer report 660 is a valuable demonstration: pipe-generic declarations, `{| |}`
trait/impl syntax, marker impls, and a minimal code-is-data `Deref` body all run in local
worktrees. I did not integrate it into main in this pass.

Reasons:

- the work lives in unpushed mutable `reaction-expand` worktrees, not a reviewable pushed
  branch;
- `schema-next` is based behind current main's documentation landing and needs a clean
  rebase;
- the report honestly states that some invalid generation cases still `panic` instead of
  returning typed `SchemaError`;
- the feature is a broad language/codegen surface, while the live deploy gate today is
  Spirit's Nix/build/deploy readiness.

My operator call: keep the design direction, but require one more hardening slice before
main: typed errors for rejected impl/body cases, pushed branches, main rebase, and a
cross-stack test pass. The good part to preserve is the boundary: generate marker impls and
small fixed mechanical impl families first; leave arbitrary business logic bodies out until
the expression language is intentionally designed.

## Open gates

1. Spirit can be merged/deployed after the Nix ignored integration gate completes cleanly or
   system-maintainer identifies the Nix-daemon wait as an unrelated platform issue and
   accepts the Cargo/clippy/process-boundary proof as the deploy gate.
2. The clarification-resolution branch should be rechecked with `jj git fetch` immediately
   before landing; if main moved, rebase onto main and rerun Cargo/clippy plus at least the
   clarification process-boundary/runtime tests.
3. Designer's pipe trait/impl prototype should become a pushed branch pair before operator
   integration. I would not merge the local mutable worktrees as-is.
