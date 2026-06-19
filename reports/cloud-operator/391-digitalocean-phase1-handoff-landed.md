# 391 · DigitalOcean Phase-1 handoff landed

Cloud-operator review and integration of cloud-designer report 66 / bead `primary-hpkj`.

## What I reviewed

- `reports/cloud-designer/66-cloud-operator-handoff.md` — accepted as the actionable handoff.
- `reports/cloud-designer/64-digitalocean-live-test-runbook.md` — source for Tier-1 test and Tier-2 encoder gap.
- `reports/cloud-designer/65-cloud-node-image-home.md` — confirmed as design/intent background; no cloud wire change needed for image ids.
- `reports/cloud-designer/68-cloud-engine-audit/0-frame-and-method.md` — currently an audit frame, not an implementation blocker.
- `/git/github.com/LiGoldragon/cloud` repo intent/architecture/agent contract before code.

## Audit findings

- P0 was already done before this operator slice: cloud main commit `7f190c36` changes DigitalOcean gopass path to `digitalocean.com/api-token`.
- The original disposable live test was not safe enough to land verbatim: `ensure_ssh_key` can be read-only when a key/public key already exists, and delete-before-assert does not cover panic before the explicit delete.
- A Rust `Drop` guard can clean up normal unwind/panic paths, but cannot make SIGKILL or all process-kill cases safe. External sweep remains the emergency live-ops safety net.
- The Tier-2 blocker was real: the daemon accepted only binary rkyv startup but had no command-line encoder.
- The default package still intentionally builds default features; a separate DigitalOcean-enabled package is the right additive deploy surface.

## Landed in cloud working copy

- Added `tests/digitalocean_live.rs`, ignored by default, with:
  - per-run `ssh-keygen` ED25519 key generation;
  - unique DigitalOcean key/droplet name;
  - pre-droplet `POST /v2/account/keys` write-scope probe;
  - RAII cleanup for droplet and SSH key;
  - explicit delete before assertions.
- Extended the DigitalOcean `Api` trait and `HttpApi` with `delete_ssh_key` for cleanup.
- Added `examples/write_config.rs` to emit the daemon's binary `DaemonConfiguration` rkyv startup file.
- Added `packages.digitalocean` and `apps.daemon-digitalocean` with `--features digitalocean,cloudflare`.
- Added `apps.digitalocean-live-test` as the Nix-owned entry for the live Tier-1 runner.
- Added Nix checks for DigitalOcean hermetic tests, ignored live-test compilation, and feature-enabled clippy.

## Verification

- `nix flake check --print-build-logs` — passed.
- `nix build .#digitalocean --no-link --print-build-logs` — passed.
- `cargo clippy --locked --features digitalocean,cloudflare --all-targets -- -D warnings` — passed.

No live DigitalOcean action was run in this operator slice.

## Remaining work

- Tier-2 full-daemon live chain is still not run. It now has the encoder and DO-capable package surface needed for a cleaner attempt, but it still requires explicit live authorization.
- The committed live test's `Drop` guard is not a substitute for a kill-safe external sweep after live runs.
- The broader cloud-designer report 68 audit may produce follow-up beads after its synthesis lands.
