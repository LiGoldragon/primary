# 673 — Offline first e2e: proven true at once (capstone)

The first e2e production, offline full-chain, is **proven**: the harness
`tests/end_to_end_offline_full_chain.rs` passes — spirit records intent → ships the unshipped suffix
to mirror A (`Durability::ServerCommitted`) → router A→B forwards an object-accepted notice
(`ForwardedRemote`, delivered body == notice at a HarnessSocket) → mirror B restores **exactly up to
the router-announced head**, byte-identical records (`[alpha=revised, gamma=third]`,
`current_commit_sequence == notice.sequence`, matching digest). This is the offline realization of the
`d6he` chain (spirit → vcs(mirror) → router → mirror), with criome stubbed per the psyche's
"no key encryption for now" steer. Both "networking through the router" and "spirit with vcs … fetched
by the mirror" are now demonstrated end-to-end.

## The branch stack (5 branches, 4 repos — all pushed to origin)

| repo | branch | state |
|---|---|---|
| spirit | `mirror-shipper-reland` (`75d0e8d4`) | leg-1 shipper + the full-chain harness; `mirror-shipper` feature + both `mirror_shipper.rs` proofs + the full-chain test green |
| meta-signal-spirit | `mirror-target-reland` (`5d61ae8c`) | `MirrorTarget`/`MirrorAddress` nouns + `mirror_target` slot re-added (schema+regen) |
| mirror | `arc-shipper-mainline` (`6bcefa4f`) | additive `Arc<Engine>` `ComponentShipper` (`from_shared_engine`) |
| signal-router | `router-network-transport` | m1 forwarding contract (the one gap below) |
| router | `router-network-transport` | m2 networked forwarding daemon (two-RouterRuntime loopback forward) |

## Proven vs stubbed vs deferred (honest scope)

- **Proven:** the full data path and the causal seam — mirror B restores precisely the head the router
  announced, nothing more.
- **Stubbed (offline, by the psyche's steer):** criome attestation = `AcceptFixedTestIdentity`; no real
  BLS on the path. This is exactly "no key encryption for now."
- **Harness-local (not a shipped contract):** `MirrorObjectNotice { store, head }` (reuses
  signal-mirror's `HeadMark`). It seeds the production `MirrorObjectNotify` — `5osd`'s router-triggers-
  the-mirror's-own-fetch shape is milestone two.
- **Deferred to the live/production track:** mirror-target persistence across daemon restart (the
  store-axes slice `37bafef`, needed for self-resume); the real router-carried notify + mirror auto-fetch.

## The single operator gap to a clean-checkout green

The pin-unify's feared triad-runtime conflict does **not** exist — all branches pin triad-runtime,
sema-engine, nota-next, and signal-frame to `branch=main`, unifying onto one current rev each. The real
wall is one level deeper: `signal-router@router-network-transport` lags on an **old schema-next /
schema-rust-next generator**; unifying onto current HEAD makes `schema-rust-next`'s build.rs reject
signal-router's stale checked-in `src/schema/lib.rs` with `StaleGeneratedArtifact`. Pinning *down* is
impossible (the old generator won't compile against the new IR). **Proven fix (operator, router lane):**
regenerate `signal-router@router-network-transport` (`SIGNAL_ROUTER_UPDATE_SCHEMA_ARTIFACTS=1` → a
+234-line richer artifact: Display/AsRef/PartialEq impls) and commit on that branch. The harness agent
proved this greens the test on a clean checkout, then reverted the change (no committed `[patch]`, no
hidden local hack). This single regeneration is the only thing between the proven-passing harness and a
clean-checkout green — and a designer must not carry a router-lane artifact commit.

## Operator handoff (main integration)

Once signal-router is regenerated: integrate the 5-branch stack onto code-repo main (operator owns main
+ rebase). Independent of that, **criome Part 1** (669/3 — land the pushed signal-criome admission
contract + the auth-pilot stack onto criome main) removes the placeholder and can land anytime. Minor:
standardize the `TailnetClient`/`MirrorTailnetClient` naming on main (671).

## Live/gated track — designed, build-ready, waiting

`669/3` (criome main-integration checklist + Option-A cluster-root provisioning ceremony) and `669/4`
(router m3 real criome attestation + replay/freshness window; transport resolved to **Yggdrasil**;
new `criome.nix` + `message-router.nix` NixOS modules + a `MessageFabric` capability) are ready. This
is the second milestone: real BLS attestation on the path + a live two-node tailnet forward. It
re-engages exactly the key-encryption work the psyche deferred, so it starts on the psyche's go.

## Bottom line

The offline first e2e is true at once. The remaining offline step is one operator regeneration →
clean green → 5-branch main integration. The live/gated track is fully designed and waits for the
go to re-engage crypto + cross-node deploy.
