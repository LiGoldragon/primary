# 184 — Orchestrate short-header ingress implementation

*Kind: Implementation Report · Topic: orchestrate-ingress-short-header · Date: 2026-05-25 · Lane: second-operator*

## Outcome

Implemented and pushed a complete orchestrate mainline slice: the daemon now validates incoming Signal `ShortHeader` values on both ordinary and owner sockets before dispatching into `OrchestrateService`.

Mainline commits pushed:

- `/git/github.com/LiGoldragon/signal-frame` — `7d91b7f4` — `signal-frame: qualify dispatch result emission`
- `/git/github.com/LiGoldragon/signal-frame` — `37ecf582` — `signal-frame: fully qualify handler result emission`
- `/git/github.com/LiGoldragon/signal-frame` — `1493c59f` — `signal-frame: satisfy macro emission clippy`
- `/git/github.com/LiGoldragon/signal-orchestrate` — `c7495176` — `signal-orchestrate: update signal-frame lock pin`
- `/git/github.com/LiGoldragon/signal-orchestrate` — `c8e6efad` — `signal-orchestrate: update signal-frame clippy-clean pin`
- `/git/github.com/LiGoldragon/owner-signal-orchestrate` — `f9a7eeca` — `owner-signal-orchestrate: update signal-frame lock pin`
- `/git/github.com/LiGoldragon/owner-signal-orchestrate` — `499eb68a` — `owner-signal-orchestrate: update signal-frame clippy-clean pin`
- `/git/github.com/LiGoldragon/orchestrate` — `a3d636e7` — `orchestrate: validate short headers on daemon ingress`

## What Changed

`orchestrate/src/daemon.rs` now captures `frame.short_header()` before consuming the frame body, then validates that the decoded request root matches the generated contract-owned `kind_from_short_header` result.

The check applies to:

- ordinary `signal-orchestrate` requests;
- owner `owner-signal-orchestrate` requests.

Unknown root bytes and mismatched decoded roots return `signal_frame::OperationDispatchError` before service dispatch. That means malformed frames cannot reach the executor-backed service or mutate state.

`signal-frame` needed a small macro hygiene fix first: generated dispatch traits now use fully qualified `::std::result::Result`, so contract crates with local `Result<T>` aliases can consume the current dispatch/short-header APIs.

## Tests Added

`orchestrate/tests/daemon_cli.rs` now has socket-level witnesses for malformed headers:

- `ordinary_socket_rejects_mismatched_short_header_before_dispatch`
- `owner_socket_rejects_mismatched_short_header_before_dispatch`

These send well-formed Signal frames with wrong short-header root bytes and assert the daemon closes without replying.

## Verification

Cargo:

- `signal-frame`: `cargo test`
- `signal-frame`: `cargo clippy --all-targets -- -D warnings`
- `signal-orchestrate`: `cargo test`
- `owner-signal-orchestrate`: `cargo test`
- `orchestrate`: `cargo test`
- `orchestrate`: `cargo clippy --all-targets -- -D warnings`

Nix, all with `--option max-jobs 0`:

- `/git/github.com/LiGoldragon/signal-frame`: `nix flake check --option max-jobs 0`
- `/git/github.com/LiGoldragon/signal-orchestrate`: `nix flake check --option max-jobs 0`
- `/git/github.com/LiGoldragon/owner-signal-orchestrate`: `nix flake check --option max-jobs 0`
- `/git/github.com/LiGoldragon/orchestrate`: `nix flake check --option max-jobs 0`

## Remaining Work

This lands the production ingress safety slice. It does not yet make orchestrate schema-derived.

The next complete slice should be one of:

- schema lowering support for multi-endpoint and unit endpoint roots;
- schema-derived generated ordinary and owner request enums for `signal-orchestrate`;
- contract-owned orchestrate `VersionProjection` consumed by `upgrade`;
- daemon no-downtime drain-with-mirror handover after projection exists.
