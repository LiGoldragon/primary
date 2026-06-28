# L5 — criome-verified forward durably LANDS an Append in a real mirror

Implementation evidence. The L5 gap from
`CriomosImplementer-WitnessRunEvidence.md`: a criome-VERIFIED inbound forward
carrying a `signal-mirror::Append` was `ForwardAccepted` but the carried object
never reached the co-resident mirror's `ComponentSocket`, so no head landed.
This closes it with a real-mirror durable-landing witness and durable Nix
evidence. No production main touched.

## Task and scope

Make a criome-verified inbound forward carrying a `signal-mirror::Append`
actually DELIVER to a co-resident mirror so the record durably LANDS (the
mirror's head reflects the appended object), and prove it with a Rust
integration test plus a flake check. Build on router `criome-auth-witness`
@ `9f4d3894` (which already carries the `GrantDirectMessage` + ComponentSocket
bootstrap surfaces). Do not weaken the criome verify gate; no polling; hardwired
grants only.

## Root cause localized (router introspection, not guessed)

The delivery machinery was already correct. The relay itself is
`HarnessDelivery::deliver_to_component_socket`
(`src/harness_delivery.rs:130-146`): it opens the actor's `ComponentSocket`,
writes the routed object's octets under the length-prefixed signal-frame
envelope, reads one reply — payload-blind, so an `Append` rides identically to a
`NotifyObject`.

A `Forwarded` message reaches that relay through `retry_pending`
(`src/router.rs:2149-2300`). It parks instead of delivering at exactly three
decision points, all of which depend on receiver wiring the bootstrap must
declare — none on the criome auth:

- `src/router.rs:2168-2202` — `ReadHarnessDeliveryTarget` misses (recipient not
  registered). A `Forwarded` message has `may_resolve_remote() == false`
  (`src/router.rs:2479-2481`), so it cannot fall through to a remote route and
  hits `next.push(pending)` at line 2200 (park).
- `src/router.rs:2203-2226` — `CheckChannel` returns
  `ChannelDecision::NeedsAdjudication`; parked at line 2225 with no grant.
- `src/router.rs:2241-2296` — target resolved AND channel authorized, but
  `DeliverHarness` -> `HarnessDelivery::deliver` returns `Ok(false)` because the
  registered actor has `endpoint == None` (`src/harness_delivery.rs:41-42`);
  `delivery_result` is false and it parks at line 2295.

`apply_forwarded` (`src/router.rs:2353-2387`) enqueues the forward, runs
`retry_pending().await`, and returns `ForwardApplied::Accepted` regardless of
the delivered count. That reply-vs-delivery split (flagged by the auditors) is a
reply-semantics observation, NOT the park cause: acceptance is correctly gated
on a successful criome verify (the four named checks confirm), and the durable
landing is a separate, independently-witnessable fact (the mirror head).

Why the two-VM witness saw "no connection" at L5: it pinned the audited router
base `7dd747f9`, whose `router-write-bootstrap` could declare NEITHER the
mirror actor's `ComponentSocket` endpoint NOR an `operator -> mirror`
direct-message grant. So the deployed receiver registered the mirror with no
delivery endpoint and no grant, and the verified forward parked (at the channel
gate, or — once a grant existed — at the no-endpoint delivery return). Branch
`9f4d3894` added BOTH bootstrap surfaces; what was missing was the end-to-end
proof that the relay then durably lands an `Append` in a real mirror.

## What changed (router `criome-auth-witness`, on top of `9f4d3894`)

No router runtime source changed. The relay path was already correct; the fix
was the deployable bootstrap surface (already on the base) plus this proof:

- `tests/criome_forward_lands_in_mirror.rs` (new) — the L5 witness. A real
  co-resident `criome` daemon BLS-verifies the forward; a real `mirror::Engine`
  over a versioned `sema-engine` store sits behind the destination
  `ComponentSocket` (served over the same length-prefixed signal-frame envelope
  the generated mirror working tier uses). The wiring is in-process
  `RouterInput::RegisterActor` (ComponentSocket endpoint) + `GrantChannel`
  (`operator -> mirror`) — byte-for-byte what `BootstrapApply::from_operation`
  produces for `RegisterActor`-with-endpoint and `GrantDirectMessage`
  (`src/router.rs:3452-3480`), so it faithfully exercises the deployment relay.
  The witnessed claim is the mirror's DURABLE HEAD read back over
  `signal-mirror::ObserveHeads`: empty before the forward, `sequence 1` with the
  forwarded entry digest after — the verified forward is the sole cause. The
  `ForwardAccepted` reply is asserted too, but it is not the landing proof.
- `flake.nix` — new check `router-criome-forward-lands-in-mirror` runs that test
  (Nix-owned durable evidence).
- `Cargo.toml` / `Cargo.lock` — dev-deps `mirror` (branch `criome-auth-witness`,
  rev `d30cd180`) + `tempfile`. The lock keeps `signal-frame 0.3.0`
  (`b78c8077`) and `signal-mirror 0.1.1` (`34ed3fdd`) shared across router and
  mirror — the ComponentSocket wire is NOT split. `sema-engine` unifies to the
  router's `0.6.3` (`98ba507b`); the mirror was pinned at `0.6.2` but the bump
  is additive (subscription fanout only), so it compiles unchanged.

## Checks run — all green on the prometheus remote builder, rev `221b5fb0`

New L5 witness (the deliverable):

```
nix build "github:LiGoldragon/router/221b5fb04b838f3a5bbd2a6839d60aa2574902fd#checks.x86_64-linux.router-criome-forward-lands-in-mirror" -L
```

```
router-test> +++ command cargo test --release --locked --test criome_forward_lands_in_mirror criome_verified_forward_lands_an_append_in_the_co_resident_mirror -- --exact
router-test> running 1 test
router-test> test criome_verified_forward_lands_an_append_in_the_co_resident_mirror ... ok
router-test> test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.16s
```
out: `/nix/store/2mdcaf0rivar9frzmz0l09vc0xndqkjw-router-test-0.4.1` (NIX_EXIT=0)

The four named checks (all PASS, prometheus, same rev):

| flake check | named test | out path | exit |
|---|---|---|---|
| router-accepts-only-real-criome-attestation | `router_accepts_forward_under_real_criome_bls_attestation` | fplmlb7b… | 0 |
| router-refuses-forward-without-criome-credential | `router_refuses_forwards_without_a_valid_criome_attestation` | llb10a2z… | 0 |
| router-write-configuration-carries-network-fields | `router_configuration_carries_listen_identity_and_criome_socket` | 1270qclz… | 0 |
| router-write-bootstrap-carries-hardwired-peers | `router_bootstrap_carries_hardwired_peers_and_actor_homes` | qcj6v9i5… | 0 |

Inner-loop confirmation (laptop `cargo test`, before the Nix runs): the L5
witness and all four named tests passed identically.

Not run: the full `default` flake check (entire test suite). The change is
additive (dev-deps + one new test + one new flake check; zero router runtime
source), so unrelated tests are behaviourally unchanged. Recommend the auditor
run `nix flake check` once for completeness.

## Branch and revision

- Repo: `router` — branch `criome-auth-witness`
- Revision: `221b5fb04b838f3a5bbd2a6839d60aa2574902fd` (parent `9f4d3894`)
- Pushed to `origin/criome-auth-witness`. NOT on any production main (gated on
  re-audit, per policy).
- Mirror dev-dep pinned at `LiGoldragon/mirror` `criome-auth-witness`
  `d30cd180507cd52d0369d2ec8b49136fdfca8458`.

## What the downstream (two-VM) witness must do to observe the landing

1. Repin the witness's router input from the audited base `7dd747f9` to this rev
   `221b5fb0` (or `9f4d3894`+this) so `router-write-bootstrap` can declare the
   mirror ComponentSocket endpoint and the grant.
2. In the receiver's bootstrap NOTA (`BootstrapWriteRequest`), give the mirror
   actor-home a `(Some (ComponentSocket <mirror-working-socket>))` endpoint
   (4th field) AND add an `(operator mirror)` entry to the 5th
   direct-message-grants list. The forward's source actor is `operator`, so the
   grant must be `operator -> mirror` (the receiver does NOT re-stamp a
   directly-constructed forward's `from`).
3. Read the landing from the mirror, not the router reply. Query the mirror's
   working socket with `signal-mirror::ObserveHeads (Some <store>)` and assert
   the returned `HeadMark` is `sequence 1` with the forwarded entry digest.
   CRITICAL (auditor note, confirmed): `EntryDigest` is `(Bytes 32)`. If the
   witness reads the head via the mirror CLI as NOTA text, it must compare the
   32 DECIMAL bytes, NOT the 64-char hex — the original witness grepped the hex
   and would never match even on a real landing. (The Rust witness here compares
   the typed `EntryDigest`, so it is immune; the deployment NOTA path is not.)
4. The mirror store must be REGISTERED first (meta `RegisterStore`); an Append to
   an unregistered store is refused `UnknownStore` (the head row must exist).

## Surprises / things the auditor must know

- The router relay needed NO code change. The existing in-process e2e test
  already delivered a `NotifyObject` to a ComponentSocket witness; the only
  untested ground was a DURABLE `Append` into a REAL mirror, which this witness
  now covers. The earlier "necessary but not sufficient" read was because the
  native chain wasn't wired with BOTH the ComponentSocket endpoint and the grant
  at once.
- The prior native chain ran SEPARATE daemon binaries (socket-level wire only).
  This Rust witness compiles router + mirror into ONE binary, which forces cargo
  to unify every shared crate to one rev. That unification held cleanly
  (signal-frame 0.3.0 shared, sema-engine bump additive) ONLY because the mirror
  `criome-auth-witness` branch was aligned to signal-frame 0.3.0. Using mirror
  `main` (signal-frame 0.2.1) would split the wire and fail to compile — the
  dev-dep MUST stay on the aligned branch.
- `ForwardAccepted` still does not imply delivery (it means verified +
  committed). That is intentional and unchanged; the durable landing is the
  separately-witnessed fact. If a future intent wants the reply to carry
  delivery status, that is a `signal-router` wire change, out of this scope.
