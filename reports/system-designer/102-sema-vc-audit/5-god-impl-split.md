# 102/5 — God-impl split: landed (and a reviewer false-negative caught)

*The behavior-preserving decomposition the psyche confirmed ("definitely should
be elegantly split"). Two parallel slices, both green; `sema` stays actor-free.
One adversarial reviewer returned a false "fabricated" verdict by looking in the
wrong repo — caught and corrected by direct verification.*

## What landed

| Repo | Branch | Head | Ver | Verdict |
|---|---|---|---|---|
| sema-engine | `engine-decomposition` (on `record-key-sum`) | `f074b985` | 0.6.2 | approve (partial-by-design) |
| spirit | `store-decomposition` (on `vc-followups`) | `8eeeda8` | 0.13.1 | green; reviewer false-negative — orchestrator-verified |

**engine-decomposition** — extracted the two largest *state planes* off `impl
Engine` onto data-bearing owners: **`CommitLog`** (`src/commit_log.rs`: the
hash-chained log tables + cached `CHAIN_HEAD` + count counters + the append choke
point + range/replay reads + the layout-skew refold) and **`Outbox`**
(`src/outbox.rs`: the mirror outbox rows + `MIRROR_CURSOR` + durability). `Engine`
keeps the verb facade + the atomic write-transaction coordination, lending
`&WriteTransaction` to `CommitLog::append_*` and `Outbox::record` so a mutation
still commits data + log + outbox + chain-head + counts in **one** txn. Proven
behavior-preserving: 116 tests pass *identically*, the `tamper.rs`/`fold.rs`/
`checkpoint.rs`/`import.rs` witness files are **byte-for-byte unchanged**, the
public surface is **byte-identical** (510 `pub` items before and after), no
actors/async added. `engine.rs` 2363 → 2179.

**store-decomposition** — extracted five data-bearing owners off `impl Store`:
`RecordIdentifierMint` (`record_identifier.rs`), `ArchiveDatabase` (`archive.rs`),
`StoreFamilyDirectory` + `Migration::marker_key` (`family_directory.rs`),
`StoreError` + remediation (`error.rs`), `GuardianRecordBundle`
(`guardian_bundle.rs`). `store.rs` → `store/mod.rs` (1843 → 1511). `tests/`
untouched; public API relocated, not changed; the query-selection `matches`-impls
deliberately kept in `mod.rs` (orphan rule).

## The reviewer false-negative (worth recording)

The store reviewer returned **needs-fixes / "fabricated deliverable"** — claiming
the branch, head, and files didn't exist. Every load-bearing claim it made was
wrong: it looked for `store.rs` in **`sema`** (it lives in **spirit**), declared
the branch absent (it is on `origin/store-decomposition` @ `8eeeda8`), and
imported the *engine* slice's `RecordKey`-struct→enum and line-count facts as if
they were this slice's. I verified directly: the branch, the head, all five
owner submodules, and `tests/` being untouched all exist, and I re-ran
`cargo test --features production-migration` myself — **green, 0 failed**,
including the moved `store::error` test.

The lesson for these workflows: an adversarial reviewer can fail by *mislocating*
the artifact and then confabulate a confident rejection. The orchestrator must
spot-verify a "fabricated/doesn't-exist" verdict against the filesystem/VCS
before trusting it — a reviewer's false negative is as costly as a builder's
false positive. (The engine reviewer, by contrast, verified in an isolated
workspace at the exact pushed head and was correct.)

## Honest status of "elegantly split"

The *substantive* elegance — **state ownership** — is done: the log, outbox, and
store's identity/archive/family-directory state now live on the nouns that own
them, not dumped on a god-object. But both facade files remain over the
~thousand-line bar: `engine.rs` ~2179 and `store/mod.rs` ~1511, because the
**verb facade** (assert/mutate/retract/commit + identified variants +
match/replay, all with large generic signatures that must stay on the type) is
intrinsically large. The engine agent also, by deliberate and sound choice, left
subscription-persistence on `Engine` (its counter is probed by the open-time
layout heuristic) and versioned-entry minting inline (tightly bound to each
mutation's generics).

So one open question for the psyche (a real judgment call, not a clear task):
the verb facade can be further distributed across by-concern `impl Engine` /
`impl Store` files (mutation verbs, query/replay, …) to get each file under the
no-thousand-line bar — purely organizational, behavior-preserving. That trades a
single cohesive facade file for several smaller ones. Worth doing for the
line-count rule, or is the verb facade legitimately cohesive as one file? Holding
for the call rather than fragmenting cohesion for line-count's sake.

## Integration

The split tips are the new deployable heads: sema-engine `engine-decomposition`
@ `f074b985`, spirit `store-decomposition` @ `8eeeda8`. They stack on the
functional arc, so the integration order in `primary-qu28` is unchanged; operator
repins consumers to these tips at integration. The splits are API-preserving, so
no consumer code changes.
