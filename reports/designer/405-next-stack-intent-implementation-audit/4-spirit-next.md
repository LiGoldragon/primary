# 405/4 — spirit-next: intent↔implementation audit (the integration pilot)

*Kind: Audit sub-report · Topics: spirit-next, nexus, sema, signal, schema,
mail-keeper, tests, audit, intent · 2026-05-28*

*Read-only audit of `spirit-next` at pinned `main`
`6938dd6af1aa69d7102f9a40799c3de4e39bae55` ("spirit: add nix-built binary
integration tests"). HEAD confirmed equal to the pin; no drift. Cargo.lock
pins the three substrate crates at EXACTLY the sibling-audit commits
(nota-next `fa14c7fb`, schema-next `e0681f2f`, schema-rust-next
`68559f86`), so the emitted `src/schema/lib.rs` audited here is the output
of the same emitter audited in report 3.*

## Verdict

`spirit-next` is the most honest repo in the stack: its own `ARCHITECTURE.md`
and `INTENT.md` name nearly every gap this audit independently confirms.
The schema-at-the-heart discipline is genuinely strong — every wire-boundary
type is schema-emitted, there are ZERO hand-written boundary shims, ZERO
free functions, ZERO ZST namespace holders, the CLI honors the single-NOTA-
argument rule, and the validation gate is a real non-bypassable witness type.
The test surface is the best in the stack: 25 tests pass, 9 of them launching
ACTUAL Nix-built binaries over a real Unix socket (verified green this
session against remote-built store path
`fykq67a9...spirit-next-0.1.0`), every assertion against schema-emitted
types. BUT two crown intent items are not met. (1) The "three execution
centers" are NOT three runtime centers — there is no Nexus actor that owns
mail in a being-processed state and translates BOTH directions; "Nexus" is a
set of methods (`into_nexus_output`, `into_sema_input`) on generated enums,
and the actual orchestration is a procedural chain inside `Engine::handle`
(engine.rs:38-58) that calls SEMA directly (engine.rs:49), bypassing any
Nexus-owns-the-mail-while-SEMA-runs semantics. The vocabulary is present and
typed, but the runtime topology is a flat handler dressed in triad
vocabulary. (2) SEMA is `Vec<StoredRecord>` in `Mutex<Store>` (store.rs:17,
engine.rs:13) — purely in-memory, NO redb, NO `.sema` file, NO durable
artifact. Per records 1007/1008 this is explicitly "not a full SEMA proof."
Both gaps are openly documented as known limits, so they are honest
PARTIALs, not concealed DIVERGENCEs — but they are the two load-bearing
claims of the whole architecture, and in the integration pilot they are
prototyped-as-language, not proven-as-runtime.

## Per-item classification

### Item 1 — Three execution centers (records 967, 970): PARTIAL (vocabulary outruns runtime topology)

The three names exist and are typed, but they are not three runtime centers.

- **Signal**: a real admission actor. `SignalActor` (engine.rs:18-20) is a
  data-bearing object (`next_message_identifier: Mutex<Integer>`) with
  `accept` (engine.rs:82-89). This is a genuine center.
- **Nexus**: NOT a center — it is methods on generated enums.
  `NexusEngine::execute` (engine.rs:192-196) is a one-line
  `input.into_nexus_output()`. The translation logic lives in
  `NexusInput::into_nexus_output` (engine.rs:240-248) and
  `NexusOutput::into_sema_input` / `into_signal_output` (engine.rs:250-264)
  — free-standing transformations on generated nouns. The `Engine` struct
  (engine.rs:10-15) is named "the data-bearing Nexus actor" in the docs but
  actually OWNS the SEMA store (`store: Mutex<Store>`, engine.rs:13) and the
  mail ledger — so "Nexus" and "SEMA" are the same object, not two centers.
- **SEMA**: a real writer object (`Store`, store.rs:13-18) implementing
  `SemaEngine` (store.rs:30-52), but owned BY the Engine, not a peer center.

The decisive evidence is `Engine::handle` (engine.rs:38-58). The SEMA call
is made DIRECTLY by the orchestrator at engine.rs:49
(`self.store.lock().expect("store lock").apply(sema_input)`) — the ONLY
`.apply()` call site in the codebase (grep-confirmed). There is no Nexus
object that "receives the SEMA reply" as record 970 prescribes; the SEMA
output is handed back to a generated-enum method
(`NexusInput::Sema(sema_output).into_nexus_output()`, engine.rs:50-52),
which is data transformation, not a center receiving mail.

### Item 2 — Nexus is the MAIL KEEPER (records 966, 970): PARTIAL → leaning MISSING on the core claim

The record-970 flow is: `Signal IN → Nexus accepts mail (BEING-PROCESSED) →
Nexus translates to SEMA query → SEMA runs → Nexus receives SEMA reply →
Nexus translates to Signal response (with logging) → Signal OUT`. *"When
Nexus has the mail, the mail is in the BEING-PROCESSED state; Nexus IS the
runtime representation that a mail is being processed."*

What exists:
- A typed mail object — `NexusMail<Payload>` (schema/lib.rs:1125-1128) with a
  `MessageIdentifier`. Created when Signal dispatches (schema/lib.rs:1227-1228).
- Lifecycle events — `MailLedgerEvent::{Sent,Processed}` (schema/lib.rs:254-257)
  recorded through `MailLedger` (engine.rs:28-31, 125-151).
- A "sent" hook firing at the Signal→Nexus handoff (engine.rs:110-122).

What is MISSING relative to the prescribed flow:
- **No object owns the mail in a being-processed state across the SEMA call.**
  In `Engine::handle`, `NexusMail` is constructed and immediately consumed
  inside `dispatch_mail_with_nexus` (schema/lib.rs:1221-1232) — it never
  survives across the `store.apply` call. By the time SEMA runs
  (engine.rs:49), the mail object is gone; what flows is a bare `SemaInput`
  (engine.rs:48). So there is no runtime representation that "the mail is
  being processed while SEMA runs."
- **Nexus does NOT translate both directions as a center.** The forward
  translation (`into_nexus_output`, engine.rs:241-247) and reverse
  (`into_signal_output`, engine.rs:258-263) are enum methods, invoked by the
  orchestrator, not by a mail-owning Nexus.
- **The "with logging" clause is half-met.** The `Sent` event fires before
  dispatch (engine.rs:120) and a `Processed` event fires AFTER the whole
  chain (engine.rs:53-56) — but the `Processed` event is recorded by
  `Engine::handle` itself, keyed off the final `Output`, NOT by a Nexus
  receiving the SEMA reply. The database marker does travel on the SEMA
  reply and into the Signal response (store.rs:36-38 → engine.rs:50-52 →
  schema/lib.rs:200-202), which matches record 970's marker-propagation
  clause.

Net: the mail *vocabulary* (identity, sent/processed events, hook) is
schema-typed and present, but the *mail-keeper runtime role* — an object
that holds the mail in-flight while SEMA executes and translates the reply
back — does not exist. This is the single largest intent gap in the pilot.

### Item 3 — Pattern A push + on_sent hook (records 989, 990): MET (validation gate), MET (hook)

- **Validation is a non-bypassable type-level gate.** `SignalAccepted`
  (engine.rs:22-26) has PRIVATE fields (`input`, `sent` — no `pub`). It is
  constructed in exactly ONE place: engine.rs:85-88, inside
  `SignalActor::accept`, AFTER `input.validate()?` (engine.rs:83). External
  code cannot fabricate a `SignalAccepted` and skip validation — it is a true
  witness type. `push_to_nexus` (engine.rs:110-122) consumes
  `SignalAccepted` by value, so the only path into Nexus is through a
  validated witness. Strong MET.
- **on_sent hook is real and fires before Nexus accepts.** `push_to_nexus`
  fires `self.sent.push_to(hook)?` (engine.rs:120) BEFORE
  `dispatch_mail_with_nexus` (engine.rs:121). The ordering is explicitly
  tested: `runtime_triad.rs:61-73` (the `SentHookProbe::message_sent` asserts
  `nexus.accepted_inputs() == []` at hook time) and
  `runtime_triad.rs:91-131`. The hook is a real trait (`MessageSentHook`,
  schema/lib.rs:1136-1140) with a generated push method
  (schema/lib.rs:1148-1155). MET and tested.
- **Push = sending a typed object onward.** The Signal validates, then
  pushes the `Input` object via `dispatch_mail_with_nexus` into a
  `NexusMail` (schema/lib.rs:1221-1232). MET in shape.

### Item 4 — Four-position schema languages for Nexus and SEMA (record 982): PARTIAL

`NexusInput`/`NexusOutput`/`SemaInput`/`SemaOutput` ARE schema-emitted, not
hand-written. They are declared in `schema/lib.schema:13-16` and emitted as
enums at `src/schema/lib.rs:155-178`. The Input/Output halves of each plane's
language exist and round-trip. So the "each plane its own Input/Output
language" part is MET.

The gap is the FULL four-position shape (Imports / Input / Output /
Namespace). The schema declares per-plane reuse vocabulary
(`SignalReuse`/`NexusReuse`/`SemaReuse`, schema/lib.schema:6-12, emitted at
src/schema/lib.rs:137-153) — that is the Imports/Exports position. But:
- These reuse types are inert. `NexusReuse`/`SemaReuse` are emitted with
  `from_nota_block`/`to_nota` (src/schema/lib.rs:394-428) but are never
  imported or used by any runtime code (grep: no `NexusReuse`/`SemaReuse`
  references in `src/*.rs` outside the generated file and the `pub use` in
  lib.rs:29,31). They are scaffolding, not a working import mechanism.
- There is no Namespace position in any meaningful runtime sense — the
  single-colon namespace strings (`signal:sema:Magnitude`) appear only as
  test fixtures (`runtime_triad.rs:249-267`,
  import_export_paths_use_single_colon_namespaces), proving the string
  FORMAT but not a namespace RESOLUTION mechanism.

So: Input/Output positions MET and live; Imports/Namespace positions emitted
but inert. PARTIAL.

### Item 5 — SEMA = database work / durable file (records 1007, 1008): PARTIAL (in-memory only) — the bead is confirmed

`Store` holds `records: Vec<StoredRecord>` (store.rs:17) inside `Mutex<Store>`
(engine.rs:13). It is fully in-memory:
- `Store::record` does `self.records.push(...)` (store.rs:59).
- `Store::observe` does `self.records.iter().find(...)` (store.rs:64-67).
- grep across `src/` + `Cargo.toml` for `redb|.sema|sqlite|durable` returns
  ZERO matches. `redb` is not even a dependency.
- `.gitignore` lists `*.redb` (anticipatory) but no redb is written.

This exactly matches bead `primary-q2au` (in-memory store) and the audit
yardstick §1.4. Per records 1007/1008, an in-memory `Store` "can prototype
the SemaInput/SemaOutput language but it is not a full SEMA proof until the
operation writes the durable database artifact." The `SemaInput`/`SemaOutput`
LANGUAGE is proven (store.rs:30-52 implements `SemaEngine::apply`); the
DURABLE-WRITE half is absent. `ARCHITECTURE.md:97-107` and `INTENT.md:62-74`
both state this plainly. PARTIAL, honestly disclosed.

One sub-finding worth flagging for the synthesis: the `DatabaseMarker`
(`CommitSequence` + `StateDigest`) is computed deterministically in memory
(store.rs:78-94); `StateDigest` is a `wrapping_mul(31)` fold over records
(store.rs:85-94), explicitly "a deterministic prototype marker, not a
content-addressed state hash" (ARCHITECTURE.md:188-189). So the marker that
records 935/970 want to carry "the state commit sequence and digest" is
present in shape but not a real content-addressed commit identity.

### Item 6 — Schema at the heart, no hand-written boundary shims (records 999, 1000): MET (no shims) + AHEAD (emitter support surface)

This is the repo's strongest result. Every type crossing a system boundary
is schema-emitted, and there are NO hand-written duplicate/shim boundary
types.

- `ValidationError` is schema-authored (schema/lib.schema:28) and emitted
  (src/schema/lib.rs:228-233). The runtime constructs the GENERATED enum
  (engine.rs:209,212,221) — no hand-written validation-error shim. (Record
  1000 explicitly forbids "a hand-written ValidationError shim"; satisfied.)
- `DatabaseMarker` is schema-authored (schema/lib.schema:23) and emitted
  (src/schema/lib.rs:198-202); the runtime builds the GENERATED struct
  (store.rs:79-82) — no hand-written DatabaseMarker shim. (Also explicitly
  forbidden by record 1000; satisfied.)
- `SignalRejection`, `SemaReceipt`, `ObservedRecords`, `ErrorReport`,
  `Entry`, `Query`, `Kind`, `Magnitude`, `Input`, `Output`, all Nexus/SEMA
  enums — all schema-emitted (src/schema/lib.rs). The hand-written code in
  `src/*.rs` attaches BEHAVIOR (validate, into_*, apply) to these generated
  nouns; it never re-declares them.
- The freshness gate is real: `build.rs:66-81` regenerates in memory and
  fails if `src/schema/lib.rs` is stale; the flake check
  `generated-schema-source-checked-in` (flake.nix:119-135) backstops it.

**AHEAD / carry-forward nuance — the emitter "support surface".** 17 types
in the emitted file do NOT appear in `schema/lib.schema` (verified by
name-by-name grep): `MessageIdentifier`, `MessageRoot`, `MessageSent`,
`NexusMail`, `MessageProcessed`, `MessageSentHook`, `MessageProcessedHook`,
`InputNexus`, `OutputNexus`, `NexusEngine`, `SemaEngine`, `UpgradeFrom`,
`AcceptPrevious`, `InputRoute`, `OutputRoute`, `SignalFrameError`,
`NotaDecodeError` (src/schema/lib.rs:965-1279). These are emitted by
`schema-rust-next`'s support surface, NOT authored in the schema. This is a
borderline tension with "schema is the canonical truth source for EVERY type
crossing a boundary": the mail lifecycle nouns (`MessageSent`, `NexusMail`,
`MessageProcessed`) and the engine traits cross boundaries yet are
emitter-invented, not schema-declared. The repo names this exact gap as a
known limit (ARCHITECTURE.md:193-194: *"`MessageSent`, `NexusMail`, and
`MessageProcessed` are generated by the Rust emitter's support surface rather
than authored in a shared core schema"*) and INTENT.md:51-52 wants them as
"generated schema nouns." So: NO hand-written shims (the literal record-1000
prohibition is MET), but the canonical-schema-for-everything ideal is met by
EMITTER MAGIC rather than by AUTHORED SCHEMA — a real architectural debt the
synthesis should weigh, because it means the schema language cannot yet
express the mail/engine vocabulary and the emitter hardcodes it.

### Item 7 — Tests PROVE not pretend (records 998, 1005, 1006): MET (best in stack) with one caveat

The canonical record-1006 shape — Nix-built binaries launched by the test,
real rkyv over a real Unix socket, schema-emitted-type assertions — is
genuinely implemented and PASSES.

- `tests/nix_integration.rs` launches ACTUAL Nix-built binaries, NOT
  `CARGO_BIN_EXE_*`. It resolves binaries from a Nix store path
  (`NixBuiltBinaries::from_directory`, nix_integration.rs:145-162) obtained
  either from `SPIRIT_NEXT_NIX_BUILD_RESULT` or by invoking `nix build`
  itself (nix_integration.rs:169-200). The flake check
  `nix-integration-witness` (flake.nix:150-176) asserts
  `! grep CARGO_BIN_EXE` on that file. **Verified this session**: ran
  `scripts/run-nix-integration-tests`; all 9 tests pass against remote-built
  store path `/nix/store/fykq67a9...spirit-next-0.1.0` (built on
  `prometheus.goldragon.criome`).
- Every `nix_integration.rs` assertion parses CLI stdout back through the
  schema-emitted `Output::from_str` (`run_cli_for_output`,
  nix_integration.rs:293-311) and matches typed variants
  (nix_integration.rs:381-390, 409-416, 487-503, 523-533) — never raw-string
  assertions. Schema-emitted-type discipline MET.
- `tests/runtime_triad.rs` asserts against schema-emitted witnesses:
  `MailLedgerEvent` (runtime_triad.rs:103-106, 300-319), `NexusInput`/
  `NexusOutput` (runtime_triad.rs:123-130, 230-246), `SemaInput`/`SemaOutput`
  (runtime_triad.rs:138-147, 169-170), and drives the planes through the
  generated traits `SemaEngine::apply` (runtime_triad.rs:138,170) and
  `NexusEngine::execute` (runtime_triad.rs:172). The `NexusProbe`
  (runtime_triad.rs:17-43) is a test double but it implements the GENERATED
  `InputNexus` trait and records GENERATED `NexusInput` values — so even the
  double speaks schema types, satisfying records 998/1000.
- `tests/generated_signal_plane.rs` asserts against generated `Input`/
  `Output`/`InputRoute`/`SignalFrameError`/`SignalRejection`/`ValidationError`
  (generated_signal_plane.rs:1-118) — frame encode/decode round-trips on the
  generated types. Schema-typed.
- `tests/process_boundary.rs` launches `CARGO_BIN_EXE_*` binaries
  (process_boundary.rs:26,33,48,63) over a real socket but asserts on RAW
  STRINGS (process_boundary.rs:43-46, 58-61, 73-76), e.g.
  `"(RecordAccepted (1 (1 39)))"`. This is the one test file that "pretends"
  more than it "proves" per record 1006: cargo-built (not Nix-built) AND
  string-asserted. It is the LESSER-proof shape the intent deprecates. Not a
  violation (it predates and is superseded by nix_integration.rs) but worth
  noting it is now redundant with the stronger nix tests.

**Caveat on the flake checks themselves.** The flake `checks` (flake.nix:109-291)
are overwhelmingly `grep`-based structural witnesses (e.g.
`runtime-triad-visible` greps for ~25 string anchors across source files).
These prove "the named symbols are present in the named files," NOT "the
runtime behaves." They are a drift tripwire, not a behavioral proof — a
file could grep-pass while being semantically wrong. The behavioral proof is
carried by `checks.test` (cargo test) and the nix-integration app. The
grep-checks are a reasonable anti-regression net but should not be mistaken
for proof; a synthesis reader scanning the flake might over-credit them.

### Item 8 — Method-only Rust, no ZST namespace holders (records 712, 882, 881): MET

- ZERO column-0 free functions in `src/` + `build.rs` (grep
  `^(pub...)? fn ` minus `fn main(` returns nothing). Every `fn` is a method
  or associated function inside an `impl` block or a trait impl. The two
  `fn main` are in the binaries (spirit-next.rs:5, spirit-next-daemon.rs:5) —
  permitted. The flake check `no-production-free-functions`
  (flake.nix:255-262) enforces this.
- ZERO unit-struct ZST namespace holders in `src/` (grep `^struct Name;`
  returns nothing). Flake check `no-production-unit-structs`
  (flake.nix:263-269) enforces it. All structs are data-bearing
  (`SignalActor` holds a counter, `MailLedger` holds events, `Store` holds
  records, `SocketPath`/`ConfigurationText`/`CheckedInSchemaSource` are
  lifetime-bearing borrow wrappers — legitimate, not ZSTs).
- Verb-belongs-to-noun is well applied: `Entry::validate` (engine.rs:207-217),
  `Magnitude::weight` (store.rs:107-119), `MessageSent::into_mail_ledger_event`
  (engine.rs:282-289), `From` impls for error conversion
  (daemon.rs:30-40, transport.rs:33-43).

MET.

### Item 9 — Single-argument NOTA CLI rule (workspace override): MET

- `spirit-next` CLI takes exactly one argument: `single_argument` requires
  the args slice to be `[argument]` (spirit-next.rs:34-39), then parses it as
  a NOTA string or a path (read_single_argument, spirit-next.rs:41-49). NO
  `--flags` (grep for `--`/`clap`/`getopts` finds only `env::args()`).
- `spirit-next-daemon` likewise: `[argument]` only (spirit-next-daemon.rs:29-34),
  parsed as NOTA-or-path by `Configuration::from_single_argument`
  (config.rs:11-31). NO flags.
- The socket path for the CLI is read from `SPIRIT_NEXT_SOCKET` env var
  (spirit-next.rs:27-28), NOT a flag — consistent with the no-flags rule
  (config goes through NOTA or env, never `--`).

MET. Minor note: the CLI's NOTA-vs-path heuristic only accepts inline NOTA
starting with `(` (spirit-next.rs:42), so a top-level `[...]` or `{...}` NOTA
string would be treated as a path; the daemon's heuristic is broader
(`['(','[','{']`, config.rs:12). A harmless asymmetry, not an intent
violation, since the CLI's only root type `Input` is always parenthesized.

## Test-surface inventory

| Test file | Tests | Binary path | Socket | Assertion type | Proof tier |
|---|---|---|---|---|---|
| `tests/nix_integration.rs` | 9 (all `#[ignore]`) | Nix-built store path (nix_integration.rs:145-200) | real Unix socket | schema-emitted `Output::from_str` + typed variants | PROOF (record-1006 canonical) |
| `tests/runtime_triad.rs` | 9 | in-process (`Engine`/`Store`/`SignalActor`) | none | schema-emitted (`MailLedgerEvent`, `NexusInput/Output`, `SemaInput/Output`) via generated traits | in-process, schema-typed |
| `tests/generated_signal_plane.rs` | 6 | in-process | none | schema-emitted (`Input`/`Output`/`SignalRejection`/`ValidationError`) | in-process, schema-typed |
| `tests/process_boundary.rs` | 1 | `CARGO_BIN_EXE_*` (cargo-built) | real Unix socket | RAW STRINGS | real-process but string-asserted (lesser proof) |

Counts:
- **Real-binary tests**: 10 total (9 Nix-built in nix_integration.rs + 1
  cargo-built in process_boundary.rs). Of these, 9 are Nix-built (the
  record-1006 gold standard); 1 is cargo-built.
- **In-process tests**: 15 (9 runtime_triad + 6 generated_signal_plane).
- **Schema-emitted-type assertions**: 24 of 25 tests. Only
  process_boundary.rs (1 test) asserts on raw strings.
- **Synthetic test-only enums**: 0. The only test double is `NexusProbe`
  (runtime_triad.rs:17-43), which implements the GENERATED `InputNexus`
  trait and stores GENERATED `NexusInput` — not an ad-hoc enum. The flake
  check `runtime-triad-visible` even asserts `! grep "enum TraceEvent"`
  (flake.nix:252) to forbid the historical synthetic-enum pattern.

Run results this session:
- `cargo test`: 16 passed, 0 failed, 9 ignored (the nix tests). Green.
- `scripts/run-nix-integration-tests`: 9 passed, 0 failed. Green. Built the
  package on the remote builder and exchanged real rkyv frames over real
  sockets against the Nix-built binaries.

Total: **25 tests, all passing.**

## Crown findings (direct answers to the audit questions)

**(a) Are the three execution centers + Nexus-as-mail-keeper REAL in code,
or vocabulary on a flat handler?** Vocabulary on a flat handler, with real
typed scaffolding. Signal IS a real center (`SignalActor`). Nexus and SEMA
are NOT two centers: the `Engine` object owns the `Store` (engine.rs:13), and
"Nexus" is a set of methods on generated enums
(`NexusInput::into_nexus_output` etc., engine.rs:240-264) invoked
procedurally by `Engine::handle` (engine.rs:38-58). No object holds the mail
in a being-processed state while SEMA runs — `NexusMail` is consumed before
the SEMA call (schema/lib.rs:1221-1232, then engine.rs:48-49). The mail
lifecycle EVENTS are schema-typed and logged, but the mail-KEEPER ROLE does
not exist as runtime topology. The intent's "THREE EXECUTION CENTERS" is, in
the pilot, one orchestrator method + three typed languages.

**(b) Is SEMA durable-file-writing or in-memory?** In-memory.
`Vec<StoredRecord>` in `Mutex<Store>` (store.rs:17, engine.rs:13). No redb,
no `.sema`, no file write anywhere (grep-confirmed zero matches). Confirms
bead `primary-q2au`. Per records 1007/1008 this is "not a full SEMA proof."

**(c) Which boundary types are hand-written shims vs schema-emitted?** ZERO
hand-written boundary shims — the literal record-1000 prohibitions
(ValidationError shim, DatabaseMarker shim, observer-state shim) are all
satisfied; every boundary type is schema-emitted and the runtime attaches
behavior to the generated nouns. The nuance: 17 emitter-SUPPORT-surface types
(mail nouns, engine traits, route enums; src/schema/lib.rs:965-1279) cross
boundaries but are EMITTER-invented rather than SCHEMA-authored — debt the
repo itself flags (ARCHITECTURE.md:193-194), not a hand-written shim.

**(d) Do the tests prove via real Nix binaries and schema-emitted types?**
Yes, for the 9 nix_integration tests (verified green this session against
Nix-built binaries, all schema-typed assertions). 15 more in-process tests
also assert schema-emitted types. 1 test (process_boundary.rs) is the lesser
shape (cargo-built + raw-string). Honest count: 9/25 real-Nix-binary,
24/25 schema-emitted-assert, 0/25 synthetic-enum.

## Top gaps (ranked)

1. **No Nexus mail-keeper runtime; "three centers" is a flat orchestrator.**
   (Item 1, 2.) The crown architectural claim — Nexus owns the mail in a
   being-processed state and translates both directions — is absent.
   `Engine::handle` (engine.rs:38-58) calls SEMA directly (engine.rs:49); no
   object holds the mail across the SEMA call. Highest-severity because it is
   THE consolidating intent (record 970) and this is the pilot meant to
   prove it.

2. **SEMA is in-memory; no durable artifact.** (Item 5.) `Vec` in a `Mutex`
   (store.rs:17). Records 1007/1008 say this is not a full SEMA proof. The
   second crown claim, unproven at runtime.

3. **Mail/engine vocabulary is emitter-hardcoded, not schema-authored.**
   (Item 6 nuance.) `MessageSent`/`NexusMail`/`MessageProcessed` + the engine
   traits (src/schema/lib.rs:1108-1279) cross boundaries but are not in
   `schema/lib.schema`. The schema language cannot yet express them, so
   "schema at the heart" is partly achieved by emitter magic. Blocks the
   record-1000 ideal that EVERY boundary type be schema-canonical.

4. **Per-plane Imports/Namespace positions are inert.** (Item 4.)
   `NexusReuse`/`SemaReuse` are emitted but never used (grep: no runtime
   references); namespace strings appear only as test fixtures. The
   four-position language shape (record 982) is half-real: Input/Output live,
   Imports/Namespace are scaffolding.

5. **`StateDigest` is a toy fold, not a content-addressed state hash.**
   (Item 5 sub-finding.) `wrapping_mul(31)` over records (store.rs:85-94);
   ARCHITECTURE.md:188-189 concedes it. The database marker that records
   935/970 want to carry real commit identity is shape-only.

6. **`process_boundary.rs` is the lesser-proof shape and now redundant.**
   (Item 7.) Cargo-built binaries + raw-string assertions
   (process_boundary.rs:43-46) — superseded by the stronger Nix tests; could
   be retired or upgraded to schema-typed assertions.

7. **The repo-triad split is absent.** (Stated limit, ARCHITECTURE.md:191-192.)
   No `spirit` / `signal-spirit` / `owner-signal-spirit` separation; this is
   one crate with both binaries. Expected for a pilot, but it means the
   component-triad override is not exercised here.

8. **Schema diff/upgrade is absent at the schema level** despite emitted
   `UpgradeFrom`/`AcceptPrevious` traits (src/schema/lib.rs:1267-1279). The
   traits exist (AHEAD of use) but nothing implements them and no upgrade is
   tested (grep: no `UpgradeFrom for` impl in `src/`). ARCHITECTURE.md:190
   concedes "Schema diff/upgrade is absent."

## Notes on honesty and convergence

The repo's self-documentation is unusually accurate: `ARCHITECTURE.md`
§"Known limits" (lines 181-196) and `INTENT.md` (lines 62-74) pre-disclose
gaps 2, 3, 5, 7, 8 almost verbatim. This makes the PARTIALs honest rather
than concealed — the divergence is between INTENT and IMPLEMENTATION, not
between the repo's CLAIMS and its implementation. The operator main has
genuinely moved toward record-1006 (Nix binary tests landed in the pinned
commit) and record-964/982 (schema-emitted plane enums + engine traits) — the
convergence the frame anticipated is real for the TYPE surface and the TEST
surface. Where convergence has NOT reached is the RUNTIME TOPOLOGY (gap 1)
and DURABILITY (gap 2): the pilot proves the schema-derived TYPES and the
process BOUNDARY end-to-end, but not yet the three-centers/mail-keeper
runtime shape or durable SEMA that records 967/970/1007 describe.
