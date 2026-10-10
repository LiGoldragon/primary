# Next Spirit Readiness And Rename Status - 2026-06-04

## Scope

This report covers the schema-derived Spirit repository at
`/git/github.com/LiGoldragon/spirit`, now pushed on `main` at commit
`e0c2edc2` (`spirit: complete internal rename`).

The current production Spirit remains `persona-spirit`. This repository is the
next schema-derived Spirit candidate.

## Rename Status

Done in `spirit`:

- Cargo package renamed from `spirit-next` to `spirit`.
- Rust library crate renamed from `spirit_next` to `spirit`.
- Binaries renamed from `spirit-next` / `spirit-next-daemon` to `spirit` /
  `spirit-daemon`.
- Environment variables renamed from `SPIRIT_NEXT_SOCKET` /
  `SPIRIT_NEXT_TRACE_SOCKET` to `SPIRIT_SOCKET` / `SPIRIT_TRACE_SOCKET`.
- Schema package identity renamed from `spirit-next:lib` to `spirit:lib`.
- README, repo `INTENT.md`, repo `ARCHITECTURE.md`, `skills.md`, tests,
  scripts, `flake.nix`, and `flake.lock` use the new repo-local name.
- `/git/github.com/LiGoldragon/spirit-next` and `repos/spirit-next` remain
  transitional symlinks to `spirit`.

Not closed yet:

- Workspace skills and older reports still carry `spirit-next` examples.
- `schema-next` and `schema-rust-next` tests/docs still use `spirit-next` as a
  sample schema identity.
- `persona-spirit` and `CriomOS-home` intentionally still carry a deployment
  slot named `spirit-next` for the production Persona Spirit stack.
- Older design concept repos still mention the old name historically.

This means the internal repo rename is complete, but bead `primary-o2kc`
should stay open until cross-repo references are triaged by kind.

## Verification Completed

Passed in `/git/github.com/LiGoldragon/spirit` after the rename:

- `cargo fmt`
- `cargo test`
- `cargo test --features nota-text`
- `cargo test --features testing-trace`
- `cargo test --all-features`
- `cargo clippy --all-features -- -D warnings`
- `nix flake check -L`

`flake.lock` was aligned to the Cargo-tested source revisions:

- `schema-next` `711b5fc9`
- `schema-rust-next` `a789a85e`
- `triad-runtime` `6daf2954`

The explicit local-stack integration script
`scripts/run-nix-integration-tests` was started with local checkout overrides,
but it was stopped after a long remote Nix build without reaching test output.
That is not a locked-repo failure; it means compatibility with the moving local
schema stack was not established in this pass.

## Readiness Situation

Strong development-pilot readiness:

- The schema pipeline is live: `schema/lib.schema` lowers through
  `schema-next`, materializes `schema/lib.asschema`, emits checked-in Rust
  under `src/schema/lib.rs`, and build freshness checks enforce that path.
- The CLI accepts NOTA text and talks to the daemon over generated binary
  rkyv signal frames.
- The daemon process boundary is tested with real CLI/daemon processes.
- SEMA storage now routes through `sema-engine` over `.sema`, not direct
  runtime `redb` calls in the daemon store.
- The dependency test proves `redb 2.x` is not in the runtime tree; the
  remaining `redb 2.x` path is build-time schema tooling.
- Nexus owns the Signal-to-SEMA decision loop in the pilot runtime.
- Trace builds use `triad-runtime` framing/client infrastructure and generated
  trace event nouns.
- Nix package/check names now use `spirit`.

Not production-cutover ready:

- `persona-spirit` is still production Spirit and carries the deployed
  wrapper/versioning surface.
- Cross-repo references to `spirit-next` need triage before the rename bead can
  close. Some are stale repo references; some are deployment-slot names; some
  are historical design reports or schema identity examples.
- The generic schema-emitted component runner is not fully landed. The repo has
  `DaemonCommand` as the startup noun, but the reusable triad runner remains a
  next implementation slice.
- The explicit local-stack Nix integration run did not complete, so the
  candidate is verified against locked sources, not against every moving local
  schema checkout.
- Open follow-up beads still name schema/runtime gaps: `primary-vllc`
  (schema-next dual-lowering witness), `primary-a1px` (OutputNexus
  dispatcher), `primary-9hx0` (split `lib.schema`), and `primary-lrf8`
  (mail queue/fanout observers).

## Operator Judgment

The next Spirit repository is now a coherent, test-passing development pilot
under its canonical `spirit` name. It is good enough for continued operator
work on the schema-derived stack and for feature-port experiments from
production Spirit.

It is not ready to replace `persona-spirit` in production. The next hardening
sequence is: finish cross-repo rename triage, land the generic triad runner,
run and stabilize the local-stack Nix integration path, then revisit production
cutover once deployment wrappers and version handover are explicit.
