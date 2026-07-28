# Ethos vertical witness proposal — 2026-07-28

## Decision boundary

This is a **prototype-only** implementation proposal, based on read-only source
inspection. It does not claim a current green build or test: no build, test,
fetch, deployment, store write, VCS operation, or source mutation was performed.

It assumes the recovery map's recommended posture is permitted: retain
`schema` + `schema-rust` as the bounded production compatibility compiler while
a disposable Ethos → Nomos → Logos witness is developed. If the psyche instead
requires final Ethos shape now, the strict-lane blockers below apply and this
proposal is not authorization to change a live component compiler.

The current repository and package names remain internally Schema-named
(`schema-engine`, `core-schema`, `signal-schema`), even though their
checkout/design names are Ethos. This proposal calls the intended stages Ethos,
Nomos, and Logos, and names current crates/files exactly where implementation
must touch them.

## Current evidence

| Claim | Classification | Direct witness |
| --- | --- | --- |
| The existing process witness launches four processes and compiles/behavior-tests emitted Rust. | Wired, but wrong topology | `language-engine-witness/tests/e2e.rs` launches `sema-storage`, `schema-engine`, `nomos-engine`, and `logos-engine`; writes a locked crate and runs three `cargo test --locked` feature modes. |
| All three language daemons are stateless clients of one central storage socket. | Wired, disconfirming | Every engine's `src/lib.rs` has a `SemaPlane` that opens a `UnixStream` to `signal-sema-storage::Request`; each binary defaults its second daemon argument to `/tmp/new-language-engine/sema.sock`. |
| Normal Ethos ingress is authority-bound. | False for current ordinary ingress | `ethos-engine/src/lib.rs` handles `IngestTypeSchema` via `LegacySchemaIngest::migrate_text` and saves its parse-order `NameTable`. Its source marks this offline lean explicitly. |
| Authority binding and canonical rebuilding exist. | Wired library/test path only | `ethos-engine/src/authority_ingest.rs` exposes `ParsedSchema::{declared_identities,build_universe}`; `tests/equivalence.rs` drives real durable `sema_storage::Runtime::BindIdentities` and checks two front ends' content identity. |
| Nomos chooses an input package. | False for current daemon request | `signal-nomos::Request::Transform` has no selector. `nomos-engine/src/lib.rs` always uses `MacroPackage::enriched_fixture()`, yet records `NomosPackage::WireFixture`. |
| A typed package is available instead of a raw text fixture. | Wired library capability | `core-nomos/src/package.rs` has a stringless, content-identified `MacroPackage` plus name-table sibling. `fixtures.rs` exposes distinct `plain_fixture`, `wire_fixture`, and `enriched_fixture`; `enriched_fixture` has a non-empty typed `GenerationClass` selection. |
| Logos is stored and projected through Rust text. | Wired under central storage | Nomos stores `DocumentPayload::Logos`; Logos `HashFetch`es it and invokes `textual_rust::RustSource::project_item`. |
| A translator/name authority exists in the final intended topology. | Undesigned | The design record requires a small separate daemon, but leaves its name, wire, durable schema, mint/bind flow, stale-entry policy, and all-three-engine consultation contract open. The present `sema-storage` authority is the overruled central-storage prototype, not an acceptable final translator. |

The existing `language-engine-witness` is consequently valuable as a harness but
not as acceptance evidence for the desired topology. Its `ARCHITECTURE.md`
correctly insists on real processes, temporary state, compilation, and behavior;
its `e2e.rs` proves the contrary storage fact by fetching Logos from the one
`sema` socket after restart.

## Smallest credible witness

Launch four temporary OS processes under one `TempDir`:

```text
temporary/translator.sema + translator.sock
                  │ bind-or-mint only
                  ▼
temporary/ethos.sema + ethos.sock ── authority-stamped EthosReady ──► Nomos
                                                                      │
temporary/nomos.sema + nomos.sock ── persisted LogosReady ──────────► Logos
                                                                      │
temporary/logos.sema + logos.sock ── RustProjected ────────────────► witness
```

The requested *three-daemon witness* is the Ethos, Nomos, and Logos chain. The
translator is a fourth, deliberately tiny authority process, not a storage
daemon and not an additional language stage. It owns only its own temporary
authority database. Every language daemon owns a distinct temporary embedded
`sema-engine` database. No process receives, opens, or is passed
`signal-sema-storage`'s socket.

### Exact happy path

1. Start the translator, then Logos and subscribe to its push stream before
   ingress, then Nomos and Ethos. Pass distinct absolute paths for all four
   sockets and all four databases; reject duplicate canonical paths before
   spawn.
2. Send native Ethos text for existing `spirit-min.schema` to a new
   authority-required Ethos request. Ethos parses with
   `ParsedSchema::from_native`; constructs its `DeclaredIdentity` set; makes
   a real socket `BindOrMint` request to the translator; calls
   `build_universe` on the reply; persists the canonical schema plus canonical
   names and the returned authority assignment in **Ethos's** Sema DB; then emits
   an `EthosReady` event.
3. Nomos consumes that typed event, persists the **selected** typed
   `MacroPackage` before applying it, applies that exact object to the
   authority-stamped Ethos schema, persists the resulting Logos document and
   names in **Nomos's** Sema DB, and emits `LogosReady { logos_hash,
   package_identity, package_revision }`.
4. Logos consumes the typed Logos event, reads its input over the event boundary
   (not from central storage), persists the received Logos document in
   **Logos's** Sema DB before projection, projects it through `TextualRust`,
   and emits `RustProjected`.
5. The witness writes the returned Rust verbatim into the existing locked
   `generated-spirit` scratch crate and runs the present default,
   `--no-default-features`, and `--all-features` public-behavior tests.
   Retain working programs as the oracle; do not add a `schema-rust` byte
   comparison.
6. Kill all four processes, retain only their temporary directories, restart
   against the same four paths, and prove: the translator returns the same
   assignment for the same declared identities; Ethos reopens its canonical
   ingress record; Nomos reopens exactly the selected package and Logos; Logos
   reopens its persisted Logos/projection record; a second named fixture pushes
   to a different Rust result. Remove the entire `TempDir` at test completion.

This deliberately treats the native Ethos front end as the witness ingress.
The legacy parser may remain in its current compatibility test, but it must not
be the ordinary ingress of this witness: otherwise its parse-order name table
would make the central defect invisible.

## Bounded prototype contract

The public final translator protocol is not designed, so the prototype must
make its contract private to the witness lane and visibly temporary. Its sole
supported operation is the already-real semantic operation, renamed only
locally for clarity:

```text
BindOrMint {
  whole: opaque fixture handle,
  declarations: [{ resolved key bytes, resolved shape hash, MintOrBind }]
}
  -> { universe integer, assignments: [{ key, type integer, Minted|Bound }] }
```

Its durable laws are non-negotiable and already exercised by the old authority:

- same whole/key returns the prior identity, including after restart;
- a new key receives a never-reused identity;
- an explicit continuation with a mismatched shape is rejected without a write;
- no empty declaration set is accepted.

For this witness, `whole` is a test-owned opaque byte handle and
`MintOrBind` is the only accepted intent. That is enough to prove real
authority-bound Ethos ingress. It does **not** decide the final daemon name,
root namespace enum, external ontology, author-facing identity syntax,
cross-deployment identity, stale-entry retirement, or permanent public wire.

The selected Nomos package shall be
`MacroPackage::enriched_fixture()`, but the selection must be a request value,
not the daemon's default. This is deliberately selected typed data: it carries
its macro definitions, `PackageRevision(1)`, name-table sibling, and
generation-class selection. The test must persist and assert its
`content_identity()` and revision, then run a negative selection with
`plain_fixture()` or `wire_fixture()` and assert the distinct identity and
distinct output/behavior expectation. Calling a constructor in the implementation
is permitted only in witness setup to build the typed request object; the
daemon's transform branch must not call any `*_fixture()` constructor.

The first vertical contract should be directional rather than recreating a
shared storage schema:

- `signal-ethos` owns an authority-stamped Ethos document/event and Ethos
  local lookup/subscription records.
- `signal-nomos` imports that Ethos event type and owns the typed
  `Transform { ethos, package, output_slot }` request and `LogosReady`
  event. It must not import `signal-sema-storage`.
- `signal-logos` imports the Nomos Logos event type and owns local
  projection/subscription records. It must not import `signal-sema-storage`.

The exact archival shape of `AuthorityStampedEthos` needs a narrow
implementation design before code: current `EncodedUniverse` is not itself
an archivable public payload, and Nomos currently consumes only
`CoreSchema + NameTableBytes`. The witness must carry enough persisted
evidence to show the schema used by Nomos came from
`ParsedSchema::build_universe`, not merely attach an unused authority receipt.
The least expansion is an archived envelope containing canonical declared
schema, canonical name-table bytes, minted universe, and ordered
`IdentityAssignment` values. Whether the full universe becomes a durable
cross-engine value is a final-contract question and is out of this prototype.

## Expected mutation set

This is the smallest set that can genuinely remove the central fallback. It is
not a request to edit it now.

| Repository | Exact likely files | Purpose |
| --- | --- | --- |
| `language-engine-witness` | `AGENTS.md`, `ARCHITECTURE.md`, `Cargo.toml`, `Cargo.lock`, `flake.nix`, `flake.lock`, `tests/e2e.rs`, existing fixtures/lock only if the emitted dependency closure changes | Re-pin the delivered producers, replace the central four-process launch with Ethos/Nomos/Logos plus temporary translator, preserve compile/behavior/restart gates, and add fault injections. This repository is the one existing process-level owner. |
| `ethos-engine` | `src/lib.rs`, `src/authority_ingest.rs`, `src/bin/schema-engine.rs`, one feature-gated test-translator binary and its private protocol module, `tests/equivalence.rs`, new focused process/local-store test if needed, `Cargo.toml`, `Cargo.lock`, `flake.nix`, `flake.lock`, `ARCHITECTURE.md` | Replace `SemaPlane`'s shared-socket storage client with an embedded local Sema adapter; make native authority binding the witness ingress; persist and event the authority-stamped Ethos record; take translator socket/config separately from local state. The temporary translator code sits beside the sole prototype client so no public signal crate is invented. |
| `nomos-engine` | `src/lib.rs`, `src/bin/nomos-engine.rs`, new `tests/` coverage, `Cargo.toml`, `Cargo.lock`, `flake.nix`, `flake.lock`, `ARCHITECTURE.md` | Embed Nomos state, receive the typed Ethos artifact, persist the explicitly selected `MacroPackage` and Logos, and emit typed Logos readiness without `HashFetch` to shared storage. |
| `logos-engine` | `src/lib.rs`, `src/bin/logos-engine.rs`, new `tests/` coverage, `Cargo.toml`, `Cargo.lock`, `flake.nix`, `flake.lock`, `ARCHITECTURE.md` | Embed Logos state, receive/persist typed Logos before projection, keep `TextualRust` as projection authority, and push the resulting Rust. |
| `signal-ethos` | `src/lib.rs`, `tests/round_trip.rs`, `Cargo.toml`, `Cargo.lock`, `ARCHITECTURE.md` | Replace shared storage payload imports with Ethos-owned archive records and add an authority-required ingress request/reply. |
| `signal-nomos` | `src/lib.rs`, `tests/round_trip.rs`, `Cargo.toml`, `Cargo.lock`, `ARCHITECTURE.md` | Add the typed package-bearing transform and Logos-ready event; depend directionally on Ethos contract only. |
| `signal-logos` | `src/lib.rs`, `tests/round_trip.rs`, `Cargo.toml`, `Cargo.lock`, `ARCHITECTURE.md` | Consume the Nomos output type and keep only Logos projection/public event shapes. |
| `signal-sema-storage` and `sema-storage` | No new production behavior in the recommended prototype lane | They are expressly excluded from the witness closure. Do not rename, extend, or repurpose the obsolete central daemon to call it a translator. Their existing authority implementation is reference material only. |
| `core-ethos`, `core-nomos`, `core-logos`, `protos` | Prefer no source change; pins/locks only if archive visibility or a necessary owned public constructor blocks the envelope | The witness should use current `ParsedSchema`, `MacroPackage`, and `TextualRust` capabilities. A new permanent generic persistence abstraction in Protos would be unnecessary scope. |
| `protos-engine` | No Rust code or Cargo manifest. At most later `flake.nix`, `flake.lock`, and `scripts/` integration invocation after the owner witness is published | It may assemble a published owner check but must not host or duplicate daemon protocol/fixture logic. |

A temporary translator implementation needs a home. The least harmful
prototype choice is a **feature-gated test binary and private protocol module
in `ethos-engine`**, with its own `sema-engine` dependency and no published
signal crate. `language-engine-witness` launches that binary as a separate OS
process; Ethos and that binary share one private module compiled only behind a
`vertical-witness` feature. That makes the authority real (process, socket,
durable database, restart law) without pretending that its unsettled name/wire
is a permanent component. If that private feature is unacceptable, stop before
code: the alternative is a new durable translator repository and public signal
contract, which requires the unresolved psyche ruling below.

The three engine repositories will need their own small, component-owned
embedded persistence adapters. They may use `sema-engine` directly, as
`sema-storage` currently demonstrates, but must not import the
`signal-sema-storage::{Request,DocumentPayload,Wire}` contract. Sharing a
new generic storage package is not the smallest witness and risks recreating
the central layer under another name.

## Pins and build closure

Current manifests are not a coherent final family closure. For example:

- `ethos-engine` pins `core-schema`
  `d3cdee9ac2c17de16a7745c9854344d8bbcde64e`,
  `signal-schema` `bc68dc8fa1b16b00156ca36e2690fd77fda91a52`,
  and `signal-sema-storage`
  `31ab48608a3c2eab0733dcb16a3351251a70789d`.
- `nomos-engine` and `logos-engine` also pin that same
  `signal-sema-storage` revision; their direct package pins are
  `core-nomos` `cb9705de181b50053b4e634a3b9ad4798103164b`,
  `signal-nomos` `2c09647bb08825806c1485ba11aca844d4b60fff`,
  `signal-logos` `c248235c4adfea86b7754b7ce71b056bc90088b0`, and
  `textual-rust` `ee7859ff10b0710fab9e87672c66d8c889b67c63`.
- The existing witness pins its old producers:
  `sema-storage` `269953164460cd842c1f3f8c9c93e4afe1e3628e`,
  `schema-engine` `9ba190dca112ca70c6383514793cc12e7913d488`,
  `nomos-engine` `526baea6af52a3c39b9fd84a42658014f3423bb4`, and
  `logos-engine` `7f75d37513b967b9b8581aa707f513379bb74bac`.

Prototype implementation must publish compatible producer revisions first,
then pin those full revisions consistently in `language-engine-witness`
`Cargo.toml` and `flake.nix`, refresh both locks, and check that Cargo has
one compatible `core-ethos/core-nomos/core-logos/name-table/textual-rust`
closure. The obsolete `sema-storage` and `signal-sema-storage` must be
absent from the witness runtime dependency graph; if a transport-only frame
helper is retained, move/copy only the neutral `signal-frame` framing
boundary, never the storage request types.

Run each producer's Nix checks (`build`, `test`, `doc`, `fmt`,
`clippy`) at its published revision, then the witness's same check set.
`protos-engine` may subsequently pin and invoke only the published witness
check, following its exact-revision and source-free rules.

## Proof gates and deliberate failure injections

A passing happy path is insufficient. The process witness must contain these
negative controls:

| Injection | Expected failure proving |
| --- | --- |
| Put a listening fake socket at the old `sema.sock`, or set the old default path to a canary server that records any connection. | The test fails if any Ethos/Nomos/Logos process connects; a passing run has zero canary connections and the old central storage crates are absent from the runtime closure. |
| Pass Ethos, Nomos, and Logos the same database path, or pre-create one daemon's state at another's path. | Startup rejects non-unique canonical local-state paths before ingest. This prevents three labels over one database. |
| Deny translator startup or return a malformed/empty/missing assignment. | Ethos rejects ingress and writes no local TypeSchema/ready event; Nomos and Logos receive nothing. |
| Reorder a fixture's declarations or perturb parser/interner order through a second front-end parse while keeping declared source semantics. | Authority-bound canonical Ethos content/assignments remain equal; a deliberately invoked legacy ingress is rejected or produces a test failure, never an accepted witness result. |
| Replay the same whole/declarations after restart. | Translator returns the same universe/local identities and reports binding rather than reminting. |
| Send `Continue` with an existing identity and a different structural shape. | Translator rejects without durable mutation; a subsequent valid bind returns the previous assignment. |
| Have Nomos receive `plain_fixture`/a package whose identity differs from the selected enriched package, or monkeypatch a hidden `enriched_fixture()` call. | The request's package identity/revision and persisted record disagree, so the test fails. The implementation must have no fixture-constructor call in the daemon transform arm. |
| Delete/misclassify the Ethos envelope or send a non-authority-stamped payload to Nomos. | Nomos rejects it before package application. |
| Send wrong document kind/hash to Logos or kill Nomos before it persists Logos. | Logos rejects; no projection event is emitted. |
| Kill each daemon after durable acknowledge and restart all four. | Each owner reads only its own retained state; the second fixture still pushes end-to-end. |
| Corrupt the generated Rust or omit the selected package's required generation class. | The locked scratch crate's existing public behavior/compile gates fail. |

The witness should also preserve the current incompatible `signal-frame`
handshake assertion, but frame compatibility is not evidence of correct
storage topology.

## What does not need a psyche ruling for the prototype

After the bounded-compatibility posture is approved, implementation may:

- use `spirit-min.schema` and `second-min.schema` as disposable fixtures;
- create only temporary sockets, databases, generated crates, and process
  state beneath `TempDir`;
- reuse existing `ParsedSchema`, `MacroPackage`,
  `TextualRust`, `sema-engine`, and locked behavioral fixtures;
- choose the already implemented `enriched_fixture` as one explicit typed
  test package, provided the request/persistence asserts its identity rather
  than silently selecting it;
- use a private, test-feature-only translator process with the existing
  bind-or-mint semantics, clearly named as provisional;
- keep all live Schema consumers and their generated artifacts untouched.

## Decisions that remain blocked

The following must not be guessed or turned into permanent code:

1. The migration posture itself: bounded temporary Schema compatibility, or
   immediate final Ethos.
2. Whether a private test-only translator is acceptable. If not, its permanent
   repository/component name, signal wire, ownership, migration story, and
   public archive surface must be approved first.
3. The translator's final whole/declaration identity representation, explicit
   authoring markers, root enum variant set, any external ontology, and
   stale-entry/retirement policy.
4. Whether every engine must make a direct translator request in the first
   slice, and what Nomos/Logos names mean at that boundary. The proposed slice
   proves the indispensable Ethos ingress authority; it does not invent
   unruled Nomos/Logos allocation semantics.
5. The final archival shape of an authority-stamped Ethos cross-daemon payload.
   The proposed envelope is a bounded witness adapter, not a component compiler
   contract.
6. The first production component to port and the required
   `schema-rust`-equivalence contract. No existing component generator,
   checked-in artifact freshness workflow, Cargo metadata, frame surface, or
   daemon runtime contract has been replaced.
7. Manifest naming/alias policy and the independent meaning of “Logics”.

If strict final Ethos is chosen, E1B/E2B from the recovery map block
Mind/Messenger recovery: final terminology/inventory and translator authority
must be decided; the replacement generator must cover checked-in artifact
freshness, Cargo schema-directory metadata, signal frames, and daemon/runtime
Rust generation; normal Ethos ingress, Nomos durable package selection,
per-daemon state, translator, and the full vertical witness must be complete
before any dependent component may use the new compiler. The prototype above
is useful evidence but cannot remove those prerequisites.

## Cleanup and rollback

The witness accepts no production path, socket, database, user profile, or
service. It creates all state under one test `TempDir`; `Drop`/finally
terminates children, removes Unix sockets, and deletes that directory. A test
failure retains the directory only when an explicit diagnostic opt-in is set;
that opt-in must print its exact path and never point outside the temporary
root.

Rollback is code-only: revert the unpublished prototype commits in their
isolated worktrees and restore the prior pins/locks as one coordinated change.
Do not migrate, delete, or alter `sema-storage` state. Do not deploy the
translator or the witness daemon arguments. Promotion requires a new explicit
decision and separate component acceptance.

## Exact authorization request

> Authorize prototype-only Ethos → Nomos → Logos vertical-witness work under
> the bounded temporary Schema compatibility posture. The work may modify only
> the named Ethos/Nomos/Logos engine and signal-contract repositories plus
> `language-engine-witness`; it may create a private test-feature translator
> process and per-process embedded Sema state only inside temporary test
> directories. It must not modify, deploy, rename, migrate, or connect to
> `signal-sema-storage`, `sema-storage`, production Spirit data, live
> components, Schema/`schema-rust` consumers, or system configuration. The
> witness must prove authority-bound native Ethos ingress, an explicitly
> selected and persisted typed Nomos package, persisted Logos, Rust projection,
> locked compilation and behavior, per-daemon state isolation, and failure when
> central storage or parse-order identity is used. This authorization does not
> establish a final translator name/wire/storage policy, a permanent component,
> or permission to promote the prototype.
