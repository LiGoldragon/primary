# 138/1 — Track A: router cross-host transport P1 fixes (sound, pushed)

*Build → adversarial verify. Verdict: **sound**, build reproduced (forced
recompile to rule out stale cache), recommended for merge.*

## Result

Branch **`transport-p1-fixes-138`** in `/git/github.com/LiGoldragon/router`,
commit `39ec67e9` (change `qymklpyr`), based on `origin/router-network-transport`
(NOT main). **Pushed.** No `signal-router` schema change needed — schema
`74484ac` already carried the wire `forwarded: ForwardMarker` field, the
`AlreadyForwarded` refusal reason, and `RouterForwardAccepted(MessageSlot)`; the
daemon just wasn't using them.

All five P1/P2 transport defects (system-operator audit 229) cleared:

| # | Defect | Fix | Evidence |
|---|---|---|---|
| 1 | `cargo fmt` fails on 5 files | formatted | `cargo fmt --check` exit 0 |
| 2 | `ForwardAccepted` returns fake slot 0 | `ForwardApplied::Accepted(SignalSlot)` carries the real minted slot; ingress writes it back | e2e asserts `slot != 0` (`end_to_end_remote_forward.rs:428`) |
| 3 | "Accepted" semantics ambiguous | **Decision: durable-peer-receipt**, not live-local-delivery — persists before best-effort retry, so a parked-for-adjudication forward is still Accepted | `apply_forwarded` persists (router.rs:2301) before `retry_pending` (2308); doc-comment + INTENT.md |
| 4 | `ForwardMarker` loop guard unused on ingress | `apply_forwarded` refuses inbound `ForwardMarker::Forwarded` with `AlreadyForwarded` **before persisting** (a router only emits `Origin` on first hop, so inbound `Forwarded` = A→B→A cycle) | router.rs:2281; test `already_forwarded_ingress_is_refused_and_not_delivered` |
| 5 | **SECURITY:** daemon installs `AcceptFixedTestIdentity` even with real config | `RouterEngine::from_configuration` → `RouterNetworkConfiguration::from_daemon_configuration`: when `criome_socket_path` is set it returns `Error::CriomeVerifierUnavailable` (milestone-3 client not built) **rather than silently running the offline verifier**; the offline verifier is reachable only when no criome socket is configured | router.rs:995-1011; 2 unit tests at 3670 |

Build green: `cargo fmt --check`, `cargo build --offline`, `cargo test --offline`
(lib 3/3, e2e 2/2, + 32/12/1/3/2/16 across suites), `cargo clippy --offline
--all-targets -D warnings` — all pass; reviewer reproduced with a forced recompile.

## What the reviewer flagged (P3, not a regression)

A **legacy flag-based `router` daemon path** (`src/bin/router.rs` →
`RouterDaemon::run` → `RouterNetworkConfiguration::offline()`) still constructs
the offline verifier — but `offline()` sets `listen_address=None`, so
`bind_tailnet_ingress` returns early and **no TCP forward ingress is ever bound**;
the offline verifier is inert (no network peer can reach it). Recommend retiring
that path in a follow-up — it also violates the AGENTS.md no-flags /
binary-startup-only daemon contract.

## Remaining (handed to operator)

- The **milestone-3 criome forward-attestation client** is the follow-up that
  lifts the `CriomeVerifierUnavailable` refusal so a criome-backed node can
  start. (This is where the Track B decision lands — see 138/2.)
- Replay/freshness (seen-nonce window) is still milestone 3.
- Operator owns rebasing router main onto this branch; no PR opened.
