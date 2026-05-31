# 4 — spirit-next design audit

*Kind: audit · Topics: spirit-next, schema-core, actor-systems, boilerplate-elimination, layering · 2026-05-31 · designer lane sub-agent*

## Scope

Audit of `spirit-next` (`/git/github.com/LiGoldragon/spirit-next/`) as the
integrated runtime: Signal admission, Nexus mail keeper, SEMA redb store,
the CLI and daemon binaries, the transport, and the build-time schema
pipeline. Treats the schema-emitted module
(`src/schema/lib.rs`, 1269 lines) as a generated artifact — included where it
duplicates code per-component, excluded from "lift this from hand-written code"
findings.

Sister findings (Gap C in designer 435, Gap 4 in operator 263) are
hypotheses; this audit examines the live code to see whether the hypothesis
holds at the scale predicted and to find additional substrate gaps the
prior surveys did not name.

Source budget: 4056 lines total (1269 generated, 1379 hand-written src,
1408 tests + build.rs).

## Finding 1: Generated `src/schema/lib.rs` is ~600 lines of envelope boilerplate that every component will duplicate

The generated module (1269 lines) splits cleanly:

**Component-specific (~300 lines)**: schema vocabulary — `Topic`,
`Topics`, `Entry`, `Query`, `Magnitude`, `Kind`, `Input`, `Output`,
`SemaInput`/`SemaOutput`, `NexusInput`/`NexusOutput`, the receipt /
records / report payloads, `ValidationError`, `MailLedgerEvent`,
`SentMail`, `ProcessedMail`, `MailIdentifier`, `ShortHeader`,
`DatabaseMarker` etc. (lines 13-266).

**Universal envelope substrate (~600 lines)** that will appear
identically in every schema-emitted runtime:

- type aliases for `String` / `Integer` / `Boolean` / `Path` (lines 3-6)
- `short_header` module with route header constants (lines 728-737)
- `SignalFrameError` enum + `Display` + `Error` impls (lines 739-762)
- `Input::{route, short_header, route_from_short_header,
  encode_signal_frame, decode_signal_frame}` (lines 780-831) AND
  the byte-identical four-method block for `Output` (lines 833-890)
- `Signal<Root>` / `Nexus<Root>` / `Sema<Root>` envelope triple —
  identical body, identical methods (lines 946-1028)
- `pub mod schema::Plane<S,N,M>` cross-plane enum (lines 927-944)
- `MessageIdentifier`, `OriginRoute`, `MessageRoot`, `MessageSent`,
  `NexusMail<Payload>`, `MessageProcessed<Reply>`, their hook traits,
  their impls (lines 892-1119)
- six identical one-line `with_origin_route` impls (lines 1121-1197)
- `signal` / `nexus` / `sema` plane module re-exports (lines 1157-1173)
- `InputNexus` / `OutputNexus` traits with `dispatch_mail_with_nexus`
  methods (lines 1199-1247) — note this dispatch is UNUSED;
  `SignalAccepted::process_with` (engine.rs:163-176) hand-matches the
  same variants
- `NexusEngine` / `SemaEngine` / `UpgradeFrom` / `AcceptPrevious` (lines
  1249-1269)

Designer 435 Gap C estimated ~600 lines per component; the live module
confirms it (1269 − ~300 component-specific − ~370 NOTA bridges = ~600
universal). When schema-core lands, the generated module drops to ~300
lines and the saving compounds across every new component.

The unused `dispatch_mail_with_nexus` is a smaller signal: either lift
the `InputNexus` trait to schema-core and use it from `SignalAccepted`
(removing the hand-match), or stop emitting it.

## Finding 2: Three identical `FromMail<Payload>` impls — schema-shaped boilerplate that should derive

`src/nexus.rs:105-154` carries three impls of
`FromMail<T> for Mail<BeingProcessed>`:

```rust
impl FromMail<Entry> for Mail<BeingProcessed> {              // :105
    fn from_mail(mail: NexusMail<Entry>) -> Self {
        let identifier = mail.identifier();
        let origin_route = mail.origin_route();
        Self {
            identifier, origin_route,
            phase: BeingProcessed {
                sema_input: mail
                    .into_nexus_input()
                    .into_nexus_output()
                    .into_sema_input(),
            },
        }
    }
}
// identical body for Query (:122) and RecordIdentifier (:139)
```

The bodies are byte-identical modulo the type parameter. The same
shape recurs in `src/engine.rs:326-345` — three identical
`NexusMail<X>::into_nexus_input` impls, one per Signal payload type. The
content is the same Signal-payload-to-Nexus-input wrapping the schema
hands back as `NexusInput::Signal(Input::<Variant>(payload))`.

Why three? Because Rust can't generically write `impl<T> FromMail<T>
where Input: From<T>` without a `From<Payload> for Input` impl per
variant — but those WOULD be schema-derivable. The schema knows that
`Input` has variants `Record(Entry)`, `Observe(Query)`,
`Remove(RecordIdentifier)`; an emitter could derive
`impl From<Entry> for Input` for each variant payload type and then the
runtime's three `FromMail` impls collapse to one generic impl.

The pattern recurs in `engine.rs:387-398` (`SemaOutput::into_signal_output`)
where four matches map `SemaOutput::*` to `Output::*` — same structural
mapping the schema already knows. Designer 435 Gap C names this kind of
"hand-rolled glue that the substrate could derive" as a category.

Cumulative cost: ~80 lines of variant-by-variant hand mapping that a
schema-aware emitter could collapse. The mappings are not Stage-5 code
("everything is data") — they're routine `From<Variant> for Enum` impls
that derive-macros emit elsewhere in the Rust ecosystem.

## Finding 3: The store's redb table handling duplicates schema-next's `AsschemaStore`

Spirit-next's `src/store.rs` (333 lines) and schema-next's
`src/store.rs` (203 lines) each open a redb database, ensure tables,
write+read rkyv archives keyed by an identifier. The substrate shape is
identical:

| Operation | spirit-next/store.rs | schema-next/store.rs |
|---|---|---|
| Open with mkdir + create-or-open | :89-102 | :21-41 |
| Ensure tables | :108-122 | :162-184 |
| Write rkyv archive in a transaction | :124-146 | :47-87 |
| Read rkyv archive from a transaction | :148-161, :190-194 | :89-156 |
| Boxed redb error variants | :250, :268-302 (5 `From` impls) | (uses error enum; schema-next routes through `SemaDatabaseOperation`) |

Each store re-encodes the same redb pattern: open a write transaction,
open one or more tables, mutate, commit; or open a read transaction,
open a table, iterate. The diversity between the two stores is small:

- spirit-next stores `Entry`-by-identifier; schema-next stores
  `AsschemaArtifact`-by-identity-string
- spirit-next maintains a two-key ledger (`next-identifier`,
  `commit-sequence`) in a second table; schema-next doesn't
- spirit-next computes a `StateDigest` over committed records;
  schema-next doesn't
- spirit-next has typed `Record` / `Observe` / `Remove` operations;
  schema-next has `put_artifact` / `get_artifact` / `export_nota_file`

The five `impl From<redb::SomethingError> for StoreError` blocks
(store.rs:268-302) deserve their own note: same five-impl pattern would
appear in every redb-using store. The boxed `redb::Error` (`Box<redb::Error>`
because redb's error type is large) is a signal that the error-flattening
should be a library function.

**The shape that wants to exist** is roughly:

```rust
// in schema-core (or a sibling crate like sema-store-core)
pub struct SemaStore<Operations: SemaEngine> {
    database: Database,
    path: PathBuf,
    operations: Operations,
}

pub trait SemaTableLayout {
    type RecordKey;
    type RecordValue;
    fn records_table() -> TableDefinition<Self::RecordKey, Self::RecordValue>;
    fn ledger_table() -> TableDefinition<&'static str, u64>;
}
```

The redb transaction scaffolding, the ledger counter management, and the
`From<redb::*Error>` impls all live in the substrate; each component
declares its `SemaTableLayout` and what mutation each `Input` variant
does on the open transaction.

Whether schema-next's `AsschemaStore` can ALSO be expressed through this
substrate is a separate question — it's a single-table no-ledger store —
but the redb-open-and-cycle-transactions logic IS shared.

Both audits (operator 263 Gap 4, designer 435 Gap C) named this for the
support nouns; this finding extends it to the redb operational layer.
A single `SemaStore<T: SemaEngine>` would compress these 333 + 203 lines
to ~100-150 lines of shared substrate plus ~30 lines per component.

## Finding 4: Daemon configuration is binary rkyv, not hand-rolled NOTA — concern already resolved

The audit prompt asked about a 9-field positional NOTA configuration
record. That shape is gone. `src/config.rs` (85 lines, May 30) is
derive-driven: `Configuration { socket_path, database_path }` with
`#[derive(rkyv::Archive, rkyv::Serialize, rkyv::Deserialize)]`. The
`from_binary_path` / `to_binary_bytes` methods are five-line rkyv
wrappers (config.rs:43-61). Spirit record 1244 / operator 246's
NOTA-surface split closed this; the daemon binary literally cannot
decode NOTA because nota-next is behind `nota-text` and the daemon
doesn't enable that feature (Cargo.toml:20-22).

Surviving concern, Stage-5 horizon: should `Configuration` itself be
schema-emitted as an `OwnerSignal::Configure` variant per operator 263
Gap 6? Today it's a hand-written rkyv struct; tomorrow it joins the
owner-signal schema. Not a present-day boilerplate concern.

## Finding 5: The Signal/Nexus/SEMA actor chain holds a clean type-state pattern that the substrate should host

This is the strongest piece of the spirit-next design. The
type-level being-processed witness — `Mail<BeingProcessed>` is the
ONLY path from accepted Signal to SEMA call; only `run_sema` produces
`Mail<Processed>` — is enforced by Rust's privacy rules
(nexus.rs:174-185). The phase-specific data lives in `BeingProcessed`
(`sema_input` field) and `Processed` (`output` field), so they're
structurally distinct values, not one struct wearing a marker (nexus.rs:46-55).

This is sound design. But every component built on this substrate will
re-author the same pattern: a `Mail<Phase>` with phase-specific
contents, the `run_sema` private transition, the `BeingProcessed` ↔
`Processed` typestate, the `MailLedgerHook` infallible event sink. That
substrate belongs in schema-core too, parameterised by the component's
`SemaEngine`:

```rust
// in schema-core
pub struct Mail<Engine: SemaEngine, Phase> { ... }
pub struct BeingProcessed<Engine: SemaEngine> { sema_input: Engine::Input }
pub struct Processed<Engine: SemaEngine, Output> { output: Output }
impl<E: SemaEngine> Mail<E, BeingProcessed<E>> {
    fn run_sema(self, store: &mut E) -> Mail<E, Processed<E, ...>> { ... }
}
```

Then a component's `nexus.rs` shrinks to its specific output translation
and the three `FromMail` impls (themselves derivable per Finding 2).

Note also: the `NexusEngine for Nexus` impl at nexus.rs:224-231 is
single-line. The generated `NexusEngine` trait requires
`execute(&self, input: nexus::Nexus<nexus::Input>) ->
nexus::Nexus<nexus::Output>`, and Nexus delegates to
`input.into_nexus_output()` — a method on the GENERATED `Nexus<Input>`
type. The trait surface and the runtime impl are wired through the
generated nouns; that's the right shape. The schema-core extraction
should preserve this wiring.

## Finding 6: Cross-actor messaging is synchronous + Mutex-locked, with no actor substrate yet

`Engine` holds `nexus: Mutex<Nexus>` (engine.rs:25); every accessor
takes the lock (`self.nexus.lock().expect("nexus lock")`, eight call
sites). `Daemon::run` shares one `Arc<Engine>` per connection
(daemon.rs:67-72) and processes one frame per stream synchronously
(daemon.rs:82-88).

This is intentional pilot scope (ARCHITECTURE.md:196-198: kameo /
`sema-engine` is the production destination). Per AGENTS.md's
actor-systems lens: no async handlers exist, so no blocking-in-handlers
violation; no `kameo`/`tokio` substrate is carried, which is correct
pilot scope. The actor substrate question lands with `sema-engine`,
not in spirit-next.

One present-tense nit: the eight `expect("nexus lock")` call sites want
a `nexus_guard()` helper or `LockedNexus<'a>` newtype to centralize the
poison-recovery expectation. ~8 lines saved.

## Finding 7: The CLI binary still hand-parses argument shape; both binaries duplicate ~30 lines of CLI scaffolding

`src/bin/spirit-next.rs:34-49` parses arguments by string introspection:

```rust
fn read_single_argument(&self, argument: &str) -> Result<String, Box<dyn std::error::Error>> {
    if argument.trim_start().starts_with('(') {
        Ok(argument.to_owned())
    } else if Path::new(argument).exists() {
        Ok(fs::read_to_string(argument)?)
    } else {
        Err("inline operation must be a parenthesized NOTA value".into())
    }
}
```

This violates the spirit of the NOTA-only-argument rule (per AGENTS.md
"NOTA is the only argument language"): the parsing decides
"NOTA literal vs path" by string prefix, not by reading the input as
NOTA. The clean shape is for the NOTA codec to accept either form
through one function — `nota_next::NotaSource::from_argument` or
equivalent — so this branching lives in the codec, not the binary.

The two binaries also duplicate ~30 lines of identical CLI scaffolding:

- `struct SpiritNext{,Daemon}Cli { arguments: Vec<String> }`
  (spirit-next.rs:12-14, spirit-next-daemon.rs:12-14)
- `from_environment() { Self { arguments: env::args().skip(1).collect() } }`
  (spirit-next.rs:17-21, spirit-next-daemon.rs:17-21)
- `fn single_argument(&self) -> Result<&str, Box<dyn std::error::Error>>`
  with the same `match self.arguments.as_slice()` body
  (spirit-next.rs:34-39, spirit-next-daemon.rs:29-34)
- `fn main() { if let Err(error) = ...::from_environment().run() { ... } }`
  (spirit-next.rs:5-10, spirit-next-daemon.rs:5-10)

That's about 30 lines per binary, ~25 of which are identical. A small
`spirit_next::cli::SingleArgumentBinary` or
`schema_core::cli::SingleNotaArgument` substrate would carry the
once-only main + single-argument-extraction logic. This is the same
problem the broader component-triad rule already names (every component
has its CLI; that CLI doesn't grow flag soup; it accepts one NOTA arg).
The substrate should be there.

Per the AGENTS.md method-on-noun discipline: `SocketPath<'path>`
(daemon.rs:96-112) carries `path: &'path Path` and one method
`remove_stale`. It IS a real data-bearing type — it borrows the path —
but the noun is doing very little (one method that's effectively a
function on `Path`). The substrate-extraction question: does this
belong on a future `DaemonSocket` noun in schema-core, where its job
includes binding, removing stale, accepting connections?

## Finding 8: Test scaffolding is admirably schema-shaped; missing utility is the `TempDir` + `Engine` opener

Tests use schema-emitted types as witnesses, per INTENT.md:110-113.
`tests/runtime_triad.rs` asserts on `MailLedgerEvent`, `SentMail`,
`ProcessedMail`, `Plane::<Output, NexusOutput, SemaOutput>`, and
`Output::FromStr`. `tests/generated_signal_plane.rs` covers route+frame
round-trip on generated types directly. `tests/socket_negative.rs`
proves the binary boundary rejects raw NOTA. No test-only shadow enums.

The cross-test repetition that will recur per-component: the `SemaFile`
helper (runtime_triad.rs:13-33) plus the `entry` / `query` /
`full_query` / `partial_query` / `route` / `sema_message` constructors
(runtime_triad.rs:48-100). Another component's integration test will
re-author the same shape; a `SemaTestHarness<Engine>` substrate
(probably in schema-core) would lift the tempdir-scoped Engine opener.

Sidebar: schema-emitted nouns have no builder shape, so tests use ad-hoc
fixed-default constructors. A derive that emits per-struct builders or
`Default`-friendly skeletons would help both tests and runtime code.

## Finding 9: Method-on-noun discipline holds

Every Rust function is a method on a non-ZST data-bearing type or a
trait impl. `Engine`, `SignalActor`, `Nexus`, `Mail<Phase>`, `Store`,
`SemaFile`, `Configuration`, `Daemon`, `SignalTransport`, `MailLedger`,
`MailLedgerHook`, `SocketPath<'path>`, the two CLI nouns, the test
`WorkspaceManifest` / `LengthPrefixedFrame` — all carry real data. The
generated module's emitted methods land in `impl` blocks of named
types. No ZST namespace holders. No free functions outside `fn main()`
and `#[cfg(test)]`.

Nit: `tests/dependency_surface.rs:31-50` writes the assert logic
inline rather than as methods on `WorkspaceManifest`
(`manifest.assert_excludes(crate)` / `assert_includes(crate, features)`).
The substrate moves in Findings 1-5 should preserve the discipline.

## Finding 10: ARCHITECTURE.md predicts the schema-core extraction; the audit confirms the scale

`ARCHITECTURE.md:330-343` ("Known limits") already names the schema-core
gap — `MessageSent`, `NexusMail`, `MessageProcessed`, the mail support
trio, plus "the durable marker toward a shared schema-core type." The
ARCHITECTURE-named "next slice" matches operator 263 Gap 4 and designer
435 Gap C. The audit's contribution is the line-by-line boundary: ~300
component-specific lines vs ~600 universal lines in spirit-next's
generated module — a 70%+ deduplication target across every future
component. The mail support nouns (lines 1031-1119, 169-198) reference
component-shaped `Input`/`Output` only through generic parameters and
route fields — clean separation; lifting them out is mechanically
straightforward.

## Top 3 broad improvements for spirit-next (ordered by impact × scope)

### 1. Schema-core extraction (Designer 435 Gap C × Operator 263 Gap 4 × this audit Findings 1, 5, 10)

**Lift the universal envelope substrate into a `schema-core` crate.** Today
~600 of the 1269 lines in spirit-next's generated `src/schema/lib.rs` are
universal: `Signal<R>`, `Nexus<R>`, `Sema<R>`, `Plane<S,N,M>`,
`OriginRoute`, `MessageIdentifier`, `ShortHeader`, `SignalFrameError`, the
short-header constants module, `Input`/`Output` frame methods (which are
shape-identical per root enum), `MessageSent`, `NexusMail`, `MessageProcessed`,
their hooks, the `with_origin_route` plane-wrapping methods, and the
`NexusEngine`/`SemaEngine`/`UpgradeFrom`/`AcceptPrevious` trait surfaces.

The runtime substrate also lifts: `Mail<Phase>` typestate, the
`MailLedgerHook` pattern, the `Engine`-as-composer shape, and probably
the `SemaStore<T>` redb-cycle wrapper named in Finding 3.

Impact: every new component drops ~500-600 lines of generated code and
~300-400 lines of hand-written runtime code. The deduplication compounds
across the future component triad. Scope: one new crate
(`schema-core` or split-by-concern as Designer 435 suggests), one
emitter teaching ("use schema_core::T;" vs "emit a local T"), one
spirit-next reshape that imports the substrate. The patches landed for
one component are the template for every component after.

This is the largest single design improvement available to spirit-next
and the broader stack.

### 2. Schema-aware variant projection — `From<Variant> for Enum` and `Into<NextEnum>` derives (this audit Finding 2)

**Make the emitter derive the variant-to-enum projections and the
sibling-plane translations that the runtime currently hand-rolls.**
Today `engine.rs:326-345` hand-writes three identical
`NexusMail<X>::into_nexus_input` impls because Rust can't express the
"my variant payload became the enum" map generically without
`From<Payload> for Enum` impls. Those impls ARE schema-derivable: the
schema declares `Input::Record(Entry)`, the emitter knows it,
`impl From<Entry> for Input { fn from(e) -> Self { Self::Record(e) } }`
follows.

Similarly, `SemaOutput::into_signal_output` (engine.rs:389-398),
`nexus_plane::Nexus<Output>::into_signal_output`
(engine.rs:373-380), `nexus_plane::Nexus<Output>::into_sema_input`
(engine.rs:365-372), and `nexus_plane::Nexus<Input>::into_nexus_output`
(engine.rs:347-362) all hand-write structural matches between sibling
enums. The enum-to-enum maps depend on schema choices (`SemaOutput::Recorded`
→ `Output::RecordAccepted`) but are 100% structural; an emission
directive in the schema ("project this enum to that enum by these
variant correspondences") would derive them.

Impact: ~120 lines of variant-by-variant matching deleted across
engine.rs and nexus.rs; the three `FromMail` impls collapse to one
generic; future components can't drift in HOW they translate.
Scope: emitter change (probably an `Asschema::EnumProjection` opcode
plus `RustModule::Impl(impl From<X> for Y)` emission); schema
authoring change to declare the projections; runtime simplification.

Smaller than schema-core but compounds with it: schema-core alone leaves
the per-component variant-translation glue. The variant-projection
derive is what makes the component runtime code become "Engine composes
SignalActor + Nexus + Store" and not much else.

### 3. `SemaStore<T>` substrate over redb (this audit Finding 3)

**Lift the redb-cycle scaffolding into a generic
`SemaStore<Layout: SemaTableLayout, Engine: SemaEngine>` substrate.**
Today spirit-next's `Store` (333 lines) and schema-next's `AsschemaStore`
(203 lines) each re-implement the same redb open / ensure-tables / begin-
write / open-table / mutate / commit / begin-read / open-table / iterate
sequence. The store-specific code is narrow: which key, which value,
which schema operations, which ledger keys.

`SemaStore<T>` carries: the redb open with mkdir + create-or-open, the
ensure-tables scaffold parameterised by `T::tables()`, the typed
`From<redb::DatabaseError>` / `TransactionError` / `TableError` /
`StorageError` / `CommitError` impls (five identical implementations
each store currently writes), the `begin_write` / `with_table` / `commit`
helper methods, and the `commit_sequence` + `state_digest` ledger
pattern as opt-in mixins.

Impact: ~200 lines deleted across spirit-next's `Store` (the redb
scaffolding) and another ~150 from schema-next's `AsschemaStore`; the
five `From<redb::*Error>` impls collapse to a single generic one. Future
SEMA stores arrive in ~30 lines: declare their table layout, declare
their typed mutation methods.

Scope: a new `sema-store-core` crate (or `schema-core::store` module);
trait-driven so neither spirit-next nor schema-next changes shape much
outwardly. Smaller scope than schema-core but a clean and independent
slice.

## Notes on what is NOT broken

A short list of design choices the audit examined and found to be
sound:

- **The Mail<Phase> typestate.** Phase-specific contents in
  `BeingProcessed { sema_input }` and `Processed { output }` — not a
  marker on one struct — is correct (records 970/999/1000 carried
  through). Lift the substrate; don't redesign the pattern.
- **The Engine-as-composer split.** `Engine` owns Signal admission +
  the locked `Nexus`; `Nexus` owns the durable Store + MailLedger;
  `Store` owns the redb database. Each noun has one job. The hand-
  written runtime layer is correctly hand-written per ARCHITECTURE.md's
  framing.
- **The CLI/daemon dependency split.** Binary-only daemon
  (`spirit-next-daemon` requires no features), NOTA-text-enabled CLI
  (`spirit-next` requires `nota-text`), enforced by
  `tests/dependency_surface.rs`. Operator 246's design landed and works.
- **Test surface uses schema-emitted nouns.** No shadow languages, no
  test-only enums — runtime_triad.rs proves the full chain through
  generated types. INTENT.md:110-113 is honoured.
- **No NOTA hand-parsing in the daemon.** Spirit record 1244's "daemon
  is binary-only" is realized; the audit-prompt's worry about a "9-field
  positional NOTA configuration record" is a leftover concern — that
  shape is gone since 2026-05-30.
- **NOTA-only single-argument rule.** Both binaries take exactly one
  argument (NOTA literal, NOTA path, or rkyv binary path). No flags.
  Per AGENTS.md's hard override.
- **No `---` separators in markdown.** Per AGENTS.md hard override; the
  generated module and the hand-written files use headings for
  structure, not horizontal rules.
- **The cross-plane `schema::Plane<S,N,M>` enum** (generated lines
  927-944) is the right shape: when code needs to branch across planes,
  it matches that enum and gets the typed envelope back. The runtime
  uses it correctly in tests (runtime_triad.rs:113-126, 192-203, 221-238,
  396-501).

## Total line-count cost the three improvements would address

| Improvement | spirit-next savings | cross-stack savings |
|---|---|---|
| 1 — schema-core | ~600 lines generated + ~200 hand-written (substrate of `Mail`, `MailLedger`, `Engine`-shape) | every new component drops the same ~600 lines |
| 2 — variant projection derives | ~120 lines across engine.rs + nexus.rs | every component using sibling-enum projections |
| 3 — `SemaStore<T>` substrate | ~200 lines in store.rs | ~150 in schema-next's AsschemaStore; new SEMA stores arrive in ~30 lines each |

Cumulative spirit-next reduction: ~1100 lines (of ~2700 hand-written +
generated). Per-component going-forward reduction: ~700-900 lines per
new component.

These three are independent (any one can land alone) but compose well.
The order designer 435 recommends — C first, then variant projections,
then SemaStore — matches this audit's impact ranking.
