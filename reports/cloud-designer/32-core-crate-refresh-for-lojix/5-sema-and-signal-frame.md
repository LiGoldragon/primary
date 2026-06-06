# sema / sema-engine / signal-sema / signal-frame — refresh for the lojix stack

Survey for cloud-designer. Scope: the storage kernel (`sema`), the
database engine library (`sema-engine`), the Sema operation vocabulary
(`signal-sema`), and the signal wire kernel (`signal-frame`), read against
the current lojix triad-port at
`/git/github.com/LiGoldragon/lojix/triad-port`.

The blunt headline up front: **lojix does not depend on `sema`,
`sema-engine`, or `signal-sema` at all today, and its `signal-frame`
dependency is vestigial (declared, never used in source).** None of the
flagged "new developments" force a change on lojix. The single genuinely
actionable item is a deliberate, optional port of lojix's hand-written
in-memory `Store` onto `sema-engine` for real persistence — and the
analysis below argues that is **premature** at M1.

## What lojix actually depends on (drift baseline check)

`triad-port/Cargo.toml` dependencies: `nota-codec`, `nota-config`,
`nota-next` (optional, `nota-text` feature), `meta-signal-lojix`,
`signal-lojix`, `rkyv`, `thiserror`, `triad-runtime`; build-dep
`schema-rust-next`. There is **no** `sema`, `sema-engine`, or
`signal-sema` entry.

`signal-frame` IS present in lojix's `Cargo.lock`, pinned at `d61ebf2`
(`triad-port/Cargo.lock:471,542,554`), pulled in transitively through
`signal-lojix`, `meta-signal-lojix`, and `triad-runtime`. But:

- `signal-lojix/triad-port/Cargo.toml:24` declares `signal-frame`, yet
  `grep -rn "signal_frame::|::signal_frame" signal-lojix/triad-port/src`
  finds **zero** non-comment uses. The generated `lib.rs` defines its
  own `encode_signal_frame`/`decode_signal_frame` (schema-rust-next
  emission) and imports nothing from `signal_frame`. The dependency is
  **vestigial** — a leftover declaration, not a live coupling.
- `triad-runtime`'s only use of `signal-frame` (per the dep fingerprint)
  is its own internal need; lojix's `daemon.rs` imports framing from
  `triad_runtime`, not `signal_frame`.

So lojix's "pin of signal-frame at d61ebf2" is real in the lockfile but
load-bearing on nothing. `signal-frame` HEAD is `6f5a77f`, four commits
ahead of the pin (`ee407c8`, `6f5a77f` plus the two flagged ones are at
or below it). Refreshing the pin changes no lojix behavior.

HEAD revs at survey time:

| Crate | HEAD | Date | lojix pin |
|---|---|---|---|
| `sema` | `09f2a42` | 2026-06-05 | n/a (no dep) |
| `sema-engine` | `e1aeef1` | 2026-06-05 | n/a (no dep) |
| `signal-sema` | `c132e9a` | 2026-06-05 | n/a (no dep) |
| `signal-frame` | `6f5a77f` | 2026-06-05 | `d61ebf2` (vestigial, via deps) |

## (b) Wire framing: signal-frame vs triad-runtime — reconciled by layering, not divergent

This is the clearest finding. lojix's `decode_signal_frame` /
`encode_signal_frame` come from **schema-rust-next's emission**, not from
`signal-frame`. There are three distinct framing implementations in play,
and they compose cleanly:

1. **Inner frame (schema-rust-next generated, in lojix's own
   `src/schema/sema.rs:1056-1130` and `nexus.rs:929-985`).**
   `encode_signal_frame` produces `[u64 LE short_header][rkyv archive]`
   — an 8-byte little-endian discriminant header followed by the rkyv
   body. **No length prefix.** `decode_signal_frame` strips the 8-byte
   header, routes by it, rkyv-decodes the rest, and re-checks the header
   against the decoded value (`HeaderMismatch` witness). This is lojix's
   `SignalFrameError` enum, emitted per-crate.

2. **Outer transport frame (triad-runtime `LengthPrefixedCodec`,
   `triad-runtime/src/frame.rs`).** Wraps the inner bytes in a `[u32 BE
   length][body]` envelope with a `MaximumFrameLength` guard. lojix's
   `daemon.rs:191-208` does exactly this: `codec.read_body(stream)` →
   `Input::decode_signal_frame(body.bytes())` on the way in, and
   `reply.encode_signal_frame()` → `FrameBody::new(..)` →
   `codec.write_body(..)` on the way out. lojix caps the body at 8 MiB
   (`MAXIMUM_REQUEST_FRAME_BYTES`, audit R1) rather than the codec's 4
   GiB u32 default.

3. **signal-frame's own framing (`signal-frame/src/frame.rs`).** Defines
   `ShortHeader` (also 8-byte LE, `SHORT_HEADER_BYTE_COUNT = 8`),
   `ExchangeFrame`/`StreamingFrame` with `encode_length_prefixed`
   producing `[u32 BE length][u64 LE ShortHeader][rkyv ExchangeFrameBody]`.
   This is a **parallel, hand-written** path. lojix uses NONE of it. The
   signal-frame macros (`macros/src/emit.rs:912-924`) emit
   `ExchangeFrame`/`StreamingFrame` aliases for contracts that go through
   *signal-frame's* generator — which lojix's contracts do not.

**Are they reconciled or divergent?** Reconciled by convention,
divergent by codepath. Both the schema-rust-next emitter and signal-frame
agree on the 8-byte LE short-header convention and a u32 BE length
prefix; the byte layouts are compatible by design. But they are two
independent implementations: schema-rust-next inlines the header into the
generated type's methods (no `ExchangeFrameBody` enum wrapper), while
signal-frame wraps the body in an `ExchangeFrameBody<Req, Reply>` enum.
A frame produced by signal-frame's `ExchangeFrame::encode_length_prefixed`
is **not** byte-identical to lojix's `LengthPrefixedCodec` +
`encode_signal_frame` (signal-frame nests the payload inside an enum
discriminant; lojix's generated route enum sits at the rkyv top level).
There is no shared codec these two pin to. This is fine for now — lojix
is internally consistent — but it is a latent duplication: the workspace
has two "8-byte-header + length-prefix" wire framers and they are not the
same code.

**Bearing on lojix:** none requiring action. The framing lojix uses is
self-consistent and live. signal-frame's `frame.rs` and the four flagged
commits are not in lojix's path.

## (c) "Effect surfaces" and "rejection witness" — signal-frame's macro DSL, not lojix's runtime

The two flagged signal-frame commits that sound like they touch lojix's
Nexus effect plane do **not**:

- **`d3c0d17` "emit schema crystallized effect surfaces"** is a change to
  `signal-frame/macros/` (the `signal_channel!` proc-macro generator). It
  adds `Operation`/endpoint enums, `ExtendedHeader`, `Effect`,
  `EffectTable`, `Interact`, `InteractionActor`, and fan-out output
  records to *that macro's* emission, replacing the old hand-written
  macro path. lojix uses schema-rust-next, a different emitter, and its
  generated code references **none** of these symbols
  (`grep EffectTable|InteractionActor|crystalliz` in
  `lojix/triad-port/src` → zero hits). lojix's real-nix-IO effect plane
  lives entirely in its hand-written `schema_runtime.rs` (`run_effect`
  drives `std::process::Command` for `nix eval`/`nix build`). signal-frame's
  `Effect`/`EffectTable` is a wire-contract scaffold concept, unrelated
  to lojix's process-execution effect continuations.

- **`f7ffd75` "accept schema-input rejection witness"** is a trybuild UI
  test (`tests/ui/channel_macro/schema_input_rejected.stderr`) asserting
  that signal-frame's `signal_channel!([schema])` macro **fails to
  compile** with a specific error. It is a *compile-time* witness for the
  macro DSL's input grammar. It has nothing to do with lojix's *runtime*
  rejection witnesses (`QueryRejected`/`DeployRejected` with
  `RejectionReason`, e.g. `daemon.rs:233-260`,
  `schema_runtime.rs:912,933,961`). Those are lojix's own schema-derived
  reply variants. No bearing.

- **`d61ebf2` "constrain schema boxed nota codecs"** and **`a03b3c4`
  "route schema marker through schema reader"** are likewise both inside
  `signal-frame/macros/` (and a UI test). They tighten how signal-frame's
  macro reads `.schema` markers and emits boxed NOTA codecs. lojix never
  invokes this macro. No bearing.

**Verdict on (c):** all four flagged signal-frame commits are internal to
signal-frame's *parallel* schema-macro generator, which lojix's stack
does not use. They do not touch lojix's effect plane or its rejection
witnesses. They are NOT applicable to lojix.

## (a) Should lojix's hand-written Store be ported onto sema-engine?

### What lojix has today

`lib.rs:107-185`: a `Store` = `Mutex<StoreState>`. `StoreState` holds four
generated `Vec`-backed newtype tables — `LiveSetTable`, `GcRootsTable`,
`EventLogTable`, `ContainerLifecycleTable` — plus four `u64` counters
(`commit_sequence`, `deployment_sequence`, `generation_sequence`,
`subscription_sequence`). All in-memory; the doc comment on `lib.rs:10-12`
and `162-165` explicitly names "sema-engine / redb persistence is a noted
follow-on" and says it "mirrors the `cloud` `Store` shape." Writes lock
the whole `StoreState`, bump `next_commit_sequence()`, and push/scan the
`Vec`s. The daemon builds a fresh per-request `SchemaRuntime` over a
shared `Arc<Store>` (`daemon.rs:220`).

### What sema-engine now offers (the genuinely new surface)

The three flagged sema-engine commits added **identified record
families**, which is the structurally relevant new capability:

- **`817236a` "add identified record families"** (+879 lines): adds
  `IdentifiedTableDescriptor`/`IdentifiedTableReference`/`IdentifiedRecord`
  (`table.rs:30-130`), `RecordIdentifier` (`record.rs:42-74`, a durable
  `u64` with `first()`/`next()`), `register_identified_table`,
  `assert_identified`, `retract_identified`, `match_identified`
  (`engine.rs:74-275,707`), and the `IDENTIFIED_COUNTERS` redb table
  that persists the next-identifier per table across reopen
  (`engine.rs:80-91,119-133`).
- **`e1aeef1` "add identified mutation"** (+167): adds
  `mutate_identified` + `IdentifiedMutation`/`IdentifiedMutationReceipt`
  (`engine.rs:215`, `mutation.rs:49-63,131-193`), completing
  assert/mutate/retract/match on engine-assigned identity.
- **`08d3d2b`** is a 5-line ARCHITECTURE doc note that `Retract` is
  destructive once redb reclaims pages — a durability caveat, no code.

**Why identified families matter to lojix:** lojix's `live_set`,
`event_log`, and `containers` are all append-with-monotonic-counter
tables, and `gc_roots` is keyed by a synthetic generation identity. This
is exactly the shape `IdentifiedTableDescriptor` serves: the engine
allocates and persists the `RecordIdentifier`, advances a durable
`CommitSequence` per write, and writes a commit-log entry — replacing
lojix's hand-rolled `next_commit_sequence`, `next_generation_identifier`,
`next_deployment_identifier`, and `next_event_log_position` counters
(`lib.rs:137-159`) with engine state. The `CommitSequence` high-water mark
is also the documented mechanism for the version-handover story lojix will
eventually need.

### What a port would actually take — and why it is non-trivial

This is **not** a drop-in. Concrete frictions, each load-bearing:

1. **Query model mismatch (the big one).** lojix reads/mutates by
   *composite domain predicates*: `gc_roots` is found by
   `(generation_identifier, cluster_name, node_name)` and by `label`
   (`schema_runtime.rs:884-891,906-925,944-958,972-979`); pin/unpin mutate
   a row *in place* selected by a multi-field match. sema-engine's `Match`
   reads by `QueryFilter::{All, Key, KeyRange}` only (`query.rs:150-197`);
   `PredicatePlan`/`Constrain`/`Project`/`Aggregate`/`Infer`/`Recurse`
   exist as typed plan nodes but return `UnsupportedReadPlan` until
   execution semantics land (`error.rs`, ARCHITECTURE §"Unsupported
   read-plan"). So lojix would either (a) `match` the whole table and scan
   in memory (re-introducing the linear scans, now with rkyv decode cost),
   or (b) maintain its own secondary-index tables keyed by label /
   composite key. Neither is free.

2. **Single-owner engine vs lojix's per-request fresh runtime.**
   sema-engine's `Engine` is explicitly a single-owner handle; concurrent
   callers race the commit log and "must own each `Engine` from one actor
   and serialise all engine calls through that actor" (ARCHITECTURE
   Constraints, `engine.rs` open). lojix today builds a fresh
   `SchemaRuntime` per request over a shared `Arc<Store>` and relies on the
   brief `Mutex` lock for atomicity (`daemon.rs:220`,
   `schema_runtime.rs:860` etc.). Porting means lojix needs ONE owning
   `Engine` (behind its own `Mutex` or a dedicated actor), not a fresh
   handle per request — a real change to the concurrency design that
   currently lets a 4ms query run alongside a multi-minute deploy. The
   `Engine` lock would serialize the actual write commits (acceptable —
   writes are brief) but lojix must ensure long `nix` IO happens
   *outside* any held engine lock (it already structures effects this way,
   but the boundary would need re-auditing).

3. **`state_digest` has no engine equivalent.** lojix's generated
   `DatabaseMarker` carries `commit_sequence` AND `state_digest`
   (`schema_runtime.rs:336-346` fakes `state_digest = commit_sequence`).
   sema-engine exposes `CommitSequence` and `SnapshotIdentifier`, no
   digest. lojix would keep faking `state_digest` (or map it to
   `SnapshotIdentifier`); the engine does not supply it.

4. **EngineRecord trait + rkyv bounds.** Each ported table's record type
   must `impl EngineRecord` (`record_key`) for keyed families, or be used
   under an identified family, and satisfy `EngineStoredValue`'s rkyv
   bounds (`record.rs:76-125`). lojix's generated records already derive
   rkyv (the bounds are satisfiable), but the `record_key` placement is a
   per-table design decision lojix has not made.

5. **New dependency surface + redb file lifecycle.** lojix gains `sema`,
   `sema-engine`, `signal-sema` (sema-engine pulls `signal-sema` and a
   `signal-frame` `NonEmpty` utility — note lojix already transitively has
   signal-frame). It must choose a `.sema` file path, a `SchemaVersion`,
   and own open/close. `EngineOpen::new(path, SchemaVersion::new(1))`.

### Recommendation on (a): defer. It is the right destination but premature now.

The workspace intent is explicit and unambiguous that lojix storage
should *eventually* go "via sema-engine" (active-repositories Replacement
Stack row for `lojix`; `lib.rs` doc comment names it a follow-on). And
sema-engine is genuinely mature for this: it has identified families with
durable counters, the `CommitSequence` handover spine, commit-log replay,
and a typed per-crate error enum — it is library-complete for lojix's
table shapes *modulo the predicate-query gap*.

But porting now is premature because:

- **M1's goal is the pipeline + two-socket round-trip + concurrency**, all
  of which are done with the in-memory Store. Persistence is not on M1's
  critical path. The `Store` doc comment itself frames it as a follow-on.
- **The predicate-query gap (friction 1) is the real cost** and it lands
  *before* lojix gets any value: lojix's most-used reads are composite-key
  scans that sema-engine cannot execute as plans yet. Porting today buys
  durable redb but forces either in-memory post-`match` scanning or
  hand-built secondary indices — re-creating the linear-scan logic lojix
  already has, plus rkyv decode overhead, plus a redb file. Net negative
  until `Constrain`/`PredicatePlan` execution lands in sema-engine.
- **The concurrency redesign (friction 2) is a genuine risk** to the
  one M1 property the report calls out as proven (a query answered in ~4ms
  while a deploy ran). Moving to a single-owner `Engine` needs care to
  preserve that, and is not worth spending M1 risk budget on.

The right sequencing: keep the in-memory `Store` through M1; revisit the
port when (i) lojix needs persistence across daemon restarts (the first
real production requirement), or (ii) sema-engine's predicate read-plan
execution lands (removing friction 1), whichever comes first. When that
happens, the identified-family API is the correct target and the
`StoreState` counters map directly onto engine state.

## Adversarial check — what is NOT a new development for lojix

- **All four flagged `signal-frame` commits** (`d61ebf2`, `a03b3c4`,
  `d3c0d17`, `f7ffd75`): internal to signal-frame's `signal_channel!`
  macro generator. lojix uses schema-rust-next, not this macro. Zero
  bearing. The "effect surfaces" and "rejection witness" names are
  false-friends — they are wire-contract-macro scaffolding and a
  compile-fail trybuild test, not lojix's runtime effect plane or its
  runtime rejection replies.
- **sema-engine `08d3d2b`** (Retract-destructive doc): a durability caveat
  worth knowing IF lojix ever ports (a retracted gc_root is unrecoverable
  once pages reclaim — matters for the pin/retire history story), but it
  is a doc note, not code, and does not apply while lojix is in-memory.
- **`signal-sema`** is not consumed by lojix and would only arrive
  transitively if lojix adopts sema-engine. Its recent commit
  (`c132e9a` "remove stale signal-frame dependency") is housekeeping. The
  six Sema operations (`Assert`/`Mutate`/`Retract`/`Match`/`Subscribe`/
  `Validate`) are deliberately NOT on lojix's public wire — lojix's
  contracts (signal-lojix/meta-signal-lojix) own contract-local roots
  (Deploy/Pin/Query/...), consistent with the "six words stay off the
  public contract spine" discipline. No action.

## Concrete recommendations

1. **Refresh the vestigial `signal-frame` pin only as part of a routine
   `cargo update` of the transitive deps — or drop the unused declaration
   from `signal-lojix`/`meta-signal-lojix` `Cargo.toml`.** The pin at
   `d61ebf2` is load-bearing on nothing; HEAD is `6f5a77f`. Better: file
   a cleanup to remove `signal-frame` from `signal-lojix`'s deps since no
   source uses it (verify `meta-signal-lojix` likewise). Small effort, low
   risk; removes a confusing "lojix pins signal-frame" signal.

2. **Do NOT port the `Store` to sema-engine in M1.** Keep the in-memory
   `Store`. Record (in lojix's INTENT/ARCHITECTURE) that the port target
   is sema-engine *identified families*, blocked on either a real
   persistence requirement or sema-engine predicate-read-plan execution.
   Medium effort to write the note; the port itself is large.

3. **When the port does happen, target identified families, not keyed
   families, for `live_set`/`event_log`/`containers`; build a secondary
   index (or accept post-match scan) for `gc_roots`' label/composite
   lookups.** Map `StoreState`'s counters onto `CommitSequence` +
   `RecordIdentifier`; keep faking `DatabaseMarker.state_digest` (or map
   to `SnapshotIdentifier`). Large effort, medium risk (concurrency
   redesign to single-owner `Engine`).

4. **No action on the framing duplication, but note it.** schema-rust-next
   and signal-frame both implement an 8-byte-header + u32-length framer
   and they are not the same code. If the workspace later wants ONE wire
   framer, that is a schema-rust-next ↔ signal-frame reconciliation
   decision above lojix's pay grade — lojix is a downstream consumer of
   whatever schema-rust-next emits. Flag for the nota/schema designers.

## Open questions

- Is signal-frame's declared-but-unused dependency in
  `signal-lojix`/`meta-signal-lojix` intentional (reserved for a future
  envelope) or stale? The doc comment says "signal-frame mail envelope"
  but no code uses it.
- When sema-engine predicate/`Constrain` read-plan execution lands, does
  it cover the multi-field equality lojix needs for `gc_roots`
  (generation_identifier + cluster_name + node_name + label)? That gate
  decides whether the port is clean or still needs hand-built indices.
- Does lojix want persistence across restarts before M2, or is in-memory
  acceptable through the smoke-deploy milestone? This is the trigger for
  the port and is a psyche/roadmap question, not a technical one.
