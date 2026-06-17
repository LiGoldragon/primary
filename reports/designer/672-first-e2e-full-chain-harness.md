# 672 — The first OFFLINE full-chain e2e harness: spirit → mirror A → router → mirror B

P5 of the 669 fan-out, built per the design in
`reports/designer/669-first-e2e-offline-build/2-offline-e2e-harness-design.md`
(option (b): two real green legs joined by a router-carried object-accepted
notice, no new shipped contract).

## Bottom line

The harness is **written, compiles, and the test PASSES** — the full offline
chain is proven true at once. But that green requires ONE upstream code-repo
change I proved but did not commit (it crosses the router lane): regenerating
`signal-router@router-network-transport`'s checked-in schema artifact. On a
clean checkout the harness stops at a `StaleGeneratedArtifact` build-script
panic. So:

- **Designer deliverable, landed and pushed:** the harness test, the dev-deps,
  the unified lockfile, on spirit branch `mirror-shipper-reland` @ `75d0e8d4`.
- **Operator handoff (H4), proven:** regenerate signal-router's artifact on its
  branch; the moment it lands, the harness is green from clean.

## Pin-unify map and outcome (the critical first step)

The test binary links four feature branches at once, so they must agree on one
version each of the shared crates. I read every branch's `Cargo.toml` and
`Cargo.lock`.

| Shared crate | spirit `mirror-shipper` | mirror `arc-shipper-mainline` | router `router-network-transport` | signal-router `router-network-transport` | Unifies? |
|---|---|---|---|---|---|
| triad-runtime | `branch=main` | `branch=main` | `branch=main` | — | YES (one rev `7a84034b`) |
| sema-engine | `branch=main` | `branch=main` | `branch=main` | — | YES (one rev `73eea24b`) |
| nota-next | `branch=main` | `branch=main` | `branch=main` | `branch=main` | YES (`7426a6a7`) |
| signal-frame | `branch=main` | `branch=main` | `branch=main` | `branch=main` | YES (`e2eae5c2`) |
| signal-mirror | `branch=main` (dev) | `branch=main` | — | — | YES |
| signal-router | — | — | `router-network-transport` | (self) | YES (only router consumes) |
| **schema-next** | `e7216260` | `e7216260` | `e7216260` | **`f460e7b6`** | **NO** |
| **schema-rust-next** | `6e04d70` | `cad9ec27` | `0a7d1db2` | **`00763d6`** | **NO** |

The design feared a triad-runtime split (router needing `tailnet-listener`
while spirit/mirror are on `main`). **That fear was wrong — router-network-
transport pins triad-runtime `branch=main`, the same as everyone else.** All of
triad-runtime/sema-engine/nota-next/signal-frame unify cleanly: every consumer
pins `branch=main`, so Cargo collapses each onto one current-HEAD rev. I proved
this with `cargo metadata` (resolves clean) and the unified `Cargo.lock`
(one source per shared crate; the only multi-entry crate is sema-engine, whose
two extra entries are spirit's off-by-default `production-migration` packages
pinned to fixed revs — not in this test's tree).

### The real wall: schema generator-stack skew (not triad-runtime)

The unification fails one level deeper, in the schema codegen stack. The
`schema-next` IR crate and the `schema-rust-next` generator co-evolve, and each
component checks in a generated wire-contract artifact (`src/schema/lib.rs`).
`schema-rust-next`'s `build.rs` (at `…/schema-rust-next/6e04d70/src/build.rs:431`)
**refuses to build against a stale checked-in artifact** — it regenerates with
the current generator and panics `StaleGeneratedArtifact` if the result differs.

Three of the four branches (spirit, mirror, router) lock `schema-next =
e7216260` (current main HEAD). **`signal-router@router-network-transport` is the
lone laggard: `schema-next = f460e7b6`, `schema-rust-next = 00763d6`.** When the
harness unifies everything onto current HEAD (`schema-next e7216260` +
`schema-rust-next 6e04d70`), the newer generator emits a strictly richer
artifact for signal-router (the identifier newtypes gain `Display`, `AsRef<str>`,
`PartialEq<&str>` impls — +234 lines, 1301 → 1535) and rejects signal-router's
stale checked-in one.

The skew is one-directional and cannot be papered over by pinning DOWN: I tried
pinning spirit's `schema-rust-next` to signal-router's older `00763d6`, and
`schema-rust-next` itself **fails to compile** against the newer `schema-next`
(`no method lower_to_rust on &schema_next::Root`; non-exhaustive
`TypeReference::Application`). The old generator cannot run on the new IR. So the
only viable unification is UP, on current HEAD, with signal-router's artifact
regenerated.

### Proven fix (operator H4 handoff)

Regenerating signal-router's artifact against the unified HEAD works — proven:
`SIGNAL_ROUTER_UPDATE_SCHEMA_ARTIFACTS=1 cargo test …` regenerated
`src/schema/lib.rs` (the +234-line richer artifact), after which the harness
compiled and the test passed. Restoring the original stale artifact returns the
build to the `StaleGeneratedArtifact` panic. Both states are reproduced.

**The operator step:** on `signal-router@router-network-transport`, run the
crate's build with `SIGNAL_ROUTER_UPDATE_SCHEMA_ARTIFACTS=1` against current
`schema-next`/`schema-rust-next` main, commit the regenerated `src/schema/lib.rs`
(+ the bumped `Cargo.lock`) on that branch, push. This is a router-lane
code-repo-branch commit; a designer must not carry it (cross-lane), and it must
not be a local `[patch]` hack. After it lands, the harness is green from a clean
checkout with no further change. (Likely the same regeneration is wanted on
`router@router-network-transport` if its own artifacts lag, though router locked
the current `schema-next` so it is not the blocker here.)

## The harness

`~/wt/github.com/LiGoldragon/spirit/mirror-shipper/tests/end_to_end_offline_full_chain.rs`
(756 lines), gated behind the existing off-by-default `mirror-shipper` feature.

Placement: a spirit feature-branch integration test, per 669/2. The chain's
entry point is spirit; leg 1's assertions (`ShipOutcome::Shipped { head }`,
`Durability::ServerCommitted`, `durability_of`, `unshipped_outbox`,
`publish_latest_checkpoint` → `CheckpointReceipt`) map exactly to the raw
`mirror::ComponentShipper` + `sema_engine::ComponentEngine` path, so the harness
is a faithful composition of the two proven tests rather than going through
spirit's `Engine` wrapper.

Dev-deps added to `spirit/mirror-shipper/Cargo.toml` (file:line):

- `Cargo.toml:159-167` — `router`/`signal-router` (branch `router-network-transport`),
  `signal-message`/`signal-harness` (branch `main`), `kameo 0.20`.
- `Cargo.toml:76-83` — the `[[test]]` registration behind `mirror-shipper`.

One harness-local invention — the seam that makes the legs causal:
`MirrorObjectNotice { store, sequence, digest }`
(`end_to_end_offline_full_chain.rs:84-156`). It reuses signal-mirror's
`HeadMark` shape (sequence + 32-byte digest), NOTA-encoded into the router
message body and parsed back on the witness side. It is the seed of the future
`signal-router`/`signal-mirror` `MirrorObjectNotify`.

### The assertions (all pass with the operator fix applied)

Leg 1 — spirit ship to mirror A (`…:478-540`):
- Pre-ship `store_durability() == QueuedForMirror`.
- `ship_unshipped()` → `ShipOutcome::Shipped { head }`.
- `store_durability() == ServerCommitted`; `durability_of(head) == ServerCommitted`.
- `unshipped_outbox().is_empty()`.
- `publish_latest_checkpoint()` → receipt `sequence==1`, `covered_end==3`.
- Capture `MirrorObjectNotice` from the confirmed head.

Leg 2 — router A→B carries the notice (`…:543-660`):
- Submit on router A a `SubmitStamped` whose body is `notice.to_nota()`,
  origin `External(Owner)`, recipient the notify-target.
- Witness on router B receives: `harness == mirror-b-notify`, `sender == owner`,
  `body == notice.to_nota()`.
- **Seam:** `MirrorObjectNotice::from_nota(witnessed.body) == notice` — the head
  announced over the router is exactly the head mirror A confirmed.
- Router A trace contains `RouterTraceStep::ForwardedRemote`.
- Typed observation: `RouterDeliveryStatus::ForwardedRemote` for the slot.

Leg 3 — mirror B fetch + restore, driven by the witnessed notice (`…:662-740`):
- `MirrorTailnetClient::new(mirror_a_address).Restore(parsed.store)` → `Restored(bundle)`.
- `bundle.suffix.len() == 2` (gamma + the beta tombstone).
- Import via `begin_import`/`ingest_checkpoint`/`ingest_suffix`/`commit(&Families)`.
- **Causal seam:** `target.current_commit_sequence() == CommitSequence::new(parsed.sequence)`
  — mirror B restored exactly up to the head the router announced.
- `parsed.digest == confirmed_head.entry_digest().bytes()`.
- Query surface on B equals the source records and equals `[alpha=revised, gamma=third]`.
- `source.current_commit_sequence() == target.current_commit_sequence()`.
- Graceful router teardown.

### Green test result

With signal-router's artifact regenerated (the operator fix, proven locally):

```
running 1 test
test intent_recorded_on_node_a_ships_notifies_over_router_and_restores_identically_on_node_b ... ok
test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.05s
```

Zero warnings on the test build.

On a clean checkout (signal-router's committed stale artifact):

```
error: failed to run custom build command for `signal-router … router-network-transport#74484ac3`
  panicked at …/schema-rust-next/6e04d70/src/build.rs:431:14:
  checked-in wire contract schema artifacts are fresh: StaleGeneratedArtifact {
    path: ".../signal-router/.../src/schema/lib.rs",
    update_environment_variable: "SIGNAL_ROUTER_UPDATE_SCHEMA_ARTIFACTS" }
```

## Is the full offline chain now proven true at once?

**Yes — the data path is proven end to end in one binary**, and the proof is one
operator commit away from being green on any clean checkout / CI. The single
test exercises, in order: spirit's real versioned engine + production
`ComponentShipper` shipping over loopback TCP to a real mirror `Service`
(`ServerCommitted`); two real `RouterRuntime`s forwarding the object-accepted
notice A→B over loopback TCP with the offline accept-fixed verifier
(`ForwardedRemote`), delivered to a local witness; and mirror B fetching from
mirror A over `MirrorTailnetClient` and restoring **exactly up to the head the
router announced**, with byte-identical records and a continuous digest chain.

What it does NOT yet prove (explicitly the option-(a) second milestone, per
669/2 and Spirit `5osd`): a real router `EndpointKind::Mirror`/notify endpoint, a
mirror-side reactor that fetches on the delivered notice automatically, and a
two-`Service` mirror↔mirror server-to-server fetch. The first green hands those
a proven payload shape (`MirrorObjectNotice`) to promote.

## Changes (file:line)

- `~/wt/.../spirit/mirror-shipper/tests/end_to_end_offline_full_chain.rs:1-756` — the harness (new file).
- `~/wt/.../spirit/mirror-shipper/Cargo.toml:76-83` — `[[test]]` registration.
- `~/wt/.../spirit/mirror-shipper/Cargo.toml:159-167` — router/signal-router/signal-message/signal-harness/kameo dev-deps.
- `~/wt/.../spirit/mirror-shipper/Cargo.lock` — unified pin set (+94 lines).
- Committed `75d0e8d4` on spirit branch `mirror-shipper-reland`, pushed to origin.

## Operator handoff, restated

`signal-router@router-network-transport` (and check `router` likewise) carries a
schema artifact generated by an older `schema-next f460e7b6`/`schema-rust-next
00763d6` and is stale against current main HEAD. Regenerate
`signal-router/.../src/schema/lib.rs` with `SIGNAL_ROUTER_UPDATE_SCHEMA_ARTIFACTS=1`
against current `schema-next e7216260`/`schema-rust-next 6e04d70`, commit on the
`router-network-transport` branch, push. Proven to unblock the harness to a clean
green. Designer must not carry it (cross-lane), and no `[patch]` hand-hack.
