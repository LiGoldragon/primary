---
title: 547 — Spirit production-parity port (new schema-derived spirit)
role: designer
variant: Decision
date: 2026-06-07
topics: [spirit, persona-spirit, production-parity, migration, identity, privacy, recorded-time, observe, archive, lifecycle, handoff, sema-engine]
description: |
  Implemented the production feature port from report 546 — bringing ALL deployed
  persona-spirit features into the new schema-derived spirit (Spirit decision
  0huc). 16-agent workflow: parallel per-feature design → sequential green-gated
  implementation → full verification. ALL 7 feature clusters landed GREEN and
  committed on branch designer-production-parity-2026-06-06 (77bfd721, +6630/-429
  over 41 files): 165 tests pass (up from 90), clippy -D clean, freshness guard
  holds. No core-crate bypass (sema-engine stays the store under the new base36
  identity). Remaining for cutover (designed-not-landed): the physical Upgrade
  socket tier + supervision (cross-repo, blocked on schema-rust-next
  ListenerTier), a migration that reads the PRODUCTION rkyv store, and the
  deployment packaging. Handoff: operator integrates the branch to spirit main.
---

# 547 — Spirit production-parity port

## What this is

The implementation of report 546's recommendation, under psyche decision `0huc` (Decision, High, 2026-06-06: "bring ALL production Spirit features into the new one; parity wins over the pilot's simplifications"). A 16-agent workflow designed each feature in parallel, then implemented them **sequentially behind a hard green-gate** (each feature had to build + test + clippy clean and was committed; a feature that could not reach green would revert so the branch stayed green). All seven landed green.

Result lives on the designer feature branch **`designer-production-parity-2026-06-06`** (tip `77bfd721`), pushed; **+6630/−429 across 41 files**. Code-repo main is operator-owned, so this is a handoff for operator integration.

## Verification (whole branch, green)

- **Build:** `cargo build --all-features` clean.
- **Tests:** **165 passed / 0 failed / 9 nix-gated-ignored** across 24 suites + doc-test (was 90 before the port). New suites: `recorded_time` 6, `observe_vocabulary` 7, `privacy_access_control` 13, `record_identity` 8, `identity_migration` 3, `meta_owner_lifecycle` 7; grown: `process_boundary` 13, `collect_removal_candidates` 6, `runtime_triad` 29.
- **Clippy:** `cargo clippy --all-features -- -D warnings` clean.
- **Freshness guard:** holds — with `SPIRIT_UPDATE_SCHEMA_ARTIFACTS` unset, touching all four `.schema` sources and plain-building does NOT trip the check-mode panic; `jj status` clean afterward. (Note: a raw `git status --porcelain` misreports in this jj workspace because it shares the `/git/.../spirit/.git` backend; `jj status` is authoritative and the freshness build itself — the load-bearing invariant — passes.)
- **Discipline spot-checks:** no `Box<dyn>`, no residual stringly wire error, no top-level free functions in hand-written src, meta interface root now >1 variant.

## What landed (per feature)

Each is a linear ancestor of HEAD, green + committed.

- **`0ae65f97` — 4-field Record shorthand + duplicate-topic validation.** The shorthand is a CLI text-edge normalization (`src/cli_text.rs`), not a wire-shape change — privacy omitted defaults to `Zero`, preserving the schema-derived idiom while making the documented authored surface (used everywhere, incl. `skills/spirit-cli.md`) work again. Added a `DuplicateTopic` `ValidationError` variant + the engine check.
- **`9605e171` — recorded-time provenance + qualitative recency.** A daemon clock (`src/clock.rs`, injectable for tests) stamps every `StampedEntry`; `WithProvenance` mode returns the time; `RecordedTime`/recency selection (depths + Since/Until/Between) filters in the store. (Deviation: bumped the sema schema version 1→2 to carry the time field; archive carries `StampedEntry`.)
- **`1c2f4725` — Observe vocabulary parity.** Added `Topics` listing with per-topic counts, a `CertaintySelection` filter, the `Any` topic-match, and `State`(PresenceView)/`Questions` placeholders (the same deliberate placeholders production ships). (Deviation: `CertaintySelection` appended last on the `Query` to keep positional back-compat.)
- **`15505569` — privacy access-control tier.** Wired the previously-ignored SO_PEERCRED `ConnectionContext` (`src/access.rs`): the owner-uid gate clamps non-owner reads to `Exact(Zero)`, rejects elevated subscriptions (filter-before-gate risk closed by rejecting non-owner elevated `SubscribeIntent`), and redacts elevated `Lookup`. Restores the workspace "private closed by default" discipline as an enforced tier, not a caller-supplied filter.
- **`a0aafc71` — CollectRemovalCandidates safety + store-error-swallow fix.** Restored the exact-`Zero` certainty+privacy admission guard (`CollectionQueryNotExactZeroPublic` — a broad sweep is now rejected), a per-request `Print` output target, and the full skip taxonomy; **fixed the 546 design bug** — genuine store failures now surface as `Output::Error` and unknown `Untap` tokens as a typed `ObserverTokenNotFound` rejection (no more empty-success swallow masking a partial sweep).
- **`6489ceb9` — base36 random friendly identity + long-id decode + migration binary.** A friendly `RecordIdentifier` over a base36 code (`src/record_identifier.rs`): server-minted 96-bit random, collision-rejected, bands 4..=7, `>=4`-char long-id decode, typed `RecordIdentifierError`. **No sema-engine bypass** — the engine row id stays internal (scan-resolved for lookup/remove/change-certainty); `sema-engine` remains the store. Forward migration (`src/migration.rs` + `spirit-migrate` bin) carries base36 codes losslessly via `Store::import_record`.
- **`989e5b50` — owner/upgrade lifecycle + meta >1-variant + typed wire error.** The meta socket now multiplexes `Configure` (kept at short_header `0x00` for back-compat) + owner lifecycle (`Start`/`Drain`/`Reload`/`Register`/`Retire` over an engine `LifecycleState`) + version handover (`AskHandoverMarker`/`ReadyToHandover`/`HandoverCompleted` reading the live store marker, typed `HandoverRejectionReason`) — a 9-variant meta `Input` root (fixes the Spirit `1401` single-variant violation). The stringly `ErrorMessage` is promoted to a typed `SemaFailureReason` across 13 call sites.

## What remains for cutover (designed-not-landed, tracked in ARCHITECTURE.md)

The component features are in. Cutover is still a migration, not a swap — three pieces remain, all flagged in the branch's `ARCHITECTURE.md` + the INTENT.md manifestation:

1. **Separate physical Upgrade socket tier + engine-management supervision + state-mirroring execution.** The lifecycle/handover *vocabulary* landed on the meta socket, but a distinct Upgrade listener tier (and `Mirror`/`Divergence`/`RecoverFromFailure` supervision) is **blocked on a cross-repo change**: `schema-rust-next` hardcodes `ListenerTier{Working, Meta}`. This needs an emitter change to allow a third tier before spirit can declare it.
2. **A migration that reads the PRODUCTION rkyv store.** `spirit-migrate` exists and carries base36 codes losslessly, but it reads a *new-spirit* source store; reading the deployed persona-spirit on-disk format (to carry the live intent DB forward) is not yet built.
3. **Deployment packaging.** The empty `nix/`, the CriomOS-home flake module authoring the `Configuration` NOTA + systemd service, versioned `spirit-vX.Y.Z` wrappers, and the `PERSONA_SPIRIT_*` socket-env contract. This is a system-operator/cloud lane concern.

## Handoff

- **Operator:** integrate `designer-production-parity-2026-06-06` (`77bfd721`) into spirit main (the standard cross-lane integration; code-repo main is operator-owned). It is additive, linear, and independently green; `cargo update` not required (no dep bumps beyond what's in the branch's Cargo.lock).
- **Psyche decision still open from 546 §recommendation #4 (identity):** I took "bring all the features" as *restore base36 identity* and implemented it without bypassing sema-engine. If you instead wanted the `u64`-counter model kept with a re-keying migration, this branch went the other way — say so and I'll revisit. The remaining cutover pieces (esp. #1 cross-repo and #3 deployment) are the next decisions when you want to push toward an actual production swap.
