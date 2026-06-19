# 694/2 — spirit: validate-on-criome → propagate → interchangeable

Research for the cluster-propagation PoC. This file answers the spirit
half of the loop: how spirit accepts a new state object, asks criome to
authorize the exact content-addressed digest (`2st7`/`w2g3`), acquires a
new authorized head from criome (`nfvm`), and how three spirit engines
become interchangeable. The strongest reusable witness is the OFFLINE
full-chain e2e harness in the spirit repo — built on next.

## TL;DR — the load-bearing finding

The whole spirit-side propagation spine **already exists and ships as
production code on main**, and there are **two green-class witnesses** in
the spirit repo to clone directly:

1. `spirit/tests/mirror_shipper.rs` — the spirit-engine→mirror→**fresh
   spirit store** restore loop. This is the closest thing to "machine A
   ships, a fresh machine acquires identical state," using the REAL
   `spirit::Engine`, the REAL `from_shared_engine` Arc seam, and the REAL
   `Store::import`. It proves A→A' interchangeability through a mirror.
2. `spirit/tests/end_to_end_offline_full_chain.rs` — the full
   spirit→mirror-A→**router A→B notice**→mirror-B-fetch→restore chain in
   ONE binary, with the router carrying a content-addressed head notice.
   This is the leg-2 (router type/coordinate fanout) that the
   mirror_shipper loop lacks.

The PoC for "3 spirits interchangeable" is: take harness (2)'s structure,
replace the harness-local `MirrorObjectNotice` with the now-**production**
`signal_mirror::ObjectNotice` / `Input::NotifyObject` contract (it landed
since report 673), restore into a real `spirit::Store` (as in harness (1))
instead of a generic `ComponentEngine`, and fan the notice to TWO spirits
(B and C) instead of one witness socket. criome's 2-of-3 authorization
wraps the digest that becomes the notice's head — that is the one genuinely
new seam this PoC must add (see gaps).

## What is the "new state object" and how spirit accepts it

Spirit's working input vocabulary is the schema-emitted
`signal_spirit::Input` enum. The first variant — and the literal "state
object" — is `Input::State(State)` where `State(Statement)`
(`signal-spirit/src/schema/signal.rs:141,1412`; schema source
`signal-spirit/schema/signal.schema:44,54`). The durable mutators are
`Record`, `Propose`, `Clarify`, `Supersede`, `Retire`, `ChangeRecord`,
etc. Every such write flows:

```
Input → Engine::handle_async                         (spirit/src/engine.rs:409)
      → SignalAdmission::admit  (mint origin route, validate)   (engine.rs:642)
      → SignalAccepted::process_with  (&mut Nexus single-flight) (engine.rs:743)
      → Nexus → SemaEngine::apply_inner  (the durable SEMA write) (store/mod.rs:125)
      → Store appends to the versioned commit log (Arc<sema_engine::Engine>)
```

After the local commit, the daemon's post-commit hook drains the unshipped
outbox to the mirror (`spirit/src/daemon.rs:153`,
`engine.ship_unshipped_to_mirror()`), best-effort: the local commit
already landed, so an unreachable mirror just leaves the suffix queued.

## How spirit asks criome to authorize the exact content-addressed digest (2st7/w2g3)

This is the one piece that is **intent-settled but not yet on the spirit
code path** — the offline e2e stubs criome per the psyche's "no key
encryption for now" steer (673). The settled mechanism (`2st7`):

- criome authenticates the **submitter** — the `SO_PEERCRED` caller
  resolved to a registered criome `Identity`, not merely the log.
- It is **after-the-fact, non-blocking, out-of-band attestation** binding
  the caller to the exact per-operation **content-addressed digest**.
- criome verifies bytes + principal; the spirit guardian keeps the full
  content verdict.

The content-addressed digest already exists in spirit as the engine's
per-entry head: every versioned commit produces a `MirrorHead`
(`commit_sequence` + 32-byte `entry_digest`) — see
`ComponentShipper::expected_head` / `mirror_head_from_mark`
(`mirror/src/shipper.rs:168,262`). The digest criome must authorize is
exactly `head.entry_digest()` of the new head. So "ask criome to authorize
the exact digest" = hand criome `(principal, store, sequence,
entry_digest)` after the local commit, and get back a 2-of-3-signed
authorization over that digest. **The PoC must add this call** (the
criome-quorum research agent owns the authorize side); spirit's
contribution is producing the digest, which it already does.

## How spirit acquires / adopts a new AUTHORIZED HEAD from criome (nfvm)

`nfvm` (verified by Lookup) is the governing record: *"criome is the
authority on the latest approved authorized head; Spirit fetches or
receives that authorized head from criome rather than deciding it locally,
and keeps its own accepted database … the Spirit daemon … learns to get a
criome authorization to fetch a new head."*

The acquire mechanism is **already coded** as the import path, and the
"which head to fetch" coordinate is **already a shipped contract**:

- **The notice (the authorized-head reference).** `signal_mirror`'s
  production `ObjectNotice` (`signal-mirror/src/schema/lib.rs:247`):
  ```
  pub struct ObjectNotice { pub store: StoreName, pub head: HeadMark, source: Source }
  ```
  where `HeadMark { sequence, digest }` (`lib.rs:108`) IS the
  content-addressed authorized head, and `Source(Option<MirrorAddress>)`
  (`lib.rs:242`) is the optional "where to fetch it from" — the exact seam
  for criome/router to tell a spirit where to pull the new head. It is
  carried on the wire as `signal_mirror::Input::NotifyObject(ObjectNotice)`
  (`lib.rs:381`), answered by `Output::ObjectNoticeAccepted(receipt)` /
  `ObjectNoticeRejected(rejection)` with typed reasons `UnknownStore`,
  `SourceUnavailable`, `HeadBehind` (`lib.rs:394,275`). Mirror checks a
  notice with `Store::check_object_notice` — *"accepting the notice means
  this mirror already holds that exact content-addressed head, not merely a
  higher sequence number"* (`mirror/src/store.rs:385-393`). This is the
  **production realization of the harness-local `MirrorObjectNotice`** the
  673 capstone seeded.

- **The fetch + adopt (the acquire itself).** `Store::import(path,
  checkpoint, suffix)` (`spirit/src/store/mod.rs:382`) opens a fresh
  spirit store, `begin_import()` → `ingest_checkpoint` → `ingest_suffix`
  → `commit(&StoreFamilyDirectory)`, landing the imported log + counters
  verbatim so the restored store is *"indistinguishable from the original
  at the imported range."* The fetch transport is
  `MirrorTailnetClient::exchange(Input::Restore(RestoreQuery))`
  → `Output::Restored(RestoreBundle)` (`mirror/src/shipper.rs:42`).
  `mirror_shipper.rs::restore_from_mirror` (lines 116-143) is the exact,
  working spirit-side fetch-and-adopt routine.

So "spirit acquires a new authorized head" = receive an `ObjectNotice`
(head + source) → call `Restore` against the source mirror → `Store::import`
up to that head. The notice's `head.digest` is precisely what criome
authorized, closing the `2st7`/`nfvm` loop. (Today `Store::import`
constructs a NEW store; for a running daemon to ADOPT a head into its live
engine, see gaps — this is the one "acquire into a running engine" seam.)

## The OFFLINE full-chain e2e harness — what it ALREADY proves and its shape

`spirit/tests/end_to_end_offline_full_chain.rs` (28 KB, one
`#[tokio::test(flavor = "multi_thread")]`). Report 673 records it passing;
I did **not** independently re-run it (deps are git-pinned to `main`; a
cold build was out of scope). What it proves at once, by leg:

| Leg | What it proves | Real components | file:line |
|---|---|---|---|
| 1 | spirit-shaped engine records intent, ships unshipped suffix → mirror A persists → `ServerCommitted`; outbox drained | real `mirror::ComponentShipper`, real `mirror::Service` over loopback TCP, real `sema_engine::Engine` | 453-525 |
| 2 | router A→B forwards an object-accepted **notice** (body = NOTA head coordinate) → delivered to a HarnessSocket on B; A's trace = `ForwardedRemote` | two real `router::RouterRuntime`s, real loopback TCP, typed `RouterMessageTraceQuery` | 529-690 |
| 3 | mirror B fetches from mirror A and restores **exactly up to the router-announced head**; byte-identical records `[alpha=revised, gamma=third]`; matching digest | real `MirrorTailnetClient` Restore, real `ComponentEngine::begin_import` | 692-755 |

Structure to clone:
- `ComponentFixture` (213-277): opens a versioned `sema_engine::Engine`,
  registers a `Thought` table, `populate()` writes alpha/beta + checkpoint
  + gamma + beta-tombstone. (For the PoC, swap `Thought` for a real
  `spirit::Store` so the records are real intent `Entry`s — harness (1)
  already does this.)
- `running_mirror` (284-299): one in-process `mirror::Service` on
  `127.0.0.1:0`, `ServiceLink`, queried bound address.
- `MirrorObjectNotice` (92-160): the harness-local seam — store +
  sequence + 32-byte digest, NOTA-encoded as the router message body,
  parsed back on B. **Replace with `signal_mirror::ObjectNotice`** (now
  shipped) for the PoC.
- `HarnessWitness` (307-379): a Unix socket that accepts one
  signal-harness delivery and reports the body back. The router fans the
  notice here. **For the PoC, B and C are real spirit engines that, on
  receiving the notice, drive `Restore`+`import`** — not passive witnesses.
- `import_restore_bundle` (425-448): decode checkpoint + suffix, run the
  import session. (Use `spirit::Store::import` instead.)
- The causal assertions (714-755): `target.current_commit_sequence ==
  notice.sequence`, `delivered_notice.digest ==
  confirmed_head.entry_digest`, identical query results. **This is the
  interchangeability assertion** — generalize it to B == A and C == A.

## How the mirror shipper drain + the `from_shared_engine` Arc seam work

The seam that makes spirit and its shipper share ONE engine:

- `Store` holds `database: Arc<sema_engine::Engine>`
  (`spirit/src/store/mod.rs:87`) and exposes
  `engine_handle() -> Arc<SemaDatabase>` (line 346) which clones the SAME
  Arc — *"the shipper reads the durable outbox the store's working writes
  append to and records the server-confirmed head back into it."*
- `MirrorShipper::configure` (`spirit/src/shipper.rs:53`) takes that Arc
  and builds `ComponentShipper::from_shared_engine(engine, addr,
  store_name)` (`mirror/src/shipper.rs:109`). Because `sema_engine::Engine`
  is intentionally **not `Clone`**, sharing is via `Arc` clone: store and
  shipper hold clones of one engine, so the working writes the store
  appends ARE the outbox the shipper ships, and `acknowledge_mirror` flows
  back into the same engine.
- The drain: `ComponentShipper::ship_unshipped` (`mirror/src/shipper.rs:175`)
  reads `engine.unshipped_outbox()`, replays the suffix from the first
  unshipped sequence, encodes each `VersionedCommitLogEntry` into an
  `EntryEnvelope` (carrying prev-digest + entry-digest + rkyv payload —
  payload-blind to the mirror), sends `Input::Append(EntrySuffix)` with
  `expected_head` (optimistic-concurrency guard), and on
  `Output::Appended(receipt)` calls `engine.acknowledge_mirror(head)`,
  flipping the shipped range to `Durability::ServerCommitted`.
- `MirrorShipper` is **OFF by default** (`Armed: Option<ComponentShipper>`,
  `shipper.rs:39`); it arms only when an owner `Configure` carries a
  `MirrorTarget::Address` (`engine.rs:490-500`). The daemon's
  `handle_working_input` calls `ship_unshipped_to_mirror()` unconditionally
  after every working write and pays nothing when unarmed (`daemon.rs:152`).

`spirit/tests/mirror_shipper.rs` exercises this end to end with the REAL
`spirit::Engine`: configure target → `record()` → local checkpoint →
`record()` → `engine.ship_unshipped_to_mirror()` (the exact daemon hook,
line 189) → assert `ServerCommitted` + empty outbox → publish checkpoint →
`restore_from_mirror` into a **fresh `spirit::Store`** → assert
`restored.len() == engine.store().len()` AND `restored.database_marker()
== engine.store().database_marker()` (lines 222-223). The `database_marker`
equality (commit sequence + blake3 `state_digest`,
`spirit/src/store/mod.rs:1138,1157`) is a content-addressed
interchangeability check: two spirit stores with the same marker hold the
same accepted state.

## How 3 spirit engines become INTERCHANGEABLE

The interchangeability claim reduces to three already-proven facts plus
one new fan-out:

1. **Same authorized head ⇒ same state.** A spirit store restored up to
   head H is byte-identical to the source at H (`Store::import` lands the
   log + counters verbatim, `store/mod.rs:382`; proven by
   `mirror_shipper.rs` `database_marker` equality and by
   `end_to_end_offline_full_chain.rs` identical-records + matching-digest).
   The `state_digest` (blake3 over records+referents folded with commit
   sequence) is the content address: equal marker ⇔ interchangeable.
2. **The head travels as a typed reference, not a payload** (`m0p2`,
   `57f9`): `ObjectNotice { store, head: HeadMark{sequence,digest},
   source }` is a 40-ish-byte coordinate; the router fans the reference and
   each spirit pulls the bytes itself (`Restore`). This is exactly the
   "criome/spirit emit references, components fetch" discipline.
3. **The router fans by type** (router research agent owns this): the
   notice is matched/routed by signal-standard
   `ComponentKind`/`Differentiator`/`AuthorizedObjectKind`. In the offline
   harness this is a direct A→B remote route (`InstallRemoteRoute`,
   `end_to_end_offline_full_chain.rs:599`); the PoC fans to B and C.

So: A commits → criome 2-of-3 authorizes digest D → notice
`(store, head{seq,D}, source=A's mirror)` → router fans to B and C → B and
C each `Restore`+`import` to head{seq,D} → all three stores share marker
(seq, state_digest) → interchangeable.

```mermaid
sequenceDiagram
  participant SA as spirit A (Engine + Arc&lt;Engine&gt; + ComponentShipper)
  participant MA as mirror A (Service)
  participant CQ as criome quorum (2-of-3)
  participant R as router (type-fan)
  participant SB as spirit B
  participant SC as spirit C
  SA->>SA: Input::State / Record → SEMA commit → MirrorHead{seq,digest}
  SA->>MA: ship_unshipped (EntrySuffix, payload-blind) → ServerCommitted
  SA->>CQ: authorize exact digest (2st7) [NEW SEAM]
  CQ-->>SA: 2-of-3 signed authorization over digest
  SA->>R: NotifyObject(ObjectNotice{store,head,source=MA})
  R->>SB: fan by type (Differentiator/AuthorizedObjectKind)
  R->>SC: fan by type
  SB->>MA: Restore(RestoreQuery) → bundle → Store::import to head
  SC->>MA: Restore(RestoreQuery) → bundle → Store::import to head
  Note over SA,SC: markers equal (seq, state_digest) ⇒ interchangeable (nfvm)
```

## Exact spirit/mirror surface the PoC must call

- `spirit::Engine::new(Store)`, `start()`, `handle_async(Input)`,
  `configure(ConfigureRequest)`, `ship_unshipped_to_mirror()`,
  `publish_checkpoint_to_mirror()`, `mirror_shipping_armed()`, `store()`
  — `spirit/src/engine.rs:340,382,409,472,522,532,511,432`.
- `spirit::Store::open`, `import(path, checkpoint, suffix)`,
  `engine_handle() -> Arc<SemaDatabase>`, `database_marker()`, `len()`,
  `checkpoint()` — `spirit/src/store/mod.rs:262,382,346,1138,1124,352`.
- `spirit::shipper::{MirrorShipper, MirrorShipperError}` (gated
  `mirror-shipper`) — `spirit/src/lib.rs:102`.
- `signal_spirit::Input::{State,Record,Propose,...}` — the new-state
  object — `signal-spirit/src/schema/signal.rs:1411`.
- `mirror::{ComponentShipper, MirrorTailnetClient, ShipOutcome, Service,
  ServiceLink}` — `mirror/src/lib.rs:45-51`;
  `ComponentShipper::from_shared_engine`, `ship_unshipped`,
  `publish_latest_checkpoint`, `expected_head` —
  `mirror/src/shipper.rs:109,175,229,168`.
- `signal_mirror::{Input::{Append,Restore,NotifyObject,PublishCheckpoint},
  Output::{Appended,Restored,ObjectNoticeAccepted,ObjectNoticeRejected},
  ObjectNotice, ObjectNoticeReceipt, ObjectNoticeRejectionReason, HeadMark,
  RestoreQuery, RestoreBundle, StoreName}` —
  `signal-mirror/src/schema/lib.rs:247,256,275,108,378,394`.
- `mirror::Store::check_object_notice(ObjectNotice)` (the
  already-holds-this-exact-head check) — `mirror/src/store.rs:389`.

## Gaps and PoC workarounds

1. **criome 2-of-3 authorize-the-digest is not on the spirit code path.**
   The offline e2e stubs criome (`AcceptFixedTestIdentity`). Intent
   (`2st7`/`w2g3`) is settled but no `Engine`→criome call exists.
   *Workaround:* the criome-quorum research/impl agent owns the authorize
   call; spirit hands it the `MirrorHead.entry_digest()` (already produced
   on every commit, `shipper.rs:168`) and only emits the `ObjectNotice`
   after a 2-of-3 authorization returns. In the PoC harness, wrap the
   digest with the real signal-criome contract where it builds; mark
   RED/shimmed if it does not (per frame discipline).

2. **"Acquire into a RUNNING spirit engine" — `Store::import` builds a NEW
   store.** Today the proven adopt path (`Store::import`,
   `restore_from_mirror`) constructs a fresh store at a new path; a live
   daemon adopting a head into its already-open `Arc<Engine>` is not yet a
   method. *Workaround:* the PoC's three "spirit engines" each open a
   fresh `Store` on receiving the notice (exactly `mirror_shipper.rs`'s
   `restore_from_mirror` shape) and assert marker equality — this proves
   interchangeability of the resulting state without needing live in-place
   adoption. Name the operator bead: a `Store::adopt_head` / engine-level
   import-into-live-store seam (`sema_engine` already has
   `begin_import`/`ingest_suffix`; the live-engine wrapper is the gap).

3. **The router-carried notice in the offline harness is harness-local
   (`MirrorObjectNotice`).** *Workaround:* the production
   `signal_mirror::ObjectNotice` / `Input::NotifyObject` contract landed
   since 673 (`signal-mirror/src/schema/lib.rs:247,381`; mirror handles it,
   `mirror/src/store.rs:389`). The PoC carries the real `ObjectNotice` as
   the router body (or routes it as a typed signal-router envelope — the
   router research agent owns the type-match). The `Source` field is the
   built-in "fetch from here" coordinate.

4. **Fan to ONE witness, not two real spirits.** The offline harness fans
   the notice to a single `HarnessWitness` socket. *Workaround:* register
   TWO remote routes (B and C) and make each a real `spirit::Store` that
   runs `restore_from_mirror` on receipt; assert
   `marker(A) == marker(B) == marker(C)`.

5. **mirror-target persistence across restart is deferred** (673). Not on
   the PoC's single-pass in-process critical path; the three instances are
   configured in-process at startup.

## Build / dep reality

- spirit (HEAD `fe04c12`, this branch) and mirror (HEAD `b26c139`) both
  pin every contract dep to `branch = main` (`spirit/Cargo.toml:88-138`,
  `mirror/Cargo.toml:40-51`), so Cargo unifies shared transitive crates
  (triad-runtime, sema-engine, nota-next, signal-frame, schema-rust-next)
  onto one rev each — the pin-unify wall from 673 is resolved on main.
- The spirit propagation tests require the `mirror-shipper` feature
  (`spirit/Cargo.toml:64,74,85`); the daemon binary build excludes it (no
  nota-next in the daemon tree).
- I did **not** run a build/test in this session (cold git-dep build out
  of scope); 673 records the offline full-chain harness as passing and
  both `mirror_shipper.rs` proofs green on the predecessor branch stack
  now merged to main. Treat green as reported-not-observed until the
  implement phase re-runs it.
