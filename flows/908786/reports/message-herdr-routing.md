# Message Herdr routing

## Result

Message main `55657f4e90716071b55fa9dc133eb7d2083b7182` is the
published delivery candidate. The actual GitHub `refs/heads/main` was read
after push and matched that revision exactly. Its producer dependency remains
`signal-flow` `968ae3b00a64ebcb1ef05e21a0a55cee55ad015c`.

The paired Flow implementation is main
`61d765e4814035c2c0a1424e670a1b62da3d10b6`. Flow now preserves route
ownership when a registered Herdr route becomes stale: it returns Herdr
unavailable and the native endpoint parked. A native-only row that never had a
Herdr binding retains its native readiness.

No service, live Message store, migration, or activation changed. The active
`messenger-v6.sema` selection was not touched.

## Delivery behavior

### Exact producer graph

A subsequent read-only audit inspected the exact published revision rather
than a moving main ref. Its direct Cargo dependencies are:

| Producer | Revision |
| --- | --- |
| `signal-message` v4 | `37c3e5b75b05f86b7dc27198bb4523ccbd495e4b` |
| `meta-signal-message` | `87a54b0a1cbc9aa02f9ff62e46c6ffca52f9ec25` |
| `signal-flow` | `968ae3b00a64ebcb1ef05e21a0a55cee55ad015c` |

The lock also retains `signal-message` v3 at
`a9708f3384af18129cb1c983ffed850c4d631e46` through the meta producer.
This is a distinct transitive dependency, not the ordinary Message v4
contract. A complete deployment graph must preserve that distinction.

Message injects the complete `NexusDelivery` boundary into `MessageEngine`, so
the tests exercise the same Flow resolver and Herdr subprocess adapter against
disposable sockets and processes.

For a Herdr route, Message:

1. resolves the complete Flow node again immediately before delivery;
2. requires the same Flow, harness session, harness kind, and complete Herdr
   route;
3. requires Herdr status `idle` or `working` and
   `interactive_ready: true`;
4. reads the visible screen and accepts the actual blank Claude or Codex
   composer forms;
5. submits the producer-rendered `ClusterMessage` Datom exactly once; and
6. checks the endpoint identity again after a successful prompt submission.

Waiting, missing status, false interactive readiness, a nonblank composer, a
wrong terminal, changed Flow resolution, and unavailable Flow resolution all
refuse before prompt submission. A Flow node serialized with Herdr unavailable
and native readiness parked returns `Parked` without opening the native socket.
The direct Claude protocol fixture remains the positive native-only route
witness.

`Accepted` means transport submission only. It does not claim that the target
harness read, interpreted, or completed the message. Herdr has no revision or
compare-and-swap token spanning identity, screen read, and prompt operations,
so the blank-composer snapshot cannot be made atomic with submission. The
post-submit identity check detects a replacement observed after submission,
but it cannot prove harness consumption.

Before crossing the harness boundary, Message persists a nonretryable
`Parked` row. Successful transport submission promotes it to `Accepted`.
Refusal, timeout, a nonzero prompt result, or post-submit identity uncertainty
leaves it durably `Parked` and nonretryable. Reopening the v6 store and
repeating the same source event returns the stored receipt without submitting
again.

## Checks

The following local gates passed on the published source:

- `cargo test --all-targets --all-features`
- `cargo clippy --all-targets --all-features -- -D warnings`
- `cargo fmt --all -- --check`
- `cargo test --lib nexus_delivery::tests -- --nocapture` with eight routing
  tests passing

`nix flake check --max-jobs 0 -L` passed all 24 current x86_64-linux checks on
the configured `ssh-ng://nix-ssh@prometheus.goldragon.criome` remote builder.
The gate includes named checks for canonical single submission, unready
composer refusal, stale-Herdr no-native-fallback, the native-only positive
protocol, and durable ambiguous delivery without retry.

The exact added attributes under `checks.x86_64-linux` are:

| Attribute | Rust witness |
| --- | --- |
| `message-herdr-route-submits-canonical-datom-once` | `herdr_delivery_submits_the_canonical_datom_once` |
| `message-herdr-route-refuses-unready-composers` | `herdr_guard_refuses_busy_nonblank_wrong_terminal_unready_and_missing_status` |
| `message-stale-herdr-route-never-falls-back-to-native` | `stale_herdr_route_with_parked_native_endpoint_never_falls_back` |
| `message-native-only-direct-protocol-remains-routable` | `flow_resolution_and_claude_delivery_use_direct_protocols` |
| `message-herdr-uncertain-delivery-is-durable-without-retry` | `accepted_and_ambiguous_parked_v6_rows_reopen_without_retry` |

The routing witnesses reside in `nexus_delivery::tests`; the final witness
also exercises persistence through the engine. This attribute extraction is
an exact-source audit, not another execution or a Home integration result.

The first full Nix run found 15 check attributes that still named relay and
cluster binaries or fixtures deleted in the earlier main revision
`6751ec128c68`. Those impossible attributes were removed. The complete flake
gate was then rerun and passed; no failed or pending check is presented as
acceptance evidence.

## Sources

- Living direction and launch context:
  `/home/li/primary/flows/908786/vision/default-effort.md` and
  `/home/li/primary/flows/908786/log.md`
- Message component rules: `/git/github.com/LiGoldragon/message/AGENTS.md`
- Rust doctrine:
  `/git/github.com/LiGoldragon/standards/good-rust-practices.md`
- Message implementation:
  `/git/github.com/LiGoldragon/message/src/nexus_delivery.rs`,
  `/git/github.com/LiGoldragon/message/src/engine.rs`, and
  `/git/github.com/LiGoldragon/message/flake.nix`
- Message revision:
  `55657f4e90716071b55fa9dc133eb7d2083b7182`
- Flow route-ownership revision:
  `61d765e4814035c2c0a1424e670a1b62da3d10b6`
- Signal Flow producer revision:
  `968ae3b00a64ebcb1ef05e21a0a55cee55ad015c`
- Paired Flow evidence:
  `/home/li/primary/flows/908786/reports/flow-herdr-routing.md`
