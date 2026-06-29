# Implementation Evidence — bead `primary-p0gg` (per-store ContentAddressing, REPLACEABLE)

Append-time per-store `ContentAddressing` policy that refuses a digest-mismatched
body BEFORE it lands, built and witnessed GREEN on operator/feature bookmarks.
Nothing pushed to a production main. `private-repos/` untouched.

## Scope and base line

- Bead: `primary-p0gg` — "mirror: refuse digest-mismatched body at append via
  typed per-store `ContentAddressing` policy."
- Design followed: `agent-outputs/MirrorAppendDigestValidation/DesignWorker-AppendDigestPolicy-Design.md`
- Ruling honored: REPLACE, do not add. `StoreRegistration` newtype is REPLACED by
  a record carrying addressing; no parallel/compat op was introduced.

## Branches / bookmarks (per repo) and base

| repo | base (main) | operator bookmark | tip | pushed? |
|------|-------------|-------------------|-----|---------|
| `meta-signal-mirror` (`/git/github.com/LiGoldragon/meta-signal-mirror`) | `9d2aeddf` | `operator/p0gg-content-addressing` | `44dfac6c4de9ed2e45517ee72c1fd39513e9182b` | YES (operator branch only, NOT main) |
| `mirror` (`/git/github.com/LiGoldragon/mirror`) | `5102f5ed` (== `main`, == `criome-auth-witness`) | `operator/p0gg-content-addressing` | `538f5124` | NO (committed locally; not pushed) |
| `signal-mirror` | `34ed3fdd` | — | unchanged | unchanged |

The mirror change sits directly on `5102f5e`/`main` (the cargo-checkout line the
design anchored to), NOT the stale `criome-auth-witness` worktree dir.

## The REPLACEMENT — new `StoreRegistration` shape and every updated consumer

Old (removed): `StoreRegistration(StoreName)` newtype.
New (generated from `meta-signal-mirror/schema/lib.schema`):

```
ContentAddressing [Opaque SemaVersionedLog]          ;; Opaque first = default
StoreRegistration { store.StoreName addressing.ContentAddressing }
```

Generated Rust: `pub struct StoreRegistration { pub store: StoreName, pub
addressing: ContentAddressing }`; `pub enum ContentAddressing { Opaque,
SemaVersionedLog }` (derives `Copy`). The old `StoreRegistration::new` and
`From<StoreName>` are gone; `Input::register_store` now takes the whole record.

Consumers updated (in-repo, all compile + pass):

- `meta-signal-mirror/tests/round_trip.rs` — register round-trip now iterates both
  `ContentAddressing` variants.
- `mirror/src/engine.rs` — `handle_meta` passes the record; `register_store(reg)`
  reads `reg.store`; `apply_inner` maps `reg.addressing` meta->local and calls
  `Store::register_store(name, addressing)`.
- `mirror/src/store.rs` — `register_store(&StoreName, ContentAddressing)`.
- `mirror/tests/daemon_logic.rs` — 3 `RegisterStore` record sites + 1 direct
  `Store::register_store(&store, ContentAddressing::Opaque)`.
- `mirror/tests/end_to_end_arc.rs` — 2 record sites.
- `mirror/tests/landed_body_readback.rs` — 1 record site.

Operator NOTA command grammar (generated; the meta CLI parses owner NOTA into
`meta_signal_mirror::Input` at `client.rs:91` / `bin/meta_mirror.rs` via the
generated `NotaDecode`, no hand-written parser):

- OLD: `(RegisterStore spirit)`
- NEW: `(RegisterStore (spirit Opaque))` or `(RegisterStore (spirit SemaVersionedLog))`

  Captured by a throwaway probe (removed after). The break is the intended
  replacement; the contract round-trip test proves encode/decode symmetry.

## The recompute guard (acceptance criterion 2)

- `mirror/src/readback.rs` — `LandedBody::addresses_to(&self, &signal_mirror::EntryDigest) -> bool`,
  the verb on the type owning the octets. Both failure modes (decodes-to-different-digest,
  and fails-to-decode) collapse to `false`. Reuses the existing
  `content_address()` recompute through `sema_engine::VersionedCommitLogEntry::new`.
- `mirror/src/decision.rs` — a true FOURTH guard `body_addressing_violation` on
  `RegisteredLedger`, beside the three linkage guards; hooked into `into_decision`
  after `known_divergence`, before any `AcceptSuffix`. `Opaque` returns `None` on
  its first match arm without touching `entries` — a provable no-op leaving the
  decision+persist path byte-identical. `SemaVersionedLog` refuses the first body
  that does not `addresses_to` its carried digest with the EXISTING
  `AppendRejectionReason::DigestMismatch` (no new wire variant). The refusal routes
  to `Output::AppendRejected` and never reaches `apply_inner`/`persist_suffix`.

## Storage (acceptance criterion 1) — additive family, no migration

- `mirror/schema/sema.schema` — local `ContentAddressing` enum; `StorePolicy {
  store.String addressing.ContentAddressing }`; `PolicyFamily (Family { ...
  table.store-policies ... })`; `RegisteredLedger` gained `addressing.ContentAddressing`.
- `mirror/src/store.rs` — `impl EngineRecord for StorePolicy` (keyed by store);
  `ContentAddressing::from_meta` (the one meta->local contact point, sibling of
  `RetentionSetting::from_order`); `Store.policies` table + `policy_family()`
  registered in `Store::open`; `policy_row` reader; `load_ledger` reads the policy
  (missing row => `Opaque`); `register_store` upserts the policy row (assert for a
  virgin store, mutate on re-registration since retire keeps the row).

### SchemaVersion decision: keep `SchemaVersion::new(1)` (justified)

The regenerated `family_identity` diff adds ONLY `POLICY_FAMILY`; the four
existing family hashes (HEAD/ENTRY/CHECKPOINT/RETENTION) are byte-identical, so
NO stored rows migrate. sema-engine `73eea24` `register_table` treats an unknown
family as `FamilyRegistration::New` and inserts it into the dynamic CATALOG;
`SchemaVersion` is the storage-kernel LAYOUT version, unaffected by family count.
A 5th family is therefore a compatible additive evolution under `new(1)`; bumping
to `new(2)` would be unnecessary and could trigger a layout refold. (This is the
one place I chose less-conservatively than the design's "maybe bump", with the
hash-diff + register_table semantics as the evidence.)

### meta wire version

`meta-signal-mirror` Cargo package `0.1.0 -> 0.2.0` (breaking wire change; old
encoded `RegisterStore` no longer decodes). The schema-generation version string
in both build.rs files stays `"0.1.0"` (import-identity token shared between the
producer and mirror's hardcoded dependency declaration; changing it would break
schema import resolution). `mirror` package `0.1.2 -> 0.1.3` (additive storage
family + new behavior). Reject wire + nexus decision schema unchanged.

## sema-engine rev built against

`73eea24b294a2bdcac470111afc387e7ce06608e` — the EXACT determinism-proven rev.
`cargo update -p meta-signal-mirror` did NOT move sema-engine (still `73eea24` in
`mirror/Cargo.lock`), so the design's determinism proof holds unchanged; no
re-run was required. (It did bump build-time schema tooling — `schema`,
`schema-cc`, `schema-rust` — to current `main`; those are codegen tools, not the
determinism-critical runtime.)

## External consumers of StoreRegistration / RegisterStore (for landing)

Reachable (must be updated at landing, producers-before-consumers — after
meta-signal-mirror operator branch merges to main):

- `spirit` (`/git/github.com/LiGoldragon/spirit`), pins `meta-signal-mirror`
  `branch = "main"` and `mirror` `branch = "main"`. Three test construction sites
  use the OLD `StoreRegistration::new(StoreName::new(...))`:
  - `tests/criome_gate_1of1.rs:130`
  - `tests/mirror_shipper.rs:102`
  - `tests/end_to_end_offline_full_chain.rs:469`
  Each becomes `StoreRegistration { store: ..., addressing: ContentAddressing::Opaque }`.

Unreachable (flagged, NOT entered): any `meta-signal-mirror` consumer under
`private-repos/` is off-limits to this role. I did not enter `private-repos/`.
The landing step must enumerate and update any private consumers of
`RegisterStore`/`StoreRegistration` before retiring the meta-signal-mirror
operator branch. No private scope was inspected.

## Verification

Inner-loop (cargo, sandbox-disabled for git/network):

- `meta-signal-mirror`: `cargo test` and `cargo test --all-features` — 6 passed
  (incl. the both-variant register round-trip).
- `mirror`: full `cargo test` — append_addressing_refusal 1, daemon_logic 17,
  end_to_end_arc 2, landed_body_readback 1; all OK, no regressions.
- `mirror`: `cargo clippy --all-targets -- -D warnings` clean; `cargo fmt --check` clean.

Durable Nix witness (acceptance criterion 3) — `mirror-append-refuses-digest-mismatch`:

- STATUS: GREEN. Built from the mirror repo on the `538f5124` operator commit
  with the operator `meta-signal-mirror` (`44dfac6c`) fetched from GitHub by crane.
  Output path: `/nix/store/qil1981bchvlm13802irqc0c0d270xvr-mirror-test-0.1.3`.
  Build log (the test ran inside the sandbox):

  ```
  +++ command cargo test --release --locked --test append_addressing_refusal refuses_mismatched_body_and_lands_matching_body -- --exact
       Running tests/append_addressing_refusal.rs
  running 1 test
  test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.02s
  ```

  Command: `nix build .#checks.x86_64-linux.mirror-append-refuses-digest-mismatch -L`
  (cwd `/git/github.com/LiGoldragon/mirror`). The first two attempts hit transient
  infra failures on the `prometheus` remote builder ("Nix daemon disconnected",
  then "failed to start SSH connection") — `mirror-deps` had already compiled
  cleanly both times; the final realization forced a local build with
  `--builders ''`. Not a code failure.
- The check executes `tests/append_addressing_refusal::refuses_mismatched_body_and_lands_matching_body`,
  which witnesses, on a real versioned sema-engine genesis body:
  (a) a `SemaVersionedLog` store REFUSES the tampered body (carried digest from
  entry A, payload from a different genuine entry B) with `DigestMismatch`, and it
  is NOT persisted — `landed_entries` empty AND observed head `None`;
  (b) the FAITHFUL body lands and re-hashes (via `LandedBody::content_address`) to
  the carried head;
  (c) an `Opaque` control store lands the SAME tampered body unchanged
  (payload-blind, Spirit 0yx5).

## Deviations from the design / residual risk for the auditor + landing

- SchemaVersion stays `new(1)` (design floated a possible bump). Evidence above.
- `RegisteredLedger.addressing` schema field is lowercase (generates `pub
  addressing: ContentAddressing`), not the design's capitalized `Addressing`
  (which would have wrapped a newtype). Cleaner; identical semantics.
- `register_store` UPSERTS the policy (assert-or-mutate) rather than a bare assert,
  because retire keeps the policy row and sema-engine `assert` errors on an
  existing key. Re-registration overwrites with the freshly chosen addressing.
- Minor atomicity note: registration asserts head then policy in two
  transactions; a crash between leaves a registered store reading as `Opaque`
  until re-registration. Acceptable (owner op, retried); flagged for the auditor.
- Feature-line override to carry at landing: `mirror/Cargo.toml` pins
  `meta-signal-mirror` to `branch = "operator/p0gg-content-addressing"` and
  `Cargo.lock` to `44dfac6c`. At landing, meta-signal-mirror operator branch merges
  to main first, then mirror flips back to `branch = "main"` and re-locks.
- `mirror` operator bookmark `538f5124` is committed but NOT pushed; the
  meta-signal-mirror operator bookmark IS pushed (non-main). Nothing on any
  production main. `private-repos/` untouched.

## Changed files

`meta-signal-mirror`: `schema/lib.schema`, `src/schema/lib.rs` (generated),
`Cargo.toml`, `Cargo.lock`, `tests/round_trip.rs`.

`mirror`: `schema/sema.schema`, `src/schema/sema.rs` (generated), `src/store.rs`,
`src/decision.rs`, `src/readback.rs`, `src/engine.rs`, `flake.nix`, `Cargo.toml`,
`Cargo.lock`, `tests/append_addressing_refusal.rs` (new), `tests/daemon_logic.rs`,
`tests/end_to_end_arc.rs`, `tests/landed_body_readback.rs`.
